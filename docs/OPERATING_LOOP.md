# The Operating Loop

Genius-Mastery already knows how to map capability, gather evidence, challenge assumptions, verify behavior, and teach what survives. This contract adds the missing connective tissue: the record of **why a move is being made, what it may change, what happened, and what becomes stronger afterward**.

```text
MISSION → CONTEXT → OPTIONS → IMPACT → ACTION → OUTCOME
                                      ↓
                         VERIFY → LEARN → STRENGTHEN ↺
```

## Why this belongs in the kernel

A new Genius entity needs room to aim beyond its present implementation. The horizon is not a false claim. It is a directional instrument. The operating loop therefore keeps two truths visible at once:

- **aspiration remains expansive** and can describe the intended frontier;
- **execution remains honest** through explicit maturity, outcome, and evidence states.

The loop never treats “not in the current window” as “does not exist.” Retrieval states are explicit:

- `known_from_context`
- `operator_reported`
- `retrieval_pending`
- `not_searched`
- `searched_found`
- `searched_not_found`
- `unavailable`
- `contradicted`

`searched_not_found` means a search result, not factual disproof. `contradicted` is reserved for an actual conflict that has been identified and recorded.

## Runtime use

Create a loop record from Python:

```python
from genius.operating_loop import build_loop, validate_loop

record = build_loop(
    mission="Preserve the strongest useful direction",
    context=["The project is new and still aspirational"],
    options=[
        "Clip the aspiration",
        "Preserve the horizon and label maturity honestly",
    ],
    impact=[
        "Preserving the horizon protects discovery",
        "Explicit maturity states protect truth",
    ],
    action="Preserve aspirations while implementing one verifiable slice",
    evidence_state="operator_reported",
)
assert validate_loop(record) == []
```

An outcome is initially `observed` rather than silently promoted to `verified`. Verification, learning, and strengthening are later recorded explicitly. This makes the system more capable without making it more reckless.

## Contract boundary

This is a **decision-and-learning record**, not an autonomous authority grant. It does not execute external side effects by itself, certify evidence, or replace the claim/evidence ledger. It gives those systems a shared spine so that future execution can remain mission-aware, impact-aware, and recoverable.
