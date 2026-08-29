#!/usr/bin/env python3
"""Genius doctor wrapper for the repository source tree."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from genius.doctor import doctor_report


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    print(doctor_report(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
