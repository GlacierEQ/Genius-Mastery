"""Family discovery and cross-Genius composition intelligence."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


_STOPWORDS = {
    "genius", "capability", "method", "kernel", "shared", "contract",
    "interface", "repository", "mastery", "mapped", "implemented",
}


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if len(token) >= 3 and token not in _STOPWORDS
    }


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"expected mapping in {path}")
    return data


def discover_family(root: Path) -> list[dict[str, Any]]:
    """Discover local Genius repositories and their composition contracts."""
    root = root.resolve()
    repositories: list[dict[str, Any]] = []

    if (root / "GENIUS.yaml").exists():
        candidates = [root]
    else:
        candidates = sorted(
            path for path in root.iterdir()
            if path.is_dir() and path.name.startswith("Genius-")
        )

    for repo_root in candidates:
        genius_path = repo_root / "GENIUS.yaml"
        if not genius_path.exists():
            continue
        genius = _load_yaml(genius_path)
        repository = str(genius.get("repository") or repo_root.name)
        if not repository.startswith("Genius-"):
            continue

        contract_rel = str(
            genius.get("composition_contract") or "interfaces/COMPOSITION.yaml"
        )
        contract_path = repo_root / contract_rel
        contract: dict[str, Any] = {}
        contract_state = "missing"
        if contract_path.exists():
            contract = _load_yaml(contract_path)
            contract_state = "loaded"

        repositories.append(
            {
                "repository": repository,
                "purpose": genius.get("purpose"),
                "root": str(repo_root),
                "spec_version": contract.get("spec_version"),
                "contract_state": contract_state,
                "provides": list(contract.get("provides") or []),
                "consumes": list(contract.get("consumes") or []),
            }
        )

    repositories.sort(key=lambda item: item["repository"])
    return repositories


def analyze_family(root: Path) -> dict[str, Any]:
    """Resolve family dependencies and surface complementary capability pairs."""
    repositories = discover_family(root)
    by_repo = {item["repository"]: item for item in repositories}

    providers: dict[tuple[str, str], dict[str, Any]] = {}
    capability_rows: list[dict[str, Any]] = []
    for repo in repositories:
        for provided in repo["provides"]:
            if not isinstance(provided, dict) or not provided.get("id"):
                continue
            cap_id = str(provided["id"])
            row = {
                "repository": repo["repository"],
                "id": cap_id,
                "description": str(provided.get("description") or ""),
                "stage": str(provided.get("stage") or "unknown"),
                "interface": provided.get("interface"),
                "evidence_refs": list(provided.get("evidence_refs") or []),
            }
            providers[(repo["repository"], cap_id)] = row
            capability_rows.append(row)

    bindings: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for consumer in repositories:
        for consume in consumer["consumes"]:
            if not isinstance(consume, dict):
                continue
            provider_repo = str(consume.get("repository") or "")
            capability = str(consume.get("capability") or "")
            if not provider_repo or not capability:
                continue
            provider = providers.get((provider_repo, capability))
            binding = {
                "consumer": consumer["repository"],
                "provider": provider_repo,
                "capability": capability,
                "reason": consume.get("reason"),
                "minimum_spec_version": consume.get("minimum_spec_version"),
                "resolved": provider is not None,
            }
            if provider is not None:
                binding["provider_stage"] = provider["stage"]
                binding["provider_interface"] = provider["interface"]
                binding["provider_evidence_refs"] = provider["evidence_refs"]
                bindings.append(binding)
            else:
                unresolved.append(binding)

    synergies: list[dict[str, Any]] = []
    for index, left in enumerate(capability_rows):
        for right in capability_rows[index + 1:]:
            if left["repository"] == right["repository"]:
                continue

            left_tokens = _tokens(left["id"] + " " + left["description"])
            right_tokens = _tokens(right["id"] + " " + right["description"])
            shared = sorted(left_tokens & right_tokens)
            if not shared:
                continue

            union = left_tokens | right_tokens
            similarity = len(shared) / max(1, len(union))
            evidence_bonus = min(
                0.2,
                0.04 * (
                    len(left["evidence_refs"]) + len(right["evidence_refs"])
                ),
            )
            score = min(1.0, similarity + 0.08 * len(shared) + evidence_bonus)
            synergies.append(
                {
                    "repositories": sorted(
                        [left["repository"], right["repository"]]
                    ),
                    "capabilities": [left["id"], right["id"]],
                    "shared_terms": shared,
                    "score": round(score, 4),
                    "reason": (
                        "Complementary capability vocabulary suggests a "
                        "composition candidate; execution/evidence still required."
                    ),
                }
            )

    synergies.sort(
        key=lambda item: (-item["score"], item["repositories"], item["capabilities"])
    )
    capability_rows.sort(key=lambda item: (item["repository"], item["id"]))
    bindings.sort(key=lambda item: (item["consumer"], item["provider"], item["capability"]))
    unresolved.sort(key=lambda item: (item["consumer"], item["provider"], item["capability"]))

    consumers_by_provider: dict[str, list[str]] = {}
    for binding in bindings:
        consumers_by_provider.setdefault(binding["provider"], []).append(
            binding["consumer"]
        )

    return {
        "schema_version": 1,
        "root": str(root.resolve()),
        "repository_count": len(repositories),
        "capability_count": len(capability_rows),
        "repositories": repositories,
        "capabilities": capability_rows,
        "resolved_bindings": bindings,
        "unresolved_bindings": unresolved,
        "provider_fanout": {
            repo: sorted(set(consumers))
            for repo, consumers in sorted(consumers_by_provider.items())
        },
        "composition_candidates": synergies,
        "truth_note": (
            "Resolved bindings prove declared contract compatibility only. "
            "Composition candidates are discovery hypotheses until challenged "
            "and verified in execution."
        ),
    }


def family_report(analysis: dict[str, Any], *, top: int = 10) -> str:
    lines = [
        "Genius family composition intelligence",
        f"repositories: {analysis.get('repository_count', 0)}",
        f"capabilities: {analysis.get('capability_count', 0)}",
        f"resolved bindings: {len(analysis.get('resolved_bindings') or [])}",
        f"unresolved bindings: {len(analysis.get('unresolved_bindings') or [])}",
        "",
        "Top composition candidates:",
    ]
    candidates = list(analysis.get("composition_candidates") or [])
    for index, item in enumerate(candidates[: max(1, top)], 1):
        repos = " + ".join(item["repositories"])
        caps = " × ".join(item["capabilities"])
        terms = ", ".join(item["shared_terms"])
        lines.append(
            f"{index:>2}. {repos}: {caps} score={item['score']:.4f} "
            f"shared=[{terms}]"
        )
    if not candidates:
        lines.append("  (none discovered)")

    unresolved = list(analysis.get("unresolved_bindings") or [])
    if unresolved:
        lines.extend(["", "Unresolved declared dependencies:"])
        for item in unresolved:
            lines.append(
                f"  - {item['consumer']} -> {item['provider']}:{item['capability']}"
            )
    return "\n".join(lines)
