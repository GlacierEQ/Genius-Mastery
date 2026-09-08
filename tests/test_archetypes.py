"""Comprehensive unit tests for the Genius Lineage Archetypes."""
from pathlib import Path
import json
import pytest

from genius.archetypes import (
    ARCHETYPES,
    ArchetypeDefinition,
    archetype_catalog_report,
    archetype_report,
    archetype_to_family,
    get_archetype,
    list_archetypes,
    match_archetypes,
)
from genius.synthesize import infer_families, synthesize_role
from genius.validate import validate_repo
import yaml


EXPECTED_ARCHETYPE_IDS = [
    "aerospace",
    "microcode",
    "nanosphere",
    "security",
    "energy",
    "physics",
    "chemistry",
    "biology",
    "law",
    "document-processing",
    "document-generation",
    "metadata-depth",
    "filesystem",
    "cloud-database",
    "device",
    "pc",
    "mac",
    "linux",
    "android",
    "ios",
    "email",
    "automation",
    "model-weights",
    "spiritual-awareness",
    "scifi",
    "nerd-geek",
]


def test_all_26_canonical_archetypes_registered():
    assert len(ARCHETYPES) == 26
    for aid in EXPECTED_ARCHETYPE_IDS:
        assert aid in ARCHETYPES, f"Missing archetype: {aid}"
        arch = ARCHETYPES[aid]
        assert isinstance(arch, ArchetypeDefinition)
        assert arch.id == aid
        assert arch.name.startswith("Genius-")
        assert arch.lineage == "Genius Lineage"
        assert arch.domain in {"frontier_science", "systems_platforms", "legal_enterprise", "physical_systems", "sovereign_infrastructure", "telos_culture"}
        assert len(arch.description) > 20
        assert len(arch.keywords) >= 3
        assert len(arch.layers) >= 4
        assert len(arch.targets) >= 3
        assert len(arch.invariants) >= 3
        assert len(arch.tools) >= 2
        assert len(arch.verification_gates) >= 2
        assert len(arch.teaching_transfer) > 20


def test_get_archetype_resolution_and_aliases():
    # Direct ID match
    assert get_archetype("aerospace").id == "aerospace"
    assert get_archetype("ios").id == "ios"
    assert get_archetype("cloud-database").id == "cloud-database"

    # Name match
    assert get_archetype("Genius-Aerospace").id == "aerospace"
    assert get_archetype("Genius-iOS").id == "ios"
    assert get_archetype("Genius-Microcode").id == "microcode"

    # Fuzzy/case-insensitive/space-separated match
    assert get_archetype("genius aerospace").id == "aerospace"
    assert get_archetype("genius-cloud-database").id == "cloud-database"
    assert get_archetype("cloud_database").id == "cloud-database"
    assert get_archetype("spiritual awareness").id == "spiritual-awareness"
    assert get_archetype("nerd geek").id == "nerd-geek"

    # Unknown
    assert get_archetype("nonexistent-domain-xyz") is None
    assert get_archetype("") is None


def test_list_archetypes_and_domains():
    all_archs = list_archetypes()
    assert len(all_archs) == 26

    frontier = list_archetypes("frontier_science")
    assert any(a.id == "aerospace" for a in frontier)
    assert any(a.id == "physics" for a in frontier)
    assert any(a.id == "biology" for a in frontier)
    assert any(a.id == "nanosphere" for a in frontier)

    systems = list_archetypes("systems_platforms")
    assert any(a.id == "microcode" for a in frontier) or any(a.id == "microcode" for a in systems)
    assert any(a.id == "linux" for a in systems)
    assert any(a.id == "ios" for a in systems)
    assert any(a.id == "android" for a in systems)

    telos = list_archetypes("telos_culture")
    assert any(a.id == "spiritual-awareness" for a in telos)
    assert any(a.id == "scifi" for a in telos)
    assert any(a.id == "nerd-geek" for a in telos)


def test_match_archetypes_by_explicit_name_or_tokens():
    # Explicit archetype
    matched = match_archetypes("Engineer", ["build systems"], archetype="aerospace")
    assert len(matched) >= 1
    assert matched[0].id == "aerospace"

    # Token matching in role
    matched_role = match_archetypes("Microcode Engineer", ["optimize hot path"])
    assert any(a.id == "microcode" for a in matched_role)

    # Token matching in outcomes
    matched_outcomes = match_archetypes("Specialist", ["calculate Tsiolkovsky delta-v for orbit"])
    assert any(a.id == "aerospace" for a in matched_outcomes)

    # Multiple matching archetypes
    matched_multi = match_archetypes("Systems Architect", ["deploy on linux and ios with security"])
    matched_ids = {a.id for a in matched_multi}
    assert "linux" in matched_ids
    assert "ios" in matched_ids
    assert "security" in matched_ids


def test_archetype_to_family_conversion():
    arch = get_archetype("physics")
    family = archetype_to_family(arch)
    assert family["id"] == "physics"
    assert family["name"] == "Genius-Physics"
    assert "Lagrangian and Hamiltonian formulation synthesis" in family["targets"]
    assert any("Noether's theorem" in inv for inv in family["invariants"])
    assert "symplectic_integrator" in family["tools"]
    assert any("Symplectic phase-space volume" in g for g in family["verification_gates"])


def test_infer_families_preserves_base_and_enriches():
    # Normal role without archetype keywords
    base_res = infer_families("Standard Worker", ["perform generic operations"])
    assert "reasoning" in base_res
    assert "research" in base_res

    # With aerospace archetype
    aero_res = infer_families("Rocket Engineer", ["calculate orbital trajectory"], archetype="aerospace")
    assert "aerospace" in aero_res
    assert "orbital trajectory propagation via high-order numerical integration" in aero_res["aerospace"]["targets"]
    assert "physical_substrate" in aero_res["aerospace"]["layers"]
    assert len(aero_res["aerospace"]["invariants"]) >= 3


def test_synthesize_role_with_aerospace_archetype(tmp_path):
    root = synthesize_role(
        role="Orbital Trajectory Specialist",
        outcomes=["propagate geostationary transfer orbit with high precision"],
        dest_parent=tmp_path,
        archetype="aerospace",
    )
    assert root.name == "Genius-Orbital-Trajectory-Specialist"
    assert (root / "ROLE.yaml").exists()
    assert (root / "persona" / "PERSONA.md").exists()
    assert (root / "teaching" / "TEACHING_PLAN.md").exists()
    assert (root / "teaching" / "TEACHING.yaml").exists()
    assert (root / "capabilities" / "STACK.yaml").exists()
    assert (root / "capabilities" / "GRAPH.yaml").exists()

    # ROLE.yaml contents
    role_data = yaml.safe_load((root / "ROLE.yaml").read_text(encoding="utf-8"))
    assert role_data["archetype"] == "aerospace"
    assert "aerospace" in role_data["archetypes"]
    assert any("Tsiolkovsky" in inv for inv in role_data["domain_invariants"])
    assert "orbital_propagator" in role_data["required_tools"]

    # PERSONA.md doctrine
    persona_md = (root / "persona" / "PERSONA.md").read_text(encoding="utf-8")
    assert "Genius-Aerospace Domain Doctrine" in persona_md
    assert "Vis-viva" in persona_md
    assert "delta_v_budget_calculator" in persona_md

    # TEACHING.yaml transfer challenges
    teaching_data = yaml.safe_load((root / "teaching" / "TEACHING.yaml").read_text(encoding="utf-8"))
    challenges = teaching_data["verification"]["transfer_challenges"]
    assert any("Lambert targeting" in c for c in challenges)

    # STACK.yaml acceptance gates
    stack_data = yaml.safe_load((root / "capabilities" / "STACK.yaml").read_text(encoding="utf-8"))
    acceptance = stack_data["verification"]["acceptance"]
    assert any("Delta-v budget closure" in g for g in acceptance)
    assert any("Runge-Kutta" in g for g in acceptance)

    # GRAPH.yaml nodes and family metadata
    graph_data = yaml.safe_load((root / "capabilities" / "GRAPH.yaml").read_text(encoding="utf-8"))
    family_nodes = [n for n in graph_data["nodes"] if n.get("id") == "family:aerospace"]
    assert len(family_nodes) == 1
    assert "invariants" in family_nodes[0]["metadata"]
    assert any("Tsiolkovsky" in inv for inv in family_nodes[0]["metadata"]["invariants"])

    # GENIUS.yaml archetypes
    genius_data = yaml.safe_load((root / "GENIUS.yaml").read_text(encoding="utf-8"))
    assert genius_data.get("primary_archetype") == "aerospace"
    assert "aerospace" in genius_data.get("archetypes", [])

    # Validate repo strictly passes contract
    errors = validate_repo(root)
    assert errors == []


def test_synthesize_role_with_law_archetype(tmp_path):
    root = synthesize_role(
        role="Forensic Litigation Counsel",
        outcomes=["prepare self-authenticating evidentiary record"],
        dest_parent=tmp_path,
        archetype="law",
    )
    assert (root / "ROLE.yaml").exists()
    role_data = yaml.safe_load((root / "ROLE.yaml").read_text(encoding="utf-8"))
    assert "law" in role_data["archetypes"]
    assert any("FRE 902" in inv for inv in role_data["domain_invariants"])
    assert "bates_numberer" in role_data["required_tools"]

    stack_data = yaml.safe_load((root / "capabilities" / "STACK.yaml").read_text(encoding="utf-8"))
    assert any("Bates numbering" in g for g in stack_data["verification"]["acceptance"])

    errors = validate_repo(root)
    assert errors == []


def test_synthesize_role_with_spiritual_awareness_archetype(tmp_path):
    root = synthesize_role(
        role="Ethical Systems Steward",
        outcomes=["preserve human dignity across autonomous agent decisions"],
        dest_parent=tmp_path,
        archetype="spiritual-awareness",
    )
    role_data = yaml.safe_load((root / "ROLE.yaml").read_text(encoding="utf-8"))
    assert "spiritual-awareness" in role_data["archetypes"]
    assert any("Non-Harm" in inv or "Ahimsa" in inv for inv in role_data["domain_invariants"])

    errors = validate_repo(root)
    assert errors == []


def test_synthesize_role_with_nerd_geek_archetype(tmp_path):
    root = synthesize_role(
        role="Demoscene Hacker",
        outcomes=["cycle-exact raster synchronization"],
        dest_parent=tmp_path,
        archetype="nerd-geek",
    )
    role_data = yaml.safe_load((root / "ROLE.yaml").read_text(encoding="utf-8"))
    assert "nerd-geek" in role_data["archetypes"]
    assert any("Klaus Dormann" in g for g in role_data["verification_gates"])

    errors = validate_repo(root)
    assert errors == []


def test_archetype_reports_and_catalog():
    catalog = archetype_catalog_report()
    assert "# Genius Lineage Archetype Catalog" in catalog
    assert "Total Registered Archetypes: **26**" in catalog
    assert "Genius-Aerospace" in catalog
    assert "Genius-iOS" in catalog
    assert "Genius-Microcode" in catalog

    arch = get_archetype("microcode")
    report = archetype_report(arch)
    assert "# Genius-Microcode" in report
    assert "First-Principles Invariants" in report
    assert "Pipeline hazard prevention" in report
    assert "eBPF bytecode verification" in report
