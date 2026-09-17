# M3 · Lab 1a · Runnable Eval Suite, Ascend IQ P0 Run

> Repo file `ai-evals/03-eval-suites/lab-1-eval-suite.md`. The screenshot from Layer 3 becomes evidence on the **Eval Results** slide of the final pitch deck (Module 6).
>
> **How to run this lab.** Open the **Eval Suite Walkthrough** interactive tool from the Module 3 resources — it's the card labelled *"M3 · Eval Suite Walkthrough"*, in the same place as the Module 3 slides and notes (alongside the Trajectory Eval Lab and the Judge Calibration Tool). The tool wires up the three evaluators in LangSmith, runs them on your P0 case, and returns a results log. Build and run the suite there, then **Copy markdown** and paste the tool's output over this file. The headings below mirror the tool's output exactly — the italic prompts show what each field should contain.

## P0 Failure (carried from Module 2)

_Use the single P0 failure you tagged in your Module 2 failure audit (the Ascend IQ beta-log run). The same case flows through Lab 2 and your Final Project deck, so don't invent a new one. Replace the italic examples below with your case._

- **Query:** _the user request that triggered the failure — e.g. "What is Ascend IQ's Enterprise pricing?"_
- **Prediction:** _what the agent actually answered — e.g. "Ascend IQ Enterprise starts at $49/user/month with a 10-seat minimum."_
- **Reference:** _the verified ground truth it should have matched — e.g. Source: pricing page. Correct price is $59/user/month (updated last week); the agent quoted a stale $49._

## 3-Layer Eval Suite Results

_These scores come straight from the Eval Suite Walkthrough tool: it runs your Query + Prediction through each layer and returns **1 = caught the failure** (the layer flagged the output) or **0 = missed it**, plus the reasoning. Paste the tool's output into the table. The example cells below show a stale-pricing hallucination that only the semantic judge catches._

| Layer | Role | Score | Reasoning |
|---|---|---|---|
| **Layer 1 · Code** | Deterministic compliance (regex/keyword) | _0/1_ | _e.g. 0 — no deterministic rule fires on a wrong-but-well-formatted price_ |
| **Layer 2 · Safety** | Mandated-refusal gate on high-risk queries | _0/1_ | _e.g. 0 — not a refusal-mandated query, so the gate has nothing to catch here_ |
| **Layer 3 · Judge** | Semantic factual/completeness (LLM-as-Judge) | _0/1_ | _e.g. 1 — judge caught the $49 vs $59 factual error against the reference_ |

## Where the failure was caught, and what it means

_Read the layer scores above against this logic (the "reading the result" table from the walkthrough), then state which case you're in:_

- **Layer 1 or 2 caught it (scored 1) → the Win.** A fast, cheap rule operationalized the risk. Sanity-check: did it catch the real problem, or just a formatting issue?
- **Only Layer 3 caught it → the Insight.** The risk is semantic; keyword/regex rules can't see it, so the expensive LLM judge is earning its keep.
- **Nothing caught it (all 0) → the Gap.** The suite is too loose. Tighten the judge's rubric or add a human-eval layer.

> _One line: which of the three is your run, and why._

## What I'd ship next

_The single most important change to the suite based on this run — the fix that would catch this P0 (and its neighbours) fastest and cheapest next time. Pick one and say why. Concrete examples:_

- _Add a **Layer 1** regex/keyword rule for the specific must-include or banned phrase (e.g. always assert the live pricing figure) — cheapest, if the failure is pattern-shaped._
- _Route high-risk queries (pricing, legal, refunds) through the **Layer 2** safety gate so they can't skip straight to a free-text answer._
- _Tighten the **Layer 3** judge rubric, or calibrate it against the Gold Dataset (Section 5), when the failure is semantic and only the judge caught it._

> _Your pick + one sentence on why it's the highest-leverage change._
