"""Minimal contract tests for Genius-Mastery seed."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_genius_yaml_exists():
    assert (ROOT / "GENIUS.yaml").exists()


def test_validator_passes():
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
