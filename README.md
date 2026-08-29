# Genius-Mastery

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
| External GitHub Actions green | Unverified until observed |

Never convert “file exists” into “system works.”

## License

MIT — see LICENSE.
