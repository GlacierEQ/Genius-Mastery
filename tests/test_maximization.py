import pytest
from pathlib import Path
from genius.impact import score_graph, rank_bottlenecks
from genius.migration import migrate_genius_repo
from genius.challenge import generate_challenges, run_challenge
from genius.discovery import discover_cli_tools, discover_mcp_servers
from genius.performance import benchmark_validate

def test_impact_scores_non_empty():
    graph = {
        "nodes": [
            {"id": "test-node", "kind": "capability-family", "state": "mapped"}
        ],
        "edges": [
            {"from": "test-node", "to": "other-node", "required_for_current_mission": True}
        ]
    }
    scores = score_graph(graph)
    assert len(scores) > 0

def test_bottlenecks_are_ranked():
    graph = {
        "nodes": [
            {"id": "node-1", "kind": "capability-family", "state": "mapped"},
            {"id": "node-2", "kind": "capability-family", "state": "mapped"}
        ],
        "edges": [
            {"from": "node-1", "to": "node-2"}
        ]
    }
    bottlenecks = rank_bottlenecks(graph, top_n=2)
    assert len(bottlenecks) == 2

def test_migration_v1_to_v2_idempotent(tmp_path):
    genius_file = tmp_path / "GENIUS.yaml"
    genius_file.write_text("schema_version: 1\nkey1: val1\n")
    
    receipt1 = migrate_genius_repo(tmp_path)
    assert receipt1["from_version"] == 1
    assert receipt1["to_version"] == 2
    
    receipt2 = migrate_genius_repo(tmp_path)
    assert receipt2["from_version"] == 2
    assert receipt2["to_version"] == 2

def test_migration_preserves_all_keys(tmp_path):
    genius_file = tmp_path / "GENIUS.yaml"
    genius_file.write_text("schema_version: 1\ncustom_key: 123\n")
    migrate_genius_repo(tmp_path)
    content = genius_file.read_text()
    assert "custom_key: 123" in content

def test_challenge_generation_non_empty():
    challenges = generate_challenges("Researcher", ["Indiana Jones"], {})
    assert len(challenges) >= 3

def test_challenge_run_pass_case():
    challenges = generate_challenges("Researcher", ["Indiana Jones"], {})
    res = run_challenge(challenges[0], "success output test completed")
    assert res["passed"] is True

def test_discovery_cli_tools():
    # Only asserting git to be safe across environments, python3 might be just python depending on the environment
    res = discover_cli_tools(["python3", "git", "go"])
    assert len(res) == 3
    # Check if git is available
    git_res = next((r for r in res if r["name"] == "git"), None)
    if git_res:
        assert git_res["available"] is True

def test_discovery_mcp_servers(tmp_path):
    res = discover_mcp_servers(tmp_path)
    # We test it returns a list. In tmp_path it might be empty
    assert isinstance(res, list)

def test_benchmark_validate_runs(tmp_path):
    res = benchmark_validate(tmp_path, n=5)
    assert res["mean_ms"] >= 0
