"""Completion-core regression tests."""
import json
import yaml

from genius.challenge import run_challenge
from genius.discovery import discover_mcp_servers, write_discovery_inventory
from genius.graph import build_synthesis_graph
from genius.migration import migrate_genius_repo
from genius.sources import load_mega_skills_registry


def test_challenge_harness_supports_transparent_verifiers():
    assert run_challenge(
        {"id": "a", "verification": "contains_all", "expected_outputs": ["alpha", "beta"], "min_length": 1},
        "alpha and beta",
    )["passed"]
    assert run_challenge(
        {"id": "b", "verification": "regex", "pattern": r"receipt-[0-9]+", "min_length": 1},
        "receipt-42",
    )["passed"]
    assert run_challenge(
        {"id": "c", "verification": "json_keys", "required_keys": ["status", "receipt"], "min_length": 1},
        json.dumps({"status": "ok", "receipt": "r1"}),
    )["passed"]


def test_migration_preserves_custom_content_and_ids(tmp_path):
    root = tmp_path / "Genius-Old"
    root.mkdir()
    (root / "GENIUS.yaml").write_text(
        "schema_version: 1\nrepository: Genius-Old\npurpose: Old\nfamily: Genius\ndoctrine: mastery-not-skills\ncustom_key: keep-me\n",
        encoding="utf-8",
    )
    (root / "claims").mkdir()
    (root / "claims" / "CLAIMS.yaml").write_text(
        "schema_version: 1\nclaims:\n  - id: custom-claim\n    statement: This custom claim must survive migration.\n",
        encoding="utf-8",
    )
    receipt = migrate_genius_repo(root)
    migrated = yaml.safe_load((root / "GENIUS.yaml").read_text(encoding="utf-8"))
    assert migrated["schema_version"] == 2
    assert migrated["custom_key"] == "keep-me"
    assert "custom-claim" in receipt["preserved_ids"]
    assert (root / "interfaces" / "COMPOSITION.yaml").exists()
    second = migrate_genius_repo(root)
    assert second["from_version"] == 2
    assert second["to_version"] == 2


def test_discovery_does_not_emit_secret_values(tmp_path):
    secret = "do-not-leak-this-secret"
    (tmp_path / "mcp.json").write_text(
        json.dumps({"mcpServers": {"alpha": {"env": {"TOKEN": secret}}}}),
        encoding="utf-8",
    )
    rows = discover_mcp_servers(tmp_path)
    assert [row["name"] for row in rows] == ["alpha"]
    assert secret not in json.dumps(rows)
    target = write_discovery_inventory(tmp_path)
    assert target.exists()
    assert secret not in target.read_text(encoding="utf-8")


def test_mega_skills_dependencies_become_graph_edges(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    (registry / "skills.json").write_text(
        json.dumps({"entries": [
            {"id": "skill-a", "display_name": "Research Alpha", "dependencies": ["skill-b"]},
            {"id": "skill-b", "display_name": "Research Beta"}
        ]}),
        encoding="utf-8",
    )
    (registry / "combo-skills.json").write_text('{"entries":[]}', encoding="utf-8")
    (registry / "mega-skills.json").write_text('{"entries":[]}', encoding="utf-8")

    loaded = load_mega_skills_registry(tmp_path)
    a = next(row for row in loaded if row["id"] == "skill-a")
    assert a["dependencies"] == ["skill-b"]

    graph = build_synthesis_graph(
        "Genius-Research",
        "Research",
        ["Research Alpha"],
        {},
        [{key: value for key, value in a.items() if key != "_raw"}],
    )
    assert any(edge["relation"] == "requires" for edge in graph["edges"])
    assert any(node["kind"] == "capability-reference" for node in graph["nodes"])
