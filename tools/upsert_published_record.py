#!/usr/bin/env python3
"""Upsert one real published record in the canonical Markdown ledger.

The input is a JSON object. Records are stored in marked blocks so an update
replaces the old block instead of appending a duplicate.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

OPEN = '<!-- PUBLISHED_RECORD id="{record_id}" -->'
CLOSE = "<!-- /PUBLISHED_RECORD -->"
BLOCK_RE = re.compile(
    r'<!-- PUBLISHED_RECORD id="(?P<id>[^"]+)" -->\n.*?<!-- /PUBLISHED_RECORD -->',
    re.S,
)


def norm(value: object) -> str:
    return str(value or "").strip().lower()


def identity_keys(record: dict) -> list[tuple[str, str]]:
    platform = norm(record.get("platform"))
    return [
        ("record_id", norm(record.get("record_id"))),
        ("content_id", norm(record.get("content_id"))),
        ("url", norm(record.get("url"))),
        ("platform_published_at", f"{platform}|{norm(record.get('published_at'))}"),
        ("platform_title_date", f"{platform}|{norm(record.get('title'))}|{norm(record.get('published_date'))}"),
    ]


def render(record: dict) -> str:
    rid = record["record_id"]
    lines = [OPEN.format(record_id=rid), f"## {record.get('title', '未命名内容')}", ""]
    for key in ("record_id", "platform", "content_id", "url", "published_at", "published_date", "status", "source", "collected_at", "correction_note"):
        if record.get(key) not in (None, "", []):
            lines.append(f"- **{key}**：{record[key]}")
    if record.get("metrics"):
        lines += ["", "### 真实数据", ""]
        for key, value in record["metrics"].items():
            lines.append(f"- **{key}**：{value}")
    if record.get("script"):
        lines += ["", "### 实际发布文案", "", record["script"]]
    lines += ["", CLOSE]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Upsert a published record without creating duplicates")
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--record", required=True, type=Path, help="JSON file containing one published record")
    args = parser.parse_args()

    record = json.loads(args.record.read_text(encoding="utf-8"))
    required = ["record_id", "platform"]
    missing = [key for key in required if not record.get(key)]
    if missing:
        raise SystemExit(f"missing required field(s): {', '.join(missing)}")
    if not any(record.get(key) for key in ("content_id", "url", "published_at", "title")):
        raise SystemExit("at least one identity field is required: content_id, url, published_at, or title")

    text = args.ledger.read_text(encoding="utf-8") if args.ledger.exists() else ""
    blocks = list(BLOCK_RE.finditer(text))
    incoming_keys = {pair for pair in identity_keys(record) if pair[1]}
    matches: list[re.Match[str]] = []
    for block in blocks:
        old = {"record_id": block.group("id")}
        for key, value in re.findall(r"^- \*\*(.+?)\*\*：(.+?)$", block.group(0), re.M):
            old[key] = value
        old_keys = {pair for pair in identity_keys(old) if pair[1]}
        if old_keys & incoming_keys:
            matches.append(block)

    if len(matches) > 1:
        raise SystemExit("integrity error: more than one marked record matches this identity")

    new_block = render(record)
    if matches:
        match = matches[0]
        text = text[: match.start()] + new_block + text[match.end() :]
        action = "updated"
    else:
        heading = "## 机器可维护发布记录"
        if heading not in text:
            text = text.rstrip() + f"\n\n{heading}\n\n"
        text = text.rstrip() + "\n\n" + new_block + "\n"
        action = "created"
    args.ledger.write_text(text, encoding="utf-8")
    print(json.dumps({"action": action, "record_id": record["record_id"], "ledger": str(args.ledger)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
