# Genius-Mastery

[![Buildkite](https://badge.buildkite.com/53fcc89c70c0eb2508067aa8108bf0f15d27da721a94f8c63c.svg)](https://buildkite.com/casey-1/genius-mastery)

**Family control kernel** for the Genius repository ecosystem.

Identity rule (no exceptions):

```text
Genius-{purpose}
```

## Install (CLI)

```bash
git clone https://github.com/GlacierEQ/Genius-Mastery.git
cd Genius-Mastery
pip install -e .

genius --version
genius name "Distributed Systems"   # → Genius-Distributed-Systems
genius validate .
genius doctor .
genius new Performance --dest /tmp  # scaffolds Genius-Performance
```

Requires Python ≥ 3.10 and PyYAML.

## Doctrine

Mastery, not skills. Aspirations may be enormous; verified capability must point to evidence.

```text
MAP → RESEARCH → MODEL → BUILD → BREAK → MEASURE → VERIFY → OPERATE → EXPLAIN → SYNTHESIZE → PROVE → EXPAND ↺
```

## Family (live)

| Repository | URL |
|---|---|
| Genius-Mastery | https://github.com/GlacierEQ/Genius-Mastery |
| Genius-Code | https://github.com/GlacierEQ/Genius-Code |
| Genius-Verification | https://github.com/GlacierEQ/Genius-Verification |

See `family/INDEX.json`.

## Status (truthful)

| Surface | State |
|---|---|
| Identity contract (GENIUS.yaml v2) | Implemented |
| Core schemas | Implemented |
| `genius` CLI (name/validate/doctor/new) | Implemented |
| Installable via `pip install -e .` | Implemented |
| Generator produces self-validating domain tree | Implemented (scaffold) |
| Full migration engine v1→v2 | Not yet |
| Published to PyPI | Not yet |
| Buildkite CI (`casey-1/genius-mastery`) | Observed PASS on [build #1](https://buildkite.com/casey-1/genius-mastery/builds/1) @ `18d584778006c26ece47903ec4d05de69f9ea9fd` |

Never convert “file exists” into “system works.”

## License

MIT — see LICENSE.
