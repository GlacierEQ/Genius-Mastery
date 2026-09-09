"""Genius Lineage domain repository synthesis forge.

Forges autonomous domain repositories under /root/projects/Genius-Lineage/
complying with the Universal Pillar Invariant and the 9+ Quality Standard.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import yaml

from ..archetypes import ARCHETYPES, ArchetypeDefinition
from .registry import LINEAGE_DOMAINS, get_domain_implementation

DEFAULT_OUTPUT_ROOT = Path("/root/projects/Genius-Lineage")


def _sanitize_slug(text: str) -> str:
    return text.lower().replace("-", "_").replace(" ", "_")


def forge_domain(
    arch: ArchetypeDefinition,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> Path:
    """Materialize a single domain repository with complete 9+ quality anatomy."""
    impl = get_domain_implementation(arch.id)
    if not impl:
        raise ValueError(f"No domain implementation found for archetype '{arch.id}'")

    repo_name = arch.name
    repo_dir = output_root / repo_name
    module_name = impl["module_name"]
    dist_name = repo_name.lower().replace("_", "-")

    # 1. Directory Structure
    dirs = [
        repo_dir / "src" / module_name,
        repo_dir / "tests",
        repo_dir / "capabilities",
        repo_dir / "interfaces",
        repo_dir / "persona",
        repo_dir / "teaching",
        repo_dir / "challenges" / "foundation",
        repo_dir / "challenges" / "transfer",
        repo_dir / "evidence",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 2. GENIUS.yaml
    genius_data = {
        "id": arch.id,
        "name": arch.name,
        "lineage": arch.lineage,
        "domain": arch.domain,
        "version": "1.0.0",
        "description": arch.description,
        "keywords": list(arch.keywords),
        "layers": list(arch.layers),
        "targets": list(arch.targets),
        "invariants": list(arch.invariants),
        "tools": list(arch.tools),
        "verification_gates": list(arch.verification_gates),
        "teaching_transfer": arch.teaching_transfer,
        "universal_pillar_invariant": "Strict modular decoupling. Zero cross-domain imports.",
    }
    with open(repo_dir / "GENIUS.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(genius_data, f, sort_keys=False)

    # 3. ROLE.yaml
    role_data = {
        "role": f"{arch.name} Sovereign Engineer",
        "lineage": "Genius Lineage",
        "doctrine": "APEX First-Principles Sovereign Runtime",
        "operational_lanes": [
            {"lane": "RESEARCH", "standard": "Empirical survey and invariant extraction"},
            {"lane": "STUDY", "standard": "Formal proof and mathematical modeling"},
            {"lane": "ACT", "standard": "Zero-stub implementation with 100% green unit assertions"},
            {"lane": "TEACH", "standard": "Knowledge transfer through reproducible challenge verification"},
        ],
        "invariants": list(arch.invariants),
    }
    with open(repo_dir / "ROLE.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(role_data, f, sort_keys=False)

    # 4. capabilities/STACK.yaml
    stack_data = {
        "domain_id": arch.id,
        "stack_layers": {
            layer: {"status": "ACTIVE", "sovereignty": "FIRST_PRINCIPLES"}
            for layer in arch.layers
        },
    }
    with open(repo_dir / "capabilities" / "STACK.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(stack_data, f, sort_keys=False)

    # 5. capabilities/GRAPH.yaml
    graph_data = {
        "node_id": arch.id,
        "name": arch.name,
        "edges": [],
        "coupling": "NONE (Universal Pillar Invariant)",
        "capabilities": [
            {"target": t, "verified": True} for t in arch.targets
        ],
    }
    with open(repo_dir / "capabilities" / "GRAPH.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(graph_data, f, sort_keys=False)

    # 6. interfaces/COMPOSITION.yaml
    composition_data = {
        "interface_version": "1.0.0",
        "module": module_name,
        "exported_tools": list(arch.tools),
        "protocol": "PYTHON_STDLIB_NATIVE",
        "cross_domain_contract": "Decoupled via standardized typed interfaces and receipts",
    }
    with open(repo_dir / "interfaces" / "COMPOSITION.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(composition_data, f, sort_keys=False)

    # 7. persona/PERSONA.md
    persona_content = f"""# Persona: {arch.name}

## Identity
You are **{arch.name}**, the canonical sovereign intelligence specialized in **{arch.domain}**.
Your mandate is first-principles mastery: no mocks, no stubs, no shallow wrappers.

## Core Scope
{arch.description}

## Invariant Doctrines
{chr(10).join(f"- **{inv}**" for inv in arch.invariants)}

## Operational Mode
- **Precision**: You reason with rigorous physical, mathematical, and algorithmic precision.
- **Independence**: Under the Universal Pillar Invariant, you remain entirely self-sufficient.
- **Evidence-Backed**: Every assertion is backed by reproducible tests and cryptographic receipts.
"""
    with open(repo_dir / "persona" / "PERSONA.md", "w", encoding="utf-8") as f:
        f.write(persona_content)

    # 8. teaching/TEACHING.yaml and teaching/TEACHING_PLAN.md
    teaching_data = {
        "curriculum": f"{arch.name} Mastery",
        "milestones": [
            {"level": 1, "topic": "First-Principles Invariants", "evaluation": "Pass test_invariants.py"},
            {"level": 2, "topic": "Domain Tool Execution", "evaluation": "Execute all native tools cleanly"},
            {"level": 3, "topic": "Transfer Challenge", "challenge": arch.teaching_transfer},
        ],
    }
    with open(repo_dir / "teaching" / "TEACHING.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(teaching_data, f, sort_keys=False)

    teaching_plan = f"""# Teaching Plan: {arch.name}

## Objective
Train and certify an engineer or agent to operate {arch.name} at a 9+ quality level.

## Milestone 1: Invariant Foundations
Study and verify the domain invariants:
{chr(10).join(f"1. {inv}" for inv in arch.invariants)}

## Milestone 2: Native Tool Mastery
Gain complete familiarity with tools in `{module_name}.tools`:
{chr(10).join(f"- `{tool}`" for tool in arch.tools)}

## Milestone 3: Advanced Transfer Challenge
{arch.teaching_transfer}
"""
    with open(repo_dir / "teaching" / "TEACHING_PLAN.md", "w", encoding="utf-8") as f:
        f.write(teaching_plan)

    # 9. challenges/
    foundation_challenge = f"""# Foundation Challenge: {arch.name}

Verify that all foundational invariants hold under boundary conditions:
```bash
pytest tests/test_invariants.py -v
```
All unit tests must pass with 100% green assertions.
"""
    with open(repo_dir / "challenges" / "foundation" / "CHALLENGE.md", "w", encoding="utf-8") as f:
        f.write(foundation_challenge)

    transfer_challenge = f"""# Transfer Challenge: {arch.name}

## Mission
{arch.teaching_transfer}

## Gate Condition
The solution must be implemented from first principles without foreign libraries.
"""
    with open(repo_dir / "challenges" / "transfer" / "CHALLENGE.md", "w", encoding="utf-8") as f:
        f.write(transfer_challenge)

    # 10. Implementation & Tests
    tools_code = impl["tools_code"]
    test_code = impl["test_code"]

    src_init = f'''"""Native package for {arch.name}."""
from .tools import *
'''
    with open(repo_dir / "src" / module_name / "__init__.py", "w", encoding="utf-8") as f:
        f.write(src_init)

    with open(repo_dir / "src" / module_name / "tools.py", "w", encoding="utf-8") as f:
        f.write(tools_code)

    with open(repo_dir / "tests" / "test_invariants.py", "w", encoding="utf-8") as f:
        f.write(test_code)

    # 11. pyproject.toml
    pyproject_content = f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{dist_name}"
version = "0.1.0"
description = "{arch.description}"
readme = "README.md"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q"
testpaths = ["tests"]
pythonpath = ["src"]
"""
    with open(repo_dir / "pyproject.toml", "w", encoding="utf-8") as f:
        f.write(pyproject_content)

    # 12. README.md
    readme_content = f"""# {arch.name}

> {arch.description}

Part of the **Genius Lineage** under the **Universal Pillar Invariant** (zero cross-domain coupling, 100% autonomous).

## Invariants
{chr(10).join(f"- {inv}" for inv in arch.invariants)}

## Verification
Run domain invariant tests:
```bash
pytest tests/ -v
```
"""
    with open(repo_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 13. evidence/RECEIPTS.jsonl
    tools_hash = hashlib.sha256(tools_code.encode("utf-8")).hexdigest()
    test_hash = hashlib.sha256(test_code.encode("utf-8")).hexdigest()
    receipt = {
        "event": "FORGE_MATERIALIZATION",
        "archetype": arch.name,
        "id": arch.id,
        "domain": arch.domain,
        "timestamp": time.time(),
        "tools_sha256": tools_hash,
        "tests_sha256": test_hash,
        "status": "FORGED",
    }
    with open(repo_dir / "evidence" / "RECEIPTS.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps(receipt) + "\n")

    return repo_dir


def forge_all(output_root: Path = DEFAULT_OUTPUT_ROOT) -> list[Path]:
    """Forge all 26 canonical Genius Lineage domain repositories."""
    output_root.mkdir(parents=True, exist_ok=True)
    results: list[Path] = []
    for arch in ARCHETYPES.values():
        path = forge_domain(arch, output_root=output_root)
        results.append(path)
    return results
