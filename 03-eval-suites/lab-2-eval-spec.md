# M3 · Lab 2 · Eval Spec, Ascend IQ P0

> Repo file `ai-evals/03-eval-suites/lab-2-eval-spec.md`. The PM's contract for what "good" means and how it's enforced.
>
> Fill this with the **Eval Spec Builder** tool, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

## Part 1 · The 5-Part Eval Spec

| Question | Answer |
|---|---|
| **01 · Target Risk** | _…_ |
| Risk Type | _Output / Trajectory_ |
| Trust Metric | _Hallucination / UX Trust / Robustness / Fairness / Latency_ |
| **02 · Evaluator** | _Code-Based / Per-turn Classifier / LLM-as-Judge / Human Eval / Hybrid_ |
| Detection logic | _…_ |
| **03 · Threshold** | _a number — e.g. 100% accuracy · ±0.5% · tone ≥ 4/5 · κ ≥ 0.6_ |
| Strategy | _Safety First (max TPR) / Growth First (max TNR) / Balanced_ |
| **04 · Business Stakes** | _…_ |
| **05 · Owner** | _…_ |

## Trajectory fields

_Only if Risk Type = Trajectory. Otherwise delete this section._

| Field | Answer |
|---|---|
| Dimensions scored | _e.g. Tool selection, Argument correctness, Task completion_ |
| Matching mode | _Strict / Unordered / Subset / Superset_ |

## Part 2 · Three Audience Messages

### A. For Engineering (Jira ticket)

_Acceptance criteria in IF/THEN (GIVEN/WHEN/THEN) form — not vibes._

### B. For UX / Design

_The fallback experience when the gate blocks a response._

### C. For Leadership (bi-weekly update)

_One ROI bullet: risk avoided + coverage + what you're tracking._
