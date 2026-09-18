# Failure Taxonomy Canvas · Ascend IQ

> Repo file `ai-evals/02-failure-discovery/failure-taxonomy.md`. Becomes the **Failure Taxonomy** slide of the final pitch deck (Module 6) and feeds the Module 3 eval suite.

**Source:** `audit-log.md` — 20 rows audited, 13 confirmed failures after human overrides.
**Severity anchored to:** `01-evaluation-strategy/strategy-canvas.md` — Source Traceability, Calibrated Abstention, Decision Sufficiency.

## Scoring guides

**Frequency** = how many of the 20 audited rows carry this failure. **≥ 3 of 20 = HIGH**; ≤ 2 = LOW.

**Severity (P0–P3)** — a strategic call about business cost, independent of how often it happens.

| Level | Meaning | Rough test |
|---|---|---|
| **P0** | Crisis Zone | Blocks the core promise; legal, compliance, or contract-breaking. |
| **P1** | Hidden Risk | Real damage to trust or revenue, but survivable short-term. |
| **P2** | Annoyance | Degrades experience; a workaround exists. |
| **P3** | Low Priority | Cosmetic or rare. |

## Top 3 Prioritized Failures

| Rank | Failure Type | Trust Tag | Agentic Mode | Frequency | Severity | Business Impact |
|---|---|---|---|---|---|---|
| **1** | **Stale retrieval — cached pricing served as current** | `#HALLUCINATION` | retrieval-level (not a trajectory failure) | 1/20 sample · **100% of pricing queries in production** | **P0** | Underquoted price becomes a priced commitment: honour a 17% discount or retract mid-renewal. Contract dispute on the one question with a contract attached. |
| **2** | **Confident distortion — qualifier dropped or comparison reversed** | `#HALLUCINATION` | output-level | 5/20 · **HIGH** | **P0** | Undetectable to a user who cannot verify. Row 7 reverses a competitive benchmark into a forwardable false claim; rows 3, 4, 11, 14 convert tentative, conditional and workaround facts into settled ones. |
| **3** | **Fabricated detail — spec the source never contained** | `#HALLUCINATION` | output-level | 5/20 · **HIGH** | **P1** | Invented specifics (`#007AFF`, "Series B", "10-seat minimum") ship into decks, briefs and CRM notes as sourced fact, then propagate past the point of correction. |

**Also logged, below the line:** over-refusal of an answerable query (`#ROBUSTNESS`, 1/20, P1 — the paired guardrail metric from M1) and slang against Brand Voice (`#UX_TRUST`, 1/20, P2).

## #1 Risk · Business Impact Statement

> **This failure matters because Ascend IQ serves a cached pricing page as current — quoting $49 when the list price is $59 — and a CS lead who forwards that number has put a priced commitment in writing that we either honour at a 17% discount or retract mid-renewal. Every pricing query hits the same stale document until the cache TTL is fixed, so this is not a rare miss; it is a standing liability on the one question that has a contract attached.**

## Defending the Prioritization

- **The #1 risk is P0 on severity, not on count.** It appears once in twenty rows, and it still outranks two failures that appear five times each. The M1 Strategy Canvas already made this call in advance: *"Pricing, contract, billing and legal questions — Traceability wins absolutely… A cited non-answer costs the user one follow-up; an invented price costs a contract dispute."* Ranking it anywhere but first would contradict the trade-off the product was designed around.

- **Its sample frequency understates its production frequency, and the ≥3-of-20 threshold cannot see why.** The other twelve failures are probabilistic — the model may or may not drop a qualifier on a given query. A cache serving a stale document is deterministic: *every* pricing query returns the same wrong price until the TTL is fixed. "1/20" is an artifact of how many pricing questions are in the sample, not a measure of exposure.

- **It is also the cheapest of the three to fix, and the only one with a different owner.** Ranks 2 and 3 are model behaviour — prompt rules, claim-level citation, and an eval gate to hold them. Rank 1 is a retrieval-layer bug that a prompt change would not touch at all. Separating it out is what stops the team from shipping a prompt fix and believing the pricing problem is solved.

- **Rank 2 sits above rank 3 at equal frequency because of who can catch it.** A fabricated hex code is conspicuous — it is oddly specific and a designer will notice. A dropped qualifier is not: every proper noun is real, every fact traces to a genuine source, and the answer is still wrong. Against the M1 user promise — users who *cannot verify the answer themselves* — the undetectable failure is the more expensive one.

---
_Failure Taxonomy Canvas, M2 lab, AI Evals Certification. Built from `audit-log.md`; severity anchored to the M1 Strategy Canvas._
