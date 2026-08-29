# Changelog

All notable changes to Genius-Mastery are documented here.

## [0.2.0] — 2026-08-29

### Added
- Schema v2 identity contract (`GENIUS.yaml`)
- Claim, evidence, source, challenge, composition JSON Schemas
- Mastery vector model (no single scalar score)
- Local `tools/validate.py` and `tools/doctor.py`
- Evidence ledger conventions + counterevidence support
- Family index scaffold (`family/INDEX.json`)
- Composition protocol (`interfaces/COMPOSITION.yaml`)
- Reusable CI workflow stubs
- Source registry seed from high-authority library

### Changed
- Unified identity to hyphenated `Genius-{purpose}` only (no colon-form dual identity)

### Notes
- This is a kernel seed. Domain evidence and full migration engine are subsequent work.
