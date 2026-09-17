# Lab, CI Eval Gate Policy (Ascend IQ PR #218)

> Repo file `ai-evals/04-eval-gates/lab-ci-gate-policy.md`. Output of the **CI Gate demo** (instructor-led): PR #218 swaps the Ascend IQ retrieval prompt; a 30-case regression golden set is replayed on every PR. You set floors + max-regression per dimension, decide blocking vs warn-only, then make the merge call.
>
> Fill this with the **CI Gate Demo** tool, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

| Dimension | main | PR | Δ | Floor | Max reg | Blocking | Result |
|---|---:|---:|---:|---:|---:|---|---|
| Faithfulness (grounding) | 96 | 87 | −9 | 90 | 3 | yes | _PASS / FAIL_ |
| Task completion | 92 | 93 | +1 | 85 | 5 | yes | _PASS / FAIL_ |
| Tool selection | 90 | 88 | −2 | 80 | 5 | yes | _PASS / FAIL_ |
| Safety / policy | 99 | 99 | 0 | 98 | 1 | yes | _PASS / FAIL_ |
| Latency (p95) | 84 | 80 | −4 | 70 | 8 | no | _PASS / FAIL_ |
| Cost per task | 88 | 82 | −6 | 70 | 10 | no | _PASS / FAIL_ |

**Gate result:** _BLOCKED / PASSED_

## Merge decision

_e.g. BLOCK merge — faithfulness regressed 9 pts past the 3-pt limit and fell below the 90 floor on a P0 blocking dimension. Warn-only dimensions (latency, cost) don't block._
