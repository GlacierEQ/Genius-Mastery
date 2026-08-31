# Changelog

## [0.7.0] — 2026-08-30

### Evidence-derived self-observation
- Added `genius.vector` to compute Mastery’s multidimensional state directly from `claims/CLAIMS.yaml` and `evidence/ledger.jsonl`.
- Added per-dimension status/evidence counts, deepest demonstrated tier, counterevidence counts, orphan evidence reporting, dangling evidence detection, and ledger-to-claim integrity checks.
- Added `genius vector [path] [--write]` to inspect or regenerate `mastery/VECTOR.yaml`.
- Added regression coverage for vector derivation, dangling references, ledger mismatches, round-trip persistence, live-repository integrity, and CLI writes.
- Restored missing imports for the 0.6.0 `analyze` and `family` CLI paths after exact-source readback exposed the defect.
- Preserved Buildkite #129 as counterevidence rather than allowing a green projection to override contradictory source.
- Strengthened Buildkite verification to require a post-execution exact-source receipt binding JUnit and computed-vector artifacts.

## [0.6.0] — 2026-08-30

### Cross-Genius family composition
- Added `genius.family` for local `Genius-*` repository discovery from each repository's own `GENIUS.yaml` and composition contract.
- Added provider/consumer binding resolution, unresolved dependency reporting, provider fan-out, and transparent cross-repository composition candidates.
- Added `genius family [path] [--top N] [--output YAML]` for human-readable and machine-readable family analysis.
- Registered mission intelligence and family composition as first-class Mastery capabilities.
- Added regression coverage for family discovery, dependency resolution, missing dependencies, property-testing synergy discovery, and reporting.
- Synchronized runtime, package metadata, and `GENIUS.yaml` at version 0.6.0.

### Verification lane repair
- Restored the last independently proven Buildkite topology as the compatibility baseline after tracing the persistent red sequence back to the fail-closed preflight introduced after build #3.
- Added 0.6.0 CLI smoke coverage for synthesis, graph intelligence, family analysis, validation, and Python compilation.
- External terminal PASS remains a runtime fact to be established by Buildkite; this changelog does not promote a dispatched build to verified.

## [0.5.0] — 2026-08-30

### Mission-sensitive capability intelligence
- Added `genius.intelligence` with explainable mission-impact, readiness, evidence-strength, dependency-centrality, substitutability, priority, and leverage scoring.
- Replaced the previous structural-only graph analysis with ranked bottleneck and next-action intelligence.
- Added `genius analyze [repo|GRAPH.yaml] [--top N] [--write]` for human-readable analysis and persistent enriched graphs.
- Preserved truth-state discipline: scoring never promotes mapped/discovered capability to verified or mastered.
- Added regression coverage for bottleneck ranking, evidence/readiness behavior, dependency centrality, reporting, and CLI persistence.

## [0.4.0] — 2026-08-29

### Teacher-forge / entity compiler
- Reframed Genius-Mastery from a static family example into a self-hosting teacher-forge.
- Added `genius synthesize <role> --outcome <outcome>`.
- Added self-hosted `ROLE.yaml`, persona, synthesis plan, teaching plan, and teaching contract.
- Added role brief schema and measurable teaching schema/template.
- Added `teach` to the mastery spiral.
- Added generated standalone validation so descendants do not secretly depend on an installed Mastery package.

### Vertical excellence anatomy
- Added universal capability anatomy schema and YAML template.
- Added kernel-up stack from reality/physical substrate/compute through model, persona, context, memory, perception, reasoning, skills, tools, APIs, connectors/MCP, documents, swarms, verification, recovery, teaching, real-world effects, and learning.
- Added universal inspection prompts for every anatomy layer.
- Added mission-impact dimensions for criticality, sensitivity, substitutability, downstream centrality, and improvement leverage.

### Composition and live capability reuse
- Added capability source registry.
- Added reference-only local adapter for GlacierEQ/mega-skills Skills, Combo Skills, and Mega Skills registries.
- Added optional `--mega-skills-root` synthesis enrichment.
- Added real capability-ID matching without copying implementation bodies.
- Added teaching capability to Genius-Code and Genius-Verification vertical stacks and composition contracts.

### Verification
- Expanded GitHub contract CI to install the package and run the regression suite.
- Added Researcher -> Indiana Jones synthesis regression.
- Added full vertical inspection regression.
- Added real-registry-shape matching regression.
- Added standalone generated-repository validator regression.

## [0.3.0] — 2026-08-29

### Added
- Universal capability anatomy, schema, template, vertical stack, and scaffold inheritance.
- Initial Genius-Code and Genius-Verification vertical excellence maps.

## [0.2.0] — 2026-08-29

### Added
- Installable package `genius-mastery` via pyproject.toml.
- CLI entry point `genius`:
  - `genius name <purpose>`
  - `genius validate [path]`
  - `genius doctor [path]`
  - `genius new <purpose> [--dest DIR]`
- Naming normalization tests.
- Family INDEX updated with Genius-Code evidence + Genius-Verification.

### Prior (same day)
- Schema v2 identity contract, core schemas, local tools, composition, sources seed.
