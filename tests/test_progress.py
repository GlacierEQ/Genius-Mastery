"""Tests for composable prompt codes and progress orchestration."""
from pathlib import Path
import subprocess
import sys

import yaml

from genius.progress import build_progress_contract, progress_report, validate_progress_contract
from genius.prompt_codes import DEFAULT_PROGRESS_CODES, canonical_code, normalize_codes, parse_coded_prompt


def _write_graph(root: Path) -> None:
    graph_path = root / "capabilities" / "GRAPH.yaml"
    graph_path.parent.mkdir(parents=True)
    graph = {
        "repository": "Genius-Fixture",
        "nodes": [
            {"id": "mission:ship", "kind": "mission", "label": "Ship reliable capability", "state": "active", "mission_impact": 1.0},
            {"id": "cap:critical", "kind": "capability", "label": "Critical missing capability", "state": "mapped", "mission_impact": 1.0},
            {"id": "cap:verified", "kind": "capability", "label": "Verified support capability", "state": "verified", "mission_impact": 0.7, "evidence_refs": ["ev-1", "ev-2"]},
        ],
        "edges": [
            {"from": "mission:ship", "to": "cap:critical", "relation": "requires", "required_for_current_mission": True},
            {"from": "mission:ship", "to": "cap:verified", "relation": "requires", "required_for_current_mission": True, "evidence_refs": ["ev-3"]},
        ],
    }
    graph_path.write_text(yaml.safe_dump(graph, sort_keys=False), encoding="utf-8")


def test_chain_of_thought_alias_maps_to_reasoning_summary():
    assert canonical_code("CHAIN OF THOUGHT") == "REASONING SUMMARY"


def test_parse_stacked_plus_codes():
    codes, body = parse_coded_prompt("FIRST PRINCIPLES + RED TEAM + EVAL-SELF: Analyze this architecture.")
    assert codes == ["FIRST PRINCIPLES", "RED TEAM", "EVAL-SELF"]
    assert body == "Analyze this architecture."


def test_parse_compact_slash_codes():
    codes, body = parse_coded_prompt("TOOL-FIRST / CONTINUE / BUILD / TEST / READBACK: Fix it.")
    assert codes == ["TOOL-FIRST", "CONTINUE", "BUILD", "TEST", "READBACK"]
    assert body == "Fix it."


def test_slash_inside_canonical_code_is_not_split():
    codes, body = parse_coded_prompt("FACT / INFERENCE / HYPOTHESIS: Audit the evidence.")
    assert codes == ["FACT / INFERENCE / HYPOTHESIS"]
    assert body == "Audit the evidence."


def test_progress_defaults_are_composed_and_deduplicated():
    codes = normalize_codes(["RED TEAM", "PROGRESS"], progress_defaults=True)
    assert codes[: len(DEFAULT_PROGRESS_CODES)] == list(DEFAULT_PROGRESS_CODES)
    assert codes.count("PROGRESS") == 1
    assert codes[-1] == "RED TEAM"


def test_progress_contract_selects_ranked_next_action(tmp_path):
    _write_graph(tmp_path)
    contract = build_progress_contract(tmp_path, "Make measurable progress", context=["A working repository exists"], codes=["RED TEAM", "EVAL-SELF"])
    assert validate_progress_contract(contract) == []
    assert contract["status"] == "ready_to_execute"
    assert contract["next_best_action"]["target"] == "cap:critical"
    assert contract["decision_loop"]["status"] == "ready_to_act"
    assert contract["decision_loop"]["evidence_state"] == "searched_found"
    assert "RED TEAM" in contract["codes"]
    assert "EVAL-SELF" in contract["codes"]


def test_progress_contract_falls_back_to_recovery_without_graph(tmp_path):
    contract = build_progress_contract(tmp_path, "Recover before acting")
    assert validate_progress_contract(contract) == []
    assert contract["next_best_action"]["target"] == "recover-current-state"
    assert contract["decision_loop"]["evidence_state"] == "searched_not_found"


def test_progress_report_keeps_truth_boundary_visible(tmp_path):
    _write_graph(tmp_path)
    report = progress_report(build_progress_contract(tmp_path, "Advance safely"))
    assert "Next best action:" in report
    assert "RECOVER:" in report
    assert "VERIFY:" in report
    assert "plan != execution" in report
    assert "verification requires receipts" in report


def test_cli_codes_exposes_progress():
    result = subprocess.run([sys.executable, "-m", "genius.cli", "codes", "--category", "orchestration"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PROGRESS" in result.stdout


def test_cli_progress_emits_machine_readable_contract(tmp_path):
    _write_graph(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "genius.cli", "progress", str(tmp_path), "--mission", "Advance the strongest verified slice", "--code", "RED TEAM", "--json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert '"kind": "genius-progress-contract"' in result.stdout
    assert '"target": "cap:critical"' in result.stdout
