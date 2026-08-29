"""Capability-source adapters for Genius synthesis.

Adapters enrich a synthesized entity with real reusable capability references.
They never copy implementation bodies into the generated repository.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

MEGA_REGISTRIES = {
    "skill": "registry/skills.json",
    "combo-skill": "registry/combo-skills.json",
    "mega-skill": "registry/mega-skills.json",
}


def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", value.casefold()))


def _flatten_text(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            out.append(str(key))
            out.extend(_flatten_text(item))
    elif isinstance(value, list):
        for item in value:
            out.extend(_flatten_text(item))
    return out


def load_mega_skills_registry(root: Path) -> list[dict[str, Any]]:
    """Load atomic, combo, and mega registry entries from a local checkout."""
    root = root.resolve()
    capabilities: list[dict[str, Any]] = []
    for kind, rel in MEGA_REGISTRIES.items():
        path = root / rel
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        entries = payload.get("entries") or []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            capabilities.append(
                {
                    "kind": kind,
                    "id": entry.get("id", ""),
                    "display_name": entry.get("display_name", ""),
                    "maturity": entry.get("maturity", ""),
                    "version": entry.get("version", ""),
                    "entrypoint": entry.get("entrypoint", ""),
                    "source_repository": "GlacierEQ/mega-skills",
                    "source_registry": rel,
                    "_raw": entry,
                }
            )
    return capabilities


def match_mega_skills(
    role: str,
    outcomes: list[str],
    root: Path,
    *,
    limit: int = 16,
) -> list[dict[str, Any]]:
    """Rank real Mega Skills registry entries against a role brief.

    Scoring is deliberately transparent and deterministic. It is a first-pass
    retrieval mechanism, not semantic proof that a capability is appropriate.
    """
    query_tokens = _tokens(" ".join([role, *outcomes]))
    ranked: list[tuple[int, str, dict[str, Any]]] = []

    for capability in load_mega_skills_registry(root):
        raw = capability["_raw"]
        identity_tokens = _tokens(
            " ".join(
                str(raw.get(key, ""))
                for key in ("id", "display_name")
            )
        )
        body_tokens = _tokens(" ".join(_flatten_text(raw)))

        identity_overlap = len(query_tokens.intersection(identity_tokens))
        body_overlap = len(query_tokens.intersection(body_tokens))
        score = identity_overlap * 5 + body_overlap

        if score <= 0:
            continue

        clean = {key: value for key, value in capability.items() if key != "_raw"}
        clean["match_score"] = score
        clean["matched_terms"] = sorted(query_tokens.intersection(body_tokens))
        ranked.append((score, str(clean.get("id", "")), clean))

    ranked.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in ranked[:limit]]
