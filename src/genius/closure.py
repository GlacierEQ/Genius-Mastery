"""Release-closure diagnostics for Genius-Mastery and descendants."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from genius.validate import validate_repo
from genius.vector import compute_vector

def _yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}

def closure_status(root: Path) -> dict[str, Any]:
    root = root.resolve()
    errors = validate_repo(root)
    vector = compute_vector(root)
    roadmap = _yaml(root / "mastery" / "ROADMAP.yaml")
    frontier = _yaml(root / "frontier" / "QUEUE.yaml")
    near_term = list(roadmap.get("near_term") or [])
    blockers = [
        item for item in (frontier.get("items") or [])
        if isinstance(item, dict)
        and item.get("release_blocker") is True
        and item.get("status") not in {"resolved", "closed", "complete"}
    ]
    return {
        "schema_version": 1,
        "kind": "genius-closure-status",
        "repository": root.name,
        "validation_clean": not errors,
        "validation_errors": errors,
        "evidence_integrity_clean": bool((vector.get("integrity") or {}).get("clean")),
        "near_term_remaining": near_term,
        "release_blockers": blockers,
        "external_verification": list(roadmap.get("external_verification") or []),
        "core_complete": not errors and bool((vector.get("integrity") or {}).get("clean")) and not near_term and not blockers,
        "truth_note": "Core completion is a release boundary, not the end of open-ended mastery research.",
    }

def closure_report(status: dict[str, Any]) -> str:
    lines = [
        "Genius closure",
        f"repository: {status.get('repository')}",
        f"validation_clean: {status.get('validation_clean')}",
        f"evidence_integrity_clean: {status.get('evidence_integrity_clean')}",
        f"near_term_remaining: {len(status.get('near_term_remaining') or [])}",
        f"release_blockers: {len(status.get('release_blockers') or [])}",
        f"core_complete: {status.get('core_complete')}",
    ]
    for item in status.get("near_term_remaining") or []:
        lines.append(f"  near-term: {item}")
    return "\n".join(lines)
