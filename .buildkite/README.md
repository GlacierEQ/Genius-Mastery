# Genius Buildkite

The core Genius repositories are designed to run repository-owned Buildkite pipelines from `.buildkite/pipeline.yml`.

## One-command family bootstrap

From a checkout of `Genius-Mastery`:

```sh
bk auth login --org <org-slug>
bash .buildkite/bootstrap-genius.sh <org-slug>
```

If the Buildkite organization requires an explicit cluster:

```sh
bash .buildkite/bootstrap-genius.sh <org-slug> <cluster-name>
```

Set `TRIGGER_BUILDS=0` to reconcile pipeline configuration without triggering builds.

The bootstrap reconciles:

- `Genius-Mastery` -> `genius-mastery`
- `Genius-Code` -> `genius-code`
- `Genius-Verification` -> `genius-verification`

For every pipeline it:

1. creates the pipeline if absent;
2. points it at the GlacierEQ GitHub repository;
3. sets `main` as the default branch;
4. installs a Buildkite-side pipeline-upload step so the repository remains the source of CI truth;
5. enables commit status publishing and pull-request builds;
6. attempts GitHub webhook creation;
7. reads the pipeline back;
8. triggers a verification build unless `TRIGGER_BUILDS=0`.

## AI control

Buildkite's official remote MCP endpoint is:

```text
https://mcp.buildkite.com/mcp
```

For CI/CD control, enable the `user`, `pipelines`, and `builds` toolsets. Add `logs`, `tests`, and `annotations` for failure analysis.

## Verification

```sh
bk pipeline validate --file .buildkite/pipeline.yml
bk pipeline view <org-slug>/genius-mastery --json
bk build view --pipeline <org-slug>/genius-mastery --summary
```

A committed pipeline file is configuration, not proof of execution. Completion requires a live Buildkite build result.
