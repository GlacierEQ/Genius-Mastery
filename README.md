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
- `docs/DYNAMIC_ADJUSTMENT_AND_FOUR_PILLARS.md`
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
genius analyze . --top 10
genius analyze . --write
genius family /path/to/genius-estate --top 10
genius vector .
genius vector . --write
genius new Performance --dest /tmp
```

`genius new` creates a bare domain substrate. `genius synthesize` creates and teaches a role-shaped starting entity.


### Analyze a Genius entity

Every synthesized entity carries a capability graph. The kernel can now rank that graph by mission impact, readiness, evidence strength, dependency centrality, and recorded substitutes:

```bash
genius analyze /path/to/Genius-Engineering --top 12

# Persist the enriched analysis into capabilities/GRAPH.yaml
genius analyze /path/to/Genius-Engineering --write
```

The analysis emits ranked priorities, candidate bottlenecks, high-leverage nodes, and reasons for each score. It is an action-prioritization model, not a certification shortcut: unverified state remains unverified until evidence and challenge results justify promotion.


### Analyze the Genius family

Point Mastery at a directory containing sibling `Genius-*` repositories:

```bash
genius family /path/to/genius-estate --top 12

# Persist the complete family analysis
genius family /path/to/genius-estate \
  --output /tmp/genius-family-analysis.yaml
```

The family engine reads each repository's own `GENIUS.yaml` and composition contract, resolves declared provider/consumer bindings, exposes unresolved dependencies and provider fan-out, and proposes cross-repository capability combinations. Composition candidates remain hypotheses until their combined behavior is executed, challenged, and verified.


### Compute the mastery vector

```bash
genius vector .
genius vector . --write
```

The vector is computed from `claims/CLAIMS.yaml` and `evidence/ledger.jsonl`. It reports per-dimension claim counts, evidence coverage, demonstrated tier, counterevidence presence, dangling evidence references, and ledger-to-claim mismatches. It deliberately does **not** emit a single mastery percentage.

`--write` regenerates `mastery/VECTOR.yaml` from those source records so the diagnostic state cannot drift into hand-maintained vanity scoring.

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
- recursive capability-graph compiler;
- mission-sensitive capability intelligence with bottleneck/leverage ranking;
- evidence/readiness/substitutability-aware prioritization;
- `genius analyze` CLI with optional persistent graph enrichment;
- local Genius-family discovery and composition-contract resolution;
- unresolved dependency and provider-fanout analysis;
- cross-Genius composition candidate discovery;
- `genius family` CLI with optional YAML analysis output;
- evidence-derived multidimensional mastery vectors;
- claim/evidence referential-integrity diagnostics;
- `genius vector` CLI with deterministic vector regeneration;
- Buildkite/GitHub CI surfaces.

Still frontier work:

- automatic live Mega Skills registry ingestion;
- automatic tool / model / connector inventory ingestion;
- deeper evidence-quality calibration and learned scoring weights;
- live/remote Genius-estate ingestion beyond local checkouts;
- semantic and execution-backed composition ranking beyond lexical discovery;
- generated challenge implementation rather than mapped challenge prompts;
- full migration engine;
- continuous outcome-to-generator learning.

Never convert "generated" into "mastered" or "file exists" into "system works."

## License

MIT. See LICENSE.
