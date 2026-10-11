"""Verified mission -> reusable capability -> future mission reuse.

This module preserves mission evidence and reusable capability contracts while
keeping recommendation separate from execution truth. Selection must demonstrate
positive mission fit and must not violate explicit negative constraints.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Iterable

try:
    import fcntl
except ImportError:  # pragma: no cover - non-POSIX fallback is fail-closed below
    fcntl = None

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
_NEGATION = re.compile(
    r"\b(?:must\s+not|do\s+not|don't|without|avoid|forbid(?:den)?|exclude|never|no)\b",
    re.IGNORECASE,
)
_NEGATION_NOISE = {
    "must", "not", "without", "avoid", "forbid", "forbidden",
    "exclude", "never", "use", "using",
}


def _strings(value: Any) -> Iterable[str]:
    """Yield leaf values only; structural dictionary keys are not semantic input."""
    if value is None:
        return
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, dict):
        for key in sorted(value):
            yield from _strings(value[key])
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _strings(item)
        return
    yield str(value)


def _string_list(value: Any, field: str) -> list[str]:
    """Normalize a string or iterable of strings without character-splitting."""
    if value is None:
        return []
    values = [value] if isinstance(value, str) else value
    if not isinstance(values, (list, tuple, set)):
        raise ValueError(f"{field} must be a string or list of strings")
    normalized: list[str] = []
    for item in values:
        if not isinstance(item, str):
            raise ValueError(f"{field} entries must be strings")
        cleaned = item.strip()
        if cleaned:
            normalized.append(cleaned)
    return normalized


def _dedupe(values: Iterable[str]) -> list[str]:
    return sorted({str(value).strip() for value in values if str(value).strip()})


def _positive_and_prohibited_mission_tokens(
    mission: dict[str, Any],
) -> tuple[set[str], set[str]]:
    positive_parts: list[str] = []
    prohibited: set[str] = set()

    positive_parts.extend(_strings(mission.get("objective")))
    positive_parts.extend(_strings(mission.get("requirements")))

    constraints = _string_list(mission.get("constraints"), "constraints")
    for constraint in constraints:
        if _NEGATION.search(constraint):
            prohibited.update(_tokens(constraint) - _NEGATION_NOISE)
        else:
            positive_parts.append(constraint)

    return _tokens(" ".join(positive_parts)), prohibited


def _normalized_capability(capability: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(capability, dict):
        raise ValueError("capability must be a mapping")
    capability_id = str(capability.get("id") or "").strip()
    if not capability_id:
        raise ValueError("capability requires id")

    normalized = dict(capability)
    normalized["id"] = capability_id
    for field in ("tags", "evidence_refs"):
        if field in normalized:
            normalized[field] = _dedupe(_string_list(normalized.get(field), field))
    for field in ("input_contract", "output_contract"):
        raw = normalized.get(field)
        if raw is None:
            normalized[field] = {}
        elif not isinstance(raw, dict):
            raise ValueError(f"{field} must be a mapping")
        else:
            normalized[field] = dict(raw)
    return normalized


def extract_reusable_capability(mission_receipt: dict[str, Any]) -> dict[str, Any]:
    """Extract an explicitly declared reusable contract from verified work."""
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
            *_string_list(candidate.get("evidence_refs"), "evidence_refs"),
            *_string_list(mission_receipt.get("receipt_refs"), "receipt_refs"),
        ]
    )

    return {
        "id": capability_id,
        "description": description,
        "tags": _dedupe(_string_list(candidate.get("tags"), "tags")),
        "input_contract": dict(candidate.get("input_contract") or {}),
        "output_contract": dict(candidate.get("output_contract") or {}),
        "stage": verification,
        "source_mission_id": mission_id,
        "source_revision": mission_receipt.get("source_revision"),
        "evidence_refs": evidence_refs,
    }


def score_capability_for_mission(
    capability: dict[str, Any],
    mission: dict[str, Any],
) -> dict[str, Any]:
    """Return deterministic mission-fit + maturity + evidence scoring."""
    capability = _normalized_capability(capability)
    mission_tokens, prohibited_terms = _positive_and_prohibited_mission_tokens(mission)

    capability_text = " ".join(
        _strings(
            [
                capability.get("id"),
                capability.get("description"),
                capability.get("tags"),
                capability.get("input_contract"),
                capability.get("output_contract"),
            ]
        )
    )
    capability_tokens = _tokens(capability_text)
    matched = sorted(mission_tokens & capability_tokens)
    prohibited_matches = sorted(prohibited_terms & capability_tokens)
    blocked = bool(prohibited_matches)

    fit = len(matched) / max(1, len(mission_tokens)) if mission_tokens else 0.0
    stage = str(capability.get("stage") or "unknown").casefold()
    maturity = _STAGE_WEIGHT.get(stage, 0.0)
    evidence = 1.0 if capability.get("evidence_refs") else 0.0
    raw_score = 0.65 * fit + 0.20 * maturity + 0.15 * evidence
    score = 0.0 if blocked else round(min(1.0, raw_score), 4)

    return {
        "capability": capability,
        "score": score,
        "fit": round(fit, 4),
        "maturity": maturity,
        "evidence": evidence,
        "matched_terms": matched,
        "prohibited_terms": sorted(prohibited_terms),
        "prohibited_matches": prohibited_matches,
        "blocked_by_constraints": blocked,
        "eligible": bool(matched) and not blocked,
        "truth_note": (
            "Reuse score is a deterministic composition recommendation. "
            "Positive mission overlap is required; explicit negative constraints "
            "block incompatible capabilities. Mission execution and provider "
            "readback remain separately verified."
        ),
    }


def select_reusable_capability(
    mission: dict[str, Any],
    capabilities: Iterable[dict[str, Any]],
    *,
    minimum_score: float = 0.35,
) -> dict[str, Any]:
    """Rank learned capabilities and select only a positively matched eligible one."""
    if not 0.0 <= float(minimum_score) <= 1.0:
        raise ValueError("minimum_score must be between 0 and 1")

    ranked = [score_capability_for_mission(capability, mission) for capability in capabilities]
    ranked.sort(
        key=lambda row: (
            not bool(row["eligible"]),
            -float(row["score"]),
            str((row.get("capability") or {}).get("id") or ""),
        )
    )

    selected = None
    for row in ranked:
        if row["eligible"] and row["score"] >= minimum_score:
            selected = row
            break

    return {
        "mission_id": mission.get("mission_id"),
        "minimum_score": minimum_score,
        "selected": selected,
        "ranked": ranked,
    }


@contextmanager
def _registry_lock(path: Path):
    """Serialize registry read-modify-write so concurrent writers cannot lose data."""
    if fcntl is None:
        raise RuntimeError("capability registry locking requires POSIX fcntl support")
    lock_path = path.with_name(path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _load_registry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "capabilities": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("capabilities"), list):
        raise ValueError("capability registry must be an object with capabilities[]")

    validated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(data["capabilities"]):
        if not isinstance(item, dict) or not str(item.get("id") or "").strip():
            raise ValueError(f"registry entry {index} must be a capability mapping with id")
        normalized = _normalized_capability(item)
        capability_id = normalized["id"]
        if capability_id in seen:
            raise ValueError(f"registry entry duplicate id: {capability_id}")
        seen.add(capability_id)
        validated.append(normalized)
    return {
        "schema_version": int(data.get("schema_version") or 1),
        "capabilities": validated,
    }


def _atomic_write(path: Path, rendered: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
    finally:
        if temp_name:
            Path(temp_name).unlink(missing_ok=True)


def register_capability(path: Path, capability: dict[str, Any]) -> dict[str, Any]:
    """Idempotently persist one capability without losing prior registry evidence."""
    path = Path(path)
    normalized = _normalized_capability(capability)
    capability_id = normalized["id"]

    with _registry_lock(path):
        data = _load_registry(path)
        by_id = {item["id"]: item for item in data["capabilities"]}

        existing = by_id.get(capability_id)
        if existing is not None and existing != normalized:
            raise ValueError(
                f"conflicting capability already registered for id {capability_id}"
            )
        by_id[capability_id] = normalized

        rendered_obj = {
            "schema_version": int(data.get("schema_version") or 1),
            "capabilities": [by_id[key] for key in sorted(by_id)],
        }
        rendered = json.dumps(rendered_obj, indent=2, sort_keys=True) + "\n"
        digest = hashlib.sha256(rendered.encode("utf-8")).hexdigest()

        if not path.exists() or path.read_text(encoding="utf-8") != rendered:
            _atomic_write(path, rendered)

    return {
        "path": str(path),
        "capability_id": capability_id,
        "capability_count": len(rendered_obj["capabilities"]),
        "sha256": digest,
    }
