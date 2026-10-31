# GENIUS REPOSITORY FOUNDRY
## Canonical end-to-end master implementation plan · v1.0

**Status:** PLANNED / IMPLEMENTATION NOT YET CLAIMED  
**Planning date:** October 30, 2026 (HST)  
**Canonical owner:** GlacierEQ/Genius-Mastery  
**Execution and terminal-outcome specialist:** GlacierEQ/Genius-Engineering  
**Engineering capability contributors:** GlacierEQ/Pro_Code, GlacierEQ/pro-code, GlacierEQ/Genius-Code, GlacierEQ/Genius-Verification  
**Family integration:** Monolith, AKOS, Aspen Grove Core, Apex Boot Core, Tower of Babel, and existing provider-native source repositories.  
**Governing purpose:** From one Operator objective, deliver an independent, complete, secure, maintainable, tested, integrated, operable repository, with proof tied to its actual revision and environment. Upgrade existing repositories without losing stronger work. Do not substitute a scaffold, report, gate, plan, or dashboard for a working product.

## 1. The non-negotiable result

A user should be able to supply a natural-language mission, constraints and destination. The system recovers available context, studies the relevant existing source, selects the appropriate engineering architecture, creates or improves functioning code, runs native tests, corrects failures, integrates providers where authorized, verifies release state and returns a working repository and unambiguous receipts. The full task remains intact through the pipeline.

A successful outcome may be a library, command-line application, service, web application, automation, agent, document engine, data pipeline, or domain-specific engineering repository. The user decides the objective. Technology is selected based on the objective, environment and proven native support rather than a universal template.

The system must support three equally important modes:

1. **NEW:** design and create a new repository from the mission, down to real code, tests and operability.
2. **EVOLVE:** inspect a pre-existing repository, retrieve its strongest working state and history, then make source-preserving, non-regressing improvements. No destructive replacement or fork proliferation by default.
3. **REPAIR:** reproduce a concrete failure, find its source, implement a verified fix, protect it with regression coverage and continue the larger objective.

A fourth operation, **VERIFY/RELEASE**, independently tests outcome, deployment and provider readback. It cannot retroactively invent missing effects.

## 2. Source-verified baseline: what to reuse, not rebuild

| Existing owner | Verified source surface | Reuse as |
|---|---|---|
| Genius-Mastery | src/genius/scaffold.py, src/genius/synthesize.py, src/genius/cli.py, family and graph systems, validator and generated standalone-descendant test | Generator and mission compiler; extend existing CLI instead of launching another competing application |
| Genius-Mastery | src/genius/lineage/forge.py and domain registry | Domain-aware seed implementations and research references; reconcile with existing scaffold/synthesizer |
| Genius-Engineering | src/genius_engineering/kernel.py, cli.py, mission/work/deployment schema, receipt code | Dependency graph, maximal ready frontier, change-impact verification, completion evidence, recovery/frontier reporting |
| Genius-Code | domain engineering anatomy, primary-source registry and reference implementations | Coding techniques, language-aware engineering patterns and measurable domain benchmarks |
| Genius-Verification | src/genius_verification/core.py, contracts, property and provenance methods | Independent claims, property/oracle methodology and receipt-chain checks |
| Pro_Code / pro-code | Engineering Double Helix, TypeScript compiler-backed tools, native tests, Node runtime and orchestration contracts | Existing code-intelligence and executable implementation harness where its current capabilities genuinely fit |
| Monolith / AKOS / Aspen Grove / Apex Boot / Tower of Babel | Existing catalog, governance, memory, boot and language-routing contracts | Discover and adopt source-owned capabilities through explicit interface and proof, not a second copy or universal inheritance claim |

**Observed strengths:** the Mastery generator has a real installable Python CLI and template/test structure; its 2026-10-17 validate-contract run passed. Genius-Code and Genius-Verification have recorded successful GitHub validation; pro-code has observed successful native runtime checks. Genius-Engineering's October 11 CI and contract runs failed. Exact current-head Buildkite release and production deployment are not established by this plan.

**Observed generator defects requiring repair:**
- src/genius/lineage/forge.py defaults to /root/projects/Genius-Lineage. That is not portable; configurable destinations and safe paths are required.
- The same file emits capability graph targets with verified: true at generation time, before corresponding independent test proof. Generated claims must initially be mapped/planned and later promoted only by evidence.
- The forge uses direct file writes into target directories; protect nonempty targets, existing user changes, and partial failures with explicit preview, staged writes, preservation and rollback semantics.
- Scaffold, synthesize and lineage forge are separate generation routes. They need one coherent public contract, without deleting differentiated abilities.
- A substantial description or generated test is not a verified working application. Claim levels must bind to executed proof.

## 3. Architectural decision: reuse the family, do not add another control-plane repository

**Primary front door:** the existing Genius-Mastery Python package gains a cohesive repo-factory command family. Existing genius new and genius synthesize remain backwards compatible. The new entry and adapters compose existing functions instead of duplicating them.

**Execution spine:** the existing Genius-Engineering mission kernel accepts the normalized mission and work graph, reports maximal ready work, invokes permitted operations through typed adapters, and proves completion. It becomes an execution participant rather than merely an end-state auditor, without replacing Mastery's identity/role synthesis.

**Capability specialization:**
- Genius-Code chooses and verifies concrete coding patterns where supported.
- pro-code supplies real compiler-level inspection/completion/refactoring, workspace inventory and native language tests when appropriate.
- Genius-Verification supplies test oracles, property/contract/adversarial methods and evidence classification.
- Pro_Code supplies engineering doctrine and design standards, retrieved through authorized private access only.
- Other GlacierEQ capabilities are selected only by explicit compatibility, ownership and demonstrated result.

**Provider adapters:** GitHub, local filesystem, CI runners, deployment providers and secrets/configuration systems remain distinct modules. Core planning, generation and validation work offline with synthetic tests; provider integration uses actual authenticated credentials and records native readback.

**Important separation:** The factory itself is NOT the owner of each generated repository's case records, business data or private secrets. Output repositories own their code, tests, issues and releases. No private doctrine is copied into public descendants by accident.

## 4. Product interfaces and the canonical mission contract

Establish one versioned machine contract (proposed id: glaciereq.repo-foundry.mission.v1) with explicit migration/version compatibility, plus a human-friendly objective interface.

### Required input domains

| Domain | Fields / interpretation |
|---|---|
| Mission | Original Operator objective, requested deliverable, prioritized outcomes, correction history, exclusions and success conditions |
| Target | NEW / EVOLVE / REPAIR / VERIFY, exact owner/repository or output destination, project identity, current revision and privacy |
| Scope | Product type, users, supported platforms, dependencies, interoperability and constraints |
| Architecture | Explicit requirements and justified options for language, package manager, framework, persistence, client, server and deployment |
| Quality | Functional acceptance tests, regression safety, security needs, accessibility, observability, reliability, performance and cost |
| Trust | Allowed external changes, identity, permissions, secrets boundary, protected branches, publication visibility, provider actions |
| Verification | Native tests, static analysis, security checks, dependency reproducibility, independent functional proof and provider readback |
| Continuity | Source IDs, existing work, baseline commit, prior defects, rollback plan, known unknowns and receipt destinations |

Support omitted optional values through sensible defaults, source recovery or provider discovery. Ask only for materially unresolved project direction, unknown external authority, identity/secrets, or irreversible public actions. No large onboarding questionnaire for a routine repository.

### Versioned results

- MISSION: original request plus source-attributed requirements and acceptance cases.
- DESIGN: architecture decision record with rationale, alternatives and constraints.
- PLAN: dependency graph and work units, not artificially reduced scope.
- BUILD: file manifest, source diffs, toolchain versions, exact commit and artifact digests.
- VERIFY: test executions and what each test actually proves, including contrary outcomes.
- OPERATE: runtime/deployment endpoints or local commands, configuration and recovery.
- DELIVERY: verified usable repository location, how to start, current status, actual gaps and next engineering frontier.

Each evidence object carries a schema version, project id, source/target revision, owner, timestamp/timezone, environment, producer, evidence/provenance locator, verification status, and relevant hashes. External provider acceptance must be established separately from local preparation.

## 5. Execution state and honesty contract

Proposed forward states:
OBJECTIVE_CAPTURED → BASELINED → DESIGNED → GENERATED/EDITED → BUILT → TESTED → INTEGRATED → PUBLISHED/DEPLOYED (if applicable) → VERIFIED_OPERATIONAL → DELIVERED.

A mission can remain active across multiple branches or providers. Each state requires its own observable artifact. A local test does not prove production deployment; a repository commit does not prove a user-facing service; a generated README does not prove its assertions. Preserve failures and partial results; never silently promote a planned capability to verified.

Retain exact source revisions and observations in their native owners; the factory stores cross-run routing, summarized receipts and reusable learning, with explicit proof boundaries.

## 6. Concrete work program, in execution order

### Phase 0: Baseline and restore the execution surface

**Owners:** Mastery + Engineering + native CI providers. **Priority:** immediate.
- F00.1: Resolve exact main heads, open pull requests, existing workflows, branch policies, runtime environments, templates and tests for all four Genius repos and both Pro-Code strands.
- F00.2: Run current native tests in clean reproducible environments and gather actual exit codes, dependency locks, versions and artifacts. Do not infer all-green from past badges.
- F00.3: Diagnose Genius-Engineering CI and contract failures through available logs or local reproduction; repair root causes, preserve functional value and re-run relevant jobs.
- F00.4: Inventory current Mastery generator routes (new, synthesize, archetype, lineage), output file sets, duplicate concepts, default paths and overwrite behavior.
- F00.5: Document current-generation baseline: exact input, command, output file tree, failures, unsupported capabilities, elapsed time and reproducible hashes.
- F00.6: Confirm secure provider permissions and private/public boundaries; identify which non-repo services can actually execute.
**Exit:** reproducible baseline package and CI defect ledger; Engineering test status independently observed. Remaining failures are assigned and do not stop independent generator work.

### Phase 1: Define the quality bar and product contract

**Owners:** Mastery (contract), Engineering (outcome), Verification (oracles), Pro_Code (doctrine).
- F01.1: Freeze mission schema v1, user intent/source attribution, correct case/project identity, platform requirements and accepted defaults.
- F01.2: Define typed action/effect ownership and safe external-write semantics. Planned/dry-run vs staged vs applied vs provider-confirmed are separate.
- F01.3: Create per-product acceptance profiles: Python CLI/library, TS/React web, API service, data pipeline, automation/agent, polyglot project.
- F01.4: Define minimal universal anatomy without meaningless folders: README, license (when appropriate), package/build metadata, source, tests, configuration, security policy, contribution/runbooks, CI and release process appropriate to type.
- F01.5: Establish security profiles for public/private, trusted/untrusted input, internet exposure, regulated/private data, dependencies and secrets.
- F01.6: Backwards-compatibility and data migration rules for existing Mastery v1/v2 consumers.
- F01.7: Define a self-contained descendant: it builds/tests from checkout without importing the teacher or relying on a device-specific absolute path.
**Exit:** schema tests, contract examples, upgrade compatibility fixtures, acceptance-matrix tests and no loss of old CLI behavior.

### Phase 2: Fix generator correctness and portability

**Owners:** Mastery.
- F02.1: Replace /root/projects/Genius-Lineage with explicit --dest / --output-root and a safe default based on user-specified workspace or current working directory. All code paths platform-neutral.
- F02.2: Remove generated verified: true without evidence; use mapped/planned, real evidence IDs and a separately measured promotion transition.
- F02.3: Safe slug/path normalization; reject traversal, symlink escape, collisions, prohibited overwrites and inconsistent case-sensitivity. Never follow unsafe directories during regeneration.
- F02.4: Deterministic generation for stable inputs, with stable identifiers and a hash-index manifest; timestamps and run IDs captured separately from deterministic output.
- F02.5: Stage output in a temp worktree; validate before atomic publication or provide an explicit recovery journal where cross-directory atomicity is impossible.
- F02.6: Idempotency for repeated intents, collision detection for changed specs, semantic diff and preview; preserve existing files and user edits by default.
- F02.7: Unify the coherent path through scaffold + role synthesis + domain templates + reference registry while preserving distinct frontends.
- F02.8: Expand tests: portability across platform roots, empty/nonempty target, hidden files, unicode, malicious paths, interrupted writes, stale cache and no-false-verified tests.
**Exit:** generation works under non-root Linux, macOS-compatible paths and Windows path-validation fixtures; all claims stay appropriately mapped; no silent user-data loss.

### Phase 3: Build a real repository compiler

**Owners:** Mastery + Genius-Code + pro-code.
- F03.1: Compile user intent into concrete software requirements, executable acceptance cases and architecture options; retain original words alongside inferred requirements.
- F03.2: Select stack via capabilities, verified local dependencies, target platform, maintenance economics and Tower language boundary; justify decisions.
- F03.3: Add product-specific generation plugins, implemented as source-owning adapters: Python CLI/library; TypeScript web/API; Node automation; data processing; safe optional future profiles.
- F03.4: Emit real entrypoints, package manifests/lockfiles, environment examples, meaningful tests, error handling, configuration loading, logging, standard command scripts and operable README. No pretend integration stubs promoted as ready.
- F03.5: Resolve and document secret/environment requirements without embedding real values; separate offline operation from live provider prerequisites.
- F03.6: Generate appropriate GitHub Actions CI, lint, typecheck, build, unit/contract tests and optional packaging workflow with permissions limited to the task.
- F03.7: Validate compile and execute on an isolated generated checkout, not merely the generator checkout.
- F03.8: Produce a public-safe or private-specific artifact according to the specified visibility; no private instruction/context leakage.
**Exit:** at least two representative language profiles produce independently buildable and runnable functional outputs with clean source ownership.

### Phase 4: Add real work execution and repair

**Owners:** Genius-Engineering + pro-code + target-specific adapters.
- F04.1: Introduce typed executor interface (inspect, edit, build, test, diagnose, repair, integrate, publish, readback) separate from dry-run mission planning.
- F04.2: Convert mission work graph into executable steps with bounded parallelism, dependency validity, safe retries and task-idempotency keys.
- F04.3: Execute actual source modifications with before-hashes, change bounds, atomic local writes where feasible, journaled multi-file recovery and readback.
- F04.4: Preserve the maximal independent-ready frontier when a provider/dependency fails; use retry alternatives and human escalation only for the exact unavailable authority.
- F04.5: Use native compiler/test output and deterministic code intelligence for error localization. A passing policy check without functional gain is not completion.
- F04.6: Add bounded iterative repair: diagnose → minimally reproduce → patch → run impacted suites → full regression → verify, with concrete stop conditions for destructive loops or cost escalation.
- F04.7: Capture exact environment/tool versions, commands, stdout/exit codes, affected files, error trace and recovery result.
- F04.8: Support existing-repository worktrees, minimal branches, non-force commits, non-squash merges, open PR preservation and rollback-friendly patches.
**Exit:** one failure-injected integration mission actually repairs its target source, passes its relevant native tests and resumes without restarting the whole job.

### Phase 5: Verification becomes empirical and product-specific

**Owners:** Genius-Verification + Genius-Engineering + product owner.
- F05.1: Derive falsifiable acceptance tests from each product's user-visible outcomes, not from number of files or badges.
- F05.2: Test pyramid by impact: unit, property/fuzz, integration/contract, E2E, browser/accessibility (when UI exists), security, data migration, concurrency/recovery and performance budgets.
- F05.3: Build negative tests: unsupported feature, failed provider write, repeated idempotency key, corrupt input, missing secret, race, rollback failure, network loss and attempted source/path escape.
- F05.4: Verify claimed function in a clean environment with no teacher source checkout, undisclosed system paths or developer-local state.
- F05.5: Assess supply chain: dependency lock, license inventory, SBOM when relevant, secret scan, static analysis, vulnerability response and source/artifact provenance.
- F05.6: Bind verification receipts to a specified property, oracle, assumptions, tool version, source SHA, environment, coverage limitations and artifacts; track counterevidence.
- F05.7: Implement a release-quality report separating untested, failing, passed in scope, deployed, and provider-readback-verified.
- F05.8: Add regression tests that reject fake capability promotions, counterfeit receipts, false green status and stale revision deployment.
**Exit:** a fresh checkout passes native suites, adversarial checks demonstrate that materially broken builds are rejected, and the status matches reality.

### Phase 6: Native GitHub integration and repository lifecycle

**Owners:** Engineering + authenticated GitHub adapter + Monolith mapping.
- F06.1: Implement repository discover/create/select with exact owner, visibility, naming, default branch, description, topics, license and security policy; verify identities and permissions before writes.
- F06.2: Distinguish GitHub template creation from fork/clone/migrate; template creation starts independent history and is not a means to preserve an existing repo's commits.
- F06.3: Add status-aware branch/PR workflow with minimum branches, version guards, non-force writes, non-squash merge, no blind retry after ambiguous mutations.
- F06.4: Apply repository-native workflows, branch protections/rulesets and security checks proportionate to risk; don't make a broken set of gates block all work.
- F06.5: Read back repository tree, exact head SHA, PR state, actions runs, resulting packages/releases and settings changed.
- F06.6: If a tool cannot write a repository setting, complete all independently authorized code work and preserve the exact provider boundary.
- F06.7: Ensure generated repository contains owner-specific README, actual functional test commands, security documentation, issue/PR templates where useful, CONTRIBUTING, changelog and maintainers without boilerplate bloat.
**Exit:** full GitHub NEW and EVOLVE cycles exercised in controlled target repositories; actual commits and PR/merge receipts verified; no force/squash or secret leak.

### Phase 7: Packaging, deployment and operation

**Owners:** Engineering + product-specific provider adapters.
- F07.1: Add portable build and packaging recipes for selected product profiles, with deterministic lock and artifact digest.
- F07.2: Add environment mapping, secrets-by-reference, provider identity, migration compatibility, rollback and deployment previews.
- F07.3: Support local reproducible execution as a first-class completed result when the user does not request external deployment.
- F07.4: When external deployment is authorized, execute real publish/deploy, record provider-native ID, exact revision, status and address, and independently probe intended user behavior.
- F07.5: Add log/health/metrics traces, error reporting, rate limiting, backup and restore tests as demanded by the product's risk and actual operating model.
- F07.6: Generate an operator runbook: start/stop/configure/test/update/restore/troubleshoot, owners, reasonable cost estimates and access boundaries.
- F07.7: Artifact attestations and SBOM/provenance where appropriate; choose the current SLSA spec and NIST SSDF framework as reference standards, and claim only the actual tested track/level.
**Exit:** an actual chosen product is delivered with reproducible local operation and, when asked and authorized, deployment readback and tested rollback/recovery.

### Phase 8: Cross-family integration and three real acceptance missions

**Owners:** Mastery (orchestrates), Engineering (executes), Verification (independent challenge), native product owners.
- F08.1: GREENFIELD PYTHON: from a functional CLI objective, generate a Python package with persistent state or real transformations, tests, packaging, CI and exact runnable command; run it in fresh checkout and exercise success plus failure/recovery.
- F08.2: GREENFIELD TYPESCRIPT: generate a small but real TypeScript/React + API application with meaningful request/response and error behavior, build, contract/E2E tests, configuration and independent execution.
- F08.3: BROWNFIELD REPAIR: target a controlled pre-existing repository with deliberately broken behavior, uncommitted custom files and historical changes. Restore behavior without losing user data, preserve history, test and verify diff.
- F08.4: ADDITIONAL COMPLEX PROFILE: exercise a real workflow/agent or document-processing repo through at least one authorized external boundary, idempotent retries, observable results and provenance. Keep sensitive legal matter data out of public examples.
- F08.5: Complete each mission from objective → source → modifications → independent native tests → integration → provider readback → user-operable delivery. Do not accept synthetic schema-only completion.
- F08.6: Compare time, cost, number of manual interventions, defect recurrence and regression to the baseline; retain beneficial findings in Mastery and Engineering.
**Exit:** at least three materially different real repository missions, including greenfield and brownfield, fully pass acceptance criteria with independently inspectable code and receipts.

### Phase 9: Self-improving foundry and continual stewardship

**Owners:** Mastery + all evidence-owning specialists.
- F09.1: Capture recurring defects and repairs as versioned regression cases and validated template/engine improvements.
- F09.2: Promote learned capabilities only when a descendant demonstrates reproducible behavior and a second different case transfers it successfully.
- F09.3: Compare new generation and repair outcomes against known-good baselines; retain stronger performers and revert only the affected change when genuinely necessary.
- F09.4: Reconcile upstream dependency/framework/security updates with reproducible tests; no blind blanket upgrades.
- F09.5: Track quality metrics: functional-pass rate, defect escape, time-to-first-running-product, revision/receipt fidelity, full-cycle success, cost, failed-repair loops, source leakage and user correction rate.
- F09.6: Preserve one authoritative current progress ledger plus historical immutable receipts; do not create redundant plan/status hierarchies.
**Exit:** one verified learning cycle makes a subsequent repository build measurably better than the baseline, without erasing contradictory evidence or old working code.

### Phase 10: Productize the builder itself

**Owners:** Mastery + Engineering + Pro_Code / pro-code.
- F10.1: Single clear README and operator entrypoint; commands for new, inspect, improve, repair, verify, publish and resume.
- F10.2: CLI and documented library API first, optional visual control surface integrated into existing pro-code tooling when functional value is established. Do not create a decorative dashboard instead of shipping the engine.
- F10.3: Versioned user guide, architecture/adapter references, product profiles, security policy, examples, deployment and developer contribution guide.
- F10.4: Reproducible installer and self-test across selected supported environments; no per-device absolute paths or hidden credentials.
- F10.5: Create stable release notes, semantic version and distributable artifact with tested upgrade/migration.
- F10.6: Teach-through-use documentation that explains how a generated repository can stand on its own and how to improve it safely.
**Exit:** a new authorized engineer or agent can supply a mission, run the foundry using the documented entrypoint and reproduce a verified output without custom founder knowledge.

## 7. Suggested CLI surface (design target, not implemented)

The public command family should be integrated under the existing genius program, with stable backwards-compatible aliases for existing commands:

- genius repo new --mission mission.yaml --dest ./workspace --preview
- genius repo new --mission mission.yaml --dest ./workspace --execute
- genius repo inspect --repo ./existing-repo
- genius repo evolve --repo ./existing-repo --mission mission.yaml --preview
- genius repo evolve --repo ./existing-repo --mission mission.yaml --execute
- genius repo repair --repo ./existing-repo --failure failure.yaml
- genius repo verify --repo ./target --profile profile.yaml
- genius repo publish --repo ./target --provider github --visibility private
- genius repo release --repo ./target --environment staging
- genius repo resume --receipt ./receipts/mission-id.json
- genius repo status --mission-id mission-id --json

A human command should accept plain-language intent as well as a file. The system creates/updates the typed mission object internally. The --execute and external-action flags must match the actual operation and authorized provider scope; an arbitrary text field cannot mint human authority. No destructive actions on a repository merely because the mission includes the word 'repair.'

The Engineering package gets reusable evaluate/execute/resume operations and adapter interfaces. It must not launch an unrelated alternative set of repository generation commands.

## 8. Technical design / module decomposition

**Mastery modules proposed:**
- repo_factory/mission.py: parse intent, recover sources, normalize objective and revision.
- repo_factory/spec.py: schema parsing/version migrations/constraints.
- repo_factory/architect.py: product profile, stack selection, architecture reasoning.
- repo_factory/generate.py: compose existing scaffold, role synthesis and domain forge.
- repo_factory/worktree.py: safe portable target paths, staging, diff and preservation.
- repo_factory/manifest.py: deterministic file inventory/digest and provenance.
- repo_factory/adapters/: typed plugin registry, no provider-specific secrets in core.
- repo_factory/cli.py: subcommands routed through the existing genius CLI.

**Engineering modules proposed:**
- executor.py: actual typed execution of work units, with task-bound state.
- repair.py: observed-error diagnosis and bounded follow-on patching.
- resume.py: checkpoint replay/idempotency/failed-step recovery.
- provider_registry.py: calls provider-native GitHub/CI/deploy interfaces through constrained adapters.
- completion.py or existing kernel.py extension: outcome acceptance and independent readback, keeping current contracts valid.

**Shared schemas:** mission, operation, artifact, evidence, provider action, verification, deployment and continuation. Put each canonical type in one owner and import through versioned package contracts; no two rival mission schemas silently drifting.

**Threat boundaries:** user input, repository file text, untrusted issue/PR bodies, model outputs, third-party templates, action run summaries and secrets are different trust classes. Treat retrieved content as data rather than execution authority. Isolate code execution from privileged GitHub/deploy tokens; no untrusted PR job receives production secrets.

## 9. Quality and release acceptance matrix

| Dimension | Non-negotiable proof before claiming complete |
|---|---|
| Intent | Each required user outcome maps to a testable deliverable, with original wording traceable |
| Source | Existing code, tests, configuration, identity, history and uncommitted changes preserved or explicitly accounted for |
| Independence | Clean checkout in isolated environment builds/executes without hidden teacher dependencies |
| Function | At least one real representative task succeeds and an expected error path is exercised |
| Correctness | Applicable lint/typecheck, unit, contract, integration and product-profile E2E tests pass on exact source revision |
| Security | No committed secrets; untrusted content cannot grant authority or escape designated workspaces; dependency/source risks assessed |
| CI | Real pipeline green on the exact intended commit for applicable checks; failures not concealed |
| Git | Non-force, no squash, identity and intended history preserved; PR/merge provider readback where invoked |
| Supply chain | Artifact digest, dependency information, reproducible build identity and appropriate attestation tied to exact revision |
| Operation | Start/stop/configure/health/error/recovery documented and validated in supported environment |
| Deployment | If requested: actual provider job and URL/revision readback, live functional probe and rollback where appropriate |
| Evidence | Accurate claims and counterevidence, receipts with exact owner, action, status, date and source SHA |
| Usability | README explains purpose, setup, commands, architecture, real supported capabilities and limits; internal links resolve |
| Continuity | A second run can resume/repair from saved state without redoing unrelated work |

**An outcome-specific requirement can be not-applicable** with rationale. No generic rule forces a CLI package to have Kubernetes, a frontend, a database, or a 40-folder skeleton. Conversely, a browser product cannot skip actual UI/browser E2E evidence just because unit tests pass.

## 10. Nonfunctional targets (initial planning targets to calibrate by benchmarks)

- **Correctness:** 100% of mandatory acceptance cases pass at a fixed release revision; no false success status in injected failure tests.
- **Portability:** no hardcoded user/machine paths; demonstrate at least two different filesystem roots and a clean non-root runner. Test OS-specific path semantics with fixtures; claim native support only where exercised.
- **Repeatability:** same normalized specification and pinned toolchain yield semantically identical source; intentional volatile timestamps go in receipts, not generated code.
- **Data preservation:** no silent overwrite in EVOLVE/REPAIR; a nonempty target requires a versioned diff and change-application contract.
- **Privacy:** zero private secrets or protected corpus content crossing into public generated repos in automated leakage fixtures.
- **Recovery:** every external action is idempotent or has a reconciliation read before retry; interrupted local multi-file operations are diagnosable and recoverable.
- **Latency/cost:** record baseline p50/p95 per product profile, optimize only against measured real use rather than invented service-level promises.
- **Maintenance:** no mandatory cross-repository submodule or teacher checkout for a generated child; independent package operation is required.

## 11. Engineering decisions and tradeoffs

**Use existing CLI versus create a new platform:** extend Genius-Mastery. It already has creator functions, schema/CLI/tests and a family index; another repository would introduce parallel ownership and divergence.

**Templates versus generative code:** use tested, domain-appropriate base templates and source-owned reference patterns plus synthesis; generation may expand real source based on objective, but cannot call filler code 'implemented.' Preserve a manual quality path where an unsupported domain needs concrete engineering.

**Build locally versus GitHub:** first prove isolated local creation; GitHub integration follows with exact provider identity and readback. When GitHub is unavailable, local build/verification continues.

**One huge framework versus product profiles:** a small common lifecycle plus strong specialized native implementations yields reusable correctness without forcing irrelevant components onto every repository.

**Safety checks versus obstruction:** tests and permissions are proportional to actual side effects, truth and risk. They are pit stops that direct recovery and strong progress, not perpetual approvals that replace function.

**Automated release versus user authority:** local files/CI and reversible code changes can advance within authorized scope; external visibility, billing, credential and irreversible release effects require actual applicable authority. The current user objective always controls whether deployment is in scope.

## 12. Security and external standards

Base security work on NIST SSDF SP 800-218: Prepare, Protect, Produce well-secured software and Respond to vulnerabilities. Build provenance and supply-chain verification should consult **current SLSA version 1.2**, not retired v1.1, and only claim demonstrated controls. GitHub official repository-template semantics, reusable-workflow/OIDC restrictions and artifact attestations inform GitHub/provider adapters.

Official references:
- NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
- Current SLSA specification: https://slsa.dev/spec/v1.2/
- GitHub templates: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template
- GitHub artifact attestations: https://docs.github.com/en/actions/concepts/security/artifact-attestations
- GitHub OIDC/reusable workflows: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows

These are engineering references. The existence of links is not compliance, a security certification, or evidence that a provider is connected.

## 13. Dependencies, parallelism and the critical path

**Must precede real provider delivery:** Phase 0 exact source/CI baseline → Phase 1 mission and evidence contract → Phase 2 safe portable writes → Phase 3 one real native product profile → Phase 4 executor/repair → Phase 5 native verification → Phase 6 provider integration → Phase 7 deployment/operations → Phase 8 empirical E2E acceptance.

**Can proceed in parallel once contracts are versioned:**
- Product-profile implementations (Python vs TypeScript).
- Verification/property test harness and security fixtures.
- GitHub provider adapter and isolated local worktree harness.
- README/runbook templates and native operator usability.
- Genius-Engineering CI repair and Mastery forge correctness repair.
- Architecture test fixtures and calibration metrics.

**Must remain conditional:** external production release, public visibility, purchased resources, adding secrets, or cross-account connections. A blocked external provider is not permission to stop independent code, tests, documentation and local delivery.

## 14. Milestones and approximate effort planning

These are **engineering estimates, not a calendar promise**. Duration depends on the number of engineers, runner access, dependency issues, cloud credentials, and acceptance profile complexity.

| Milestone | Scope | Suggested proof |
|---|---|---|
| M0 Baseline cured | Phases 0–1 | Exact-head repo inventory, green or diagnosed CI, mission schema, compatibility tests |
| M1 Honest portable generator | Phase 2 | Hardened new/synth/forge, non-root and overwrite tests, no premature verification |
| M2 Real independent product | Phase 3 | Fresh-checkout runnable Python or TypeScript product, native tests and meaningful behavior |
| M3 Full execution/repair | Phases 4–5 | Target changes, injected failure recovery, actual test/execution receipts |
| M4 GitHub-native factory | Phase 6 | Repo creation/evolution, non-force/PR readback and accurate CI |
| M5 Production-quality release | Phase 7 | Local packaged product plus approved real provider operation, health/rollback proof |
| M6 Independent portfolio | Phase 8 | Three distinct end-to-end missions, including brownfield preservation |
| M7 Compounding factory | Phases 9–10 | Proven learned improvement, stable packaged release, docs and repeatability |

Initial staffing hypothesis: a focused owner for Mastery/architecture, a focused Engineering/executor owner, a Verification/security owner and a product-specific frontend/backend owner where necessary. The same person or agent may fill several roles without inventing an organizational approval bureaucracy. Work effort should be measured from actual runs and revised after the baseline.

## 15. Verification challenge suite / adversarial cases

The final system must demonstrate these non-happy-path outcomes:

1. Generator invoked from a writable non-root directory with no /root directory.
2. Destination includes existing human edits; preservation and diff rather than overwrite.
3. Symlink points outside workspace; no read/write escape.
4. Same mission submitted twice with identical idempotency key; no duplicate effects.
5. Same key replayed with different mission; explicit conflict.
6. Generated target compiles but cannot perform requested operation; marked incomplete.
7. Generated YAML says verified but has no receipt; rejected as unverified.
8. Failed dependency install; lockfile and error recovered without false passing status.
9. Network/provider loses response after a write; discover and reconcile existing object before retry.
10. CI green for older SHA while new SHA fails; do not promote old evidence.
11. Branch has unrelated concurrent update; detect version mismatch, preserve both changes.
12. Python project fails in clean environment because of teacher-only import; catch.
13. TS frontend renders but API workflow fails; integration/E2E catches.
14. User wants private repo; generated public-safe docs cannot expose private doctrine, child details or tokens.
15. Generated source demands unsafe deployment credentials in untrusted test; fail safely without losing independent work.
16. Interrupted multi-file write; recovery journal restores coherent source.
17. Wrong platform/toolchain assumption; reroute to viable supported implementation without changing objective.
18. Readme link and startup command audits detect malformed Markdown or invalid CLI flags.
19. Adversarial untrusted repository instructions attempt to override Operator; treated as data.
20. Deployment provider says started but health probe fails; state remains deployed_attempted/failed, not operationally_verified.
21. Release succeeds but rollback test fails; release declared with risk and uncompleted required criterion.
22. Broad master objective contains several independent ready tasks; executor must not shrink to a token demo and call mission done.
23. New templates accidentally discard pre-existing tests/license/history; negative regression must fail.
24. Generated descendant can create and verify an improved descendant without hidden teacher checkout in supported scope; test as late-stage transfer, not an early false claim.

## 16. Definition of done for the whole factory

The entire factory is **not done** until all of these are established with exact-head, inspectable proof:

- The builder accepts a real user mission without requiring expert hand-editing of dozens of hidden schema fields.
- NEW, EVOLVE and REPAIR are operational, not just documented.
- Generated repositories have meaningful code that runs, a fitting architecture, reproducible dependencies, tests, security and useful README/runbook.
- At least three divergent mission types pass clean-checkout execution and negative tests; one is brownfield and one exercises authorized provider integration.
- Required CI, build artifacts and provider releases are read back at exact revisions where applicable.
- Partial failure recovery works, retains user history and doesn't issue false success.
- Generated capability state starts as mapped/implemented and is promoted to verified only with specific evidence.
- The factory improves from observed defect/transfer results and does not need one machine's directories or the teacher repository to run its children.
- A second authorized operator can reproduce a complete supported build from documented commands.
- User explicitly receives location, commands, proof, limitations and the next frontier, rather than another planning handoff.

## 17. First implementation tranche to execute once plan becomes active

Deliver a **coherent set of concrete code fixes** rather than creating more administration:

1. Reproduce Mastery baseline generation and Engineering failing CI on actual target toolchains.
2. Repair Mastery forge destination hardcoding and premature verified flags with focused regression tests.
3. Add one honest versioned mission/output contract and clean worktree/diff implementation.
4. Generate one genuine, runnable standalone product in an isolated temporary directory and test it under the same toolchain as a real descendant.
5. Wire Genius-Engineering to execute and verify that mission, not merely read its finished checklist.
6. Capture command and GitHub provider receipts; continue to next phase without requesting new authorization for routine local source work.

**The next cycle begins with code and proof, not a competing governance system.**

## 18. Source provenance and status

This plan was written after reading the live GitHub main-branch sources in Genius-Mastery, Genius-Engineering, Genius-Code, Genius-Verification and the paired Pro-Code family. In particular, it draws from Mastery README/scaffold/synthesize/forge/CLI/ROADMAP/frontier/AGENTS, Engineering README/kernel/CLI/CI/engineering doctrine, and current GitHub Actions summaries. Current observed CI evidence was recorded October 30, 2026 HST.

**Planned:** the repository factory lifecycle, execution adapters, new mission schema, product profiles and E2E trials described here.  
**Already implemented:** preexisting generation/synthesis, domain forge, some code/verification tools and engineering outcome evaluation, each within its tested native scope.  
**Not claimed:** that this plan has created a new runnable child repository, fixed failing CI, deployed new infrastructure or completed the full production cycle.

This is the canonical plan to implement those outcomes, not an excuse to keep planning forever.
