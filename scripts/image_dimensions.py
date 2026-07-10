#!/usr/bin/env python3
"""Small image dimension reader for generated gallery assets."""

from __future__ import annotations

from math import gcd
from pathlib import Path
import struct


def aspect_ratio(width: int, height: int) -> str:
    common_ratios = [
        ("1:1", 1, 1),
        ("4:3", 4, 3),
        ("3:2", 3, 2),
        ("3:4", 3, 4),
        ("2:3", 2, 3),
        ("9:16", 9, 16),
        ("4:7", 4, 7),
        ("1:2", 1, 2),
    ]
    actual = width / height
    for label, ratio_width, ratio_height in common_ratios:
        target = ratio_width / ratio_height
        if abs(actual - target) / target <= 0.02:
            return label
    divisor = gcd(width, height) or 1
    return f"{width // divisor}:{height // divisor}"


def image_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix == ".png":
        return png_dimensions(data)
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_dimensions(data)
    if suffix == ".webp":
        return webp_dimensions(data)
    raise ValueError(f"unsupported image type: {path}")


def png_dimensions(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or data[12:16] != b"IHDR":
        raise ValueError("invalid PNG header")
    return struct.unpack(">II", data[16:24])


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("invalid JPEG header")
    offset = 2
    while offset < len(data):
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break
        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9}:
            continue
        if offset + 2 > len(data):
            break
        segment_length = struct.unpack(">H", data[offset : offset + 2])[0]
        if segment_length < 2 or offset + segment_length > len(data):
            break
        if 0xC0 <= marker <= 0xCF and marker not in {0xC4, 0xC8, 0xCC}:
            height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
            return width, height
        offset += segment_length
    raise ValueError("JPEG dimensions not found")


def webp_dimensions(data: bytes) -> tuple[int, int]:
    if len(data) < 16 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("invalid WebP header")
    offset = 12
    while offset + 8 <= len(data):
        chunk_type = data[offset : offset + 4]
        chunk_size = struct.unpack("<I", data[offset + 4 : offset + 8])[0]
        payload = data[offset + 8 : offset + 8 + chunk_size]
        if chunk_type == b"VP8X":
            if len(payload) < 10:
                raise ValueError("invalid VP8X chunk")
            width = 1 + int.from_bytes(payload[4:7], "little")
            height = 1 + int.from_bytes(payload[7:10], "little")
            return width, height
        if chunk_type == b"VP8L":
            if len(payload) < 5 or payload[0] != 0x2F:
                raise ValueError("invalid VP8L chunk")
            bits = int.from_bytes(payload[1:5], "little")
            width = (bits & 0x3FFF) + 1
            height = ((bits >> 14) & 0x3FFF) + 1
            return width, height
        if chunk_type == b"VP8 ":
            if len(payload) < 10:
                raise ValueError("invalid VP8 chunk")
            start = payload.find(b"\x9d\x01\x2a")
            if start < 0 or start + 7 > len(payload):
                raise ValueError("VP8 frame header not found")
            width = struct.unpack("<H", payload[start + 3 : start + 5])[0] & 0x3FFF
            height = struct.unpack("<H", payload[start + 5 : start + 7])[0] & 0x3FFF
            return width, height
        offset += 8 + chunk_size + (chunk_size % 2)
    raise ValueError("WebP dimensions not found")
