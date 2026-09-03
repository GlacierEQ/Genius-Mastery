# AGENTS.md — Genius-Mastery

## Buildkite execution contract

Expected Buildkite pipeline slug: `genius-mastery`.

The authoritative family control plane is:

`GlacierEQ/apex-control-plane/scripts/reconcile_genius_buildkite.py`

It owns Buildkite pipeline reconciliation, webhook/provider settings, exact GitHub `main` head resolution, child-build dispatch/reuse, terminal Buildkite readback, exact-head GitHub status projection verification, and the family reconciliation receipt.

This repository owns the Mastery-domain execution body in `.buildkite/pipeline.yml`. Do not duplicate the control-plane upload/reconciliation logic inside the repository pipeline.

### Current verified routing

- organization: `casey-1`
- queue: `macos-self`
- pipeline: `genius-mastery`
- source: `GlacierEQ/Genius-Mastery`
- pipeline file: `.buildkite/pipeline.yml`

Do not move production evidence to `oracle-arm64` until that queue has independent live Buildkite proof.

### Security and evidence invariants

- Never treat committed YAML or build dispatch as success.
- Buildkite's base upload step owns YAML parse-warning and secret rejection.
- Containerized verification receives only explicitly required nonsecret Buildkite identity variables.
- Do not restore broad `propagate-environment: true`.
- The terminal receipt runs on the trusted host, verifies exact checkout/pipeline identity, downloads required test artifacts, and emits a SHA-256 sidecar.
- Completion requires terminal child PASS plus the matching `buildkite/genius-mastery` success projection on the exact GitHub commit.

When Buildkite tools are available, prefer the official remote MCP server at `https://mcp.buildkite.com/mcp` and inspect live builds/logs rather than inferring state.

Useful local commands:

```sh
bk pipeline validate --file .buildkite/pipeline.yml
bk pipeline view casey-1/genius-mastery --json
bk build view --pipeline casey-1/genius-mastery --summary
```

The local `.buildkite/bootstrap-genius.sh` is fallback provisioning only. It does not supersede APEX terminal verification.


## Progress kernel contract

Progress is a first-class kernel behavior.

When a task requests building, fixing, continuing, strengthening, or advancing work:

1. recover current durable state before mutation;
2. inspect applicable tools, connectors, files, repositories, evidence, and receipts;
3. rank bottlenecks and leverage rather than selecting the easiest visible task;
4. execute the strongest coherent action available;
5. persist the gain in the destination of record;
6. test and read back that destination;
7. bind verification claims to inspectable receipts;
8. retain counterevidence and feed the resulting state into the next cycle.

The canonical default stack is:

`PROGRESS + CONTINUE + TOOL-FIRST + NEXT BEST ACTION + MAXIMUM ADVANCE + EXECUTE + DURABLE + TEST + READBACK + RECEIPTS + PRESERVE GAINS`

Do not convert a progress contract into a success claim. Planned, executed, observed, and verified are distinct states.

The machine-readable implementation lives in `src/genius/progress.py`; the command vocabulary lives in `src/genius/prompt_codes.py`; the human contract lives in `docs/PROMPT_CODES_AND_PROGRESS_PROTOCOL.md`.


## Instruction engineering contract

Prompt prose is one projection of the runtime, not the runtime itself.

For instruction/prompt/agent-kernel work:

1. preserve the semantic outcome and hard constraints before editing wording;
2. separate authority, trusted context, untrusted retrieved data, tools, examples, output, and verification;
3. state stable instructions once and remove ornamental repetition;
4. prefer retrieval/progressive disclosure over unconditional context injection;
5. preserve `available != called != succeeded != verified` for every tool path;
6. request observable assumptions, evidence, checks, decision points, and conclusions rather than private reasoning traces;
7. compile/tune for the target model family instead of blindly carrying forward legacy prompt stacks;
8. use representative behavioral evals to decide whether a prompt change is actually better;
9. repair retrieval, tool metadata, state, or validation defects at their owning layer instead of compensating with more system-prompt prose.

Machine implementation: `src/genius/instruction_engineering.py`.
Contract schema: `schemas/instruction-contract.schema.json`.
Human doctrine: `docs/INSTRUCTION_ENGINEERING.md`.
CLI: `genius instruct`.
