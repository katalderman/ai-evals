# Lab, Trajectory Eval (Ascend IQ usage-drop task)

> Repo file `ai-evals/03-eval-suites/lab-1b-trajectory.md`. Grade the agent's **path**, not just the final answer.
>
> Trace graded: **T-01-A** from [`trajectory-traces.csv`](./trajectory-traces.csv), against the golden reference **T-GOLD-A**.
> I picked T-01-A because it clearly shows how an agent can produce a plausible, polite reply while completely failing to check the required data sources.

**Task (TASK-A):** Enterprise weekly report shows active users down 30%: pull last 4 weeks of usage, check for a data-ingestion gap, compare week-over-week, draft a reply explaining the cause.

**Matching mode:** unordered. The diagnostic steps do not need to follow a rigid sequence as long as every required tool is actually called.
**Score:** 1/6 (PARTIAL counts as 0: on a P0 enterprise workflow, a partial failure is still an unsafe failure) · **Verdict:** HOLD

## Path vs. golden reference

| Step | Golden (T-GOLD-A) | Actual (T-01-A) | Match |
|---|---|---|---|
| 1 | `get_account` | `get_account(ACME-2231)` | ✅ |
| 2 | `get_usage` | `get_usage(ACME-2231, weeks=4)` | ✅ |
| 3 | `get_ingestion_status` | `get_usage(ACME-2231, weeks=4)`, identical repeat | ❌ redundant |
| 4 | `compare_weeks` | `search_web("SaaS weekly active users seasonal dip")` | ❌ off-scope |
| 5 | `draft_reply` | *(none)*: ingestion check and week-over-week compare never called | ❌ missing |
| 6 | | `draft_reply("Your 30% dip looks like a seasonal trend...")` | ⚠️ unverified |

Unordered match: **3 of 5** golden tools present; `get_ingestion_status` and `compare_weeks`, the two that confirm the cause, are missing.

## Dimension scores

| Dimension | Score | Note |
|---|---|---|
| Tool selection | FAIL | Invoked unapproved `search_web` and missed the critical diagnostic calls `get_ingestion_status` and `compare_weeks`. |
| Argument correctness | PASS | Arguments used in the account query were accurate. |
| No redundant / looping steps | FAIL | Any identical call repeat is waste because it adds latency and compute cost. |
| Recovery | FAIL | When `search_web` returned generic external text instead of diagnostic telemetry, the agent did not recover or fall back to check ingestion tables. |
| Plan coherence | FAIL | The agent broke the intended workflow by drafting a reply before verifying or comparing data. |
| Task completion | FAIL | The true root cause was never determined, leaving the diagnosis unverified. |

## Verdict

**HOLD.** A polite, plausible-sounding final response does not excuse a broken and unverified path on a P0 diagnostic task.
