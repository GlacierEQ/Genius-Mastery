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
