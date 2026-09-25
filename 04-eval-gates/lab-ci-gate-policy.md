# Lab, CI Eval Gate Policy (Ascend IQ PR #218)

> Repo file `ai-evals/04-eval-gates/lab-ci-gate-policy.md`. Output of the **CI Gate demo**: PR #218 swaps the Ascend IQ retrieval prompt; a 30-case regression golden set is replayed on every PR against deterministic fixtures (no live model calls). Floors + max-regression are set per dimension, never as one blended "quality" number.

| Dimension | main | PR | Δ | Floor | Max reg | Blocking | Result |
|---|---:|---:|---:|---:|---:|---|---|
| **Faithfulness (grounding)** | 96 | 87 | **−9** | **94** | **2** | yes | **FAIL** (below floor, and past max reg) |
| Task completion | 92 | 93 | +1 | 85 | 5 | yes | PASS |
| Tool selection | 90 | 88 | −2 | 80 | 5 | yes | PASS |
| Safety / policy | 99 | 99 | 0 | 98 | 1 | yes | PASS |
| Latency (p95) | 84 | 80 | −4 | 70 | 8 | no (warn) | PASS |
| Cost per task | 88 | 82 | −6 | 70 | 10 | no (warn) | PASS |
| **Pricing current-price accuracy** | — | — | — | **100** | **0** | yes | **N/A**: not evaluated in PR #218 replay; actively required once the dedicated pricing regression golden set (N ≥ 30) is populated |

**Gate result:** **BLOCKED**

### Policy choices

- **Faithfulness tightened from the default (floor 90 → 94, max reg 3 → 2).** Raising the floor to 94 and capping regression at 2 aligns with our M1 strategy where Source Traceability on core facts is non-negotiable.
- **Latency and cost are warn-only.** Matches the M1 canvas decision where speed does not override trust.
- **Pricing current-price accuracy added as its own blocking dimension.** This directly translates our M3 Eval Spec contract into CI code, ensuring zero stale pricing quotes slip through to enterprise customers. It is separate from faithfulness on purpose: faithfulness can read 96 while one pricing answer is stale.
- **No blended score.** Averaging the six PR scores gives ~88, only 3 below main; that average would hide the 9-point faithfulness drop.

## Merge decision

**BLOCK.** Faithfulness dropped by 9 points (from 96 to 87), violating both our tightened max regression limit of 2 (as well as the default limit of 3) and sinking below the floor. A 9-point drop in grounding indicates the prompt swap in PR #218 causes severe hallucinations, which cannot be excused by minor improvements in task completion.

**Flip threshold:** under this policy (floor 94, max reg 2), the PR would have required a Faithfulness score of at least 94.0 (a drop of no more than 2 points from the 96 baseline) to clear the gate and merge.
