"""Import a permitted, locally saved FxTwitter JSON export.

Usage: python import_fxtwitter_export.py path/to/export.json
"""

import sys
from pathlib import Path

from hurbetai.datasets import import_fxtwitter_export


if len(sys.argv) != 2:
    raise SystemExit("Usage: python import_fxtwitter_export.py path/to/export.json")

count = import_fxtwitter_export(Path(sys.argv[1]), Path("data/datasets/posts.jsonl"))
print(f"Imported {count} post(s) into data/datasets/posts.jsonl")
