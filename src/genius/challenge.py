"""Executable, evidence-bounded challenge harness."""
from __future__ import annotations
import json
import re
from typing import Any, TypedDict

class Challenge(TypedDict, total=False):
    id: str
    question: str
    expected_outputs: list[str]
    hint: str
    verification: str
    related_claim: str
    pattern: str
    required_keys: list[str]
    min_length: int

class ChallengeResult(TypedDict):
    challenge_id: str
    passed: bool
    actual_output: str
    notes: str

def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_") or "challenge"

def generate_challenges(role_name: str, outcomes: list[str], families: dict[str, Any]) -> list[Challenge]:
    outcome = outcomes[0] if outcomes else "demonstrate the target outcome"
    targets: list[str] = []
    for family_name, family in sorted((families or {}).items()):
        if isinstance(family, dict):
            targets.extend(str(item) for item in (family.get("targets") or []))
        if not targets:
            targets.append(str(family_name))
    seed = targets[:3] or ["produce a concrete result", "explain verification", "identify a failure mode"]
    return [{
        "id": f"{_slug(role_name)}-chal-{i}",
        "question": f"Demonstrate {target} for {role_name} while advancing: {outcome}",
        "expected_outputs": ["success", "completed"],
        "hint": "Return a concrete result plus how it was verified.",
        "verification": "contains_any",
        "related_claim": "",
        "min_length": 6,
    } for i, target in enumerate(seed, 1)]

def _contains_any(output: str, expected: list[str]) -> bool:
    lowered = output.casefold()
    return any(item.casefold() in lowered for item in expected if item)

def _contains_all(output: str, expected: list[str]) -> bool:
    lowered = output.casefold()
    items = [item.casefold() for item in expected if item]
    return bool(items) and all(item in lowered for item in items)

def _json_keys(output: str, keys: list[str]) -> bool:
    try:
        payload = json.loads(output)
    except (TypeError, json.JSONDecodeError):
        return False
    return isinstance(payload, dict) and all(key in payload for key in keys)

def run_challenge(challenge: Challenge, candidate_output: str) -> ChallengeResult:
    output = str(candidate_output)
    verifier = str(challenge.get("verification") or "contains_any")
    expected = list(challenge.get("expected_outputs") or [])
    min_length = int(challenge.get("min_length") or 1)
    if len(output.strip()) < min_length:
        passed, notes = False, f"Output shorter than required minimum ({min_length})."
    elif verifier in {"keyword_match", "contains_any"}:
        passed = _contains_any(output, expected)
        notes = "Passed contains-any check." if passed else "Missing every expected marker."
    elif verifier == "contains_all":
        passed = _contains_all(output, expected)
        notes = "Passed contains-all check." if passed else "Missing one or more required markers."
    elif verifier == "regex":
        try:
            passed = bool(challenge.get("pattern")) and re.search(str(challenge.get("pattern")), output, flags=re.MULTILINE) is not None
        except re.error:
            passed = False
        notes = "Passed regex check." if passed else "Regex did not match."
    elif verifier == "json_keys":
        passed = _json_keys(output, list(challenge.get("required_keys") or []))
        notes = "Passed JSON-key check." if passed else "JSON output missing required keys."
    elif verifier == "nonempty":
        passed = bool(output.strip())
        notes = "Passed non-empty check." if passed else "Output is empty."
    else:
        passed, notes = False, f"Unsupported verifier: {verifier}"
    return {"challenge_id": str(challenge.get("id") or "unknown"), "passed": passed, "actual_output": output, "notes": notes}

def run_challenge_suite(challenges: list[Challenge], outputs: dict[str, str]) -> list[ChallengeResult]:
    return [run_challenge(challenge, outputs.get(str(challenge.get("id")), "")) for challenge in challenges]

def challenge_report(results: list[ChallengeResult]) -> str:
    passed = sum(1 for result in results if result["passed"])
    lines = [f"Challenge Report: {passed}/{len(results)} passed", "-" * 40]
    for result in results:
        lines.append(f"[{'PASS' if result['passed'] else 'FAIL'}] {result['challenge_id']}: {result['notes']}")
    return "\n".join(lines)
