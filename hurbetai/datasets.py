"""Prepare explicitly supplied X/FxTwitter exports for local experiments.

This module intentionally does not scrape X or make requests to FxTwitter.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def import_fxtwitter_export(source: Path, destination: Path) -> int:
    """Convert a user-provided FxTwitter JSON response into local JSONL text records.

    Only use exports you are allowed to collect, retain, and use for training.
    """
    payload: Any = json.loads(source.read_text(encoding="utf-8"))
    posts = payload if isinstance(payload, list) else payload.get("tweets", [])
    if not isinstance(posts, list):
        raise ValueError("Expected a list of posts or an object with a 'tweets' list.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with destination.open("a", encoding="utf-8") as output:
        for post in posts:
            if not isinstance(post, dict):
                continue
            text = post.get("text") or post.get("content")
            if not isinstance(text, str) or not text.strip():
                continue
            record = {
                "text": text.strip(),
                "source": "user-provided-fxtwitter-export",
                "id": str(post.get("id", "")),
            }
            output.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
    return written
