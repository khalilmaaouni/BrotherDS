---
name: brotherds
description: Use when a number is about to reach a decision. Turns a figure into a checkable claim that carries its query, its grain, its uncertainty and what it does not establish, then runs ten refusals against it and returns PASS, FAIL or NO-DATA. Triggers include "what is our", "how much did", "did the promotion work", "what is the forecast", "is this number right", "can I put this in the deck", "elasticity", "incremental", "lift", "MAPE", "forecast accuracy", and any moment you are about to state a figure a person will act on.
---

# BrotherDS

Every number that reaches a decision carries its proof, and is scored later
against what actually happened.

## When this applies

The trigger is not "someone mentioned data". It is **a number is about to reach
a decision**. If the figure will sit in a deck, a plan, a business case or a
sentence somebody acts on, it is a claim and it needs a receipt. If it is
exploratory and nobody will act on it, say so and move on. Ceremony on throwaway
work is how a good control gets abandoned.

## The first thing to do, before any SQL

Ask what decision the number serves. If there is no answer, there is no claim,
only trivia. Write the decision down before writing the query, because the
decision determines the grain, and the grain determines the query.

## The five origins

Every claim names one. Most numbers in a business are not in a system, and
treating a vendor extract, an expert's judgement and an open hypothesis as if
they were all "data" is how commercial analysis goes wrong quietly.

| Origin | Use when | You must also capture |
|---|---|---|
| `SYSTEM` | it comes from a query against a governed source | two independent routes to the same number |
| `THIRD_PARTY` | vendor, panel or external dataset | provider, collection method, coverage, known biases |
| `ELICITED` | a person's judgement, however expert | their role, the protocol used, a calibration question, the seed score |
| `ASSUMPTION` | stated and unverified | who stated it, the plausible range, what the decision does across that range |
| `HYPOTHESIS` | openly untested | the test that would settle it, the cost of being wrong |

An `ELICITED` number is not worse than a `SYSTEM` one. A well-elicited expert
estimate often beats a badly-built query. What is fatal is not knowing which one
you are holding.

## The workflow

Authoring the claim is a side effect of doing the analysis, not a separate
JSON-writing chore. Talk the analyst through the plain-words version of the
schema, then hand the answers to `bds.py author` on stdin as `key=value` lines
(dotted keys nest one level, `not_established=` may repeat for each limit,
`evidence.derivation=name|sql` may repeat for each independent route to the
number). The tool writes the file and shows the G-gate result in the same
step; never open the JSON in an editor and type it by hand.

- What decision does this number serve, and the statement itself.
- Which of the five origins, honestly.
- The grain: one row per what.
- The uncertainty: an interval and its method, or `NOT_ESTABLISHED` and why.
- What this does NOT establish, at least one, never a formality.
- The derivation (SYSTEM: two independent SQL routes) or the origin's protocol
  (THIRD_PARTY/ELICITED/ASSUMPTION/HYPOTHESIS: see `bds.py --help`'s protocol
  fields, gate G8).

```bash
python3 bds.py author claims/rgm-014.json <<'EOF'
id=RGM-014
statement=State the claim in one sentence, in the decision maker's own words.
value=8123
unit=orders
origin=SYSTEM
question=What decision does this number serve?
decision=What changes depending on the answer?
grain=one row per order line, week ending 2026-08-16
uncertainty.kind=NOT_ESTABLISHED
uncertainty.why=this is a census, not a sample
not_established=Completeness against the order-management system was not checked.
not_established=Cancellations after the week close were not reconciled.
evidence.source=~/path/to/your.duckdb
evidence.derivation=fact table rollup|select sum(orders) from fact_order_line
evidence.derivation=monthly mart|select sum(orders) from mart_weekly
EOF
python3 bds.py receipt claims/rgm-014.json out.md # the page a human reads
python3 bds.py register claims/rgm-014.json       # make its metric definition the reference
python3 bds.py score claims/rgm-014.json 8123 "ops lead" 2026-09-30
python3 bds.py ledger claims/                     # the verified claim rate
```

`author` refuses to write anything with a missing required field (id,
statement, value, unit, origin, question, decision, grain, uncertainty,
not_established) and names what is missing; nothing is silently defaulted. Use
`bds.py new` only for a scaffold you intend to hand-fill outside a guided
conversation; `author` is the path this skill actually uses.

## Naming a metric, and why it matters more than the number

If the claim computes something with a name people use in meetings (GMV,
revenue, incremental volume, share), declare it:

```json
"metric": {"name": "GMV", "definition": "gross order value before cancellations,
           all wholesalers including demo accounts", "definition_source": "..."}
```

Gate G10 compares that definition against the registry. Two claims using one
name with two definitions is a FAIL that names both. This is the failure that
actually destroys trust in a commercial team: not a wrong number, but two right
numbers that disagree because nobody wrote down what the word meant.

First use is NO-DATA, because one claim proposes rather than defines. Run
`register` to make it the reference.

Turn the conversation straight into `bds.py author` stdin. Do not ask the
analyst to write JSON; run the command for them and show them the receipt.

## What you must never do

**Never fill `not_established` with a formality.** It is the field that makes the
receipt worth carrying. A reviewer reads it to know where to spend attention. If
you write "standard caveats apply" you have destroyed the only part a busy
person actually needs. Write the specific things this analysis did not settle:
the reconciliation nobody ran, the assumption nobody tested, the population that
was not checked.

**Never write causal language you cannot support.** "Drove", "caused",
"incremental", "lift", "impact of", "thanks to". Gate G4 refuses these unless the
claim names a design (randomised holdout, difference in differences, synthetic
control, event study, and so on) AND names the test that checked that design's
assumption. If there is no design, rewrite the sentence as an association, or
declare the claim a `HYPOTHESIS` and say what test would settle it.

**Never report an accuracy figure without a baseline.** A forecast is only good
relative to carrying the last value forward. Gate G6 computes that comparison and
will tell you when a model is worse than doing nothing, which happens more often
than people expect.

**Never let a language model be the final arbiter of arithmetic.** Propose with
the model, dispose with the mathematics. The measured reliability of language
models on exactly this work is poor: the best system on Spider 2.0 scores 30.35
percent. Anything a deterministic check could verify, verify deterministically.

## Reading the verdicts

- `PASS` the gate found what it needed and it held.
- `FAIL` the gate found something wrong. Fix the claim or fix the analysis.
- `NO-DATA` the claim needed something that was never measured. **This is not a
  pass and not a block.** It is the honest state of most real analysis, and
  saying so is the product working, not failing.

A claim with several NO-DATA verdicts is normal and useful. A claim with none is
either exceptional work or a claim whose author was not honest about its limits.

## What this does not do

It does not decide whether a claim is true. It decides whether the claim is
proven, disproven or unexamined. Truth arrives later, when the outcome does, and
the `outcome` field is where reality gets to grade the work. A gate verdict is a
statement about proof. Only an outcome is a statement about the world.

It also does not review a change to a pipeline. That is BrotherSBE's data
reviewer, which already covers grain, fan out, keys, system of record,
reconciliation, freshness and cost. Do not rebuild it; if a pipeline changed,
route there.

## Talking to the person

Outcome first, in plain words. Not "G4 returned FAIL on the causal predicate".
Instead: "This says the campaign drove the increase, but nothing here separates
the campaign from what would have happened anyway. Either soften the sentence to
an association, or run a holdout and we can claim it properly."

One recommended next action, never a menu.
