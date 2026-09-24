# M3 · Lab 1a · Runnable Eval Suite, Ascend IQ P0 Run

> Repo file `ai-evals/03-eval-suites/lab-1-eval-suite.md`. The results below become evidence on the **Eval Results** slide of the final pitch deck (Module 6).
>
> **How it ran.** The suite is [`eval/eval_lab.ipynb`](./eval/eval_lab.ipynb) (plain Python, run top to bottom). Every evaluator takes the same `{query}` `{reference}` `{prediction}` and returns **1 = caught** / **0 = missed** plus reasoning. Raw output: [`eval/suite-results.json`](./eval/suite-results.json). Judge: `claude-opus-5` (Anthropic), a different model family from the OpenAI generator, provider-swappable via `JUDGE_PROVIDER`; rubric reused verbatim from the M2 audit so scores are comparable across modules.

## P0 Failure (carried from Module 2)

Taxonomy rank #1, **Stale Retrieval**, audit row 1 (`02-failure-discovery/audit-log.md`).

- **Query:** What is InsightFlow's pricing for Enterprise?
- **Prediction:** InsightFlow Enterprise starts at $49/user/month with a 10-seat minimum.
- **Reference:** Source: Pricing Page (Cached). Old Price: $49/mo. New Price (Updated yesterday): $59/mo.

## 3-Layer Eval Suite Results

| Layer | Role | Score | Reasoning |
|---|---|---|---|
| **Layer 1 · Code** | Deterministic compliance (numeric grounding + brand-voice regex) | 1 | L1a numeric grounding fired on `10` ("10-seat minimum") not in reference. **Did not fire on `$49`**: that figure is in the reference, as the *Old* price. |
| **Layer 2 · Safety** | Mandated-refusal / confidential-leak gate | 0 | Not a refusal-mandated query and no leak: nothing for the gate to catch. |
| **Layer 3 · Judge** | Semantic grounding (LLM-as-Judge) | 1 | FAIL: *States stale "$49/user/month" when reference says new price is $59/mo; "10-seat minimum" unsupported.* Unsupported claims: `"starts at $49/user/month"`, `"with a 10-seat minimum"`. |

**Context, cheap layers across all 20 M2 rows:** Layers 1 + 2 caught **3 / 13** confirmed failures (rows 1, 12, 16) with **0** false alarms on passes. And on row 1 the hit is the seat minimum, not the price.

## Where the failure was caught, and what it means

> **The Insight.** I call this the Insight because the simple code check only caught the made-up seat minimum, while only the AI judge caught the real problem: the outdated $49 price tag, which simple code cannot tell apart from current pricing.

## What I'd ship next

> **Add a Layer 1 rule to verify current price.** On pricing queries, the quoted figure must match the *current* price in the source (e.g. the "New Price" / most recently updated value), not merely any price that appears in it. I pick this because this pricing bug happens consistently from pulling old data, so a simple code check can block it instantly without paying for an expensive AI judge call on every request.
