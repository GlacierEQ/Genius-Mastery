"""Verified mission -> reusable capability -> future mission reuse.

This module extends the existing Genius composition model without claiming that
contract similarity proves runtime success.  A capability may only be extracted
from a mission whose verification status is explicitly verified, and reuse
selection remains an evidence-bounded deterministic recommendation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from genius.family import _tokens

_VERIFIED_MISSION_STATES = {"verified", "operationally_verified"}
_STAGE_WEIGHT = {
    "operationally_verified": 1.0,
    "verified": 1.0,
    "operational": 0.9,
    "implemented": 0.75,
    "mapped": 0.45,
    "designed_for": 0.3,
    "aspirational": 0.1,
    "unknown": 0.0,
}


def _strings(value: Any) -> Iterable[str]:
    if value is None:
        return
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, dict):
        for key in sorted(value):
            yield str(key)
            yield from _strings(value[key])
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _strings(item)
        return
    yield str(value)


def _dedupe(values: Iterable[str]) -> list[str]:
    return sorted({str(value).strip() for value in values if str(value).strip()})


def extract_reusable_capability(mission_receipt: dict[str, Any]) -> dict[str, Any]:
    """Extract only an explicitly declared reusable contract from verified work.

    The function deliberately does not infer a reusable capability from arbitrary
    mission prose.  Mission-specific state stays in the mission receipt; only the
    explicit reusable_capability contract crosses into the capability registry.
    """
    verification = str(mission_receipt.get("verification_status") or "").casefold()
    if verification not in _VERIFIED_MISSION_STATES:
        raise ValueError("reusable capability extraction requires a verified mission")

    mission_id = str(mission_receipt.get("mission_id") or "").strip()
    if not mission_id:
        raise ValueError("verified mission receipt must include mission_id")

    candidate = mission_receipt.get("reusable_capability")
    if not isinstance(candidate, dict):
        raise ValueError("verified mission receipt must include reusable_capability")

    capability_id = str(candidate.get("id") or "").strip()
    description = str(candidate.get("description") or "").strip()
    if not capability_id or not description:
        raise ValueError("reusable capability requires id and description")

    evidence_refs = _dedupe(
        [
            *(candidate.get("evidence_refs") or []),
            *(mission_receipt.get("receipt_refs") or []),
        ]
    )

    return {
        "id": capability_id,
        "description": description,
        "tags": _dedupe(candidate.get("tags") or []),
        "input_contract": dict(candidate.get("input_contract") or {}),
        "output_contract": dict(candidate.get("output_contract") or {}),
        "stage": "verified",
        "source_mission_id": mission_id,
        "source_revision": mission_receipt.get("source_revision"),
        "evidence_refs": evidence_refs,
    }


def score_capability_for_mission(
    capability: dict[str, Any],
    mission: dict[str, Any],
) -> dict[str, Any]:
    """Return deterministic mission-fit + maturity + evidence scoring."""
    mission_text = " ".join(
        _strings(
            {
                "objective": mission.get("objective"),
                "requirements": mission.get("requirements"),
                "constraints": mission.get("constraints"),
            }
        )
    )
    capability_text = " ".join(
        _strings(
            {
                "id": capability.get("id"),
                "description": capability.get("description"),
                "tags": capability.get("tags"),
                "input_contract": capability.get("input_contract"),
                "output_contract": capability.get("output_contract"),
            }
        )
    )

    mission_tokens = _tokens(mission_text)
    capability_tokens = _tokens(capability_text)
    matched = sorted(mission_tokens & capability_tokens)
    fit = len(matched) / max(1, len(mission_tokens))
    stage = str(capability.get("stage") or "unknown").casefold()
    maturity = _STAGE_WEIGHT.get(stage, 0.0)
    evidence = 1.0 if capability.get("evidence_refs") else 0.0
    score = round(min(1.0, 0.65 * fit + 0.20 * maturity + 0.15 * evidence), 4)

    return {
        "capability": capability,
        "score": score,
        "fit": round(fit, 4),
        "maturity": maturity,
        "evidence": evidence,
        "matched_terms": matched,
        "truth_note": (
            "Reuse score is a deterministic composition recommendation. "
            "Mission execution and provider readback remain separately verified."
        ),
    }


def select_reusable_capability(
    mission: dict[str, Any],
    capabilities: Iterable[dict[str, Any]],
    *,
    minimum_score: float = 0.35,
) -> dict[str, Any]:
    """Rank learned capabilities and automatically select the best eligible one."""
    ranked = [score_capability_for_mission(capability, mission) for capability in capabilities]
    ranked.sort(
        key=lambda row: (
            -float(row["score"]),
            str((row.get("capability") or {}).get("id") or ""),
        )
    )
    selected = ranked[0] if ranked and ranked[0]["score"] >= minimum_score else None
    return {
        "mission_id": mission.get("mission_id"),
        "minimum_score": minimum_score,
        "selected": selected,
        "ranked": ranked,
    }


def register_capability(path: Path, capability: dict[str, Any]) -> dict[str, Any]:
    """Idempotently persist a learned capability in a deterministic JSON registry."""
    path = Path(path)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": 1, "capabilities": []}
    if not isinstance(data, dict) or not isinstance(data.get("capabilities"), list):
        raise ValueError("capability registry must be an object with capabilities[]")

    by_id = {
        str(item.get("id")): dict(item)
        for item in data["capabilities"]
        if isinstance(item, dict) and item.get("id")
    }
    capability_id = str(capability.get("id") or "").strip()
    if not capability_id:
        raise ValueError("capability requires id")
    by_id[capability_id] = dict(capability)

    rendered_obj = {
        "schema_version": int(data.get("schema_version") or 1),
        "capabilities": [by_id[key] for key in sorted(by_id)],
    }
    rendered = json.dumps(rendered_obj, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    return {
        "path": str(path),
        "capability_id": capability_id,
        "capability_count": len(rendered_obj["capabilities"]),
        "sha256": digest,
    }
