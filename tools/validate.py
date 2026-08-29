#!/usr/bin/env python3
"""Genius-Mastery validator wrapper for the repository source tree."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

try:
    from genius.validate import validate_repo
except ImportError as exc:
    print(f"ERROR: cannot load Genius-Mastery validator: {exc}", file=sys.stderr)
    raise SystemExit(2)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate_repo(root)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS: contract surfaces OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
