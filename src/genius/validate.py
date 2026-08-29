"""Contract validation for a Genius repository root."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

REPO_NAME_RE = re.compile(r"^Genius-[A-Za-z0-9._-]+$")
SUPPORTED_SCHEMA = 2
SUPPORTED_CAPABILITY_SCHEMA = 1
SUPPORTED_ROLE_SCHEMA = 1
SUPPORTED_TEACHING_SCHEMA = 1

CLAIM_DIMENSIONS = {
    "foundations", "mechanisms", "implementation", "debugging",
    "verification", "performance", "reliability", "security",
    "observability", "operations", "synthesis_transfer",
    "teaching", "original_work",
}
CLAIM_STATUSES = {
    "mapped", "reproduced", "implemented",
    "adversarially_verified", "operationally_verified",
    "transferred", "frontier",
}
EVIDENCE_RESULTS = {"pass", "fail", "inconclusive", "counterevidence"}


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_claim_evidence_integrity(root: Path, errors: list[str]) -> None:
    claims_path = root / "claims" / "CLAIMS.yaml"
    claims = (load_yaml(claims_path) or {}).get("claims") or [] if claims_path.exists() else []
    claim_ids: set[str] = set()

    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim entry must be a mapping")
            continue
        cid = claim.get("id")
        if not cid:
            errors.append("claim missing id")
            continue
        if cid in claim_ids:
            errors.append(f"duplicate claim id: {cid}")
        claim_ids.add(cid)
        if claim.get("dimension") not in CLAIM_DIMENSIONS:
            errors.append(f"claim {cid}: invalid dimension {claim.get('dimension')!r}")
        if claim.get("status") not in CLAIM_STATUSES:
            errors.append(f"claim {cid}: invalid status {claim.get('status')!r}")

    ledger_path = root / "evidence" / "ledger.jsonl"
    evidence: dict[str, dict[str, Any]] = {}
    if ledger_path.exists():
        for line_number, raw in enumerate(
            ledger_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not raw.strip():
                continue
            try:
                item = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"evidence ledger line {line_number}: invalid JSON: {exc}")
                continue
            eid = item.get("id")
            if not eid:
                errors.append(f"evidence ledger line {line_number}: id missing")
                continue
            if eid in evidence:
                errors.append(f"duplicate evidence id: {eid}")
            evidence[eid] = item
            if item.get("result") not in EVIDENCE_RESULTS:
                errors.append(f"evidence {eid}: invalid result {item.get('result')!r}")

    evidence_ids = set(evidence)
    for claim in claims:
        if not isinstance(claim, dict) or not claim.get("id"):
            continue
        cid = claim["id"]
        for ref in claim.get("evidence_refs") or []:
            if ref not in evidence_ids:
                errors.append(f"claim {cid}: unknown evidence ref {ref}")

    for eid, item in evidence.items():
        for cid in item.get("claim_ids") or []:
            if cid not in claim_ids:
                errors.append(f"evidence {eid}: unknown claim ref {cid}")


def validate_capability_stack(root: Path, errors: list[str]) -> None:
    path = root / "capabilities" / "STACK.yaml"
    if not path.exists():
        errors.append("capabilities/STACK.yaml missing")
        return

    data = load_yaml(path)
    if not isinstance(data, dict):
        errors.append("capabilities/STACK.yaml is not a mapping")
        return
    if data.get("schema_version") != SUPPORTED_CAPABILITY_SCHEMA:
        errors.append(
            "capabilities/STACK.yaml schema_version must be "
            f"{SUPPORTED_CAPABILITY_SCHEMA}"
        )
    if not data.get("id"):
        errors.append("capabilities/STACK.yaml id missing")
    if not data.get("purpose"):
        errors.append("capabilities/STACK.yaml purpose missing")

    objective = data.get("objective")
    if not isinstance(objective, dict) or not objective.get("desired_reality"):
        errors.append("capabilities/STACK.yaml objective.desired_reality missing")

    layers = data.get("layers")
    if not isinstance(layers, dict) or not layers:
        errors.append("capabilities/STACK.yaml layers must be a non-empty mapping")

    verification = data.get("verification")
    if not isinstance(verification, dict):
        errors.append("capabilities/STACK.yaml verification missing")
    else:
        acceptance = verification.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance:
            errors.append(
                "capabilities/STACK.yaml verification.acceptance must be non-empty"
            )

    if not isinstance(data.get("mission_impact"), dict):
        errors.append("capabilities/STACK.yaml mission_impact missing")


def validate_capability_graph(root: Path, genius: dict[str, Any], errors: list[str]) -> None:
    raw = genius.get("capability_graph")
    path = root / raw if isinstance(raw, str) and raw else root / "capabilities" / "GRAPH.yaml"
    if not path.exists():
        if raw:
            errors.append(f"capability_graph target missing: {raw}")
        return
    data = load_yaml(path)
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(root)} is not a mapping")
        return
    if data.get("schema_version") != 1:
        errors.append(f"{path.relative_to(root)} schema_version must be 1")
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        errors.append(f"{path.relative_to(root)} nodes/edges must be lists")
        return
    node_ids = {node.get("id") for node in nodes if isinstance(node, dict) and node.get("id")}
    if len(node_ids) != len(nodes):
        errors.append(f"{path.relative_to(root)} node ids must be present and unique")
    for edge in edges:
        if not isinstance(edge, dict):
            errors.append(f"{path.relative_to(root)} edge must be a mapping")
            continue
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            errors.append(f"{path.relative_to(root)} edge references unknown node")
        if not edge.get("relation"):
            errors.append(f"{path.relative_to(root)} edge relation missing")


def validate_role_brief(root: Path, genius: dict[str, Any], errors: list[str]) -> None:
    raw = genius.get("role_brief")
    path = root / raw if isinstance(raw, str) and raw else root / "ROLE.yaml"
    if not path.exists():
        if raw:
            errors.append(f"role_brief target missing: {raw}")
        return
    data = load_yaml(path)
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(root)} is not a mapping")
        return
    if data.get("schema_version") != SUPPORTED_ROLE_SCHEMA:
        errors.append(f"{path.relative_to(root)} schema_version must be 1")
    if not data.get("role"):
        errors.append(f"{path.relative_to(root)} role missing")
    outcomes = data.get("outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        errors.append(f"{path.relative_to(root)} outcomes must be non-empty")


def validate_teaching(root: Path, genius: dict[str, Any], errors: list[str]) -> None:
    raw = genius.get("teaching_contract")
    path = root / raw if isinstance(raw, str) and raw else root / "teaching" / "TEACHING.yaml"
    if not path.exists():
        if raw:
            errors.append(f"teaching_contract target missing: {raw}")
        return
    data = load_yaml(path)
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(root)} is not a mapping")
        return
    if data.get("schema_version") != SUPPORTED_TEACHING_SCHEMA:
        errors.append(f"{path.relative_to(root)} schema_version must be 1")
    if not data.get("teacher") or not data.get("subject"):
        errors.append(f"{path.relative_to(root)} teacher/subject incomplete")
    method = data.get("method")
    if not isinstance(method, dict):
        errors.append(f"{path.relative_to(root)} method missing")
    else:
        for phase in ("explain", "demonstrate", "reconstruct", "transfer"):
            values = method.get(phase)
            if not isinstance(values, list) or not values:
                errors.append(f"{path.relative_to(root)} method.{phase} must be non-empty")
    verification = data.get("verification")
    if not isinstance(verification, dict) or not verification.get("acceptance"):
        errors.append(f"{path.relative_to(root)} verification.acceptance missing")


def validate_repo(root: Path) -> list[str]:
    """Return list of error strings; empty means PASS."""
    errors: list[str] = []
    genius_path = root / "GENIUS.yaml"
    if not genius_path.exists():
        errors.append("GENIUS.yaml missing")
        return errors

    data = load_yaml(genius_path)
    if not isinstance(data, dict):
        errors.append("GENIUS.yaml is not a mapping")
        return errors

    if data.get("schema_version") != SUPPORTED_SCHEMA:
        errors.append(
            f"Unsupported schema_version={data.get('schema_version')}; required {SUPPORTED_SCHEMA}"
        )

    repo = data.get("repository")
    if not isinstance(repo, str) or not REPO_NAME_RE.match(repo):
        errors.append(f"repository must match ^Genius-[A-Za-z0-9._-]+$, got {repo!r}")

    if data.get("family") != "Genius":
        errors.append("family must be 'Genius'")
    if data.get("doctrine") != "mastery-not-skills":
        errors.append("doctrine must be 'mastery-not-skills'")

    for field in (
        "composition_contract",
        "capability_anatomy_contract",
        "capability_graph",
        "teaching_contract",
        "role_brief",
        "synthesis_plan",
        "persona",
        "teaching_plan",
    ):
        raw = data.get(field)
        if raw and isinstance(raw, str) and not (root / raw).exists():
            errors.append(f"{field} target missing: {raw}")

    claims_path = root / "claims" / "CLAIMS.yaml"
    if claims_path.exists():
        claims = (load_yaml(claims_path) or {}).get("claims") or []
        ids: set[str] = set()
        for claim in claims:
            cid = claim.get("id")
            if not cid:
                errors.append("claim missing id")
                continue
            if cid in ids:
                errors.append(f"duplicate claim id: {cid}")
            ids.add(cid)
            if not claim.get("statement") or len(str(claim["statement"])) < 10:
                errors.append(f"claim {cid}: statement too short or missing")

    comp_path = root / "interfaces" / "COMPOSITION.yaml"
    if comp_path.exists():
        comp = load_yaml(comp_path) or {}
        provides = comp.get("provides") or []
        pids: set[str] = set()
        for item in provides:
            pid = item.get("id")
            if not pid:
                errors.append("provides entry missing id")
                continue
            if pid in pids:
                errors.append(f"duplicate capability id: {pid}")
            pids.add(pid)

    validate_claim_evidence_integrity(root, errors)
    validate_capability_stack(root, errors)
    validate_capability_graph(root, data, errors)
    validate_role_brief(root, data, errors)
    validate_teaching(root, data, errors)
    return errors
