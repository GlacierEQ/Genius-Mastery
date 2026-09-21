# Case Position Mastery

Case Position Mastery is the Genius operating layer for externally facing case campaigns. Its job is not to create more summaries. Its job is to preserve the Operator-approved position, prevent stale or misaligned outbound, and drive real institutional response through controlled, source-bound execution.

## Core doctrine

External case communication is strategic action. The system must never treat an outbound email, referral, demand, complaint, preservation request, or escalation as a generic task. Each outbound communication must be traceable to an approved campaign position, current source-bearing case state, and a defined mission objective.

The campaign engine distinguishes:

1. **Source-bearing facts** — evidence, receipts, provider records, records requests, replies, timestamps, documents, images, audio, video, dockets, and database readbacks.
2. **Operator position** — what Casey is asserting, demanding, refusing to concede, escalating, or preserving.
3. **Execution state** — what has been sent, acknowledged, answered, ignored, satisfied, superseded, or retired.
4. **Work-unit execution lease** — the per-action single-writer/idempotency identity that prevents duplicate side effects without creating a globally privileged worker.
5. **Review boundary** — the points where Operator approval is required because an action would materially alter strategy, posture, recipient class, concession risk, remedy request, representation posture, or escalation theory.

## Authority and topology

The Operator controls mission, strategy, scope, remedies, concessions, representation posture, and escalation architecture. Verbatim Operator source controls Operator intent. Provider-native state controls provider facts.

No worker, repository, validator, campaign artifact, receipt, summary, or prior send becomes a sole authority over the campaign. Any qualified peer may execute a routine constituent action when it can prove all of the following for the exact `WORK_UNIT`:

- the controlling Operator-approved plan, batch, or action class covers the action;
- the action does not materially change strategy, target, remedy, settlement/representation posture, concessions, admissions, waivers, or escalation architecture;
- current provider state shows the target/channel is still useful;
- the work-unit idempotency lease is available and the action has not already been completed, superseded, cured, withdrawn, or rendered harmful;
- provider/platform requirements can be satisfied;
- provider-native receipt/readback can be captured.

This is source recovery and consequence control, not a new permission gate. A material strategic delta becomes `REPLAN_REQUIRED` for that delta only; unaffected authorized work continues.

## The controlling distinction

A response is not automatically progress. A vague acknowledgment without ownership, tracking, routing, preservation confirmation, next step, or accountable timeline may satisfy only receipt, not the substantive objective.

The system must therefore track each objective separately:

- acknowledgment of receipt;
- intake/case/reference number when applicable;
- identified owner or responsible office;
- preservation of evidence and records;
- database/privacy correction or disclosure pathway;
- investigation or review status;
- remedial action or relief;
- records production;
- accountability for the underlying incident;
- accountability for complaint-handling failures.

## Approved execution model

```text
HYDRATE SOURCE STATE
→ LOAD CURRENT CAMPAIGN / WORK_UNIT STATE
→ RECOVER CONTROLLING OPERATOR AUTHORITY
→ READ CURRENT PROVIDER STATE
→ IDENTIFY UNSATISFIED OBJECTIVE
→ APPLY APPROVED POSITION DOCTRINE
→ ACQUIRE PER-WORK-UNIT IDEMPOTENCY LEASE
→ OPERATOR REVIEW ONLY IF A MATERIAL STRATEGIC BOUNDARY IS CROSSED
→ EXECUTE THROUGH ANY QUALIFIED PEER / PROVIDER ROUTE
→ CAPTURE PROVIDER RECEIPT
→ READ BACK TARGET STATE
→ UPDATE EXECUTION STATE
→ RETIRE STALE OR SATISFIED ACTIONS
```

## Consequence controls

These controls protect the consequence they own; they are not universal mission stoppers.

- No worker may send a case outbound without source-bearing authority for that exact work unit.
- No stale queued message may be sent without same-run current-state and idempotency checks.
- No email may assert facts beyond source-bearing support or clearly marked Operator allegation.
- No message may silently change the Operator's posture from self-directed execution to counsel-seeking, settlement-seeking, conciliatory, adversarial, public-pressure, or litigation posture.
- No duplicate escalation may be sent when the objective has already been satisfied by another recipient or newer channel.
- No vague response may be marked complete unless it satisfies the exact objective being tracked.
- No recipient silence may be treated as neutral when an approved escalation clock has expired.
- Failure of one worker/provider route changes the route, not the objective.

## Campaign doctrine object

Each campaign should define:

- matter id and matter name;
- protected party or affected person labels without unnecessary public exposure;
- current objective graph;
- approved strategic posture;
- permitted allegations and required truth labels;
- prohibited concessions and prohibited language;
- evidence anchors and provider receipts;
- active recipients and authority classes;
- escalation ladder and response clocks;
- what constitutes progress;
- what constitutes closure;
- work-unit identity and idempotency semantics;
- material review boundaries;
- stale-send suppression rules;
- execution-state records to update;
- provider-native receipts required after transmission.

## Response-pressure doctrine

When an institution acts quickly to impose a burden, restriction, label, ban, database entry, or adverse consequence, the campaign may treat delayed acknowledgment and vague non-ownership as a separate pressure point. The tone must remain controlled, but the position may be firm: serious rights-impacting allegations are not casual correspondence and require identifiable intake, routing, preservation, and response handling.

## Review boundary

Operator review is required before any outbound that materially:

- seeks outside counsel or legal referral;
- changes the remedy requested;
- changes the intended recipient class;
- accuses a new actor or institution not already within the approved campaign scope;
- introduces litigation, criminal complaint, inspector general, media, public-records escalation, privacy correction, or database-removal posture for the first time;
- offers compromise, settlement, apology acceptance, withdrawal, narrowing, or closure;
- adds emotionally loaded language that could reduce credibility or increase risk if sent externally.

Routine follow-ups inside a controlling campaign mandate do not require fresh approval merely because another qualified peer performs them. The executor must still recover the exact authority, current provider state, idempotency status, wording constraints, objective, recipient, and timing rule before transmission.

## Success standard

A case communication workflow succeeds only when the external mission state improves: evidence is preserved or acquired, a responsible owner is identified, a tracking path opens, a deadline is created, a stale action is retired, an institutional failure is documented for escalation, or a substantive response/decision is obtained. More text is not progress. More pressure without control is not progress. Controlled leverage with receipts is progress.
