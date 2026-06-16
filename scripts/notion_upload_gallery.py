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
from typing import Optional
import uuid
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.notion.com/v1"
DEFAULT_NOTION_VERSION = "2022-06-28"
DATA_SOURCE_NOTION_VERSION = "2026-03-11"


@dataclass
class ImageRecord:
    name: str
    image_path: Path
    source_path: str
    date: str
    set_title: str
    set_slug: str
    batch_id: str
    image_no: int
    variant: int
    city: str
    place: str
    category: str
    art_style: str
    age_band: str
    theme: str
    scene: str
    prompt_short: str
    file_size_mb: float
    width: int
    height: int
    aspect_ratio: str
    model: str
    album_url: str


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)
    records = latest_records(args.limit)
    print_preview(records)

    if args.sync_existing:
        return sync_existing_database(args, records)

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
    parser.add_argument("--database-id", default="", help="existing Notion database ID or URL")
    parser.add_argument("--data-source-id", default="", help="existing Notion data source ID or URL")
    parser.add_argument("--env-file", default=".notion.env", help="env file containing NOTION_TOKEN and NOTION_PARENT_PAGE_ID")
    parser.add_argument("--delay", type=float, default=0.35, help="delay between page creations, in seconds")
    parser.add_argument("--confirm-upload", action="store_true", help="actually send images and database rows to Notion")
    parser.add_argument("--sync-existing", action="store_true", help="update existing Notion rows matched by Source path without reuploading images")
    parser.add_argument("--append-missing", action="store_true", help="with --sync-existing, upload and append records missing from the existing database")
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
            width, height = image_dimensions(image_path)
            title = str(image.get("title") or image_path.stem)
            category = str(image.get("category", ""))
            art_style = str(image.get("style", ""))
            age_band = str(image.get("age", ""))
            city = city_from_album(album)
            scene = scene_from_image(album, image)
            records.append(
                ImageRecord(
                    name=f"{album.get('date', '')} / v{index:02d} / {city} - {title}",
                    image_path=image_path,
                    source_path=source_path,
                    date=str(album.get("date", "")),
                    set_title=str(album.get("title", "")),
                    set_slug=str(album.get("slug", "")),
                    batch_id=str(album.get("slug") or album.get("date") or ""),
                    image_no=index,
                    variant=index,
                    city=city,
                    place=str(image.get("place", "")),
                    category=category,
                    art_style=art_style,
                    age_band=age_band,
                    theme=str(album.get("summary") or album.get("shortTitle") or album.get("title") or ""),
                    scene=scene,
                    prompt_short=prompt_short(category, age_band, art_style, scene),
                    file_size_mb=file_size_mb(image_path),
                    width=width,
                    height=height,
                    aspect_ratio=aspect_ratio(width, height),
                    model="",
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


def scene_from_image(album: dict[str, object], image: dict[str, object]) -> str:
    title = str(image.get("title") or "")
    alt = str(image.get("alt") or "")
    summary = str(album.get("summary") or "")
    return " / ".join(part for part in [title, alt, summary] if part)


def prompt_short(category: str, age_band: str, art_style: str, scene: str) -> str:
    parts = [part for part in [age_band, category, art_style, scene] if part]
    return " | ".join(parts)[:1900]


def file_size_mb(path: Path) -> float:
    if not path.exists():
        return 0.0
    return round(path.stat().st_size / 1024 / 1024, 3)


def image_dimensions(path: Path) -> tuple[int, int]:
    if not path.exists():
        return (0, 0)
    try:
        from PIL import Image

        with Image.open(path) as image:
            return image.size
    except Exception:
        return (0, 0)


def aspect_ratio(width: int, height: int) -> str:
    if width <= 0 or height <= 0:
        return ""
    if width == height:
        return "1:1"
    if width > height:
        return "landscape"
    return "portrait"


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


def sync_existing_database(args: argparse.Namespace, records: list[ImageRecord]) -> int:
    token = require_env("NOTION_TOKEN")
    data_source_id = normalize_notion_id(args.data_source_id or os.getenv("NOTION_DATA_SOURCE_ID", ""))
    database_id = normalize_notion_id(args.database_id or os.getenv("NOTION_DATABASE_ID", ""))
    if not data_source_id and not database_id:
        print("ERROR: set NOTION_DATA_SOURCE_ID or NOTION_DATABASE_ID in .notion.env, or pass --data-source-id.", file=sys.stderr)
        return 2

    if data_source_id:
        client = NotionClient(token=token, notion_version=os.getenv("NOTION_DATA_SOURCE_VERSION", DATA_SOURCE_NOTION_VERSION))
        data_source = client.retrieve_data_source(data_source_id)
        client.ensure_data_source_properties(data_source_id, data_source, apply=args.confirm_upload)
        parent = {"data_source_id": data_source_id}
        existing_pages = client.query_pages_by_source_path(data_source_id=data_source_id)
    else:
        client = NotionClient(token=token, notion_version=os.getenv("NOTION_VERSION", DEFAULT_NOTION_VERSION))
        database = client.retrieve_database(database_id)
        client.ensure_database_properties(database_id, database, apply=args.confirm_upload)
        parent = database_page_parent(database)
        existing_pages = client.query_pages_by_source_path(database_id=database_id)

    matched = 0
    missing: list[ImageRecord] = []
    for record in records:
        page_id = existing_pages.get(record.source_path)
        if not page_id:
            missing.append(record)
            continue
        matched += 1
        print(f"[sync] {record.source_path}")
        if args.confirm_upload:
            client.update_page_metadata(page_id, record)
            time.sleep(args.delay)

    appended = 0
    if args.append_missing:
        for record in missing:
            appended += 1
            print(f"[append] {record.source_path}")
            if args.confirm_upload:
                file_upload = client.upload_file(record.image_path)
                client.create_page(parent=parent, record=record, file_upload_id=file_upload["id"])
                time.sleep(args.delay)

    if not args.confirm_upload:
        print("\ndry-run only. Add --confirm-upload to write Notion updates.")
    print(
        f"existing sync summary: matched={matched}, missing={len(missing)}, "
        f"append_requested={args.append_missing}, appended={appended if args.append_missing else 0}"
    )
    return 0


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

    def retrieve_database(self, database_id: str) -> dict[str, object]:
        return self.json_request("GET", f"/databases/{database_id}", None)

    def retrieve_data_source(self, data_source_id: str) -> dict[str, object]:
        return self.json_request("GET", f"/data_sources/{data_source_id}", None)

    def ensure_database_properties(self, database_id: str, database: dict[str, object], apply: bool) -> None:
        existing = database.get("properties")
        if not isinstance(existing, dict):
            existing = {}
        missing = {
            name: schema
            for name, schema in sync_database_properties().items()
            if name not in existing
        }
        if not missing:
            return
        print("missing database properties: " + ", ".join(sorted(missing)))
        if apply:
            self.json_request("PATCH", f"/databases/{database_id}", {"properties": missing})

    def ensure_data_source_properties(self, data_source_id: str, data_source: dict[str, object], apply: bool) -> None:
        existing = data_source.get("properties")
        if not isinstance(existing, dict):
            existing = {}
        missing = {
            name: schema
            for name, schema in sync_database_properties().items()
            if name not in existing
        }
        if not missing:
            return
        print("missing data source properties: " + ", ".join(sorted(missing)))
        if apply:
            self.json_request("PATCH", f"/data_sources/{data_source_id}", {"properties": missing})

    def query_pages_by_source_path(self, database_id: str = "", data_source_id: str = "") -> dict[str, str]:
        pages: dict[str, str] = {}
        payload: dict[str, object] = {"page_size": 100}
        if data_source_id:
            path = f"/data_sources/{data_source_id}/query"
        else:
            path = f"/databases/{database_id}/query"
        while True:
            result = self.json_request("POST", path, payload)
            for page in result.get("results", []):
                if not isinstance(page, dict):
                    continue
                source_path = source_path_from_page(page)
                page_id = page.get("id")
                if source_path and page_id:
                    pages[source_path] = str(page_id)
            if not result.get("has_more"):
                return pages
            payload["start_cursor"] = result.get("next_cursor")

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

    def update_page_metadata(self, page_id: str, record: ImageRecord) -> dict[str, object]:
        payload = {"properties": metadata_properties(record)}
        return self.json_request("PATCH", f"/pages/{page_id}", payload)

    def create_page(self, parent: dict[str, str], record: ImageRecord, file_upload_id: str) -> dict[str, object]:
        file_value = {"type": "file_upload", "file_upload": {"id": file_upload_id}}
        payload = {
            "parent": parent,
            "cover": file_value,
            "properties": {
                "Name": {"title": [{"type": "text", "text": {"content": record.name}}]},
                "Image": {"files": [file_value]},
                "Rating": {"select": None},
                "Preference": {"multi_select": []},
                "Note": {"rich_text": []},
                **metadata_properties(record),
            },
            "children": page_children(record),
        }
        return self.json_request("POST", "/pages", payload)

    def json_request(self, method: str, path: str, payload: Optional[dict[str, object]]) -> dict[str, object]:
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
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
        "Status": {
            "select": {
                "options": [
                    {"name": "Generated", "color": "gray"},
                    {"name": "Keep", "color": "green"},
                    {"name": "Reject", "color": "red"},
                    {"name": "Favorite", "color": "pink"},
                    {"name": "Posted", "color": "blue"},
                ]
            }
        },
        "Set": {"rich_text": {}},
        "Batch ID": {"rich_text": {}},
        "Image No": {"number": {"format": "number"}},
        "Variant": {"number": {"format": "number"}},
        "City": {"rich_text": {}},
        "Place": {"rich_text": {}},
        "Category": {"select": {}},
        "Art style": {"select": {}},
        "Age band": {"select": {}},
        "Theme": {"rich_text": {}},
        "Scene": {"rich_text": {}},
        "Prompt Short": {"rich_text": {}},
        "Model": {"select": {}},
        "Aspect Ratio": {"select": {}},
        "File Size MB": {"number": {"format": "number"}},
        "Width": {"number": {"format": "number"}},
        "Height": {"number": {"format": "number"}},
        "Rating": {
            "select": {
                "options": [
                    {"name": "5", "color": "red"},
                    {"name": "4", "color": "pink"},
                    {"name": "3", "color": "yellow"},
                    {"name": "2", "color": "blue"},
                    {"name": "1", "color": "gray"},
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


def sync_database_properties() -> dict[str, object]:
    properties = database_properties().copy()
    properties.pop("Name", None)
    properties.pop("Image", None)
    properties.pop("Rating", None)
    properties.pop("Preference", None)
    properties.pop("Note", None)
    return properties


def metadata_properties(record: ImageRecord) -> dict[str, object]:
    return {
        "Date": {"date": {"start": record.date} if record.date else None},
        "Status": {"select": {"name": "Generated"}},
        "Set": {"rich_text": [{"type": "text", "text": {"content": record.set_title}}]},
        "Batch ID": {"rich_text": [{"type": "text", "text": {"content": record.batch_id}}]},
        "Image No": {"number": record.image_no},
        "Variant": {"number": record.variant},
        "City": {"rich_text": [{"type": "text", "text": {"content": record.city}}]},
        "Place": {"rich_text": [{"type": "text", "text": {"content": record.place}}]},
        "Category": {"select": {"name": record.category} if record.category else None},
        "Art style": {"select": {"name": record.art_style} if record.art_style else None},
        "Age band": {"select": {"name": record.age_band} if record.age_band else None},
        "Theme": {"rich_text": [{"type": "text", "text": {"content": record.theme[:1900]}}]},
        "Scene": {"rich_text": [{"type": "text", "text": {"content": record.scene[:1900]}}]},
        "Prompt Short": {"rich_text": [{"type": "text", "text": {"content": record.prompt_short}}]},
        "Model": {"select": {"name": record.model} if record.model else None},
        "Aspect Ratio": {"select": {"name": record.aspect_ratio} if record.aspect_ratio else None},
        "File Size MB": {"number": record.file_size_mb},
        "Width": {"number": record.width or None},
        "Height": {"number": record.height or None},
        "Source path": {"rich_text": [{"type": "text", "text": {"content": record.source_path}}]},
        "Album URL": {"url": record.album_url or None},
        "Set slug": {"rich_text": [{"type": "text", "text": {"content": record.set_slug}}]},
    }


def source_path_from_page(page: dict[str, object]) -> str:
    properties = page.get("properties")
    if not isinstance(properties, dict):
        return ""
    source = properties.get("Source path")
    if not isinstance(source, dict):
        return ""
    rich_text = source.get("rich_text")
    if not isinstance(rich_text, list):
        return ""
    return "".join(str(part.get("plain_text", "")) for part in rich_text if isinstance(part, dict))


def page_children(record: ImageRecord) -> list[dict[str, object]]:
    return [
        notion_heading("Prompt"),
        notion_paragraph(record.prompt_short or "Full prompt is not available in album metadata yet."),
        notion_heading("Scene"),
        notion_paragraph(record.scene or record.theme),
        notion_heading("Review Notes"),
        notion_paragraph(""),
    ]


def notion_heading(text: str) -> dict[str, object]:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def notion_paragraph(text: str) -> dict[str, object]:
    rich_text = [{"type": "text", "text": {"content": text[:1900]}}] if text else []
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rich_text}}


if __name__ == "__main__":
    raise SystemExit(main())
