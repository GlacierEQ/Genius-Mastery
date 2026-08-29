# AGENTS.md — Genius-Mastery

## Buildkite control surface

This repository is the family control point for Genius CI.

When Buildkite tools are available, prefer Buildkite's official remote MCP server:

- Full access: https://mcp.buildkite.com/mcp
- CI/CD toolsets: user, pipelines, builds
- Debugging toolsets: user, builds, logs, tests, annotations

Do not infer CI success from the presence of `.buildkite/pipeline.yml`. Read the live Buildkite pipeline/build state and inspect failed jobs/logs before claiming success.

Expected Buildkite pipeline slug: `genius-mastery`.

## Local Buildkite CLI

Validate this repository's pipeline:

```sh
bk pipeline validate --file .buildkite/pipeline.yml
```

Inspect the live pipeline/build:

```sh
bk pipeline view genius-mastery --json
bk build view --pipeline genius-mastery --summary
```

The authoritative estate reconciler is `GlacierEQ/apex-control-plane/scripts/reconcile_genius_buildkite.py`. It performs API-level create/update, exact-SHA build dispatch, webhook reconciliation, readback, and receipt emission for all three core Genius pipelines.

The local `.buildkite/bootstrap-genius.sh` is a CLI fallback when the APEX control-plane path is unavailable.
