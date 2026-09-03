# Prompt Codes + Progress Protocol

## Purpose

Genius-Mastery treats concise prompt codes as a **command vocabulary** and treats `PROGRESS` as an **execution-orchestration contract**.

The goal is not prettier prompting. The goal is to reduce a recurring failure mode: analysis that does not change durable state.

## Core law

```text
CURRENT STATE
→ RECOVER
→ PRIORITIZE
→ EXECUTE
→ PERSIST
→ VERIFY
→ COMPOUND
↺
```

A progress cycle is successful only when the claimed post-state is supported by readback and receipts. Planning, execution, observation, and verification are distinct states.

## Default PROGRESS stack

```text
PROGRESS
+ CONTINUE
+ TOOL-FIRST
+ NEXT BEST ACTION
+ MAXIMUM ADVANCE
+ EXECUTE
+ DURABLE
+ TEST
+ READBACK
+ RECEIPTS
+ PRESERVE GAINS
```

### Semantics

- **PROGRESS** — convert current state into a measurably stronger verified state.
- **CONTINUE** — recover the last valid state rather than restarting.
- **TOOL-FIRST** — inspect applicable tools, connectors, files, repositories, and live state before guessing.
- **NEXT BEST ACTION** — select the highest-value executable move from current state.
- **MAXIMUM ADVANCE** — advance the strongest coherent reversible increment, not a token minimum.
- **EXECUTE** — perform the action instead of merely describing it.
- **DURABLE** — persist the gain in the appropriate system of record.
- **TEST** — validate behavior at the correct layer.
- **READBACK** — inspect the resulting destination state after mutation.
- **RECEIPTS** — bind success claims to inspectable evidence.
- **PRESERVE GAINS** — do not destroy validated capability unless replacement is demonstrably stronger.

## Truth-state contract

The protocol enforces four boundaries:

1. **planned != executed**
2. **executed != observed**
3. **observed != verified**
4. **verified requires receipts**

Counterevidence remains part of state and is never erased to manufacture confidence.

## Prompt-code syntax

Long form:

```text
FIRST PRINCIPLES + SYSTEMS THINKING + RED TEAM: Analyze this architecture.
```

Compact form:

```text
TOOL-FIRST / CONTINUE / BUILD / TEST / READBACK: Fix it.
```

Codes are composable. Order is preserved and duplicates collapse.

`CHAIN OF THOUGHT` is accepted as a compatibility alias for `REASONING SUMMARY`, which requests assumptions, evidence, checks, decision points, and conclusions without requiring private reasoning traces.

## Code families

The machine-readable registry in `src/genius/prompt_codes.py` is authoritative.

### Explanation
`ELI5`, `TLDR`, `DEEP DIVE`, `FIRST PRINCIPLES`, `STEP-BY-STEP`, `MENTAL MODEL`

### Reasoning
`REASONING SUMMARY`, `MULTI-PERSPECTIVE`, `SOCRATIC MODE`, `PRE-MORTEM`, `POST-MORTEM`, `SWOT`, `TRADEOFFS`, `COUNTERARGUE`, `STEELMAN`, `RED TEAM`, `DEVIL'S ADVOCATE`, `SECOND-ORDER`, `SYSTEMS THINKING`

### Quality / evidence
`VERIFY`, `SOURCE-FIRST`, `FACT / INFERENCE / HYPOTHESIS`, `EVIDENCE MATRIX`, `EVAL-SELF`, `CONTRADICTION CHECK`, `EDGE CASES`, `CONFIDENCE`, `ASSUMPTIONS`

### Execution
`EXECUTE`, `TOOL-FIRST`, `BUILD`, `FIX`, `CONTINUE`, `MAXIMUM ADVANCE`, `PRODUCTION-GRADE`, `READBACK`, `TEST`, `SHIP`

### Strategy
`PRIORITIZE`, `80/20`, `LEVERAGE`, `BOTTLENECK`, `NEXT BEST ACTION`, `DECISION MATRIX`, `SCENARIO PLAN`, `WAR GAME`

### Engineering
`ARCHITECT`, `CODE REVIEW`, `DEBUG`, `SECURITY REVIEW`, `PERFORMANCE`, `REFACTOR`, `INTEGRATE`, `HARDEN`, `BENCHMARK`

### Style
`HUMANIZE`, `JARGONIZE`, `EXECUTIVE`, `TECHNICAL`, `NO-FLUFF`, `DENSE`, `TEACH`

### Output
`TABLE`, `CHECKLIST`, `PLAYBOOK`, `BLUEPRINT`, `MATRIX`, `TIMELINE`, `TREE`, `ONE-PAGER`

### Modifiers
`FULL FIELD`, `RANKED`, `NO ASSUMPTIONS`, `PRESERVE GAINS`, `COMPOSE`, `DURABLE`, `RECEIPTS`, `MAXIMUM`

## CLI

List the registry:

```bash
genius codes
genius codes --category execution
genius codes --category orchestration
```

Build a progress contract against the current repository:

```bash
genius progress . \
  --mission "Convert the strongest bottleneck into verified capability"
```

Add codes:

```bash
genius progress . \
  --mission "Strengthen the current system" \
  --code "RED TEAM" \
  --code "EVAL-SELF"
```

Emit machine-readable state:

```bash
genius progress . \
  --mission "Strengthen the current system" \
  --json
```

The progress engine reads `capabilities/GRAPH.yaml`, reuses `mission-intelligence-v1` ranking, and embeds the existing mission-aware operating-loop record. If no graph exists, the next action becomes recovery rather than invented implementation work.

## Integration rule for agents

When the operator asks to continue, build, fix, strengthen, harden, improve, or make progress:

1. inspect actual state;
2. retrieve relevant prior context and durable evidence;
3. run mission-aware prioritization;
4. execute the strongest coherent action available;
5. write the result to the correct durable destination;
6. test;
7. read back;
8. report receipts and counterevidence;
9. begin the next cycle from that stronger state.

Do not stop at a proposal when the requested action is executable with available tools.

## Failure modes this protocol is designed to prevent

- restarting work instead of recovering it;
- asking for facts already available through tools or durable context;
- choosing the easiest action instead of the highest-leverage action;
- producing documentation while leaving the implementation unchanged;
- treating a file write as proof the system works;
- claiming success without readback;
- losing verified gains during refactors;
- hiding counterevidence;
- repeatedly analyzing the same bottleneck without changing state.

## Architectural relationship

`prompt_codes.py` defines **how a task should be attacked**.

`intelligence.py` ranks **what should be attacked next**.

`operating_loop.py` preserves **mission → context → options → impact → action → outcome**.

`progress.py` composes them into **state advancement with truth boundaries**.

That composition is the intended kernel behavior.
