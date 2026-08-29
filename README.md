# Genius-Mastery

**Family control kernel** for the Genius repository ecosystem.

Identity rule (no exceptions):

```text
Genius-{purpose}
```

This repository is **not** a super-domain. It owns the shared machinery that every domain repository depends on:

- family specification & naming normalization
- generator (`genius new`)
- schemas (claim, evidence, source, challenge, composition)
- validator / doctor / audit
- migration & upgrade engine
- reusable CI workflows
- evidence & source-quality standards
- composition protocol
- family index

## Doctrine

Mastery, not skills. Aspirations may be enormous; verified capability must point to evidence.

Foundational loop:

```text
MAP → RESEARCH → MODEL → BUILD → BREAK → MEASURE → VERIFY → OPERATE → EXPLAIN → SYNTHESIZE → PROVE → EXPAND ↺
```

There is no artificial finish line.

## Quick start

```bash
# Validate this kernel
python tools/validate.py .

# Doctor (strength/weakness surface)
python tools/doctor.py .

# Generate a new domain repo (local)
python -m genius new Code
```

## Family topology

| Repository | Role |
|---|---|
| **Genius-Mastery** | Kernel (this repo) |
| Genius-Code | Flagship domain |
| Genius-Verification | Verification primitives |
| Genius-Systems / Performance / … | Domain mastery units |

Composition is capability-based, not reputation-based. See `interfaces/COMPOSITION.yaml`.

## Status (truthful)

| Surface | State |
|---|---|
| Identity contract (GENIUS.yaml v2) | Implemented |
| Core schemas | Implemented |
| Local validator | Implemented |
| Doctor / vector | Implemented (seed) |
| Generator | Scaffold |
| Migration engine | Scaffold |
| Reusable GitHub workflows | Present |
| Family INDEX | Present |
| External CI run on GitHub | Unverified until Actions execute |

Never convert “file exists” into “system works.”

## License

See LICENSE.
