# BrotherDS: founder scope directive, 2026-08-12

Status: RECORDED, not designed and not built. This file captures a founder
directive at the moment it was given, so it is not reconstructed later from
memory. Nothing here has been turned into architecture yet, and the open
question in section 3 must be answered before anything is.

---

## 1. The directive, as given

BrotherDS is not started. It is the next step of the triumvirate. It will cover:

- Data Science
- Business Science
- Data Analytics
- Business Intelligence
- Business Analysis, upstream
- Project Management and delivery framework
- Value realization tracking
- A feedback loop for self-improvement
- Assistance to data science individuals and teams, to give the right answers
  through humans or through full agentic workflows
- Integration with the first target estate's data stack
- Delivery of customized and personalized answers by persona: per role, per
  objective, per customer
- All at a low inference cost, with the right delivery method and the right cost

---

## 2. What this changes about the existing understanding

Before this directive, the only written definition of BrotherDS was one sentence
inside BrotherSBE's analytics partnership design: that BrotherSBE owns
everything around the model and never the model itself, and that "a separate
product, BrotherDS, will own the science itself."

**That sentence is much narrower than this directive.** Owning the science is
one of thirteen items above. The directive adds the upstream question (what is
worth analysing at all), the delivery framework, value realization, a
self-improvement loop, personalization by persona, and an explicit cost
constraint on both inference and delivery.

The five-item handoff package contracted in that same BrotherSBE spec (prepared
dataset with grain and snapshot id, evaluation harness with split definition,
metric definitions by name and formula, labelled holdout with who labelled it
and when, and the open questions stated rather than guessed) remains valid as
the interface for the science half. It does not cover the other twelve items.

---

## 3. THE OPEN BOUNDARY QUESTION, for the founder, not for an implementer

Two items in the directive sit on ground the other two products already hold:

- **Project Management and delivery framework.** BrotherMode already owns the
  plan, the decisions, the progress page and the delivery packet for one
  person's work. BrotherSBE already owns the passage of a change between people,
  including its obligations, reviewers and approval.
- **Value realization tracking.** Neither existing product claims it, but it
  reads on the same objects: a change record, its evidence, and its outcome.

Left unresolved, this becomes three products each holding a partial answer to
"what is the state of this work", which is the exact failure the products were
built to prevent.

Three options, with what each costs:

**Option A: BrotherDS owns the question, the other two own the work.**
BrotherDS covers items 1 to 5 and 7 to 13, and explicitly does NOT build a
second project management or delivery framework. It reads BrotherMode's and
BrotherSBE's records rather than keeping its own. Cheapest, keeps one record per
object, and means the directive's item 6 is satisfied by integration rather than
by construction. **Recommended.**

**Option B: BrotherDS owns the analytical delivery lifecycle end to end**, with
its own project and delivery model for analytical work specifically, because
analytical work has a different shape from software change (a question can be
answered and still create no value). Costs a second record and a reconciliation
rule between the three.

**Option C: the triumvirate is restructured**, with delivery and value
realization lifted out of all three into a shared layer. Most correct in the
abstract, most expensive, and it would reopen decisions that are already
ratified in both existing products.

What would flip the recommendation: if analytical work genuinely cannot be
represented as a change record without distortion, Option A fails and Option B
becomes right. That is a design question worth one focused study before any
code, not a judgement to make in passing.

---

## 4. What is already true and should shape the design

Recorded here because they are established facts rather than assumptions.

- **The first target estate is a national beverage bottler and distributor**, and it is Snowflake-only, agentic-first,
  bilingual Japanese and English, with a commercial MVP for the CCO and the
  Commercial Leadership Team and a mid-October proof. Its native surface already
  includes Cortex Analyst, Cortex Search and Cortex Agents, semantic views, dbt
  model contracts, data metric functions, and Snowflake Trail.
- **Personalization by persona already has concrete personas in that estate:**
  the CCO and Commercial Leadership on the aggregate side, and the KAM and the
  merchandiser on the disaggregate side. "One governed view that aggregates for
  the CCO and disaggregates for a KAM or merchandiser" is an existing directive
  in that programme, not a new requirement.
- **The cost constraint is not decoration in this estate.** Snowflake already
  ships budgets and agent resource budgets that cap agent spend specifically.
  The low-inference-cost requirement should be met by using those, not by
  building a metering layer.
- **The estate forbids data leaving the environment.** Any BrotherDS design that
  extracts data to answer a question is dead on arrival there.
- **The estate's dominant fear is a confidently wrong number in front of
  leadership.** A personalization layer increases that risk rather than reducing
  it, because it multiplies the number of distinct answers given. Whatever
  BrotherDS becomes, per-persona answers have to reconcile to each other or the
  first month-end disagreement destroys it.

---

## 5. What must NOT be assumed from this file

- No architecture has been chosen.
- No overlap has been resolved. Section 3 is open.
- No timeline exists. BrotherDS is not scheduled and nothing in the pilot
  estate's or the first target estate's deployment phases depends on it.
- The relationship to `~/Documents/BrotherData-Copilot-Spec` has not been
  reconciled. That folder holds earlier related specification work and may
  contain decisions that contradict or duplicate this directive.
