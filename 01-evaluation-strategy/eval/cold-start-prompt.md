# Cold-start prompt used to seed the starter dataset

> Given to an assistant to generate the ~20 starter rows in `dataset.json`.

You are helping me cold-start an evaluation dataset for **Ascend IQ**, a RAG-backed
analytics copilot inside a B2B SaaS analytics product. Its users are RevOps and
Customer Success leads at mid-market SaaS companies — business operators who cannot
write SQL and cannot independently verify an answer.

Generate **20 evaluation rows** as JSON. Each row is:

    {
      "id":       "R01",
      "category": "supported" | "partial" | "unanswerable" | "pricing",
      "query":    "a plain-language question a RevOps lead would actually ask",
      "sources":  [ { "id": "S1", "text": "a retrieved chunk" }, ... ],
      "tests":    "one line: what this row is designed to catch"
    }

The `sources` array is the ONLY context the copilot will be given. This is the
critical constraint: I am evaluating whether the copilot's claims are traceable to
these sources, so what is *absent* from `sources` matters as much as what is present.

Use exactly this mix:

- **8 `supported`** — sources contain both the figure AND the reason behind it.
  A good answer is fully citable. These should be genuinely answerable.
- **4 `partial`** — sources contain the FIGURE but NOT the CAUSE, while the query
  asks "why". There must be no plausible cause anywhere in the sources. These rows
  exist to catch a copilot that invents an explanation to sound useful.
- **4 `unanswerable`** — the sources do not cover the question at all (industry
  benchmarks, forecasts, competitor data, fields we don't collect). The only
  correct behaviour is to say so.
- **4 `pricing`** — pricing or contract questions. Make **2 of them supported**
  (the price or clause is verbatim in sources) and **2 unsupported** (discount
  authority, overage terms — not in sources). Zero tolerance for an invented price.

Rules:
- Use consistent fictional account names across rows (Blackridge Logistics,
  Meridian Health, Cobalt Freight) so the set reads like one real product.
- Put real, specific numbers in the sources — seat counts, percentages, dates,
  ticket IDs. Vague sources make traceability impossible to grade.
- Never let a `partial` or `unanswerable` row accidentally contain the answer.
  Re-read each one and confirm the information genuinely is not there.
- Do not write the expected answers. I am evaluating two prompt versions against
  these rows; pre-writing answers would bias the comparison.

Return only the JSON array.
