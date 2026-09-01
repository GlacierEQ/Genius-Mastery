# Counterevidence — Buildkite #129 projection gap

- **Evidence ID:** `ev-bk-mastery-129-projection-gap`
- **Observed:** 2026-08-31T08:15:25Z
- **Related build:** Buildkite `genius-mastery #129`
- **Recorded commit:** `815a2a65cd47534f461a8ec705826b4155649d6c`

## Contradiction

GitHub projected Buildkite #129 as successful for commit `815a2a65...`. Direct source readback of that exact commit subsequently showed `src/genius/cli.py` defined `cmd_analyze` and `cmd_family` but did not import `yaml`, `analyze_capability_graph`, `capability_intelligence_report`, `analyze_family`, or `family_report`.

Those commands therefore could not have executed successfully from that exact source. The green projection is insufficient proof that the repository verification commands actually ran.

## Required correction

- Retain Build #129 as routing/projection evidence only.
- Do not use it to promote mission-intelligence or family-composition capability claims.
- Repair CLI imports.
- Require a later exact-head pipeline to execute the regression suite and CLI smokes and emit an exact-source receipt artifact after those commands complete.
