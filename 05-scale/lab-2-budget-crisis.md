# Lab 2, Ascend IQ Budget Crisis

> Repo file `ai-evals/05-scale/lab-2-budget-crisis.md`. Allocate Level 1/2/3 coverage across the 5 failure modes under the **$200K/quarter cap** with **max 3 at Level 3**.
>
> Fill this with the **Budget Crisis Tool**, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

**Quarterly budget cap:** $200,000
**Total Level 3 spend:** _$… (… of max 3 L3 slots used)_

## Portfolio decision grid

| Failure | Trust metric | Risk | Level | Cost |
|---|---|---|---|---|
| Data Fabrication | Hallucination Rate | P0 | _L1 / L2 / L3_ | _$…_ |
| Context Specificity | UX Trust | P1 | _L1 / L2 / L3_ | _$…_ |
| Source Attribution Failure | Robustness | P1 | _L1 / L2 / L3_ | _$…_ |
| Data Bias | Fairness | P2 | _L1 / L2 / L3_ | _$…_ |
| Cost Overruns | Latency | P3 | _L1 / L2 / L3_ | _$…_ |

_Reference L3 costs: Hallucination $85K · Context $70K · Attribution $65K · Bias $55K · Latency $25K. L2 ≈ 10% of L3, L1 ≈ 5% of L3._

## Fallback methods (non-Level 3 items)

### L_n_ · _Failure name_ (_metric_ · _risk_)
- **Method:** _the cheaper fallback you'll run instead of L3_
- **Why this fallback is defensible:** _the story you could defend in a customer incident review — especially if you downgraded a P0/P1._
