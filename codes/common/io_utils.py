"""Small JSON helpers shared by every stage."""

from __future__ import annotations

import json
import os
from typing import Any


def create_directory(path: str) -> None:
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(obj: Any, path: str) -> None:
    create_directory(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def write_json_atomic(obj: Any, path: str) -> None:
    """Write via a temporary file, so an interrupted run never leaves a
    half-written cache behind."""
    create_directory(os.path.dirname(path))
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)


def load_jsonl(path: Any) -> list:
    """Read a JSONL file; a missing file reads as empty."""
    import pathlib
    p = pathlib.Path(path)
    if not p.exists():
        return []
    out = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def append_jsonl(path: Any, record: Any) -> None:
    """Append one record, creating the file and its directory if needed."""
    import pathlib
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_jsonl_by_key(path: Any, key: str) -> dict:
    """{record[key]: record} from a JSONL file. Later records win, so a file
    used as an append-only cache reads back deduplicated."""
    out = {}
    for record in load_jsonl(path):
        k = record.get(key)
        if k is not None:
            out[str(k)] = record
    return out
