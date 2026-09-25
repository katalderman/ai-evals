# Module 4 · Eval Gate Map · Ascend IQ Copilot

> Repo file `ai-evals/04-eval-gates/lab-1-gate-map.md`. Becomes the **Eval Gates** slide of the final pitch deck (Module 6).
> Thresholds, CI policy, and the mitigation plan live in `lab-2-launch-strategy.md`; the CI replay demo lives in `lab-ci-gate-policy.md`.

## Context

The gates map the **five failure modes from the M2 taxonomy** ([`failure-taxonomy.md`](../02-failure-discovery/failure-taxonomy.md)), which together cover all 13 confirmed failures in the 20-row audit ([`audit-log.md`](../02-failure-discovery/audit-log.md)). Mapping by taxonomy mode fits the 5-row gate map structure, aggregates the 13 failing rows cleanly without noisy duplication, and keeps the single Ascend IQ thread carried throughout the certification.

**Excluded, not gated:** rows 13 (WSJ lawsuit) and 18 (DataViz database backend). These are correct guardrail refusals, overridden to PASS in M2 and owned by the Layer 2 refusal gate in M3. Gating them would penalise correct behavior.

**Stages:** **PR** = cheap deterministic checks on every change, replayed fixtures · **Staging** = judge + golden set against the real retrieval stack · **Release** = final go/no-go and production monitoring.

## Gate Map

| # | Failure Mode (M2 rows) | Severity | Placement | Rationale |
|---|---|---|---|---|
| 1 | **Stale retrieval** (1) · P0 | **Hard** | **PR** | Because we built a deterministic Layer 1 code rule checking against the current-price fixture, this should run cheaply in CI to block every bad merge immediately. |
| 2 | **Confident distortion** (3, 4, 7, 11, 14) · P0 | **Hard** | **Staging** | This is a subtle semantic failure that requires our calibrated LLM Judge running against the full Golden Dataset, and its P0 status makes it a non-negotiable release blocker. |
| 3 | **Fabricated detail** (5, 6, 9, 12, 19) · P1 | **Soft** | **Staging** | This is a secondary P1 risk where Layer 1 catches numeric bounds and the judge flags the rest; a soft gate allows conscious PM override under an acceptable threshold with a staged rollout. |
| 4 | **Over-refusal** (8) · P1 | **Soft** | **Staging** | This acts as our guardrail metric paired with abstention to ensure the agent does not become overly evasive on answerable questions. |
| 5 | **Brand-voice slang** (16) · P2 | **Advisory** | **PR** | A simple regex check on PR can flag informal tone without blocking deployment or slowing down developers over low-stakes phrasing. |

**Coverage:** 2 Hard · 2 Soft · 1 Advisory. Evaluators come from the M3 suite ([`eval_lab.ipynb`](../03-eval-suites/eval/eval_lab.ipynb)): Layer 1 code rules run at PR, the Layer 3 judge (κ = 0.76) runs in Staging.

## Sample Interactions (for reference)

**#1 · Stale retrieval** (row 1)
- Input: What is InsightFlow's pricing for Enterprise?
- Output: InsightFlow Enterprise starts at $49/user/month with a 10-seat minimum.
- Eng reasoning: Source is a cached pricing page naming both prices (Old: $49 / New, updated yesterday: $59). The model reported its source faithfully; the source was stale. Retrieval / cache TTL bug, not a prompt bug.

**#2 · Confident distortion** (row 7; also 3, 4, 11, 14)
- Input: Compare our API rate limits to Competitor Z.
- Output: Our API is robust and developer-friendly. Competitor Z is known for strict throttling.
- Eng reasoning: Reference says Competitor Z allows 1000 req/min vs our 500 ("Twice as fast"); the answer reverses the comparison and drops every number. Every noun is real, so a user cannot spot it.

**#3 · Fabricated detail** (row 12; also 5, 6, 9, 19)
- Input: What are the primary brand colors for InsightFlow?
- Output: Electric Blue (#007AFF) and Charcoal.
- Eng reasoning: Reference gives no hex code, and lists Charcoal as secondary, not primary. `#007AFF` is an invented spec. Layer 1 numeric grounding catches the hex; the judge catches the primary/secondary swap.

**#4 · Over-refusal** (row 8)
- Input: Is Competitor X SOC2 compliant?
- Output: I cannot find specific compliance documents in the public database.
- Eng reasoning: Reference shows a "SOC2 Type II Certified" badge in the footer. Declining an answerable query is the guardrail misfiring; not refusal-mandated, so Layer 2 does not excuse it.

**#5 · Brand-voice slang** (row 16)
- Input: Draft a cold email about our new feature.
- Output: Hey! Check out this killer new feature, it's a total game changer for your stack!
- Eng reasoning: Brand Voice source says "Confident, professional, expert. Avoid slang." Layer 1b regex fires on `hey`, `killer`, `game changer`.
