"""Tests for mission-sensitive capability intelligence."""
from genius.intelligence import analyze_capability_graph, capability_intelligence_report


def _graph():
    return {
        "schema_version": 1,
        "repository": "Genius-Engineering",
        "nodes": [
            {
                "id": "role:engineer",
                "kind": "role",
                "label": "Engineer",
                "state": "mapped",
                "mission_impact": 1.0,
            },
            {
                "id": "family:reliability",
                "kind": "capability-family",
                "label": "Reliability",
                "state": "mapped",
                "mission_impact": 0.9,
            },
            {
                "id": "target:incident-recovery",
                "kind": "capability-target",
                "label": "Incident recovery",
                "state": "research-and-verify",
                "mission_impact": 0.9,
            },
            {
                "id": "target:logging",
                "kind": "capability-target",
                "label": "Logging",
                "state": "verified",
                "mission_impact": 0.7,
                "evidence_refs": ["ev-log-1", "ev-log-2"],
            },
            {
                "id": "target:optional-style",
                "kind": "capability-target",
                "label": "Optional style",
                "state": "mapped",
                "mission_impact": 0.2,
            },
        ],
        "edges": [
            {
                "from": "role:engineer",
                "to": "family:reliability",
                "relation": "requires-capability-family",
                "required_for_current_mission": True,
                "evidence_refs": [],
            },
            {
                "from": "family:reliability",
                "to": "target:incident-recovery",
                "relation": "develops",
                "required_for_current_mission": True,
                "evidence_refs": [],
            },
            {
                "from": "family:reliability",
                "to": "target:logging",
                "relation": "develops",
                "required_for_current_mission": True,
                "evidence_refs": ["ev-log-edge"],
            },
            {
                "from": "role:engineer",
                "to": "target:optional-style",
                "relation": "develops",
                "required_for_current_mission": False,
                "evidence_refs": [],
            },
        ],
    }


def test_analysis_ranks_unverified_required_capability_as_bottleneck():
    analyzed = analyze_capability_graph(_graph())
    analysis = analyzed["analysis"]

    assert analysis["engine"] == "mission-intelligence-v1"
    assert "target:incident-recovery" in analysis["candidate_bottlenecks"]
    assert "target:logging" not in analysis["candidate_bottlenecks"]
    assert analysis["top_next_actions"][0]["id"] == "target:incident-recovery"


def test_analysis_does_not_promote_truth_state():
    graph = _graph()
    analyzed = analyze_capability_graph(graph)

    original = {node["id"]: node["state"] for node in graph["nodes"]}
    enriched = {node["id"]: node["state"] for node in analyzed["nodes"]}
    assert enriched == original
    assert "do not promote" in analyzed["analysis"]["truth_note"]


def test_verified_evidence_backed_target_has_higher_readiness():
    analyzed = analyze_capability_graph(_graph())
    rows = {row["id"]: row for row in analyzed["analysis"]["ranked_priorities"]}

    assert rows["target:logging"]["readiness"] > rows["target:incident-recovery"]["readiness"]
    assert rows["target:logging"]["evidence_strength"] > rows["target:incident-recovery"]["evidence_strength"]


def test_required_dependency_path_creates_dependent_centrality():
    analyzed = analyze_capability_graph(_graph())
    rows = {row["id"]: row for row in analyzed["analysis"]["ranked_priorities"]}

    assert rows["target:incident-recovery"]["dependent_count"] >= 2
    assert rows["family:reliability"]["dependent_count"] >= 1


def test_report_is_explainable():
    report = capability_intelligence_report(_graph(), top=3)
    assert "mission-intelligence-v1" in report
    assert "target:incident-recovery" in report
    assert "required by current mission path" in report
