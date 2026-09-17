# Failure Taxonomy Canvas · Ascend IQ

> Repo file `ai-evals/02-failure-discovery/failure-taxonomy.md`. Becomes the **Failure Taxonomy** slide of the final pitch deck (Module 6) and feeds the Module 3 eval suite.

## How to complete this file

1. First complete `audit-log.md` (the failure audit) — this canvas prioritizes the failures you found there.
2. Open the **M2 · Failure Taxonomy Canvas** tool from the Module 2 deck. Fill the three risk cards (click **↺ Load Ascend IQ defaults** to see a worked example first), then click **📋 Copy markdown** and paste it over the template below.
3. Anchor severity to the **user promise / trust metrics you chose in the Module 1 Strategy Canvas** (`ai-evals/01-evaluation-strategy/strategy-canvas.md`) — severity is a strategic judgment, not just a frequency count.

**Definition of done —** you're finished when the Top 3 table is fully filled (no `_…_` left), the #1 risk has a one-sentence Business Impact Statement in leadership language, and the prioritization is defended in 2–3 bullets.

### Scoring guides

**Frequency** = how many of the 20 audited rows carry this Trust Metric tag. **≥ 3 of 20 = HIGH** frequency; ≤ 2 = LOW.

**Severity (P0–P3)** — a strategic call about business cost, independent of how often it happens:

| Level | Meaning | Rough test |
|---|---|---|
| **P0** | Crisis Zone | Blocks the core promise; legal, compliance, or contract-breaking. |
| **P1** | Hidden Risk | Real damage to trust or revenue, but survivable short-term. |
| **P2** | Annoyance | Degrades experience; a workaround exists. |
| **P3** | Low Priority | Cosmetic or rare. |

**Agentic mode** (optional) — if the failure lives in the *trajectory* (the path of tool calls), tag it: `TOOL_MISUSE`, `REASONING_LOOP`, `SCOPE_ESCALATION`, or `RECOVERY_FAILURE`. Leave blank for output-only failures.

## Top 3 Prioritized Failures

| Rank | Failure Type | Trust Tag | Agentic Mode | Frequency | Severity | Business Impact |
|---|---|---|---|---|---|---|
| _Example (replace): 1_ | _Fabricated Pricing_ | _#HALLUCINATION_ | _output-level_ | _4/20_ | _P0_ | _Contract disputes; blocks Enterprise renewals._ |
| 1 | _…_ | _…_ | _…_ | _…/20_ | _P0–P3_ | _…_ |
| 2 | _…_ | _…_ | _…_ | _…/20_ | _P0–P3_ | _…_ |
| 3 | _…_ | _…_ | _…_ | _…/20_ | _P0–P3_ | _…_ |

## #1 Risk · Business Impact Statement

> _Template: "This failure matters because [technical error] results in [business consequence]." Name the concrete cost — revenue, churn, legal, or trust — not the bug._

## Defending the Prioritization

- _Why the #1 risk is P0 (severity), independent of how often it happens._
- _Frequency threshold: ≥3 of 20 = HIGH._
- _Severity anchored to the trust metrics you chose in the Module 1 Strategy Canvas._
