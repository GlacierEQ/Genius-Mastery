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

The family bootstrap is `.buildkite/bootstrap-genius.sh`. It creates or reconciles the three core Genius pipelines, installs the repository-upload step, attempts GitHub webhook creation, and can trigger verification builds.
