# Genius Buildkite

The Genius family uses a two-layer Buildkite architecture.

## Control plane

`GlacierEQ/apex-control-plane/scripts/reconcile_genius_buildkite.py` is authoritative for the family. It:

1. reconciles `genius-mastery`, `genius-code`, and `genius-verification`;
2. reuses the proven Buildkite cluster and `macos-self` queue;
3. verifies repository, cluster, branch, provider, and superseded-build settings by API readback;
4. resolves each exact GitHub `main` SHA;
5. reuses a healthy exact-head Buildkite projection or triggers a replacement build;
6. waits for the referenced Buildkite build to reach terminal PASS;
7. verifies the exact GitHub `buildkite/<slug>` success projection points to that same build;
8. emits a credential-free family reconciliation receipt that is hashed into the APEX terminal receipt.

Dispatch is not completion.

## Repository pipelines

Each Genius repository owns only its domain execution in `.buildkite/pipeline.yml`.

The Buildkite-side upload step performs source identity checks plus supported parse-warning/secret rejection before loading that file. Repository pipelines should not recreate that dynamic-upload gate.

The current Mastery repository pipeline executes natively on the `macos-self` queue in an ephemeral Python virtual environment. It deliberately does not require a Docker engine on the macOS runner.

Repository CI proves package installation, compilation, contract validation, regression tests, synthesis, mission intelligence, family analysis, runtime discovery, calibration, graph rebuild, evidence-vector integrity, and executable 1.0 closure. Terminal family reconciliation remains the responsibility of the APEX control plane and must be bound to the exact GitHub head before it is treated as external verification.

## Current routing

| Repository | Pipeline | Role | Queue |
|---|---|---|---|
| `GlacierEQ/Genius-Mastery` | `genius-mastery` | mastery kernel | `macos-self` |
| `GlacierEQ/Genius-Code` | `genius-code` | code domain | `macos-self` |
| `GlacierEQ/Genius-Verification` | `genius-verification` | verification domain | `macos-self` |

`oracle-arm64` remains an independent-runner target, not a production Genius evidence queue, until live Buildkite proof exists.

## Fallback bootstrap

From a `Genius-Mastery` checkout:

```sh
bk auth login --org casey-1
bash .buildkite/bootstrap-genius.sh casey-1
```

This is a recovery/provisioning path. The APEX reconciler remains authoritative for terminal verification.

## Buildkite AI control

Official remote MCP endpoint:

```text
https://mcp.buildkite.com/mcp
```

For CI/CD use `user`, `pipelines`, and `builds`; add `logs`, `tests`, and `annotations` for failure analysis.
