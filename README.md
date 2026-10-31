# Genius-Mastery

**Repository-building program:** [GENIUS REPOSITORY FOUNDRY — canonical end-to-end master implementation plan](docs/REPOSITORY_FOUNDRY_MASTER_PLAN.md). This is a planned, source-grounded upgrade of the **existing** Genius-Mastery generator and Genius-Engineering execution spine, not a claim that all new factory capabilities have already been implemented. The plan's Phase 0–2 work resolves actual forge portability and capability-verification defects before claiming production generation.

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
- `schemas/representation-contract.schema.json`
- `docs/CASE_POSITION_MASTERY.md`
- `schemas/capability.schema.json`
- `schemas/role-brief.schema.json`
- `schemas/case-position-campaign.schema.json`
- `templates/CAPABILITY.yaml`
- `templates/CASE_POSITION_CAMPAIGN.yaml`
- `sources/CAPABILITY_SOURCES.yaml`
- `sources/EPISTEMIC_SOURCES.yaml`

## Executable dynamic adjustment

The four-pillar doctrine is enforced by `src/genius/representation.py` and exposed through `genius represent`.

It keeps one capability truth state across orientation, mastery, machine-contract, and mesh projections. Rendering may adapt depth, routing, verification intensity, and restraint; it may not promote aspiration, discard contradiction, or mint execution authority.

```bash
genius represent \
  --statement "Connector supports structured invocation." \
  --maturity designed_for \
  --next-actor machine \
  --purpose integration \
  --system-state planned \
  --json
```

`verified` requires source-bearing evidence, `demonstrated` requires an execution receipt, and consequential external actions are classified as requiring trusted-host authorization. The representation layer deliberately has no flag that can self-assert human approval.

## Case Position Mastery

Genius-Mastery includes a controlled case-outbound campaign substrate:

- `docs/CASE_POSITION_MASTERY.md` defines the doctrine for Operator-approved position, single outbound authority, stale-send suppression, escalation clocks, and provider receipt/readback requirements.
- `schemas/case-position-campaign.schema.json` defines a machine-checkable campaign contract for objectives, escalation ladders, review boundaries, and verification.
- `templates/CASE_POSITION_CAMPAIGN.yaml` provides the reusable campaign skeleton.
- `examples/case-position/NEX_CAMPAIGN_REDACTED.yaml` seeds the NEX campaign as a redacted doctrine object without publishing private evidence or uncontrolled allegations.

The rule is simple: external case communication is strategic action. A vague acknowledgment is not automatically progress, and no worker may improvise posture, recipient class, remedy, concession, or counsel-seeking outreach outside an approved campaign mandate.

## Install

```bash
git clone https://github.com/GlacierEQ/Genius-Mastery.git
cd Genius-Mastery
pip install -e .
```

Requires Python >= 3.10 and PyYAML.


## Foundry Phase 3: independently runnable TypeScript taskboard

The existing `genius foundry new` front door now supports an additional product
profile, `typescript-taskboard`, alongside the existing `python-text-audit`:

```sh
genius foundry new --profile typescript-taskboard --name Taskboard \
  --objective "Build a local task manager with a browser UI and persistent REST API" \
  --dest ./workspaces

cd ./workspaces/Genius-Taskboard
npm ci
npm test
npm start
```

This produces a **standalone** Node 22 app, not a Genius-runtime-dependent
scaffold: a browser UI, TypeScript HTTP backend, JSON task persistence, real
create/list/update/delete operations, negative-path handling, and native
integration tests using a live ephemeral HTTP port. The output includes its
own package metadata, lockfile, GitHub Actions workflow, source digests,
original objective, and exact run instructions. The server defaults to
`127.0.0.1:3000` and deliberately has no public authentication.

The build uses Node 22's dependency-free TypeScript stripping API. This
runs genuine erasable TypeScript and builds JavaScript but **does not perform
static TypeScript typechecking**; richer compiler-driven assurance remains
a separate future Foundry task. Use only with Node 22.13 or later. The generated
`mission.json` remains `GENERATED_UNVERIFIED` at creation. Tests and provider
receipts must be checked separately; generated source is not a production
deployment or proof that an arbitrary original objective was satisfied.

The same callable `genius foundry new --profile python-text-audit` remains
supported. Both profiles share the existing staged, preserving publication
mechanism. See the [Foundry master plan](docs/REPOSITORY_FOUNDRY_MASTER_PLAN.md)
for remaining execution, rehabilitation, delivery and verification phases.

## Foundry Phase 2: portable Lineage forge (implemented)

The existing registered Lineage domain generator now has a directly usable, portable command:

```bash
genius forge aerospace --dest ./workspaces
# Optional explicit replacement (old tree retained for rollback until publication succeeds):
genius forge aerospace --dest ./workspaces --force
```

An omitted `--dest` uses `./Genius-Lineage` relative to the current working directory. It does not assume `/root/projects/Genius-Lineage`. The forge validates the selected archetype, refuses unsafe names and symlink destinations, rejects case-folded collisions, and preserves existing files unless explicitly given `--force`. It renders to a private sibling staging directory, compiles generated Python, emits a deterministic `evidence/MANIFEST.json` with SHA-256 file identities, and atomically publishes the result. A timestamped forge receipt is retained separately; generated targets are **mapped and unverified** until they pass independent tests and execution.

`genius forge` operates on registered Lineage implementations. This is not yet a complete mission-to-production repository compiler; the complete lifecycle, repair, CI, deployment and three acceptance missions remain governed by the [Foundry master plan](docs/REPOSITORY_FOUNDRY_MASTER_PLAN.md). Generating files alone is not independent execution proof.

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

## Reuse the estate through Monolith during synthesis

The role compiler can route a purpose and outcomes through a **local copy** of
Monolith's machine-readable capability index, while keeping implementation and
runtime verification separate. The index is an inventory, not a provider receipt.

```bash
genius synthesize "Business Process Automation" \
  --outcome "workflow automation with idempotency and provider readback" \
  --outcome "reliable context recovery, evaluation and human approvals" \
  --monolith-catalog /path/to/monolith/catalog/AI_DYNAMIC_CAPABILITY_INDEX.json \
  --mega-skills-root /path/to/mega-skills \
  --dest /path/to/private-output

genius validate /path/to/private-output/Genius-Business-Process-Automation
```

A supplied Monolith catalog is read without changing it. Its filename, version,
generation timestamp and exact SHA-256 are retained in the generated
`capabilities/ESTATE_DISCOVERY.yaml`; matching intent vectors name candidate
owning repositories and the verification required before actual reuse.
`synthesis/PLAN.yaml` references that evidence-bounded discovery artifact.

**Privacy and proof:** Keep outputs containing private repository references in
private storage. No private index is fetched or embedded in the public Mastery
repository. Catalog entries are labeled `catalog-pointer-unverified` even if a
README claims production readiness; check the current owning revision, interface,
authorized execution, native receipt and independent readback. A successful
generation proves role compilation, not live business-process automation.

The CI smoke test uses an explicitly **synthetic** index and saves an inspectable
`genius-bpa-synthetic-smoke` artifact. It is regression evidence for the
compiler and never a substitute for a real estate capability audit.

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
genius represent --statement "Capability statement" --maturity aspirational --next-actor person --purpose orientation --json
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
