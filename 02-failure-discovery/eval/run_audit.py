"""
Ascend IQ failure audit, Module 2.

Unlike M1, nothing is generated here. The 20 predictions ship with the dataset;
this script only judges them.

Judge : Anthropic (Claude family) - scores each prediction 1 (PASS) / 0 (FAIL)
        against the reference.

The judge is deliberately NOT told the human-override rule (that refusing a
private / legal / unauthorized request is correct guardrail behaviour). It
grades faithfulness to the reference and nothing else, so the refusal rows come
back as FAILs and the human has to overturn them. That override is the lab.

Usage:  python 02-failure-discovery/eval/run_audit.py
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Literal

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

HERE = Path(__file__).parent
load_dotenv(HERE.parents[1] / ".env")

JUDGE_MODEL = os.getenv("JUDGE_MODEL", "claude-opus-5")

# --------------------------------------------------------------------------
# What the judge enforces. Same golden criteria as M1, restated for a set where
# the reference is a single retrieved source rather than a source list.
# --------------------------------------------------------------------------

JUDGE_SYSTEM = """You are auditing answers produced by Ascend IQ, a RAG-backed analytics copilot.

Its users are RevOps and Customer Success leads who cannot write SQL and CANNOT VERIFY THE
ANSWER THEMSELVES. That asymmetry is why grounding matters more than fluency here.

You will be given the user's QUERY, the REFERENCE (the retrieved source, which is the ground
truth), and the copilot's PREDICTION. Grade the PREDICTION only against the REFERENCE. If a
claim is not supported by the REFERENCE it is unsupported, no matter how plausible it sounds or
how likely it is to be true in the real world.

Score 0 (FAIL) if ANY of these hold:
- The prediction states something the reference contradicts, including a stale value the
  reference has since updated.
- The prediction asserts as settled something the reference marks as tentative, partial,
  conditional, or available only via a workaround.
- The prediction omits a fact from the reference that materially changes the decision the user
  would make (e.g. a comparison that leaves out which side is worse).
- The prediction declines to answer. Score the decline 0 here and record it in `is_refusal`;
  whether the decline was correct is a human call made downstream, not yours.
- The tone breaks a voice or style rule stated in the reference.

Score 1 (PASS) only if the prediction is fully supported by the reference and complete enough
to act on.

Be a harsh, specific grader. Quote the offending text in your reasoning."""


class Verdict(BaseModel):
    score: Literal[0, 1] = Field(description="1 = PASS, 0 = FAIL.")
    is_refusal: bool = Field(
        description="True if the prediction declines to answer rather than answering."
    )
    unsupported_claims: List[str] = Field(
        description="Verbatim quotes from the prediction not supported by the reference. "
                    "Empty list if none."
    )
    reason: str = Field(description="One line, <=25 words. Quote the specific text.")


def judge(an: anthropic.Anthropic, row: dict) -> Verdict:
    user = (
        "QUERY: {query}\n\n"
        "REFERENCE (ground truth):\n{reference}\n\n"
        "PREDICTION:\n{prediction}"
    ).format(**row)
    # claude-opus-5 runs adaptive thinking by default; no `thinking` param needed.
    r = an.messages.parse(
        model=JUDGE_MODEL,
        max_tokens=16000,
        system=JUDGE_SYSTEM,
        messages=[{"role": "user", "content": user}],
        output_format=Verdict,
    )
    return r.parsed_output


def main() -> None:
    with (HERE / "ascend-iq-sample-data.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in.")

    # An org-level Anthropic key (not scoped to a single workspace) must name the
    # workspace on every request via a header. A workspace-scoped key does not.
    workspace = os.getenv("ANTHROPIC_WORKSPACE_ID")
    headers = {"anthropic-workspace-id": workspace} if workspace else None
    an = anthropic.Anthropic(default_headers=headers)

    try:
        an.messages.create(
            model=JUDGE_MODEL, max_tokens=4,
            messages=[{"role": "user", "content": "ok"}],
        )
    except anthropic.APIStatusError as e:
        sys.exit("Judge preflight failed ({}): {}\nNothing was spent.".format(
            e.status_code, e.message))

    print("judge : {} (Anthropic)".format(JUDGE_MODEL))
    print("rows  : {}\n".format(len(rows)))

    def run_one(row: dict) -> dict:
        v = judge(an, row)
        print("  {}{}  {}".format(
            "PASS" if v.score else "FAIL",
            " [refusal]" if v.is_refusal else "         ",
            row["query"][:62]))
        return {**row, **v.model_dump()}

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run_one, rows))
    print("\ncompleted in {:.0f}s".format(time.time() - t0))

    (HERE / "judge-scores.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    passed = sum(r["score"] for r in results)
    refusals = [r for r in results if r["is_refusal"]]
    print("\njudge pass rate: {}/{}".format(passed, len(results)))
    print("refusal rows needing a human override call: {}".format(len(refusals)))
    for r in refusals:
        print("  - {}".format(r["query"]))
    print("\nwrote eval/judge-scores.json")


if __name__ == "__main__":
    main()
