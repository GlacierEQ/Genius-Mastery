"""Contract tests for Genius-Mastery."""
from pathlib import Path
import json
import subprocess
import sys

import yaml

from genius.anatomy import ANATOMY_PROMPTS
from genius.scaffold import create_domain
from genius.synthesize import infer_families, synthesize_role
from genius.sources import match_mega_skills
from genius.validate import validate_repo

ROOT = Path(__file__).resolve().parents[1]


def test_genius_yaml_exists():
    assert (ROOT / "GENIUS.yaml").exists()


def test_capability_kernel_surfaces_exist():
    assert (ROOT / "schemas" / "capability.schema.json").exists()
    assert (ROOT / "schemas" / "role-brief.schema.json").exists()
    assert (ROOT / "schemas" / "teaching.schema.json").exists()
    assert (ROOT / "templates" / "CAPABILITY.yaml").exists()
    assert (ROOT / "templates" / "TEACHING.yaml").exists()
    assert (ROOT / "docs" / "GENIUS_ENTITY_ANATOMY.md").exists()
    assert (ROOT / "docs" / "MASTER_TEACHER_FORGE.md").exists()
    assert (ROOT / "capabilities" / "STACK.yaml").exists()
    assert (ROOT / "teaching" / "TEACHING.yaml").exists()


def test_capability_schema_is_valid_json():
    path = ROOT / "schemas" / "capability.schema.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["$schema"].endswith("2020-12/schema")
    assert data["properties"]["layers"]["type"] == "object"
    assert "teaching" in data["properties"]["layers"]["properties"]


def test_new_domain_inherits_vertical_capability_and_teaching(tmp_path):
    root = create_domain("Smoke Anatomy", tmp_path)
    stack = root / "capabilities" / "STACK.yaml"
    teaching = root / "teaching" / "TEACHING.yaml"
    assert stack.exists()
    assert teaching.exists()

    stack_text = stack.read_text(encoding="utf-8")
    assert "vertical-excellence" in stack_text
    assert "capability_composition:" in stack_text
    assert "teaching:" in stack_text
    assert "mission_impact:" in stack_text
    assert "alternate_routes:" in stack_text

    genius_text = (root / "GENIUS.yaml").read_text(encoding="utf-8")
    assert "teaching_contract: teaching/TEACHING.yaml" in genius_text
    assert "  - teach" in genius_text

    assert validate_repo(root) == []


def test_indiana_jones_researcher_infers_field_research():
    families = infer_families("Researcher", ["Indiana Jones"])
    assert "research" in families
    assert "field-research" in families
    targets = {target for spec in families.values() for target in spec["targets"]}
    assert "source discovery" in targets
    assert "field observation" in targets
    assert "geographic reasoning" in targets
    assert "evidence preservation" in targets


def test_synthesize_role_creates_teaching_entity(tmp_path):
    root = synthesize_role("Researcher", ["Indiana Jones"], tmp_path)
    assert root.name == "Genius-Researcher"
    assert (root / "ROLE.yaml").exists()
    assert (root / "persona" / "PERSONA.md").exists()
    assert (root / "synthesis" / "PLAN.yaml").exists()
    assert (root / "teaching" / "TEACHING_PLAN.md").exists()
    assert (root / "teaching" / "TEACHING.yaml").exists()

    stack = (root / "capabilities" / "STACK.yaml").read_text(encoding="utf-8")
    assert "field observation" in stack
    assert "source discovery" in stack
    assert "teach verified methods" in stack

    plan = (root / "synthesis" / "PLAN.yaml").read_text(encoding="utf-8")
    assert "GlacierEQ/mega-skills" in plan
    assert "teach-another" in plan

    teaching = (root / "teaching" / "TEACHING.yaml").read_text(encoding="utf-8")
    assert "Indiana Jones" in teaching
    assert "geographic reasoning" in teaching

    assert validate_repo(root) == []


def test_synthesized_entity_interrogates_entire_vertical_stack(tmp_path):
    root = synthesize_role("Researcher", ["Indiana Jones"], tmp_path)
    stack = yaml.safe_load(
        (root / "capabilities" / "STACK.yaml").read_text(encoding="utf-8")
    )
    assert set(ANATOMY_PROMPTS).issubset(stack["layers"])
    for layer_name, prompts in ANATOMY_PROMPTS.items():
        assert stack["layers"][layer_name]["inspection_prompts"] == prompts


def test_synthesis_can_match_real_capability_registry_shape(tmp_path):
    mega = tmp_path / "mega-skills"
    registry = mega / "registry"
    registry.mkdir(parents=True)
    (registry / "skills.json").write_text(
        json.dumps({
            "entries": [
                {
                    "id": "source-discovery",
                    "display_name": "Source Discovery",
                    "maturity": "active",
                    "entrypoint": "skills/source-discovery/SKILL.md",
                    "adds": "Research source discovery and provenance."
                }
            ]
        }),
        encoding="utf-8",
    )
    (registry / "combo-skills.json").write_text(
        json.dumps({
            "entries": [
                {
                    "id": "field-research",
                    "display_name": "Field Research",
                    "maturity": "active",
                    "entrypoint": "combo-skills/field-research/COMBO.md",
                    "adds": "Research field observation and evidence preservation."
                }
            ]
        }),
        encoding="utf-8",
    )
    (registry / "mega-skills.json").write_text(
        json.dumps({
            "entries": [
                {
                    "id": "apex-research-expedition",
                    "display_name": "APEX Research Expedition",
                    "maturity": "active",
                    "entrypoint": "mega-skills/apex-research-expedition/MEGA.md",
                    "adds": "Research expedition mission orchestration."
                }
            ]
        }),
        encoding="utf-8",
    )

    matches = match_mega_skills("Researcher", ["Indiana Jones"], mega)
    assert matches
    assert all(item["source_repository"] == "GlacierEQ/mega-skills" for item in matches)

    out = tmp_path / "out"
    out.mkdir()
    root = synthesize_role(
        "Researcher",
        ["Indiana Jones"],
        out,
        mega_skills_root=mega,
    )
    plan = yaml.safe_load(
        (root / "synthesis" / "PLAN.yaml").read_text(encoding="utf-8")
    )
    assert plan["capability_match_state"] == "local-registry-matched"
    assert plan["matched_live_capabilities"]
    assert any(
        item["id"] == "apex-research-expedition"
        for item in plan["matched_live_capabilities"]
    )


def test_generated_repo_standalone_validator_passes(tmp_path):
    root = synthesize_role("Researcher", ["Indiana Jones"], tmp_path)
    r = subprocess.run(
        [sys.executable, str(root / "tools" / "validate.py"), str(root)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_cli_synthesize_role(tmp_path):
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "genius.cli",
            "synthesize",
            "Researcher",
            "--outcome",
            "Indiana Jones",
            "--dest",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    generated = tmp_path / "Genius-Researcher"
    assert (generated / "ROLE.yaml").exists()
    assert (generated / "teaching" / "TEACHING.yaml").exists()


def test_validator_passes():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
