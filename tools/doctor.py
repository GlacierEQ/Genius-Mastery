#!/usr/bin/env python3
"""Genius doctor — strength/weakness surface (seed)."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def load_yaml(path: Path):
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    genius = load_yaml(root / "GENIUS.yaml") or {}
    claims_data = load_yaml(root / "claims" / "CLAIMS.yaml") or {}
    claims = claims_data.get("claims") or []
    vector = load_yaml(root / "mastery" / "VECTOR.yaml") or {}
    frontier = load_yaml(root / "frontier" / "QUEUE.yaml") or {}
    composition = load_yaml(root / "interfaces" / "COMPOSITION.yaml") or {}

    print("=== Genius Doctor ===")
    print(f"repository: {genius.get('repository', '?')}")
    print(f"schema_version: {genius.get('schema_version', '?')}")
    print(f"package_version: {genius.get('package_version', '?')}")
    print()
    print("Claims by status:")
    by_status: dict[str, int] = {}
    by_dim: dict[str, int] = {}
    for c in claims:
        by_status[c.get("status", "?")] = by_status.get(c.get("status", "?"), 0) + 1
        by_dim[c.get("dimension", "?")] = by_dim.get(c.get("dimension", "?"), 0) + 1
    for k, v in sorted(by_status.items()):
        print(f"  {k}: {v}")
    print("Claims by dimension:")
    for k, v in sorted(by_dim.items()):
        print(f"  {k}: {v}")
    print()
    print("Mastery vector (diagnostic):")
    dims = vector.get("dimensions") or {}
    for name, meta in dims.items():
        if isinstance(meta, dict):
            print(f"  {name}: mapped={meta.get('claims_mapped', 0)} evidence={meta.get('claims_with_evidence', 0)} tier={meta.get('deepest_tier', '-')}")
    print()
    provides = composition.get("provides") or []
    print(f"Capabilities provided: {len(provides)}")
    for p in provides:
        print(f"  - {p.get('id')} [{p.get('stage')}]")
    print()
    items = frontier.get("items") or []
    open_items = [i for i in items if i.get("status") == "open"]
    print(f"Frontier open: {len(open_items)}")
    for i in open_items[:5]:
        print(f"  - {i.get('id')}: {i.get('question', '')[:80]}...")
    print()
    print("NOTE: No single mastery percentage is emitted by design.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
