# Genius-Mastery Epistemology

## Purpose

Genius-Mastery is the family kernel, teacher-forge, and entity compiler. Its epistemic responsibility is therefore different from any one domain repository: it must govern how knowledge is acquired, classified, challenged, promoted, transferred, decayed, composed, and taught without flattening proposition-specific expertise into one universal score.

Its output is not merely information. Its output is stronger entities whose claims remain traceable to the evidence that justified them.

## Prime law

> A representation may route knowledge, but only proposition-specific evidence may justify a claim.

Memory, summaries, graphs, generated plans, embeddings, indexes, manifests, badges, dashboards, and prior assistant prose are useful navigation surfaces. None automatically outrank the source-bearing evidence relevant to the proposition under evaluation.

The family cognition loop is:

```text
RECOVER → CLASSIFY → SOURCE → MODEL → CHALLENGE → EXECUTE
       → VERIFY → READ BACK → RECONCILE → COMPOSE → TEACH → REVALIDATE
```

## 1. Separate reality from representations of reality

The Genius family should preserve at least these distinctions:

- **aspiration** — desired future capability;
- **hypothesis** — plausible but not yet established proposition;
- **mapped** — represented in plans, graphs, schemas, or capability anatomy;
- **implemented** — artifact exists in source or configuration;
- **executable** — artifact can run in an available runtime;
- **observed** — behavior was directly seen in a specific execution/environment;
- **verified** — declared acceptance criteria were satisfied with inspectable evidence;
- **reproduced** — result can be obtained again from preserved inputs and procedure;
- **transferred** — mechanism remains valid in a materially different context;
- **mastered** — knowledge survives challenge, execution, explanation, transfer, and teaching.

Do not promote between these states by rhetoric.

## 2. Authority is proposition-specific

There is no globally canonical source for every question.

For a proposition, identify the authority appropriate to its type:

```text
formal standard/specification
primary implementation/source
provider-native state / runtime receipt
original research / authoritative textbook
maintainer documentation
reproducible experiment
high-quality secondary synthesis
memory / summary / projection / anecdote
```

These are not a universal linear ranking. Source code may outrank prose for current implementation behavior; a standard may outrank source for normative requirements; provider readback may outrank configuration for current remote state; operator firsthand evidence may be primary for the operator's own intentions and actions.

Always ask: **authoritative for what proposition?**

## 3. Provenance is part of knowledge

Knowledge without origin is weakened knowledge.

Preserve, when available:

- source identity and location;
- author/provider;
- version, revision, SHA, timestamp, or publication date;
- retrieval time;
- transformation history;
- responsible agent/tool;
- supporting and contradicting sources;
- confidence and unresolved uncertainty;
- dependency on external assumptions.

A derived claim should be traceable through its derivation chain rather than detached from its source.

## 4. Contradictions are retained, not averaged away

When sources conflict:

1. preserve both claims;
2. identify whether they concern the same proposition, version, time, and scope;
3. compare source authority and directness;
4. inspect live state where possible;
5. test or reproduce the disagreement;
6. mark established, contradicted, superseded, unresolved, or context-dependent state;
7. keep the losing evidence for auditability.

Do not silently harmonize incompatible evidence into a smooth summary.

## 5. Absence of retrieval is not evidence of absence

A failed search, unavailable connector, stale index, missing memory hit, permission error, or timeout may mean only that the retrieval path failed.

Distinguish:

```text
NOT_FOUND_IN_QUERIED_SURFACE
NOT_ACCESSIBLE
NOT_INDEXED
NOT_RETRIEVED
CONTRADICTED_BY_EVIDENCE
ESTABLISHED_ABSENT
```

Only the last two are substantive factual conclusions.

## 6. Observation and inference must remain separable

Every nontrivial knowledge object should permit the reader to distinguish:

- what was directly observed or retrieved;
- what was computed;
- what was inferred;
- what assumption connected the evidence to the inference;
- what uncertainty remains.

Inference is necessary. Hidden inference is dangerous.

## 7. Uncertainty should be modeled, not hidden

Avoid false precision and binary certainty when the evidence is partial.

Uncertainty may arise from:

- sampling;
- measurement;
- incomplete state visibility;
- model mismatch;
- temporal drift;
- ambiguous terminology;
- stochastic systems;
- conflicting sources;
- tool limitations;
- dependency uncertainty;
- transfer from one environment to another.

Where quantitative uncertainty is meaningful, preserve intervals/distributions and assumptions. Where it is not, use explicit qualitative bounds rather than fabricated probabilities.

## 8. Knowledge has a half-life

Facts about APIs, models, dependencies, prices, laws, cloud state, deployments, organizational roles, and available tools can decay rapidly.

Every important knowledge object should be capable of carrying:

```text
observed_at
valid_for / scope
source_version
revalidation_trigger
revalidation_interval when useful
superseded_by
```

Fresh live state should supersede stale state without erasing history.

## 9. Reproducibility and replicability are distinct

For computational work:

- **reproducibility** asks whether the same data, code, method, and conditions yield consistent computational results;
- **replicability** asks whether independent work addressing the same question yields consistent substantive results.

The family should prefer artifacts that make both easier: source SHAs, dependency locks, environment capture, seeds, datasets, commands, logs, hashes, and acceptance criteria.

## 10. Evidence strength compounds through independence

Ten copies of the same claim are not ten independent confirmations.

Assess dependence among evidence:

- shared upstream source;
- copied implementation;
- same model or benchmark;
- same data;
- same provider projection;
- same failure mode.

Confidence rises most when different mechanisms agree under different failure modes.

## 11. Negative evidence is first-class

Failures, counterexamples, null results, rejected hypotheses, broken builds, contradictory provider state, and failed reproductions belong in durable state.

A mastery system that stores only successes systematically overestimates itself.

## 12. Verification is claim-specific

The family kernel must not substitute its own generic confidence score for domain verification.

Examples:

- code semantics → specification, type/program analysis, tests, proofs;
- distributed protocol → fault model, temporal properties, model checking, fault injection;
- performance → benchmark methodology and uncertainty;
- security → threat model and adversarial evidence;
- legal proposition → authority, jurisdiction, procedural posture, factual record;
- provider mutation → provider-native receipt/readback;
- human/organizational claim → appropriate empirical methods.

Genius-Mastery routes to domain evidence rather than pretending one method verifies everything.

## 13. Action authorization depends on both evidence and consequence

The existing family epistemic gate should continue to enforce its L-level authorization semantics. This document does not redefine those levels; it supplies the deeper evidence law beneath them.

As consequence, irreversibility, external impact, or uncertainty rises, require stronger evidence, clearer assumptions, more independent verification, and stronger recovery/readback.

Reversible local exploration can proceed under weaker evidence than destructive or externally binding action.

## 14. Source-bearing state outranks compressed routing state

Summaries, memory, indexes, manifests, graphs, and generated knowledge maps exist to make retrieval faster. They must not become lossy substitutes for source-bearing state when precision matters.

Use compression hierarchically:

```text
routing summary
  → structured claim
  → source excerpt / artifact
  → full source or executable state
```

Escalate toward the source as consequence or ambiguity rises.

## 15. Composition must preserve epistemic boundaries

When one Genius entity consumes another:

- preserve donor identity;
- preserve claim IDs and evidence references;
- preserve assumptions and limits;
- distinguish imported capability from locally verified capability;
- avoid copying stale representations when the donor remains queryable;
- record adapter/transformation logic;
- reverify environment-sensitive behavior at the consumer boundary.

Composition is not evidence laundering.

## 16. Teaching is a verification surface

A mastered concept should survive reconstruction by another competent entity.

Teaching artifacts should expose:

- definitions;
- mechanisms;
- invariants;
- assumptions;
- canonical examples;
- counterexamples;
- failure modes;
- verification method;
- transfer limits;
- exercises requiring decisions, not recall alone.

If the learner cannot apply the mechanism in a new setting, the knowledge may be memorized but not mastered.

## 17. Family promotion contract

A capability should advance through evidence-bearing transitions rather than percentages:

```text
hypothesized
→ mapped
→ sourced
→ implemented
→ executed
→ challenged
→ verified
→ reproduced
→ transferred
→ taught
→ revalidated
```

Not every capability needs every state. The required terminal state depends on mission consequence. But skipped states must be explicit rather than silently implied.

## 18. Epistemic receipt

A durable claim receipt should be able to answer:

```text
claim_id
proposition
claim_type
state
scope
sources[]
source_versions[]
observations[]
inferences[]
assumptions[]
counterevidence[]
verification_method
execution_receipts[]
artifact_hashes[]
uncertainty
observed_at
revalidation_trigger
supersedes / superseded_by
```

The exact storage schema may vary by domain; the semantic distinctions should not.

## 19. Foundational corpus

The kernel's epistemology is grounded by source families including:

- W3C PROV for entities, activities, agents, derivations, and provenance relations;
- National Academies work on reproducibility and replicability;
- NIST measurement-uncertainty guidance;
- ACM artifact evaluation and reproducibility practice;
- Stanford Encyclopedia of Philosophy's epistemology synthesis;
- domain-specific primary sources supplied by each Genius repository;
- provider-native runtime evidence and repository source state.

See `sources/EPISTEMIC_SOURCES.yaml`.

## 20. Master-teacher standard

The kernel succeeds when generated entities become progressively better at answering five questions:

1. **What do we know?**
2. **How do we know it?**
3. **What would falsify or supersede it?**
4. **What may we safely do on the strength of it?**
5. **Can another entity reconstruct and improve the result from the preserved evidence?**

## Final rule

> Never promote representation into reality, repetition into independence, execution into verification, verification into universal truth, or stale truth into current truth. Preserve provenance, contradiction, uncertainty, source authority, and the path by which stronger evidence changes the state of belief.
