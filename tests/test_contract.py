"""Contract tests for Genius-Mastery."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_genius_yaml_exists():
    assert (ROOT / "GENIUS.yaml").exists()


def test_capability_kernel_surfaces_exist():
    assert (ROOT / "schemas" / "capability.schema.json").exists()
    assert (ROOT / "templates" / "CAPABILITY.yaml").exists()
    assert (ROOT / "docs" / "GENIUS_ENTITY_ANATOMY.md").exists()
    assert (ROOT / "capabilities" / "STACK.yaml").exists()


def test_capability_schema_is_valid_json():
    path = ROOT / "schemas" / "capability.schema.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["$schema"].endswith("2020-12/schema")
    assert data["properties"]["layers"]["type"] == "object"


def test_validator_passes():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
