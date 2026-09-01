"""Tests for Genius family composition discovery."""
from pathlib import Path

import yaml

from genius.family import analyze_family, discover_family, family_report


def _write_repo(
    root: Path,
    name: str,
    purpose: str,
    *,
    provides=None,
    consumes=None,
):
    repo = root / name
    (repo / "interfaces").mkdir(parents=True)
    (repo / "GENIUS.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 2,
                "repository": name,
                "purpose": purpose,
                "family": "Genius",
                "composition_contract": "interfaces/COMPOSITION.yaml",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (repo / "interfaces" / "COMPOSITION.yaml").write_text(
        yaml.safe_dump(
            {
                "spec_version": 1,
                "repository": name,
                "provides": provides or [],
                "consumes": consumes or [],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return repo


def _family(tmp_path):
    _write_repo(
        tmp_path,
        "Genius-Mastery",
        "Mastery",
        provides=[
            {
                "id": "mastery.kernel.schemas",
                "description": "Shared schema contracts",
                "stage": "implemented",
                "interface": "schemas/",
                "evidence_refs": ["ev-schema"],
            }
        ],
    )
    _write_repo(
        tmp_path,
        "Genius-Code",
        "Code",
        provides=[
            {
                "id": "code.testing.property",
                "description": "Property based testing harness",
                "stage": "mapped",
                "interface": "challenges/",
                "evidence_refs": [],
            }
        ],
        consumes=[
            {
                "repository": "Genius-Mastery",
                "capability": "mastery.kernel.schemas",
                "minimum_spec_version": 1,
                "reason": "shared contracts",
            }
        ],
    )
    _write_repo(
        tmp_path,
        "Genius-Verification",
        "Verification",
        provides=[
            {
                "id": "verification.property.method",
                "description": "Property testing verification method",
                "stage": "mapped",
                "interface": "challenges/",
                "evidence_refs": [],
            }
        ],
        consumes=[
            {
                "repository": "Genius-Mastery",
                "capability": "mastery.kernel.schemas",
                "minimum_spec_version": 1,
                "reason": "shared contracts",
            },
            {
                "repository": "Genius-Missing",
                "capability": "missing.capability",
                "reason": "prove unresolved reporting",
            },
        ],
    )


def test_discover_family_loads_real_contract_shape(tmp_path):
    _family(tmp_path)
    repos = discover_family(tmp_path)

    assert [repo["repository"] for repo in repos] == [
        "Genius-Code",
        "Genius-Mastery",
        "Genius-Verification",
    ]
    assert all(repo["contract_state"] == "loaded" for repo in repos)


def test_family_analysis_resolves_declared_bindings(tmp_path):
    _family(tmp_path)
    analysis = analyze_family(tmp_path)

    assert analysis["repository_count"] == 3
    assert analysis["capability_count"] == 3
    assert len(analysis["resolved_bindings"]) == 2
    assert analysis["provider_fanout"]["Genius-Mastery"] == [
        "Genius-Code",
        "Genius-Verification",
    ]


def test_family_analysis_surfaces_unresolved_dependency(tmp_path):
    _family(tmp_path)
    analysis = analyze_family(tmp_path)

    assert analysis["unresolved_bindings"] == [
        {
            "consumer": "Genius-Verification",
            "provider": "Genius-Missing",
            "capability": "missing.capability",
            "reason": "prove unresolved reporting",
            "minimum_spec_version": None,
            "resolved": False,
        }
    ]


def test_family_analysis_discovers_property_testing_synergy(tmp_path):
    _family(tmp_path)
    analysis = analyze_family(tmp_path)

    candidate = next(
        item
        for item in analysis["composition_candidates"]
        if item["repositories"] == ["Genius-Code", "Genius-Verification"]
    )
    assert "property" in candidate["shared_terms"]
    assert candidate["score"] > 0
    assert "hypotheses" in analysis["truth_note"]


def test_family_report_is_human_readable(tmp_path):
    _family(tmp_path)
    report = family_report(analyze_family(tmp_path))

    assert "Genius family composition intelligence" in report
    assert "Genius-Code + Genius-Verification" in report
    assert "Unresolved declared dependencies" in report
