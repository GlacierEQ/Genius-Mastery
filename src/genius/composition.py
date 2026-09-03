"""Execution-backed contract composition for local Genius-family repositories."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any
from genius.family import analyze_family

_READY_STAGES = {"implemented", "verified", "operational", "operationally_verified"}

def execute_family_composition(root: Path) -> dict[str, Any]:
    analysis = analyze_family(root)
    repos = list(analysis.get("repositories") or [])
    ready = [
        row for row in (analysis.get("capabilities") or [])
        if str(row.get("stage") or "").casefold() in _READY_STAGES
    ]
    resolved = list(analysis.get("resolved_bindings") or [])
    unresolved = list(analysis.get("unresolved_bindings") or [])
    per_repo = {
        repo["repository"]: sum(1 for cap in ready if cap.get("repository") == repo["repository"])
        for repo in repos
    }
    combined = len({(cap.get("repository"), cap.get("id")) for cap in ready})
    isolated = max(per_repo.values(), default=0)
    core = {
        "schema_version": 1,
        "kind": "genius-family-composition-receipt",
        "repository_count": len(repos),
        "ready_capability_count": combined,
        "strongest_isolated_ready_capability_count": isolated,
        "contract_composition_gain": max(0, combined - isolated),
        "resolved_binding_count": len(resolved),
        "unresolved_binding_count": len(unresolved),
        "candidate_count": len(analysis.get("composition_candidates") or []),
        "participants": [repo["repository"] for repo in repos],
        "resolved_bindings": resolved,
        "unresolved_bindings": unresolved,
        "truth_note": (
            "This receipt proves contract discovery/resolution execution and combined capability visibility, "
            "not emergent domain behavior."
        ),
    }
    digest = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {**core, "sha256": digest}

def write_composition_receipt(root: Path, output: Path) -> Path:
    receipt = execute_family_composition(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output

def composition_report(receipt: dict[str, Any]) -> str:
    return "\n".join([
        "Genius family composition execution",
        f"repositories: {receipt.get('repository_count', 0)}",
        f"ready capabilities: {receipt.get('ready_capability_count', 0)}",
        f"strongest isolated: {receipt.get('strongest_isolated_ready_capability_count', 0)}",
        f"contract composition gain: {receipt.get('contract_composition_gain', 0)}",
        f"resolved bindings: {receipt.get('resolved_binding_count', 0)}",
        f"unresolved bindings: {receipt.get('unresolved_binding_count', 0)}",
        f"receipt sha256: {receipt.get('sha256')}",
    ])
