# Module 4 · Launch Strategy · Section 4.0 Release Criteria

> Repo file `ai-evals/04-eval-gates/lab-2-launch-strategy.md`. Your PRD's release-criteria section: the numeric thresholds, the CI gate policy, and the mitigation lever for the Soft gate.
>
> Fill this with the **Launch Strategy Builder** tool, then **Copy markdown** and paste it over this file. The headings below mirror the tool's output exactly.

## 4.0 Release Criteria

| Severity | Metric | Threshold | Dataset | Method |
|---|---|---|---|---|
| Hard | _…_ | _e.g. = 0%_ | `Ascend_IQ_Logs` | _…_ |
| Soft | _…_ | _e.g. < 2%_ | `Ascend_IQ_Logs` | _[Example Spec]_ |
| Advisory | _…_ | _e.g. tone ≥ 4/5_ | `Ascend_IQ_Logs` | _[Example Spec]_ |

## 4.1 CI Gate Policy

> _Which per-dimension regression blocks the merge vs warns, referencing a regression golden set ≥ 30. Policy is per-dimension — never one blended "quality" number. Use deterministic fixtures/replay, not live model calls._

## 4.2 Mitigation Plan · Soft Gate

**Selected Lever:** _Staged Rollout / Feature Flagging / Beta Labeling / Delay Launch_

> _One sentence: how this lever contains the Soft-gate risk while you ship._
