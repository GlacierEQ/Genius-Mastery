# src/genius/challenge.py
"""Executable challenge harness for testing capability."""
from __future__ import annotations
from typing import TypedDict, Any

class Challenge(TypedDict):
    id: str
    question: str
    expected_outputs: list[str]
    hint: str
    verification: str
    related_claim: str

class ChallengeResult(TypedDict):
    challenge_id: str
    passed: bool
    actual_output: str
    notes: str

def generate_challenges(role_name: str, outcomes: list[str], families: dict[str, Any]) -> list[Challenge]:
    challenges: list[Challenge] = []
    
    # Generate 3 challenges per capability family
    for i in range(3):
        challenges.append({
            "id": f"{role_name.lower().replace(' ', '_')}-chal-{i+1}",
            "question": f"Demonstrate outcome for {role_name}: {outcomes[0] if outcomes else 'basic'}",
            "expected_outputs": ["success", "completed"],
            "hint": "Try using the core skill.",
            "verification": "keyword_match",
            "related_claim": "claim-1"
        })
        
    return challenges

def run_challenge(challenge: Challenge, candidate_output: str) -> ChallengeResult:
    passed = False
    
    if len(candidate_output) > 5:
        if any(expected in candidate_output.lower() for expected in challenge["expected_outputs"]):
            passed = True
            
    return {
        "challenge_id": challenge["id"],
        "passed": passed,
        "actual_output": candidate_output,
        "notes": "Passed keyword check" if passed else "Missing keywords or too short"
    }

def run_challenge_suite(challenges: list[Challenge], outputs: dict[str, str]) -> list[ChallengeResult]:
    results = []
    for c in challenges:
        output = outputs.get(c["id"], "")
        results.append(run_challenge(c, output))
    return results

def challenge_report(results: list[ChallengeResult]) -> str:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pct = (passed / total * 100) if total > 0 else 0.0
    
    report = [f"Challenge Report: {passed}/{total} passed ({pct:.1f}%)", "-" * 40]
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        report.append(f"[{status}] {r['challenge_id']}: {r['notes']}")
        
    return "\n".join(report)
