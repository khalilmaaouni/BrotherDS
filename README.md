# BrotherDS

**Every number that reaches a decision carries its proof, and is scored later
against what actually happened.**

BrotherDS is the third of three products. BrotherMode records what happened
during a piece of work. BrotherSBE decides whether a change to a system can be
trusted. BrotherDS takes a different unit: **the claim**, one number that
reaches a decision, and asks whether that number is true, what it does not
establish, and whether reality later agreed with it.

MIT licensed. No account, no service, no data leaves your machine.

## Why

A pipeline can be perfectly built, perfectly reviewed and perfectly released,
and still produce a number that is wrong. Change assurance does not catch that,
because nothing changed.

On the first evening this tool was pointed at a real warehouse it found that
2,350 product identifiers each covered more than one distinct product, so draft
beer and bottled beer had been silently merged in every per-product figure ever
computed there. Nothing was broken. Everything ran. The number was just wrong.

## Install

Python 3.9 or newer. One dependency, and only for claims that query a database.

```bash
pip install duckdb
```

## Use

A claim is a JSON file. Write one, then check it.

```bash
python3 bds.py check examples/example-descriptive.json
```

The engine re-runs every derivation, applies ten gates, and returns one of
three verdicts.

```
PASS      G9.grain                   one row per calendar month, whole network
PASS      G5.rederivation            2 independent derivations agree at 10,493,293,552
NO-DATA   G3.uncertainty             not established: this is a census, not a sample
FAIL      G6.baseline                does NOT beat carrying the last value forward
```

`PASS`, `FAIL`, `NO-DATA`. **NO-DATA is never a pass and never a block.** It
means the claim needed something that was never measured, which is a different
thing from the claim being wrong.

Then render the receipt a decision maker actually reads:

```bash
python3 bds.py receipt examples/example-descriptive.json
```

And verify the engine itself:

```bash
python3 bds.py selftest
```

## The ten gates

| Gate | What it refuses |
|---|---|
| G1 | an empty "what was not established" list |
| G2 | a claim that does not name one of the five evidence classes |
| G3 | a bare number with no uncertainty and no reason for its absence |
| G4 | causal language with no design, or a design whose assumption was never tested |
| G5 | a number reached by only one path |
| G6 | MAPE on near-zero denominators, accuracy with no baseline, seasonality on too little history |
| G7 | a stated value that no longer reproduces |
| G8 | an incomplete protocol for a non-system claim |
| G9 | a number with no declared grain, or a key that is not unique |
| G10 | two claims using one metric name with two different definitions |

## The five evidence classes

Most numbers in a business are not in any system. Treating a vendor extract, an
expert's judgement and an open hypothesis as if they were all "data" is how
commercial analysis goes wrong quietly.

- **SYSTEM** a query against a governed source. Interrogated by independent
  re-derivation.
- **THIRD_PARTY** a vendor or panel dataset. Interrogated on coverage,
  collection method and known biases. Its discount does not shrink as the sample
  grows.
- **ELICITED** expert or manual judgement. Interrogated with a calibration
  question, weighted by performance rather than equally (Cooke's classical
  model beat equal weighting in 32 of 33 cross validation studies).
- **ASSUMPTION** stated and unverified. Requires a sensitivity range and a
  result.
- **HYPOTHESIS** openly untested. May inform a test. May never alone reach a
  decision.

## What this is not

Not a dashboard, not a notebook, not an AutoML platform, not a data catalogue,
not an orchestrator, and not a replacement for a language model. It governs and
scores analytical work. It does not try to be a better general analyst than the
frontier models.

An LLM may sit in a verification path only as first-pass triage that a
deterministic check or a human confirms. It may never be the final arbiter of
arithmetic. The measured state of the art justifies this: the best system on
Spider 2.0 scores 30.35 percent, and Databricks' own documentation says
single-model text-to-SQL "fails a lot in production".

**The language model may propose. The mathematics disposes.**

## Honest limits

Read `SPEC.md` for the full list. The short version: nothing forces a claim to
exist; the "not established" field is checked for being non-empty and never for
being honest; the adjustment methods for the four non-system classes are
documented but not yet computed; and no claim has yet been scored against a real
outcome, so the north-star metric honestly reports NO-DATA rather than a zero.

Those are stated here rather than discovered later, because a limit that no file
enforces should say so.
