"""Evidence-derived mastery vector computation.

The vector is a diagnostic projection of claims and receipts. It never invents
capability and never turns counts into a global mastery percentage.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


DIMENSIONS = [
    "foundations",
    "mechanisms",
    "implementation",
    "debugging",
    "verification",
    "performance",
    "reliability",
    "security",
    "observability",
    "operations",
    "synthesis_transfer",
    "teaching",
    "original_work",
]

STATUS_RANK = {
    "frontier": 0,
    "mapped": 1,
    "reproduced": 2,
    "implemented": 3,
    "adversarially_verified": 4,
    "operationally_verified": 5,
    "transferred": 6,
}


def _load_claims(root: Path) -> list[dict[str, Any]]:
    path = root / "claims" / "CLAIMS.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    claims = payload.get("claims") or []
    if not isinstance(claims, list):
        raise ValueError(f"{path}: claims must be a list")
    return [claim for claim in claims if isinstance(claim, dict)]


def _load_evidence(root: Path) -> dict[str, dict[str, Any]]:
    path = root / "evidence" / "ledger.jsonl"
    if not path.exists():
        return {}

    evidence: dict[str, dict[str, Any]] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        if not isinstance(entry, dict) or not entry.get("id"):
            raise ValueError(f"{path}:{number}: evidence entry requires id")
        evidence_id = str(entry["id"])
        if evidence_id in evidence:
            raise ValueError(f"{path}:{number}: duplicate evidence id {evidence_id}")
        evidence[evidence_id] = entry
    return evidence


def _deepest_status(status_counts: dict[str, int]) -> str | None:
    present = [status for status, count in status_counts.items() if count]
    if not present:
        return None
    return max(present, key=lambda status: STATUS_RANK.get(status, -1))


def repository_identity(root: Path) -> str:
    """Stable Genius repository id. Never the checkout directory name.

    Buildkite clones into `.../casey-1/genius-mastery`; developers clone
    `Genius-Mastery`. VECTOR.yaml must follow GENIUS.yaml, not Path.name.
    """
    root = root.resolve()
    path = root / "GENIUS.yaml"
    if path.exists():
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(payload, dict):
            repo = str(payload.get("repository") or "").strip()
            if repo:
                return repo
    return root.name


def compute_vector(root: Path) -> dict[str, Any]:
    """Compute an evidence-derived multidimensional mastery vector."""
    root = root.resolve()
    claims = _load_claims(root)
    evidence = _load_evidence(root)

    dimensions: dict[str, dict[str, Any]] = {}
    unresolved_evidence_refs: list[dict[str, str]] = []
    evidence_to_claims: dict[str, set[str]] = {}

    for dimension in DIMENSIONS:
        dimension_claims = [
            claim for claim in claims if str(claim.get("dimension") or "") == dimension
        ]
        status_counts = {status: 0 for status in STATUS_RANK}
        claims_with_evidence = 0
        counterevidence_claims = 0
        verified_claims = 0

        for claim in dimension_claims:
            claim_id = str(claim.get("id") or "")
            status = str(claim.get("status") or "")
            if status in status_counts:
                status_counts[status] += 1
            if STATUS_RANK.get(status, -1) >= STATUS_RANK["adversarially_verified"]:
                verified_claims += 1

            refs = [str(ref) for ref in claim.get("evidence_refs") or [] if ref]
            if refs:
                claims_with_evidence += 1
            if claim.get("counterevidence_refs"):
                counterevidence_claims += 1

            for ref in refs:
                evidence_to_claims.setdefault(ref, set()).add(claim_id)
                if ref not in evidence:
                    unresolved_evidence_refs.append(
                        {"claim_id": claim_id, "evidence_ref": ref}
                    )

        dimensions[dimension] = {
            "claims_mapped": len(dimension_claims),
            "claims_with_evidence": claims_with_evidence,
            "verified_claims": verified_claims,
            "counterevidence_claims": counterevidence_claims,
            "deepest_tier": _deepest_status(status_counts),
            "status_counts": {
                status: count
                for status, count in status_counts.items()
                if count
            },
        }

    orphan_evidence = sorted(
        evidence_id
        for evidence_id in evidence
        if evidence_id not in evidence_to_claims
    )
    ledger_claim_mismatches: list[dict[str, str]] = []
    claim_ids = {str(claim.get("id") or "") for claim in claims}
    for evidence_id, entry in evidence.items():
        for claim_id in entry.get("claim_ids") or []:
            claim_id = str(claim_id)
            if claim_id and claim_id not in claim_ids:
                ledger_claim_mismatches.append(
                    {"evidence_id": evidence_id, "claim_id": claim_id}
                )

    total_claims = len(claims)
    claims_with_evidence = sum(
        1 for claim in claims if claim.get("evidence_refs")
    )
    verified_claims = sum(
        1
        for claim in claims
        if STATUS_RANK.get(str(claim.get("status") or ""), -1)
        >= STATUS_RANK["adversarially_verified"]
    )

    return {
        "schema_version": 2,
        "repository": repository_identity(root),
        "representation": "evidence-derived-multidimensional-vector",
        "dimensions": dimensions,
        "totals": {
            "claims": total_claims,
            "claims_with_evidence": claims_with_evidence,
            "verified_claims": verified_claims,
            "evidence_entries": len(evidence),
            "dimensions_with_claims": sum(
                1 for value in dimensions.values() if value["claims_mapped"]
            ),
        },
        "integrity": {
            "unresolved_evidence_refs": sorted(
                unresolved_evidence_refs,
                key=lambda item: (item["claim_id"], item["evidence_ref"]),
            ),
            "ledger_claim_mismatches": sorted(
                ledger_claim_mismatches,
                key=lambda item: (item["evidence_id"], item["claim_id"]),
            ),
            "orphan_evidence": orphan_evidence,
            "clean": not unresolved_evidence_refs and not ledger_claim_mismatches,
        },
        "truth_note": (
            "This vector is a projection of recorded claims and evidence. "
            "It is not a scalar mastery score and does not infer capability "
            "beyond claim status plus linked receipts."
        ),
    }


def write_vector(root: Path, output: Path | None = None) -> Path:
    """Compute and persist the mastery vector."""
    root = root.resolve()
    target = output.resolve() if output else root / "mastery" / "VECTOR.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    vector = compute_vector(root)
    target.write_text(
        yaml.safe_dump(vector, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return target


def vector_report(vector: dict[str, Any]) -> str:
    totals = vector.get("totals") or {}
    integrity = vector.get("integrity") or {}
    lines = [
        f"Mastery vector: {vector.get('repository', 'unknown')}",
        f"claims: {totals.get('claims', 0)}",
        f"claims_with_evidence: {totals.get('claims_with_evidence', 0)}",
        f"verified_claims: {totals.get('verified_claims', 0)}",
        f"evidence_entries: {totals.get('evidence_entries', 0)}",
        f"integrity_clean: {bool(integrity.get('clean'))}",
        "",
        "Dimensions:",
    ]
    for name, row in (vector.get("dimensions") or {}).items():
        if not row.get("claims_mapped"):
            continue
        lines.append(
            f"- {name}: claims={row['claims_mapped']} "
            f"evidence={row['claims_with_evidence']} "
            f"verified={row['verified_claims']} "
            f"deepest={row['deepest_tier']}"
        )

    unresolved = integrity.get("unresolved_evidence_refs") or []
    mismatches = integrity.get("ledger_claim_mismatches") or []
    if unresolved or mismatches:
        lines.extend(["", "Integrity findings:"])
        for item in unresolved:
            lines.append(
                f"- unresolved evidence {item['evidence_ref']} "
                f"for {item['claim_id']}"
            )
        for item in mismatches:
            lines.append(
                f"- ledger {item['evidence_id']} references missing "
                f"claim {item['claim_id']}"
            )
    return "\n".join(lines)
