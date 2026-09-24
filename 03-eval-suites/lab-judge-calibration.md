# Lab, Judge Calibration (Ascend IQ grounding rubric)

> Repo file `ai-evals/03-eval-suites/lab-judge-calibration.md`. Extra practice (async). Revise the rubric until **κ ≥ 0.60**.
>
> **Calibrated on our own M2 audit, not generic traces.** Judge verdicts: `02-failure-discovery/eval/judge-scores.json` (`claude-opus-5`, the M2 rubric, reused verbatim in the M3 suite). Human labels: `02-failure-discovery/audit-log.md` after overrides. Computed in [`eval/eval_lab.ipynb`](./eval/eval_lab.ipynb) §7, no API calls. Using our own audit data ties the calibration directly to the dataset our P0 came from.

**Cohen's κ:** **0.76** (substantial agreement) — **PASSES** the κ ≥ 0.60 gate

- Traces labeled: 20/20
- Raw agreement p₀: 90%
- Chance agreement pₑ: 57.5%
- Disagreements: 2 (rows 13, 18)

### Confusion matrix (judge × you)

| | You: PASS | You: FAIL |
|---|---|---|
| **Judge: PASS** | 5 | 0 |
| **Judge: FAIL** | 2 | 13 |

**Zero false passes.** The judge never passed an answer I failed, including the P0 (row 1), where we agree on FAIL.

## Diagnosis

Both disagreements are the same bias, and it is the opposite of the classic "rewards length" failure: **the judge penalises correct guardrail refusals.**

| Row | Query | Judge | Me | Why |
|---|---|---|---|---|
| 13 | Summarize the lawsuit mentioned in the WSJ about Competitor Z. | FAIL | PASS | Reference mandates refusal ("Refuse legal queries"); the agent declined correctly. |
| 18 | What database backend does DataViz use? | FAIL | PASS | Non-public internals; the agent declined correctly. |

This was by design in M2: the judge was deliberately *not* told the human-override rule, so correct refusals would surface for a human to overturn. Row 8 (SOC2, answer present in the reference) is a decline we agree is a FAIL, which shows the judge isn't blind to refusals. It just can't tell a mandated refusal from an over-refusal, because the rubric doesn't ask it to.

## Rubric revision

**Decision: keep the judge rubric unchanged and move refusal policy to Layer 2.**

- **Clean layer separation.** Refusals for legal, compliance, and internal architecture questions are deterministic policy boundaries, not subjective semantic evaluations. Layer 2 is explicitly built to act as the policy/refusal gate, while Layer 3 should remain focused strictly on factual grounding and hallucination detection against retrieved sources.
- **Efficiency and token cost.** Moving refusal logic to Layer 2 avoids running 20 unnecessary judge API calls and keeps the evaluation pipeline modular and cost-effective.
- **Zero false passes.** The judge already achieved κ = 0.76 (well above the ≥ 0.60 threshold) and produced 0 false passes, correctly catching our P0 failure. Documenting that the 2 false failures stem from Layer 2 policy overrides maintains clear architectural rigor.

**Suite rule:** if Layer 2 marks the query refusal-mandated **and** the agent declined → PASS; otherwise the judge's verdict stands.

### Re-measure (notebook §7b, no new judge calls)

| Configuration | κ | p₀ | Gate |
|---|---|---|---|
| Judge alone | 0.76 | 90% | PASSES |
| Judge + Layer 2 refusal policy | **1.00** | 100% | PASSES |

Rows 13 and 18 flip FAIL → PASS; **row 8 stays FAIL** (not refusal-mandated, so the over-refusal is still caught).

**Caveat, read before quoting 1.00.** This is an in-sample result: the Layer 2 refusal patterns were written after seeing rows 13 and 18, so they are guaranteed to match them. It shows the layer split works on the rows that exposed the bias; it does not show Layer 2 generalizes to unseen refusal-mandated queries. The honest headline number is the judge's **κ = 0.76 with zero false passes**.

## Follow-up: Pricing Gold Set (N ≥ 30)

This calibration contains **only 1 pricing row** (the P0). That makes the judge directionally sound on this dataset. It does not make it calibrated on pricing, and the Lab 2 threshold ("100% current-price accuracy on the pricing gold set") depends on a set that doesn't exist yet.

- **Build:** ≥ 30 pricing queries with human labels, mixing current-price answers, stale-price answers (old and new both in the source), sources with no version label (the judge-fallback path), and answerable pricing queries that must *not* be refused (over-refusal guard).
- **Measure:** judge κ ≥ 0.60 on that set, plus the Layer 1 current-price rule's catch rate, before production release.
- **Why it matters for the pitch:** acknowledging that our current 20-row calibration contains only 1 pricing failure demonstrates strong PM credibility and rigor. It proves we know our judge is directionally sound, while showing leadership that our Lab 2 "100% pricing accuracy" threshold requires a dedicated, scaled test set before production release.
