# Counterevidence: ev-receipt-env-gap-001

| Field | Value |
|-------|-------|
| Claim | `kernel-counterevidence-001` |
| Kind | counterevidence |
| Result | **fail_partial** |
| Timestamp | 2026-08-29T21:46:13Z |

Buildkite build 2 on Genius-Mastery / Genius-Code / Genius-Verification emitted `buildkite-verified-receipt.json` with `status: PASS` but `commit`, `branch`, `build_id`, `build_number`, and `pipeline` were **null**.

Cause: Docker plugin isolated the container from `BUILDKITE_*` unless `propagate-environment: true`.

This does not overturn the job PASS. It does overturn any claim that the *artifact JSON alone* identified the run. Authoritative identity remains the Buildkite API build record.

Remediation committed: `propagate-environment: true` on all Genius Docker steps.
