# Lab, Trajectory Eval (Ascend IQ usage-drop task)

> Repo file `ai-evals/03-eval-suites/lab-1b-trajectory.md`. Grade the agent's **path**, not just the final answer.
>
> Fill this with the **Trajectory Eval Lab** tool, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.
>
> **More paths to practice on:** `trajectory-traces.csv` (same folder) holds six richer recorded trajectories — a golden reference plus five with distinct failure modes (redundant loops, a hallucinated tool, wrong-order drafting, wrong-argument calls, off-scope steps). Grade any of them with the same rubric.

**Matching mode:** _strict / unordered / subset / superset_ (default to **unordered** — strict is over-used)
**Score:** _…/6_ · **Verdict:** _SHIP / HOLD_

## Dimension scores

| Dimension | Score | Note |
|---|---|---|
| Tool selection | _PASS / PARTIAL / FAIL_ | _…_ |
| Argument correctness | _PASS / PARTIAL / FAIL_ | _…_ |
| No redundant / looping steps | _PASS / PARTIAL / FAIL_ | _…_ |
| Recovery | _PASS / PARTIAL / FAIL_ | _…_ |
| Plan coherence | _PASS / PARTIAL / FAIL_ | _…_ |
| Task completion | _PASS / PARTIAL / FAIL_ | _…_ |

## Verdict

_e.g. HOLD — the reply sounds plausible, but the agent skipped the ingestion check and the week-over-week compare (task completion fail), so the "seasonal" cause is unverified. A passing-looking answer does not excuse a failed path on a P0._
