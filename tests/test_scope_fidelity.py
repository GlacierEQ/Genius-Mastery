"""Scope-fidelity regression guard.

Operational policy may optimize relevance and leverage, but it must not encode a
default reduction of mission scope to the smallest/minimum convenient slice.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POLICY_SURFACES = [
    "persona/PERSONA.md",
    "docs/INSTRUCTION_ENGINEERING.md",
    "src/genius/instruction_engineering.py",
    "src/genius/prompt_codes.py",
    "src/genius/synthesize.py",
    "tests/test_operating_loop.py",
    "synthesis/PLAN.yaml",
    "capabilities/STACK.yaml",
    "capabilities/GRAPH.yaml",
]

BANNED_SCOPE_REDUCTION_PHRASES = [
    "smallest meaningful change",
    "smallest high-signal",
    "smallest owning layer",
    "smallest-layer repair",
    "smallest high-leverage dependency",
    "smallest set of actions",
    "smallest mission-relevant dependency",
]


def test_operational_policy_contains_no_default_scope_reduction_phrases():
    findings = []
    for relative in POLICY_SURFACES:
        text = (ROOT / relative).read_text(encoding="utf-8").casefold()
        for phrase in BANNED_SCOPE_REDUCTION_PHRASES:
            if phrase in text:
                findings.append(f"{relative}: {phrase}")
    assert findings == [], "scope-reduction policy contamination:\n" + "\n".join(findings)


def test_prompt_codes_explicitly_preserve_maximum_coherent_progress():
    text = (ROOT / "src/genius/prompt_codes.py").read_text(encoding="utf-8")
    assert "MAXIMUM ADVANCE" in text
    assert "LONG-RUN" in text
    assert "MISSION-DELTA" in text
    assert "do not stop after diagnosis" in text


def test_persona_diagnoses_by_leverage_not_by_minimum_scope():
    text = (ROOT / "persona/PERSONA.md").read_text(encoding="utf-8").casefold()
    assert "highest-leverage mission-relevant" in text
    assert "smallest mission-relevant" not in text
