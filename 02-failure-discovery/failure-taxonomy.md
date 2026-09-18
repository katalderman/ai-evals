# Failure Taxonomy Canvas · Ascend IQ

> Repo file `ai-evals/02-failure-discovery/failure-taxonomy.md` (the repo is your submission); becomes the Failure Taxonomy slide of the final pitch deck.
> Built from `audit-log.md` — 20 rows audited, 13 confirmed failures after human overrides. Severity anchored to `01-evaluation-strategy/strategy-canvas.md`.

## Top 3 Prioritized Failures

| Rank | Failure Type | Trust Tag | Agentic Mode | Frequency | Severity | Business Impact |
|---|---|---|---|---|---|---|
| #1 | Stale Retrieval — cached pricing served as current (row 1) | #HALLUCINATION | Retrieval-level (output-only dataset; no trajectory to audit) | 1/20 sample → LOW, but **100% of pricing queries in production** | P0 | Contract exposure, an underquoted price becomes a priced commitment: honour a 17% discount or retract mid-renewal. Hits the one question class with a contract attached. |
| #2 | Confident Distortion — qualifier dropped or comparison reversed (rows 3, 4, 7, 11, 14) | #HALLUCINATION | · | 5/20 → HIGH | P0 | Undetectable to a user who cannot verify. Row 7 reverses a competitive benchmark into a forwardable false claim; rows 3, 4, 11, 14 convert tentative, conditional and workaround facts into settled ones. |
| #3 | Fabricated Detail — spec the source never contained (rows 5, 6, 9, 12, 19) | #HALLUCINATION | · | 5/20 → HIGH | P1 | Invented specifics (`#007AFF`, "Series B", "10-seat minimum") ship into decks, briefs and CRM notes as sourced fact, then propagate past the point of correction. |

Also logged, below the line: over-refusal of an answerable query (#ROBUSTNESS, 1/20, P1 — the paired guardrail metric from M1) and slang against Brand Voice (#UX_TRUST, 1/20, P2).

## #1 Risk · Business Impact Statement

> This failure matters because Ascend IQ serves a cached pricing page as current — quoting $49 when the list price is $59 — and a CS lead who forwards that number has put a priced commitment in writing that we either honour at a 17% discount or retract mid-renewal. Every pricing query hits the same stale document until the cache TTL is fixed, so this is not a rare miss; it is a standing liability on the one question that has a contract attached.

## Defending the Prioritization

- The #1 risk is rated **P0 on severity, not on count**. It appears once in twenty rows and still outranks two failures appearing five times each. The Module 1 Strategy Canvas made this call in advance: *"Pricing, contract, billing and legal questions — Traceability wins absolutely… A cited non-answer costs the user one follow-up; an invented price costs a contract dispute."* Ranking it anywhere but first would contradict the trade-off the product was designed around.
- **Frequency is counted across the 20-row audit (threshold = 3), and for rank #1 that count understates exposure.** Ranks #2 and #3 are probabilistic — the model may or may not drop a qualifier on a given query. A cache serving a stale document is deterministic: *every* pricing query returns the same wrong price until the TTL is fixed. "1/20" measures how many pricing questions are in the sample, not how often this fails in production.
- **Severity is the qualitative business judgment, anchored to the user promise in the Module 1 Strategy Canvas** — and that promise is what separates #2 from #3 at equal frequency. Users *cannot verify the answer themselves*. A fabricated hex code is conspicuous; a dropped qualifier is not, because every proper noun is real and every fact traces to a genuine source. The undetectable failure is the more expensive one.
- **Rank #1 is also the cheapest to fix and the only one with a different owner.** Ranks #2 and #3 are model behaviour: prompt rules, claim-level citation, and an eval gate to hold them. Rank #1 is a retrieval bug a prompt change would not touch — separating it out is what stops the team shipping a prompt fix and believing pricing is solved.

---

_Failure Taxonomy Canvas, M2 lab, AI Evals Certification. Built from `audit-log.md`; severity anchored to the M1 Strategy Canvas._
