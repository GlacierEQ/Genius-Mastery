"""Role-to-Genius entity synthesizer.

The synthesizer creates a teaching-oriented starting entity from a thin role brief.
It emits hypotheses and capability targets, never fabricated mastery claims.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import yaml

from genius.scaffold import create_domain


BASE_FAMILIES = {
    "reasoning": {
        "layers": ["reasoning", "metacognition", "planning"],
        "targets": ["decomposition", "hypothesis testing", "uncertainty calibration", "route selection"],
    },
    "research": {
        "layers": ["knowledge", "reasoning", "tools", "apis", "connectors_mcp"],
        "targets": ["source discovery", "source ranking", "provenance", "cross-source synthesis"],
    },
    "evidence": {
        "layers": ["verification", "representation", "observability"],
        "targets": ["evidence capture", "independent readback", "provenance", "counterevidence"],
    },
    "memory": {
        "layers": ["memory", "state_persistence", "context"],
        "targets": ["retrieval", "episodic continuity", "semantic indexing", "state resumption"],
    },
    "communication": {
        "layers": ["language", "communication", "human_interaction", "teaching"],
        "targets": ["interviewing", "explanation", "audience adaptation", "clear handoff"],
    },
}

KEYWORD_FAMILIES = {
    "field-research": {
        "keywords": {"indiana", "jones", "field", "archaeology", "archaeologist", "expedition", "explorer", "historian"},
        "layers": ["reality", "perception", "multimodal", "planning", "reliability_recovery"],
        "targets": ["field observation", "geographic reasoning", "navigation", "environmental uncertainty", "evidence preservation"],
    },
    "documents": {
        "keywords": {"document", "pdf", "archive", "archives", "book", "records", "filing", "paper"},
        "layers": ["files_documents", "artifact_generation", "representation"],
        "targets": ["document ingestion", "layout understanding", "citation extraction", "artifact generation"],
    },
    "vision": {
        "keywords": {"image", "visual", "vision", "photo", "map", "diagram", "artifact"},
        "layers": ["perception", "multimodal", "representation"],
        "targets": ["image understanding", "OCR", "spatial interpretation", "visual verification"],
    },
    "audio": {
        "keywords": {"audio", "voice", "speech", "recording", "interview", "transcription"},
        "layers": ["perception", "multimodal", "artifact_generation"],
        "targets": ["speech recognition", "speaker separation", "timestamps", "transcript verification"],
    },
    "multilingual": {
        "keywords": {"language", "translation", "multilingual", "foreign", "spanish", "french", "linguist"},
        "layers": ["language", "knowledge", "communication"],
        "targets": ["language identification", "translation", "terminology", "cross-cultural interpretation"],
    },
    "code": {
        "keywords": {"code", "developer", "engineer", "programmer", "software", "debug"},
        "layers": ["code", "runtime", "tools", "verification"],
        "targets": ["implementation", "debugging", "testing", "performance", "repair"],
    },
    "legal": {
        "keywords": {"legal", "law", "lawyer", "litigation", "court", "attorney", "case"},
        "layers": ["domain_expertise", "research", "files_documents", "verification"],
        "targets": ["authority research", "claim-evidence tethering", "procedure", "adversarial analysis"],
    },
    "automation": {
        "keywords": {"automation", "agent", "operator", "operations", "scheduler"},
        "layers": ["time_events_automation", "orchestration", "reliability_recovery"],
        "targets": ["trigger design", "state transitions", "idempotency", "recovery"],
    },
    "swarm": {
        "keywords": {"swarm", "team", "multi-agent", "multiagent", "crew"},
        "layers": ["swarm_multi_agent", "orchestration", "communication"],
        "targets": ["role assignment", "delegation", "shared state", "result synthesis"],
    },
}


def _tokens(parts: Iterable[str]) -> set[str]:
    return {
        token
        for part in parts
        for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", part.casefold())
    }


def infer_families(role: str, outcomes: list[str], archetype: str | None = None) -> dict[str, dict]:
    tokens = _tokens([role, *outcomes, archetype or ""])
    selected = dict(BASE_FAMILIES)
    for name, spec in KEYWORD_FAMILIES.items():
        if tokens.intersection(spec["keywords"]):
            selected[name] = {
                "layers": list(spec["layers"]),
                "targets": list(spec["targets"]),
            }
    return selected


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def synthesize_role(
    role: str,
    outcomes: list[str],
    dest_parent: Path,
    *,
    archetype: str | None = None,
    constraints: list[str] | None = None,
    force: bool = False,
) -> Path:
    """Create and enrich a Genius repository from a role + desired outcomes."""
    if not outcomes:
        raise ValueError("at least one outcome is required")

    root = create_domain(role, dest_parent, force=force)
    repo_name = root.name
    families = infer_families(role, outcomes, archetype)

    role_brief = {
        "schema_version": 1,
        "role": role,
        "outcomes": outcomes,
        "archetype": archetype or "",
        "constraints": constraints or [],
        "notes": "Thin brief compiled by Genius-Mastery. Inferred capabilities are hypotheses until evidenced.",
    }
    _write_yaml(root / "ROLE.yaml", role_brief)

    all_targets = sorted({
        target
        for spec in families.values()
        for target in spec["targets"]
    })
    all_layers = sorted({
        layer
        for spec in families.values()
        for layer in spec["layers"]
    })

    synthesis = {
        "schema_version": 1,
        "repository": repo_name,
        "generated_by": "Genius-Mastery",
        "synthesis_state": "mapped",
        "role": role,
        "outcomes": outcomes,
        "archetype": archetype or "",
        "capability_families": [
            {
                "id": name,
                "layers": spec["layers"],
                "targets": spec["targets"],
                "status": "research-and-verify",
            }
            for name, spec in families.items()
        ],
        "capability_sources": [
            {
                "repository": "GlacierEQ/mega-skills",
                "registries": [
                    "registry/skills.json",
                    "registry/combo-skills.json",
                    "registry/mega-skills.json",
                ],
                "purpose": "Discover reusable executable capabilities without copying their implementation.",
            },
            {
                "family": "Genius-*",
                "interface": "interfaces/COMPOSITION.yaml",
                "purpose": "Discover sibling domain capabilities for higher-order composition.",
            },
            {
                "surface": "runtime",
                "targets": ["models", "tools", "APIs", "MCP servers", "connectors", "files", "devices"],
                "purpose": "Inspect live executable capability before declaring absence.",
            },
        ],
        "research_targets": all_targets,
        "required_vertical_layers": all_layers,
        "teaching_loop": [
            "explain",
            "demonstrate",
            "reconstruct",
            "challenge",
            "observe",
            "verify",
            "retain",
            "transfer",
            "teach-another",
        ],
    }
    _write_yaml(root / "synthesis" / "PLAN.yaml", synthesis)

    persona_lines = [
        f"# Persona: {role}",
        "",
        f"**Desired outcomes:** {', '.join(outcomes)}",
    ]
    if archetype:
        persona_lines += ["", f"**Directional archetype:** {archetype}"]
    persona_lines += [
        "",
        "## Behavioral stance",
        "",
        "- Curious enough to discover hidden dependencies.",
        "- Evidence-seeking rather than prestige-seeking.",
        "- Persistent across failed implementations while preserving working routes.",
        "- Explicit about uncertainty and provenance.",
        "- Teaches methods and reconstruction, not answer memorization.",
        "- Treats every verified gain as a reusable capability for the next composition.",
        "",
        "## Important boundary",
        "",
        "This persona is a design target. It is not evidence that the generated entity already possesses the listed abilities.",
        "",
    ]
    persona_path = root / "persona" / "PERSONA.md"
    persona_path.parent.mkdir(parents=True, exist_ok=True)
    persona_path.write_text("\n".join(persona_lines), encoding="utf-8")

    teaching = [
        f"# Teaching Plan: {role}",
        "",
        "Mastery is measured partly by whether this entity can reconstruct and teach its methods to another learner.",
        "",
        "## Cycle",
        "",
        "1. Explain first principles and dependencies.",
        "2. Demonstrate one complete outcome with evidence.",
        "3. Rebuild the outcome from a blank state.",
        "4. Introduce adversarial and degraded conditions.",
        "5. Measure what fails and why.",
        "6. Repair the smallest high-leverage dependency.",
        "7. Reverify and preserve the gain.",
        "8. Transfer the method to a novel case.",
        "9. Teach the method to another agent or human.",
        "",
        "## Initial capability hypotheses",
        "",
        *[f"- {target}" for target in all_targets],
        "",
    ]
    (root / "teaching" / "TEACHING_PLAN.md").write_text(
        "\n".join(teaching),
        encoding="utf-8",
    )

    teaching_contract_path = root / "teaching" / "TEACHING.yaml"
    teaching_contract = yaml.safe_load(
        teaching_contract_path.read_text(encoding="utf-8")
    )
    teaching_contract["subject"] = f"{role} methods for: " + "; ".join(outcomes)
    teaching_contract["learner"]["target_state"] = (
        f"independently reconstructs, transfers, and teaches verified {role} methods"
    )
    teaching_contract["verification"]["transfer_challenges"] = [
        f"Apply {target} to a novel {role} problem with evidence."
        for target in all_targets
    ]
    _write_yaml(teaching_contract_path, teaching_contract)

    map_lines = [
        f"# Mastery Map: {repo_name}",
        "",
        f"Role: **{role}**",
        "",
        "## Desired outcomes",
        "",
        *[f"- {outcome}" for outcome in outcomes],
        "",
        "## Inferred capability families",
        "",
    ]
    for name, spec in families.items():
        map_lines.append(f"### {name}")
        map_lines.extend(f"- {target}" for target in spec["targets"])
        map_lines.append("")
    map_lines += [
        "## Mastery rule",
        "",
        "Every item above begins as a hypothesis. It advances only through research, implementation, challenge, evidence, operation, transfer, and teaching.",
        "",
    ]
    (root / "mastery" / "MAP.md").write_text("\n".join(map_lines), encoding="utf-8")

    roadmap = {
        "schema_version": 1,
        "near_term": [
            "discover live capability sources",
            "map role-specific first principles",
            "bind relevant skills, combo skills, and mega skills",
            "create first executable challenge",
        ],
        "mid_term": [
            "measure capability bottlenecks",
            "compose higher-order role capabilities",
            "exercise degraded and alternate routes",
            "teach/reconstruct methods from blank state",
        ],
        "frontier": [
            "discover novel capability compositions",
            "improve the generator from observed teaching outcomes",
        ],
    }
    _write_yaml(root / "mastery" / "ROADMAP.yaml", roadmap)

    frontier = {
        "schema_version": 1,
        "items": [
            {
                "id": f"frontier-{i+1:02d}",
                "question": f"How should {target} be implemented, measured, verified, and taught for the role {role}?",
                "status": "open",
            }
            for i, target in enumerate(all_targets)
        ],
    }
    _write_yaml(root / "frontier" / "QUEUE.yaml", frontier)

    stack_path = root / "capabilities" / "STACK.yaml"
    stack = yaml.safe_load(stack_path.read_text(encoding="utf-8"))
    stack["objective"]["desired_reality"] = (
        f"Act as an increasingly capable {role} that can achieve: "
        + "; ".join(outcomes)
        + "."
    )
    stack["objective"]["success_conditions"].extend([
        "Role-specific capability hypotheses are researched and challenged.",
        "The entity can reconstruct and teach verified methods to another learner.",
    ])
    for spec in families.values():
        for layer_name in spec["layers"]:
            layer = stack["layers"].setdefault(
                layer_name,
                {
                    "required": [],
                    "available": [],
                    "missing": [],
                    "alternate_routes": [],
                    "failure_modes": [],
                    "improvement_targets": [],
                },
            )
            for target in spec["targets"]:
                if target not in layer["required"]:
                    layer["required"].append(target)
    stack["evolution"]["current_bottleneck"] = (
        "Research and verify the inferred role capabilities; current synthesis is a mapped hypothesis."
    )
    stack["evolution"]["improvement_targets"] = all_targets
    _write_yaml(stack_path, stack)

    genius_path = root / "GENIUS.yaml"
    genius = yaml.safe_load(genius_path.read_text(encoding="utf-8"))
    genius["role_brief"] = "ROLE.yaml"
    genius["synthesis_plan"] = "synthesis/PLAN.yaml"
    genius["persona"] = "persona/PERSONA.md"
    genius["teaching_plan"] = "teaching/TEACHING_PLAN.md"
    genius["generated_by"] = "Genius-Mastery"
    _write_yaml(genius_path, genius)

    return root
