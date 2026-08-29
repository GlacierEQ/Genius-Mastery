"""Contract tests for Genius-Mastery."""
from pathlib import Path
import json
import subprocess
import sys

from genius.scaffold import create_domain
from genius.synthesize import infer_families, synthesize_role

ROOT = Path(__file__).resolve().parents[1]


def test_genius_yaml_exists():
    assert (ROOT / "GENIUS.yaml").exists()


def test_capability_kernel_surfaces_exist():
    assert (ROOT / "schemas" / "capability.schema.json").exists()
    assert (ROOT / "schemas" / "role-brief.schema.json").exists()
    assert (ROOT / "templates" / "CAPABILITY.yaml").exists()
    assert (ROOT / "docs" / "GENIUS_ENTITY_ANATOMY.md").exists()
    assert (ROOT / "docs" / "MASTER_TEACHER_FORGE.md").exists()
    assert (ROOT / "capabilities" / "STACK.yaml").exists()


def test_capability_schema_is_valid_json():
    path = ROOT / "schemas" / "capability.schema.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["$schema"].endswith("2020-12/schema")
    assert data["properties"]["layers"]["type"] == "object"


def test_new_domain_inherits_vertical_capability_stack(tmp_path):
    root = create_domain("Smoke Anatomy", tmp_path)
    stack = root / "capabilities" / "STACK.yaml"
    assert stack.exists()
    text = stack.read_text(encoding="utf-8")
    assert "vertical-excellence" in text
    assert "capability_composition:" in text
    assert "mission_impact:" in text
    assert "alternate_routes:" in text


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

    stack = (root / "capabilities" / "STACK.yaml").read_text(encoding="utf-8")
    assert "field observation" in stack
    assert "source discovery" in stack
    assert "teach verified methods" in stack

    plan = (root / "synthesis" / "PLAN.yaml").read_text(encoding="utf-8")
    assert "GlacierEQ/mega-skills" in plan
    assert "teach-another" in plan


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
    assert (tmp_path / "Genius-Researcher" / "ROLE.yaml").exists()


def test_validator_passes():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
