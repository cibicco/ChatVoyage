#!/usr/bin/env python3
"""Upload recent Chat Voyage images to a Notion image database.

The script is dry-run by default. It only sends data to Notion when
`--confirm-upload` is passed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.notion.com/v1"
DEFAULT_NOTION_VERSION = "2022-06-28"


@dataclass
class ImageRecord:
    name: str
    image_path: Path
    source_path: str
    date: str
    set_title: str
    set_slug: str
    image_no: int
    city: str
    place: str
    category: str
    art_style: str
    age_band: str
    album_url: str


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)
    records = latest_records(args.limit)
    print_preview(records)

    if not args.confirm_upload:
        print("\ndry-run only. Add --confirm-upload to create the Notion database and upload images.")
        return 0

    token = require_env("NOTION_TOKEN")
    parent_page_id = normalize_notion_id(args.parent_page_id or os.getenv("NOTION_PARENT_PAGE_ID", ""))
    if not parent_page_id:
        print("ERROR: set NOTION_PARENT_PAGE_ID in .notion.env or pass --parent-page-id.", file=sys.stderr)
        return 2

    client = NotionClient(token=token, notion_version=os.getenv("NOTION_VERSION", DEFAULT_NOTION_VERSION))
    database = client.create_database(parent_page_id=parent_page_id, title=args.db_name)
    parent = database_page_parent(database)
    print(f"created database: {database.get('id')}")

    for index, record in enumerate(records, 1):
        print(f"[{index:02d}/{len(records):02d}] uploading {record.source_path}")
        file_upload = client.upload_file(record.image_path)
        client.create_page(parent=parent, record=record, file_upload_id=file_upload["id"])
        time.sleep(args.delay)

    print(f"done: uploaded {len(records)} images to Notion database {args.db_name!r}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=40, help="number of images to upload from newest albums")
    parser.add_argument("--db-name", default="Chat Voyage Images", help="Notion database title")
    parser.add_argument("--parent-page-id", default="", help="Notion parent page ID or page URL")
    parser.add_argument("--env-file", default=".notion.env", help="env file containing NOTION_TOKEN and NOTION_PARENT_PAGE_ID")
    parser.add_argument("--delay", type=float, default=0.35, help="delay between page creations, in seconds")
    parser.add_argument("--confirm-upload", action="store_true", help="actually send images and database rows to Notion")
    return parser.parse_args()


def load_env_file(path: str) -> None:
    env_path = ROOT / path
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def latest_records(limit: int) -> list[ImageRecord]:
    albums = load_album_data()
    records: list[ImageRecord] = []
    for album in albums:
        images = album.get("images", [])
        for index, image in enumerate(images, 1):
            source_path = str(image.get("src", ""))
            if not source_path:
                continue
            image_path = ROOT / source_path
            records.append(
                ImageRecord(
                    name=f"{album.get('date', '')} {image.get('label') or index:>02} {image.get('title') or image_path.stem}",
                    image_path=image_path,
                    source_path=source_path,
                    date=str(album.get("date", "")),
                    set_title=str(album.get("title", "")),
                    set_slug=str(album.get("slug", "")),
                    image_no=index,
                    city=city_from_album(album),
                    place=str(image.get("place", "")),
                    category=str(image.get("category", "")),
                    art_style=str(image.get("style", "")),
                    age_band=str(image.get("age", "")),
                    album_url=str(album.get("href", "")),
                )
            )
            if len(records) >= limit:
                return records
    return records


def load_album_data() -> list[dict[str, object]]:
    path = ROOT / "assets" / "album-data.js"
    text = path.read_text(encoding="utf-8")
    match = re.match(r"window\.CHAT_VOYAGE_ALBUMS = (.*);\s*$", text, flags=re.DOTALL)
    if not match:
        raise ValueError("assets/album-data.js has unexpected format")
    data = json.loads(match.group(1))
    if not isinstance(data, list):
        raise ValueError("assets/album-data.js payload is not a list")
    return data


def city_from_album(album: dict[str, object]) -> str:
    short_title = str(album.get("shortTitle") or album.get("title") or "")
    parts = short_title.split()
    return parts[0] if parts else ""


def print_preview(records: list[ImageRecord]) -> None:
    total_bytes = 0
    print(f"selected images: {len(records)}")
    for record in records:
        size = record.image_path.stat().st_size if record.image_path.exists() else 0
        total_bytes += size
        print(
            f"- {record.date} #{record.image_no:02d} {record.city} "
            f"{record.category}/{record.art_style} {size / 1024:.0f}KB {record.source_path}"
        )
    print(f"total image bytes: {total_bytes / 1024 / 1024:.1f}MB")


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"ERROR: missing required env var: {name}")
    return value


def normalize_notion_id(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    value = value.split("?", 1)[0].rstrip("/")
    tail = value.rsplit("/", 1)[-1]
    if "-" in tail:
        tail = tail.rsplit("-", 1)[-1]
    hex_chars = re.sub(r"[^0-9a-fA-F]", "", tail)
    if len(hex_chars) == 32:
        return str(uuid.UUID(hex=hex_chars))
    return value


def database_page_parent(database: dict[str, object]) -> dict[str, str]:
    data_sources = database.get("data_sources")
    if isinstance(data_sources, list) and data_sources:
        first = data_sources[0]
        if isinstance(first, dict) and first.get("id"):
            return {"data_source_id": str(first["id"])}
    return {"database_id": str(database["id"])}


class NotionClient:
    def __init__(self, token: str, notion_version: str) -> None:
        self.token = token
        self.notion_version = notion_version

    def create_database(self, parent_page_id: str, title: str) -> dict[str, object]:
        payload = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": database_properties(),
        }
        return self.json_request("POST", "/databases", payload)

    def upload_file(self, path: Path) -> dict[str, object]:
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        create_payload = {
            "filename": path.name,
            "content_type": content_type,
            "content_length": path.stat().st_size,
        }
        upload = self.json_request("POST", "/file_uploads", create_payload)
        upload_id = str(upload["id"])
        upload_url = str(upload.get("upload_url") or f"{API_BASE}/file_uploads/{upload_id}/send")
        self.multipart_file_request(upload_url, path, content_type)
        return upload

    def create_page(self, parent: dict[str, str], record: ImageRecord, file_upload_id: str) -> dict[str, object]:
        file_value = {"type": "file_upload", "file_upload": {"id": file_upload_id}}
        payload = {
            "parent": parent,
            "cover": file_value,
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": record.name}}]},
                "Image": {"files": [file_value]},
                "Date": {"date": {"start": record.date} if record.date else None},
                "Set": {"rich_text": [{"type": "text", "text": {"content": record.set_title}}]},
                "Image No": {"number": record.image_no},
                "City": {"rich_text": [{"type": "text", "text": {"content": record.city}}]},
                "Place": {"rich_text": [{"type": "text", "text": {"content": record.place}}]},
                "Category": {"select": {"name": record.category} if record.category else None},
                "Art style": {"select": {"name": record.art_style} if record.art_style else None},
                "Age band": {"select": {"name": record.age_band} if record.age_band else None},
                "Rating": {"select": None},
                "Preference": {"multi_select": []},
                "Note": {"rich_text": []},
                "Source path": {"rich_text": [{"type": "text", "text": {"content": record.source_path}}]},
                "Album URL": {"url": record.album_url or None},
                "Set slug": {"rich_text": [{"type": "text", "text": {"content": record.set_slug}}]},
            },
        }
        return self.json_request("POST", "/pages", payload)

    def json_request(self, method: str, path: str, payload: dict[str, object]) -> dict[str, object]:
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            API_BASE + path,
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": self.notion_version,
                "Content-Type": "application/json",
            },
        )
        return self.open_json(request)

    def multipart_file_request(self, url: str, path: Path, content_type: str) -> dict[str, object]:
        boundary = f"----chat-voyage-{uuid.uuid4().hex}"
        file_bytes = path.read_bytes()
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
        request = Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": self.notion_version,
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
        )
        return self.open_json(request)

    @staticmethod
    def open_json(request: Request) -> dict[str, object]:
        try:
            with urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise SystemExit(f"Notion API error {exc.code}: {details}") from exc
        except URLError as exc:
            raise SystemExit(f"Network error: {exc}") from exc


def database_properties() -> dict[str, object]:
    return {
        "Name": {"title": {}},
        "Image": {"files": {}},
        "Date": {"date": {}},
        "Set": {"rich_text": {}},
        "Image No": {"number": {"format": "number"}},
        "City": {"rich_text": {}},
        "Place": {"rich_text": {}},
        "Category": {"select": {}},
        "Art style": {"select": {}},
        "Age band": {"select": {}},
        "Rating": {
            "select": {
                "options": [
                    {"name": "Love", "color": "red"},
                    {"name": "Good", "color": "green"},
                    {"name": "Pass", "color": "gray"},
                ]
            }
        },
        "Preference": {
            "multi_select": {
                "options": [
                    {"name": "Art style", "color": "purple"},
                    {"name": "Person", "color": "pink"},
                    {"name": "Outfit", "color": "orange"},
                    {"name": "Color", "color": "yellow"},
                    {"name": "Silhouette", "color": "blue"},
                    {"name": "Pose", "color": "green"},
                    {"name": "Place", "color": "brown"},
                    {"name": "Vibe", "color": "default"},
                ]
            }
        },
        "Note": {"rich_text": {}},
        "Source path": {"rich_text": {}},
        "Album URL": {"url": {}},
        "Set slug": {"rich_text": {}},
    }


if __name__ == "__main__":
    raise SystemExit(main())
