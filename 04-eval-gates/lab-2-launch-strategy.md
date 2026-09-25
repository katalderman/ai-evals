# Module 4 · Launch Strategy · Section 4.0 Release Criteria

> Repo file `ai-evals/04-eval-gates/lab-2-launch-strategy.md`. Your PRD's release-criteria section: the numeric thresholds, the CI gate policy, and the mitigation lever for the Soft gate.
> One row per gate in [`lab-1-gate-map.md`](./lab-1-gate-map.md). Evaluators from the M3 suite ([`eval_lab.ipynb`](../03-eval-suites/eval/eval_lab.ipynb)).

## 4.0 Release Criteria

| Severity | Metric | Threshold | Dataset | Method |
|---|---|---|---|---|
| **Hard** · #1 Stale pricing | Stale-price rate on pricing queries | **= 0%** | Pricing golden set, N ≥ 30 | Layer 1 current-price rule against the pricing system of record; Layer 3 judge fallback when the source has no version label |
| **Hard** · #2 Confident distortion | % of answers with a dropped or reversed qualifier | **= 0%** | 30-case regression golden set | Layer 3 judge (κ = 0.76); every judge FAIL routed to a mandatory human check before blocking |
| **Soft** · #3 Fabricated detail | % of answers with an unsupported specific | **≤ 2%** | 30-case regression golden set | Layer 1 numeric grounding + Layer 3 judge |
| **Soft** · #4 Over-refusal | % of answerable queries declined | **≤ 5%** | Answerable subset (refusal-mandated queries excluded) | Layer 2 refusal classification + refusal detection |
| **Advisory** · #5 Brand voice | Slang / informal-tone rate | **≤ 5%**, warn only | 30-case regression golden set | Layer 1b slang regex |

**Why Hard #2 keeps zero tolerance with a human check:** because Cohen's κ = 0.76 means the judge is probabilistic, the human check prevents false alarms from killing good releases while maintaining a zero-tolerance safety net on user-undetectable distortions.

### Current build vs. criteria (M2 audit, 20 rows)

| Gate | Threshold | Current build | Status |
|---|---|---|---|
| Hard #1 Stale pricing | = 0% | 1 of 1 pricing queries stale (100%) | ❌ fails |
| Hard #2 Confident distortion | = 0% | 5 of 20 (25%) | ❌ fails |
| Soft #3 Fabricated detail | ≤ 2% | 5 of 20 (25%) | ❌ misses |
| Soft #4 Over-refusal | ≤ 5% | 1 of 18 answerable (5.6%) | ⚠️ just over |
| Advisory #5 Brand voice | ≤ 5% | 1 of 20 (5%) | ✅ at limit (warn) |

Directional: 20 rows, not the N ≥ 30 golden sets these criteria require. The pricing golden set does not exist yet (see [`lab-judge-calibration.md`](../03-eval-suites/lab-judge-calibration.md)).

## 4.1 CI Gate Policy

> Every PR replays the **30-case regression golden set against deterministic fixtures** (no live model calls), scored **per dimension**. **Faithfulness** (floor 94, max regression 2) and **Pricing current-price accuracy** (floor 100, max regression 0) hard-block the merge, as do task completion, tool selection, and safety / policy at their floors. **Latency (p95)** and **cost per task** are warn-only. **No blended overall quality score may be used to override or average out any single dimension regression.** Full table and the PR #218 BLOCK decision: [`lab-ci-gate-policy.md`](./lab-ci-gate-policy.md).

## 4.2 Mitigation Plan · Soft Gate

**Selected Lever:** Staged Rollout, to **5 design-partner accounts (10% of the top 50 enterprise accounts)**

> A staged rollout to 5 design-partner accounts limits contractual and relationship exposure to a tiny blast radius, giving us real-world validation to verify that fabricated details stay under 2% and over-refusal stays under 5% before scaling across the entire enterprise tier.

**Scope of the lever:** it contains **Soft**-gate risk only. Both Hard gates must pass before the first account is enabled; a staged rollout does not excuse a Hard-gate failure.
