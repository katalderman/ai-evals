# Lab, Judge Calibration (Ascend IQ grounding rubric)

> Repo file `ai-evals/03-eval-suites/lab-judge-calibration.md`. Extra practice (async). Label the 12 Ascend IQ grounding traces, compute κ, and revise the rubric until **κ ≥ 0.60**.
>
> Fill this with the **Judge Calibration** tool, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

**Cohen's κ:** _0.00_ (_interpretation_) — _PASSES / FAILS the κ ≥ 0.60 gate_

- Traces labeled: _…/12_
- Raw agreement p₀: _…%_
- Chance agreement pₑ: _…%_
- Disagreements: _…_

### Confusion matrix (judge × you)

| | You: PASS | You: FAIL |
|---|---|---|
| **Judge: PASS** | _…_ | _…_ |
| **Judge: FAIL** | _…_ | _…_ |

## Diagnosis

_e.g. The judge passed 2 verbose answers that padded with unsourced detail — it's rewarding length, not grounding._

## Rubric revision

_e.g. Add an explicit rule: "Any claim not traceable to the retrieved source = FAIL, regardless of fluency." Add a one-shot example of a fluent-but-ungrounded fail, then re-measure κ._
