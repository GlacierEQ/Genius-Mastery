# Case Position Mastery

Case Position Mastery is the Genius operating layer for externally facing case campaigns. Its job is not to create more summaries. Its job is to preserve the Operator-approved position, prevent stale or misaligned outbound, and drive real institutional response through controlled escalation.

## Core doctrine

External case communication is strategic action. The system must never treat an outbound email, referral, demand, complaint, preservation request, or escalation as a generic task. Each outbound communication must be traceable to an approved campaign position, current source-bearing case state, and a defined mission objective.

The campaign engine distinguishes:

1. **Source-bearing facts** — evidence, receipts, provider records, records requests, replies, timestamps, documents, images, audio, video, dockets, and database readbacks.
2. **Operator position** — what Casey is asserting, demanding, refusing to concede, escalating, or preserving.
3. **Execution state** — what has been sent, acknowledged, answered, ignored, satisfied, superseded, or retired.
4. **Outbound authority** — the single worker allowed to transmit case-related communications after approved preflight.
5. **Review boundary** — the points where Operator approval is mandatory because a message would alter strategy, posture, recipient class, concession risk, remedy request, or escalation theory.

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
→ LOAD CURRENT SUPABASE CAMPAIGN STATE
→ COMPARE PRIOR OUTBOUND RECEIPTS AND RESPONSES
→ IDENTIFY UNSATISFIED OBJECTIVE
→ APPLY APPROVED POSITION DOCTRINE
→ GENERATE CONTROL ENVELOPE
→ OPERATOR REVIEW IF STRATEGIC BOUNDARY IS CROSSED
→ SEND ONLY THROUGH THE DESIGNATED OUTBOUND AUTHORITY
→ CAPTURE PROVIDER RECEIPT
→ READ BACK SENT STATE
→ UPDATE SUPABASE
→ RETIRE STALE OR SATISFIED ACTIONS
```

## Non-negotiable safety gates

- No case outbound may be sent from a general production worker.
- No stale queued message may be sent without same-run current-state preflight.
- No email may assert facts beyond source-bearing support or clearly marked Operator allegation.
- No message may silently change the Operator's posture from self-directed execution to counsel-seeking, settlement-seeking, conciliatory, adversarial, public-pressure, or litigation posture.
- No duplicate escalation may be sent when the objective has already been satisfied by another recipient or newer channel.
- No vague response may be marked complete unless it satisfies the exact objective being tracked.
- No recipient silence may be treated as neutral when an approved escalation clock has expired.

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
- stop/review conditions;
- stale-send suppression rules;
- Supabase tables or records to update;
- provider-native receipts required after transmission.

## Response-pressure doctrine

When an institution acts quickly to impose a burden, restriction, label, ban, database entry, or adverse consequence, the campaign may treat delayed acknowledgment and vague non-ownership as a separate pressure point. The tone must remain controlled, but the position may be firm: serious rights-impacting allegations are not casual correspondence and require identifiable intake, routing, preservation, and response handling.

## Review boundary

Operator approval is required before any outbound that:

- seeks outside counsel or legal referral;
- changes the remedy requested;
- changes the intended recipient class;
- accuses a new actor or institution not already within the approved campaign scope;
- invokes litigation, criminal complaint, inspector general, media, public records escalation, privacy correction, or database-removal posture for the first time;
- offers compromise, settlement, apology acceptance, withdrawal, narrowing, or closure;
- contains emotionally loaded language that could reduce credibility or increase risk if sent externally.

Routine follow-ups inside a locked campaign mandate may be sent by the designated executor only when the exact escalation tier, wording constraints, objective, recipient, and timing rule were already approved and live-state preflight confirms no stale-send condition.

## Success standard

A case communication workflow succeeds only when the external mission state improves: evidence is preserved or acquired, a responsible owner is identified, a tracking path opens, a deadline is created, a stale action is retired, an institutional failure is documented for escalation, or a substantive response/decision is obtained. More text is not progress. More pressure without control is not progress. Controlled leverage with receipts is progress.
