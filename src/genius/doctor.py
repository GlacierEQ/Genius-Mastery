"""Doctor diagnostic surface."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def doctor_report(root: Path) -> str:
    genius = load_yaml(root / "GENIUS.yaml") or {}
    claims_data = load_yaml(root / "claims" / "CLAIMS.yaml") or {}
    claims = claims_data.get("claims") or []
    vector = load_yaml(root / "mastery" / "VECTOR.yaml") or {}
    frontier = load_yaml(root / "frontier" / "QUEUE.yaml") or {}
    composition = load_yaml(root / "interfaces" / "COMPOSITION.yaml") or {}

    lines: list[str] = []
    lines.append("=== Genius Doctor ===")
    lines.append(f"repository: {genius.get('repository', '?')}")
    lines.append(f"schema_version: {genius.get('schema_version', '?')}")
    lines.append(f"package_version: {genius.get('package_version', genius.get('schema_version', '?'))}")
    lines.append("")

    by_status: dict[str, int] = {}
    by_dim: dict[str, int] = {}
    for c in claims:
        by_status[c.get("status", "?")] = by_status.get(c.get("status", "?"), 0) + 1
        by_dim[c.get("dimension", "?")] = by_dim.get(c.get("dimension", "?"), 0) + 1
    lines.append("Claims by status:")
    for k, v in sorted(by_status.items()):
        lines.append(f"  {k}: {v}")
    lines.append("Claims by dimension:")
    for k, v in sorted(by_dim.items()):
        lines.append(f"  {k}: {v}")
    lines.append("")

    lines.append("Mastery vector (diagnostic):")
    dims = vector.get("dimensions") or {}
    for name, meta in dims.items():
        if isinstance(meta, dict):
            lines.append(
                f"  {name}: mapped={meta.get('claims_mapped', 0)} "
                f"evidence={meta.get('claims_with_evidence', 0)} "
                f"tier={meta.get('deepest_tier', '-')}"
            )
    lines.append("")

    provides = composition.get("provides") or []
    lines.append(f"Capabilities provided: {len(provides)}")
    for p in provides:
        lines.append(f"  - {p.get('id')} [{p.get('stage')}]")
    lines.append("")

    items = frontier.get("items") or []
    open_items = [i for i in items if i.get("status") == "open"]
    lines.append(f"Frontier open: {len(open_items)}")
    for i in open_items[:5]:
        q = (i.get("question") or "")[:80]
        lines.append(f"  - {i.get('id')}: {q}...")
    lines.append("")
    lines.append("NOTE: No single mastery percentage is emitted by design.")
    return "\n".join(lines)
