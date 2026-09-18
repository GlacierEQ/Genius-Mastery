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

## Family epistemology

[`docs/EPISTEMOLOGY.md`](docs/EPISTEMOLOGY.md) governs how Genius entities acquire, classify, promote, compose, and teach knowledge.

Prime law:

> A representation may route knowledge, but only proposition-specific evidence may justify a claim.

The family therefore preserves distinctions among aspiration, hypothesis, mapped structure, implementation, executability, observation, verification, reproduction, transfer, mastery, and revalidation. Memory hits, summaries, graphs, manifests, badges, and generated plans are routing surfaces; they do not silently outrank source-bearing evidence.

The family cognition loop is:

```text
RECOVER → CLASSIFY → SOURCE → MODEL → CHALLENGE → EXECUTE
       → VERIFY → READ BACK → RECONCILE → COMPOSE → TEACH → REVALIDATE
```

The authority nucleus is in [`sources/EPISTEMIC_SOURCES.yaml`](sources/EPISTEMIC_SOURCES.yaml), and the executable composition contract is bound into [`capabilities/EPISTEMIC_ENGINEERING.yaml`](capabilities/EPISTEMIC_ENGINEERING.yaml).

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

- `docs/EPISTEMOLOGY.md`
- `docs/GENIUS_ENTITY_ANATOMY.md`
- `docs/MASTER_TEACHER_FORGE.md`
- `docs/DYNAMIC_ADJUSTMENT_AND_FOUR_PILLARS.md`
- `docs/CASE_POSITION_MASTERY.md`
- `schemas/capability.schema.json`
- `schemas/role-brief.schema.json`
- `schemas/case-position-campaign.schema.json`
- `templates/CAPABILITY.yaml`
- `templates/CASE_POSITION_CAMPAIGN.yaml`
- `sources/CAPABILITY_SOURCES.yaml`
- `sources/EPISTEMIC_SOURCES.yaml`

## Case Position Mastery

Genius-Mastery includes a controlled case-outbound campaign substrate:

- `docs/CASE_POSITION_MASTERY.md` defines the doctrine for Operator-approved position, peer-mesh execution, per-WORK_UNIT single-writer/idempotency, stale-send suppression, escalation clocks, and provider receipt/readback requirements.
- `schemas/case-position-campaign.schema.json` defines a machine-checkable campaign contract for objectives, escalation ladders, review boundaries, and verification.
- `templates/CASE_POSITION_CAMPAIGN.yaml` provides the reusable campaign skeleton.
- `examples/case-position/NEX_CAMPAIGN_REDACTED.yaml` seeds the NEX campaign as a redacted doctrine object without publishing private evidence or uncontrolled allegations.

The rule is simple: external case communication is strategic action. A vague acknowledgment is not automatically progress. No worker may improvise posture, recipient class, remedy, concession, or counsel-seeking outreach outside an approved campaign mandate, but routine constituent actions inside that mandate may be executed by any qualified peer holding the exact WORK_UNIT idempotency lease.

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
genius discover . --write
genius calibrate .
genius compose /path/to/genius-estate --output /tmp/composition-receipt.json
genius rebuild-graph .
genius closure .
genius new Performance --dest /tmp
```

`genius new` creates a bare domain substrate. `genius synthesize` creates and teaches a role-shaped starting entity.

### Analyze a Genius entity

Every synthesized entity carries a capability graph. The kernel can rank that graph by mission impact, readiness, evidence strength, dependency centrality, and recorded substitutes:

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
