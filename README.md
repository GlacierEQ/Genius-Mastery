# Genius-Mastery

[![Buildkite](https://badge.buildkite.com/53fcc89c70c0eb2508067aa8108bf0f15d27da721a94f8c63c.svg)](https://buildkite.com/casey-1/genius-mastery)

**Teacher-forge, family kernel, and entity compiler for the Genius repository ecosystem.**

Identity rule:

```text
Genius-{purpose}
```

## What this repository is

Genius-Mastery is not a static example of a Genius repository. Its primary product is **other, stronger Genius entities**.

A thin role brief:

```text
role: Researcher
outcomes:
  - Indiana Jones
```

can be compiled into a purpose-built starting entity containing:

- role identity and directional persona;
- kernel-up vertical capability anatomy;
- inferred capability families;
- mastery map and roadmap;
- skill / Combo / Mega Skill discovery targets;
- model, tool, API, connector, MCP, runtime, document, and multimodal targets;
- teaching and reconstruction plan;
- evidence requirements;
- verification and recovery semantics;
- frontier questions and improvement targets.

Generated capability is explicitly **mapped**, not magically mastered. Research, execution, challenge, evidence, transfer, and teaching move it upward.

## Doctrine

> Mastery is demonstrated by creating stronger practitioners.

The family loop is:

```text
MAP
→ RESEARCH
→ MODEL
→ BUILD
→ BREAK
→ MEASURE
→ VERIFY
→ OPERATE
→ EXPLAIN
→ SYNTHESIZE
→ PROVE
→ EXPAND
→ TEACH ANOTHER
↺
```

The universal entity anatomy asks:

> What must exist, be accessible, be compatible, be correctly represented, and successfully operate for this capability to become true in reality?

See:

- `docs/GENIUS_ENTITY_ANATOMY.md`
- `docs/MASTER_TEACHER_FORGE.md`
- `schemas/capability.schema.json`
- `schemas/role-brief.schema.json`
- `templates/CAPABILITY.yaml`
- `sources/CAPABILITY_SOURCES.yaml`

## Install

```bash
git clone https://github.com/GlacierEQ/Genius-Mastery.git
cd Genius-Mastery
pip install -e .
```

Requires Python >= 3.10 and PyYAML.

## Forge a Genius entity

Preferred high-level operation:

```bash
genius synthesize Researcher \
  --outcome "Indiana Jones" \
  --dest /tmp

# When the real Mega Skills checkout is available, match against it:
genius synthesize Researcher \
  --outcome "Indiana Jones" \
  --mega-skills-root /path/to/mega-skills \
  --dest /tmp
```

Multiple outcomes and constraints can be supplied:

```bash
genius synthesize Researcher \
  --outcome "Indiana Jones" \
  --outcome "publication-grade evidence synthesis" \
  --constraint "preserve provenance" \
  --constraint "work across text, image, audio, and documents" \
  --dest /tmp
```

The result is a generated `Genius-Researcher` repository with `ROLE.yaml`, `persona/PERSONA.md`, `synthesis/PLAN.yaml`, `capabilities/STACK.yaml`, a teaching plan, mastery map, roadmap, and frontier queue.

The archetype/outcome is directional input. It is never treated as proof that the generated entity already possesses those abilities.

## Lower-level commands

```bash
genius --version
genius name "Distributed Systems"
genius validate .
genius doctor .
genius new Performance --dest /tmp
```

`genius new` creates a bare domain substrate. `genius synthesize` creates and teaches a role-shaped starting entity.

## Capability sources

The forge is designed to **discover and compose**, not duplicate.

Initial source families include:

- `GlacierEQ/mega-skills` atomic Skills;
- `GlacierEQ/mega-skills` Combo Skills;
- `GlacierEQ/mega-skills` Mega Skills;
- sibling `Genius-*` composition contracts;
- live models, tools, APIs, MCP servers, connectors, runtimes, browsers, files, and devices;
- authoritative research, standards, source repositories, benchmarks, and production receipts.

## Family

| Repository | Purpose |
|---|---|
| Genius-Mastery | teacher-forge + family kernel |
| Genius-Code | code vertical excellence |
| Genius-Verification | verification vertical excellence |

See `family/INDEX.json`.

## Current truth

Implemented:

- Genius identity contract;
- claim/evidence/source/challenge/composition schemas;
- universal capability anatomy schema;
- universal capability template;
- role-brief schema;
- kernel-up entity anatomy;
- vertical capability stack;
- role-to-entity synthesis engine;
- universal kernel-up inspection brain across every vertical layer;
- optional real Mega Skills registry matching without implementation duplication;
- `genius synthesize` CLI;
- scaffold generator;
- structural validators;
- regression tests including `Researcher -> Indiana Jones`;
- capability source registry;
- Buildkite/GitHub CI surfaces.

Still frontier work:

- automatic live Mega Skills registry ingestion;
- automatic tool / model / connector inventory ingestion;
- capability-graph compiler;
- mission-sensitive importance and leverage computation;
- automatic cross-Genius composition discovery;
- generated challenge implementation rather than mapped challenge prompts;
- full migration engine;
- continuous outcome-to-generator learning.

Never convert "generated" into "mastered" or "file exists" into "system works."

## License

MIT. See LICENSE.
