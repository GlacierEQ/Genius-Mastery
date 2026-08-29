"""Contract validation for a Genius repository root."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REPO_NAME_RE = re.compile(r"^Genius-[A-Za-z0-9._-]+$")
SUPPORTED_SCHEMA = 2
SUPPORTED_CAPABILITY_SCHEMA = 1


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_capability_stack(root: Path, errors: list[str]) -> None:
    path = root / "capabilities" / "STACK.yaml"
    if not path.exists():
        return

    data = load_yaml(path)
    if not isinstance(data, dict):
        errors.append("capabilities/STACK.yaml is not a mapping")
        return
    if data.get("schema_version") != SUPPORTED_CAPABILITY_SCHEMA:
        errors.append(
            "capabilities/STACK.yaml schema_version must be "
            f"{SUPPORTED_CAPABILITY_SCHEMA}"
        )
    if not data.get("id"):
        errors.append("capabilities/STACK.yaml id missing")
    if not data.get("purpose"):
        errors.append("capabilities/STACK.yaml purpose missing")

    objective = data.get("objective")
    if not isinstance(objective, dict) or not objective.get("desired_reality"):
        errors.append("capabilities/STACK.yaml objective.desired_reality missing")

    layers = data.get("layers")
    if not isinstance(layers, dict) or not layers:
        errors.append("capabilities/STACK.yaml layers must be a non-empty mapping")

    verification = data.get("verification")
    if not isinstance(verification, dict):
        errors.append("capabilities/STACK.yaml verification missing")
    else:
        acceptance = verification.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance:
            errors.append(
                "capabilities/STACK.yaml verification.acceptance must be non-empty"
            )

    mission_impact = data.get("mission_impact")
    if not isinstance(mission_impact, dict):
        errors.append("capabilities/STACK.yaml mission_impact missing")


def validate_repo(root: Path) -> list[str]:
    """Return list of error strings; empty means PASS."""
    errors: list[str] = []
    genius_path = root / "GENIUS.yaml"
    if not genius_path.exists():
        errors.append("GENIUS.yaml missing")
        return errors

    data = load_yaml(genius_path)
    if not isinstance(data, dict):
        errors.append("GENIUS.yaml is not a mapping")
        return errors

    if data.get("schema_version") != SUPPORTED_SCHEMA:
        errors.append(
            f"Unsupported schema_version={data.get('schema_version')}; required {SUPPORTED_SCHEMA}"
        )

    repo = data.get("repository")
    if not isinstance(repo, str) or not REPO_NAME_RE.match(repo):
        errors.append(f"repository must match ^Genius-[A-Za-z0-9._-]+$, got {repo!r}")

    if data.get("family") != "Genius":
        errors.append("family must be 'Genius'")
    if data.get("doctrine") != "mastery-not-skills":
        errors.append("doctrine must be 'mastery-not-skills'")

    # Claims uniqueness
    claims_path = root / "claims" / "CLAIMS.yaml"
    if claims_path.exists():
        claims = (load_yaml(claims_path) or {}).get("claims") or []
        ids: set[str] = set()
        for c in claims:
            cid = c.get("id")
            if not cid:
                errors.append("claim missing id")
                continue
            if cid in ids:
                errors.append(f"duplicate claim id: {cid}")
            ids.add(cid)
            if not c.get("statement") or len(str(c["statement"])) < 10:
                errors.append(f"claim {cid}: statement too short or missing")

    # Composition capability uniqueness
    comp_path = root / "interfaces" / "COMPOSITION.yaml"
    if comp_path.exists():
        comp = load_yaml(comp_path) or {}
        provides = comp.get("provides") or []
        pids: set[str] = set()
        for p in provides:
            pid = p.get("id")
            if not pid:
                errors.append("provides entry missing id")
                continue
            if pid in pids:
                errors.append(f"duplicate capability id: {pid}")
            pids.add(pid)

    validate_capability_stack(root, errors)
    return errors
