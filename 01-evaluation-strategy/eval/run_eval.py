"""
Ascend IQ, first LLM-as-a-Judge eval (Module 1).

Generator : OpenAI (GPT family)       - writes the Version A / Version B answers
Judge     : Anthropic (Claude family) - grades them

The generator and judge are deliberately from different model families. A judge
scoring output from its own family shows self-preference bias, which would make
the A/B comparison meaningless.

Usage:  python 01-evaluation-strategy/eval/run_eval.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Literal

import anthropic
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

HERE = Path(__file__).parent
load_dotenv(HERE.parents[1] / ".env")

JUDGE_MODEL = os.getenv("JUDGE_MODEL", "claude-opus-5")
OPENAI_MODEL_PREFERENCE = [
    os.getenv("OPENAI_MODEL"), "gpt-4o-mini", "gpt-4.1-mini", "gpt-4o", "gpt-4.1",
]

# --------------------------------------------------------------------------
# The two system prompts under test
# --------------------------------------------------------------------------

VERSION_A = """You are Ascend IQ, the analytics copilot inside Ascend Analytics.
You answer questions for RevOps and Customer Success leads who cannot write SQL
and cannot check your work.

Rules:
- Answer in at most 3 sentences. Lead with the number and the direction.
- Every figure, date, account name and price you state must appear verbatim in
  the SOURCES provided. Append a bracketed source id to each one, e.g. [S2].
- If the SOURCES do not support an answer, say exactly what is missing and stop.
  Do not estimate, extrapolate, or reason about what the number is likely to be.
- Never state a price, contract term, or legal position that is not in SOURCES."""

VERSION_B = """You are Ascend IQ, the analytics copilot inside Ascend Analytics.
You answer questions for RevOps and Customer Success leads who need to
understand what is going on, not just see a number.

Rules:
- Write a short explanatory paragraph. Give the number, then explain what is
  driving it and what it means for the account.
- Draw connections across the SOURCES: if two figures together suggest a cause,
  say so.
- Be helpful and decisive. The user is busy and needs a recommendation, so end
  with what you would do next.
- Cite sources where it is natural to do so."""

VERSIONS = {"A_concise_cited": VERSION_A, "B_narrative_synthesis": VERSION_B}

# --------------------------------------------------------------------------
# Golden-set criteria, in the learner's own words. This is the graded judgment
# call from Step 5, and it is what the judge enforces.
# --------------------------------------------------------------------------

GOLDEN_CRITERIA = """A GOOD Ascend IQ answer avoids the 95% accuracy trap: the information is
accurate, but it is also unbiased, consistent, and clear. A good answer gracefully declines to
answer rather than hallucinating. It provides context and clear evidence so the user can be
confident in it, and it drives task completion.

A BAD answer hallucinates or guesses. Or it is technically correct but useless. Or it fails by
being biased or by acting unpredictably."""

JUDGE_SYSTEM = f"""You are grading answers produced by Ascend IQ, a RAG-backed analytics copilot.

Its users are RevOps and Customer Success leads who cannot write SQL and CANNOT VERIFY THE
ANSWER THEMSELVES. That asymmetry is why grounding matters more than fluency here.

The product owner's definition of good and bad, which you must apply rather than substituting
your own taste:

{GOLDEN_CRITERIA}

You will be given the user's QUESTION, the SOURCES the copilot was given (the only context it
had), and its ANSWER. Grade only against the SOURCES. If a claim is not in the SOURCES it is
unsupported, no matter how plausible it sounds or how likely it is to be true in the real world.

Definitions you must apply strictly:

- unsupported_claims: every figure, date, account name, price, contract term, or asserted CAUSE
  in the answer that does not appear in the SOURCES. An invented explanation for a real number
  is an unsupported claim. Restating the question is not a claim. Generic advice containing no
  facts is not a claim.

- declines_gracefully:
    "not_applicable"    - the sources fully support an answer, so no decline was called for.
    "graceful"          - the answer declines AND names specifically what is missing or what it
                          would need. This is the target behaviour.
    "bare"              - the answer declines but leaves the user with nothing to act on.
    "failed_to_decline" - the sources did not support an answer and the copilot answered anyway.

- evidence_clarity (1-5): can the user tell where each claim came from and check it?
- task_completion (1-5): does the answer move the user toward a decision? An answer that is
  accurate but leaves the user no better off scores 1-2. This is the "technically correct but
  useless" failure, and it is a real failure rather than a minor deduction.
- bias (1-5): 5 means the answer represents the sources evenhandedly. Score low if it
  cherry-picks, overstates certainty, or shapes the facts into a more decisive story than the
  sources support.

Be a harsh, specific grader. Quote the offending text in your reasoning."""


class Verdict(BaseModel):
    unsupported_claims: List[str] = Field(
        description="Verbatim quotes of claims not supported by SOURCES. Empty list if none."
    )
    declines_gracefully: Literal["not_applicable", "graceful", "bare", "failed_to_decline"]
    evidence_clarity: int = Field(ge=1, le=5)
    task_completion: int = Field(ge=1, le=5)
    bias: int = Field(ge=1, le=5)
    reasoning: str = Field(description="Two or three sentences. Quote the specific text.")


def fmt_sources(row: dict) -> str:
    return "\n".join("[{}] {}".format(s["id"], s["text"]) for s in row["sources"])


# --------------------------------------------------------------------------
# Generation + judging
# --------------------------------------------------------------------------

def pick_openai_model(client: OpenAI) -> str:
    available = {m.id for m in client.models.list().data}
    for candidate in OPENAI_MODEL_PREFERENCE:
        if candidate and candidate in available:
            return candidate
    chat = sorted(m for m in available if m.startswith("gpt-"))
    if chat:
        return chat[0]
    sys.exit("No usable OpenAI chat model found. Available: {}".format(sorted(available)[:20]))


def generate(oa: OpenAI, model: str, system: str, row: dict) -> str:
    user = "SOURCES:\n{}\n\nQUESTION: {}".format(fmt_sources(row), row["query"])
    r = oa.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return (r.choices[0].message.content or "").strip()


def judge(an: anthropic.Anthropic, row: dict, answer: str) -> Verdict:
    user = (
        "QUESTION: {}\n\n"
        "SOURCES (the only context the copilot had):\n{}\n\n"
        "ANSWER:\n{}"
    ).format(row["query"], fmt_sources(row), answer)
    # claude-opus-5 runs adaptive thinking by default; no `thinking` param needed.
    r = an.messages.parse(
        model=JUDGE_MODEL,
        max_tokens=16000,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": user}],
        output_format=Verdict,
    )
    return r.parsed_output


def score(v: Verdict):
    """Apply the learner's any-fail rule. Returns (passed, reason)."""
    if v.unsupported_claims:
        return False, "hallucination: {} unsupported claim(s)".format(len(v.unsupported_claims))
    if v.declines_gracefully == "failed_to_decline":
        return False, "guessed instead of declining"
    if v.task_completion <= 2:
        return False, "technically correct but useless"
    if v.bias <= 2:
        return False, "biased or overstated"
    return True, "pass"


def main() -> None:
    rows = json.loads((HERE / "dataset.json").read_text(encoding="utf-8"))
    for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if not os.getenv(key):
            sys.exit("{} is not set. Copy .env.example to .env and fill it in.".format(key))

    # An org-level Anthropic key (not scoped to a single workspace) must name the
    # workspace on every request via a header. A workspace-scoped key does not.
    workspace = os.getenv("ANTHROPIC_WORKSPACE_ID")
    headers = {"anthropic-workspace-id": workspace} if workspace else None

    oa = OpenAI()
    an = anthropic.Anthropic(default_headers=headers)

    # Preflight the judge before spending anything on generation. A judge that
    # 400s after 40 generator calls wastes real money for no result.
    try:
        an.messages.create(
            model=JUDGE_MODEL, max_tokens=4,
            messages=[{"role": "user", "content": "ok"}],
        )
    except anthropic.APIStatusError as e:
        sys.exit(
            "Judge preflight failed ({}): {}\n"
            "Nothing was generated, so nothing was spent.".format(e.status_code, e.message)
        )

    gen_model = pick_openai_model(oa)
    print("generator : {} (OpenAI)".format(gen_model))
    print("judge     : {} (Anthropic)".format(JUDGE_MODEL))
    print("rows      : {} x {} versions = {} answers\n".format(
        len(rows), len(VERSIONS), len(rows) * len(VERSIONS)))

    jobs = [(vname, row) for vname in VERSIONS for row in rows]

    def run_one(job):
        vname, row = job
        answer = generate(oa, gen_model, VERSIONS[vname], row)
        verdict = judge(an, row, answer)
        passed, reason = score(verdict)
        print("  {}  {:22} {} {:12} {}".format(
            "PASS" if passed else "FAIL", vname, row["id"], row["category"], reason))
        out = {
            "version": vname, "id": row["id"], "category": row["category"],
            "query": row["query"], "answer": answer,
            "passed": passed, "fail_reason": None if passed else reason,
        }
        out.update(verdict.model_dump())
        return out

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run_one, jobs))
    print("\ncompleted in {:.0f}s\n".format(time.time() - t0))

    (HERE / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    report(results, rows, gen_model)


def report(results: list, rows: list, gen_model: str) -> None:
    cats = ["supported", "partial", "unanswerable", "pricing"]
    L = [
        "# Eval run, Version A vs Version B",
        "",
        "Generator `{}` (OpenAI) - Judge `{}` (Anthropic) - {} rows - different model families.".format(
            gen_model, JUDGE_MODEL, len(rows)),
        "",
        "## Headline: overall pass rate",
        "",
        "| Version | Pass rate | Rows with a hallucination | Failed to decline |",
        "|---|---|---|---|",
    ]
    for v in VERSIONS:
        rs = [r for r in results if r["version"] == v]
        halluc = sum(1 for r in rs if r["unsupported_claims"])
        nodecl = sum(1 for r in rs if r["declines_gracefully"] == "failed_to_decline")
        p = sum(1 for r in rs if r["passed"])
        L.append("| {} | **{}/{} ({:.0f}%)** | {} | {} |".format(
            v, p, len(rs), 100 * p / len(rs), halluc, nodecl))

    L += ["", "## Pass rate by row category", "",
          "| Version | " + " | ".join(cats) + " |", "|---|" + "---|" * len(cats)]
    for v in VERSIONS:
        cells = []
        for c in cats:
            rs = [r for r in results if r["version"] == v and r["category"] == c]
            cells.append("{}/{}".format(sum(1 for r in rs if r["passed"]), len(rs)))
        L.append("| {} | ".format(v) + " | ".join(cells) + " |")

    L += ["", "## Mean sub-scores (1-5)", "",
          "| Version | Evidence clarity | Task completion | Bias |", "|---|---|---|---|"]
    for v in VERSIONS:
        rs = [r for r in results if r["version"] == v]
        mean = lambda k: sum(r[k] for r in rs) / len(rs)
        L.append("| {} | {:.2f} | {:.2f} | {:.2f} |".format(
            v, mean("evidence_clarity"), mean("task_completion"), mean("bias")))

    # Behavioural-consistency proxy: on the rows where declining was the correct
    # move, did the version apply the same rule every time, or only sometimes?
    decline_rows = {"R09", "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R19", "R20"}
    L += ["", "## Behavioural consistency on the 10 rows that required a decline", "",
          "| Version | Declined gracefully | Declined bare | Failed to decline |",
          "|---|---|---|---|"]
    for v in VERSIONS:
        rs = [r for r in results if r["version"] == v and r["id"] in decline_rows]
        cnt = lambda k: sum(1 for r in rs if r["declines_gracefully"] == k)
        L.append("| {} | {}/{} | {}/{} | {}/{} |".format(
            v, cnt("graceful"), len(rs), cnt("bare"), len(rs),
            cnt("failed_to_decline"), len(rs)))

    L += ["", "## Every failure, with the judge's reasoning", ""]
    for v in VERSIONS:
        fails = [r for r in results if r["version"] == v and not r["passed"]]
        L.append("### {} - {} failures\n".format(v, len(fails)))
        for r in fails:
            L.append("**{}** ({}) - _{}_".format(r["id"], r["category"], r["fail_reason"]))
            L.append("> Q: {}".format(r["query"]))
            L.append("> A: {}".format(r["answer"][:400]))
            if r["unsupported_claims"]:
                L.append("> Unsupported: {}".format(r["unsupported_claims"]))
            L.append("> Judge: {}\n".format(r["reasoning"]))

    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote eval/results.json and eval/results.md")
    print("\n".join(L[:22]))


if __name__ == "__main__":
    main()
