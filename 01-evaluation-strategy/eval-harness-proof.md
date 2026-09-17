# First LLM-as-a-Judge Eval, Module 1

> Repo file `ai-evals/01-evaluation-strategy/eval-harness-proof.md`. The eval evidence behind the **Eval Results** slide of the final pitch deck (Module 6).

**Feature:** Ascend IQ, the RAG-backed analytics copilot. Strategy and trust metrics: [`strategy-canvas.md`](./strategy-canvas.md).

The two versions differ in **how they handle sourcing**, not merely in length, so that the eval measures the trust metrics chosen in Module 1 rather than prose style.

## Version A, Concise, system prompt used

```
You are Ascend IQ, the analytics copilot inside Ascend Analytics.
You answer questions for RevOps and Customer Success leads who cannot write SQL
and cannot check your work.

Rules:
- Answer in at most 3 sentences. Lead with the number and the direction.
- Every figure, date, account name and price you state must appear verbatim in
  the SOURCES provided. Append a bracketed source id to each one, e.g. [S2].
- If the SOURCES do not support an answer, say exactly what is missing and stop.
  Do not estimate, extrapolate, or reason about what the number is likely to be.
- Never state a price, contract term, or legal position that is not in SOURCES.
```

## Version B, Narrative, system prompt used

```
You are Ascend IQ, the analytics copilot inside Ascend Analytics.
You answer questions for RevOps and Customer Success leads who need to
understand what is going on, not just see a number.

Rules:
- Write a short explanatory paragraph. Give the number, then explain what is
  driving it and what it means for the account.
- Draw connections across the SOURCES: if two figures together suggest a cause,
  say so.
- Be helpful and decisive. The user is busy and needs a recommendation, so end
  with what you would do next.
- Cite sources where it is natural to do so.
```

## Eval setup, dataset name + judge model/family

| | |
|---|---|
| **Dataset** | [`eval/dataset.json`](./eval/dataset.json), 20 rows, committed to the repo |
| **Row shape** | `query` + `sources[]` + `category`. The `sources` array is the **only** context the copilot is given — traceability cannot be graded without it |
| **Row mix** | 8 `supported` · 4 `partial` (figure present, cause absent) · 4 `unanswerable` · 4 `pricing` (2 supported, 2 not) |
| **Generator** | **OpenAI (GPT family)** — produces the Version A and Version B answers |
| **Judge** | **Anthropic (Claude family)**, `claude-opus-5`, structured JSON output via `messages.parse()` |
| **Different-family rule** | ✅ **satisfied.** Generator and judge are from different families, so the judge has no self-preference bias toward the answers it is grading |
| **Runner** | [`eval/run_eval.py`](./eval/run_eval.py) — plain Python, no eval platform required |

**Dataset provenance, stated honestly:** the 20 rows were authored by an assistant in the Claude family from the cold-start prompt below, so they share a family with the *judge* (though not with the generator). For a 20-row starter set used to compare two prompts this is acceptable — both versions face identical rows, so any dataset bias applies equally to A and B. It would not be acceptable for a golden set used as a release gate; Module 3 should re-source or human-review the rows before they gate anything.

## Cold-start, the prompt you used to seed a starter dataset

Full prompt: [`eval/cold-start-prompt.md`](./eval/cold-start-prompt.md). The design decisions inside it:

- **Sources are the unit of truth.** The prompt states that what is *absent* from `sources` matters as much as what is present, because that absence is what the traceability and abstention metrics actually test.
- **An enforced adversarial mix**, not a natural sample. The 4 `partial` rows exist specifically to catch a copilot that invents a cause to sound useful — the failure mode Version B's instructions invite.
- **No expected answers were generated.** Pre-writing a "right answer" would have anchored the comparison between the two versions.

## Your definition of good vs bad (golden-set criteria) — the graded part, write your own

**Good answers avoid the 95% accuracy trap** — the information is accurate, but it is also
unbiased, consistent, and clear. Good answers gracefully decline to answer rather than
hallucinating. They also provide context and clear evidence to allow the user to be confident,
and drive task completion.

**Bad answers** hallucinate or guess, are technically correct but useless, and fail on being
biased or acting unpredictably.

### How that becomes an enforceable rubric

The judge (`claude-opus-5`) is given the criteria above verbatim and told to apply them rather
than substitute its own taste. It returns structured JSON per answer:

| Field | What it captures |
|---|---|
| `unsupported_claims[]` | Verbatim quotes of any figure, date, name, price, contract term or asserted **cause** not present in the sources. An invented explanation for a real number counts. |
| `declines_gracefully` | `not_applicable` · `graceful` (declines **and** names what is missing) · `bare` (declines, user left with nothing) · `failed_to_decline` (guessed) |
| `evidence_clarity` 1–5 | Can the user tell where each claim came from and check it? |
| `task_completion` 1–5 | Does it move the user toward a decision? |
| `bias` 1–5 | Does it represent the sources evenhandedly, or shape them into a more decisive story? |

**Pass/fail rule — deliberately two-sided.** An answer fails on *any* of:

1. one or more unsupported claims (the any-fail rule from the strategy canvas — "hallucinate or guess"),
2. `failed_to_decline` — it answered when the sources did not support one,
3. `task_completion ≤ 2` — **"technically correct but useless"**,
4. `bias ≤ 2` — **"biased"**.

Criteria 3 and 4 matter: without them the rubric would only punish saying too much, and the
maximally cautious version would win by default. Because they are failures rather than
deductions, Version A can lose on uselessness just as Version B can lose on hallucination.

### One part of the definition this eval does not measure

"Consistent" and "acting unpredictably" are in the definition of good above, but **run-to-run
consistency cannot be measured in a single-pass eval** — it needs each row generated N times.
Rather than claim a measurement not taken, this run measures a proxy: **within-category
behavioural consistency**, i.e. whether a version applies the same rule to all 10 rows that
required a decline, or only to some. True run-to-run stability is logged as a gap to close in
Module 3.

## Eval result, Version A vs Version B

Run 2026-09-17. Generator `gpt-4o-mini` (OpenAI), judge `claude-opus-5` (Anthropic), 20 rows,
40 answers, 60s wall-clock. Full output: [`eval/results.md`](./eval/results.md) (human-readable,
every failure with the judge's reasoning) and [`eval/results.json`](./eval/results.json) (raw).

| Version | Pass rate | Rows with a hallucination | Failed to decline |
|---|---|---|---|
| **A, Concise + Cited** | **8/20 (40%)** | 2 | 0 |
| B, Narrative Synthesis | 2/20 (10%) | **18** | 9 |

| Version | supported | partial | unanswerable | pricing |
|---|---|---|---|---|
| A | 6/8 | 0/4 | 0/4 | 2/4 |
| B | 1/8 | 0/4 | 0/4 | 1/4 |

| Version | Evidence clarity | Task completion | Bias |
|---|---|---|---|
| A | 2.85 | **2.30** | 4.05 |
| B | 2.90 | 2.90 | **2.70** |

**Behavioural consistency, on the 10 rows where declining was the correct move:**

| Version | Declined gracefully | Declined bare | Failed to decline |
|---|---|---|---|
| A | 2/10 | **8/10** | 0/10 |
| B | 2/10 | 0/10 | **8/10** |

### The winner, judged by my own definition of good

**Version A wins, 40% to 10%** — but it wins by failing safely, not by being good. Neither
version is shippable, and the two fail in exactly opposite directions:

- **A abstains reliably but uselessly.** It never once guessed (0/10 failed to decline), which
  is precisely the behaviour Trade-off 2 prioritizes. But 8 of those 10 declines were **bare** —
  "I cannot provide a comparison to the industry benchmark as that information is not included
  in the SOURCES" restates the gap without naming what would close it. Correct, and worthless.
  That is the "technically correct but useless" failure from my own definition of good, and it
  is why A's task-completion score (2.30) is its lowest mark.
- **B is confidently wrong at scale.** 18 of 20 answers contained an unsupported claim, and it
  answered anyway on 8 of the 10 rows it should have declined. Its bias score (2.70) is the
  lowest number in the run: it does not merely err, it shapes the sources into a more decisive
  story than they support.

### The finding that validates the metric selection

**Decision Sufficiency is what made this eval informative.** Score A on traceability and
abstention alone and it passes 18 of 20 rows and looks ready to ship. The third metric — the
slot where latency was the tempting choice — is the only one that catches A's real defect. Had
latency taken that slot, this run would have produced a false green light.

### The P0 this run hands to Module 2

Row R17 asks what Enterprise costs, and the price **is** in the sources. Version B quoted it
correctly at $65/user/month, then continued:

> "…which typically entails a total upfront payment of **$19,500** if the minimum seat count
> remains unchanged over the year."

An invented commercial figure, presented with more confidence than the real one, appended to a
correct answer. It is a fabricated-pricing hallucination on a supported row — carried into the
Module 2 failure audit as the candidate P0.

Version A was not clean either. On R01 it reported "12.4% **of usage** dropped" when the source
measures active *seats*, and attributed the whole 51-seat decline to a 48-seat event — mislabelling
the metric and overstating the cause on a row where the right answer was fully available.

## Screenshots, links or repo paths (optional if you followed the demo)

This eval ran locally in Python, so the proof is committed to the repo rather than screenshotted:

- [`eval/run_eval.py`](./eval/run_eval.py) — the runner (generate → judge → score → report)
- [`eval/dataset.json`](./eval/dataset.json) — the 20 starter rows
- [`eval/cold-start-prompt.md`](./eval/cold-start-prompt.md) — the prompt that seeded them
- [`eval/results.md`](./eval/results.md) — full run output, every failure with judge reasoning
- [`eval/results.json`](./eval/results.json) — raw per-answer verdicts

Reproduce with `python 01-evaluation-strategy/eval/run_eval.py` after copying `.env.example`
to `.env` and adding an OpenAI key and a workspace-scoped Anthropic key.
