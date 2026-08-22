# The boundary study: does analytical work fit a change record?

Status: STUDY. It recommends. It does not ratify.
Date: 2026-08-16. Requested by: the founder directive of 2026-08-12, section 3,
which reserves this resolution for the founder and says of the question itself:
"That is a design question worth one focused study before any code, not a
judgement to make in passing."

This is that study. Nothing in it changes a boundary. Section 3 stays open until
the founder closes it.

A note on naming: this document uses role words (the pilot estate, the first
target estate) rather than the two client and company names that nine already
tracked files in this repository carry. The repository is private for exactly
that reason, and a public MIT release has to separate them first. New files do
not deepen the debt.

---

## The answer in one paragraph

No. Analytical work does not fit a change record without distortion, and the
evidence is concrete rather than theoretical: of the five real claims this
product ran on its first night, four cannot be keyed to a diff at all. But that
finding is narrower than it first looks, and reading it too widely would be the
expensive mistake. What does not fit is the UNIT, the claim itself. What fits
perfectly well is everything the founder's Option A was actually protecting: the
plan, the schedule, the progress page, the delivery packet. BrotherDS needs none
of those, has built none of them, and should build none of them.

So the recommendation splits the directive's two contested items rather than
answering them together, because the evidence answers them differently.

---

## The test, stated before it was run

A unit of analytical work fits a change record if it can be represented by
BrotherMode's ten-state task lifecycle and its five-field change passport
without losing information that a decision needs.

The passport's five fields, verbatim from the founder-authoritative chain
document: what was done (the change identity, its diff range, and the files it
touched), who did it, what was run, what was not established, where it came
from.

The failure signal is precise: the record cannot carry the claim's identity,
or cannot carry its resolution, or forces a many-to-one relationship where the
real one is many-to-many.

---

## The five cases, and what each did

These are the five claims this engine ran on the night of 2026-08-16, against a
real warehouse the founder owns outright. Each is described by its shape, not by
its numbers, because the numbers live in gitignored files.

**Case 1: a grain defect found by observation.** 2,350 identifiers in the
pilot estate each cover more than one distinct product, so every per-product
figure ever computed there has silently merged different things. Nothing was
changed to find this. No file was edited, no pipeline was modified, no release
happened. The passport's first field, the change identity and its diff range, is
empty, and it is the field the record is keyed on.
**Verdict: cannot be represented.** The most valuable output of the first night
of use has no row in a change record.

**Case 2: a base figure re-derived two ways.** This one could be attached to a
commit, if the SQL were committed. But the claim is not the SQL, the claim is
the number. One commit can produce six claims, and one claim can draw on three
commits and a spreadsheet somebody sent. The relationship between changes and
claims is many-to-many.
**Verdict: representable only by distortion.** Keying a claim on a diff range
forces a false cardinality, and the false cardinality is the kind that produces
two teams' worth of argument at month end.

**Case 3: a forecast that lost to its own naive baseline.** The verdict that
matters here, whether reality agreed, arrives one to three months after the work
is finished. In the change lifecycle, `monitored -> closed` is the last
transition and `closed` is terminal, with no move out, forward or backward, with
or without a reason. A claim scored MISSED after its record closed has nowhere
to go.
**Verdict: cannot be represented.** The lifecycle's terminal state lands before
the claim's decisive event.

**Case 4: a causal claim with no identification strategy.** The defect is in the
sentence somebody wrote next to the number, not in any code. There is nothing to
diff, and no file to name.
**Verdict: cannot be represented.**

**Case 5: a stated number that no longer reproduces.** It stopped reproducing
because the source moved underneath it, not because anybody changed anything on
the analytical side. The change record's question, what did you change, has the
answer: nothing, and that is the problem.
**Verdict: cannot be represented.**

Four of five cannot be keyed to a diff. One can, at the cost of a false
cardinality. The founder's stated flip condition is met on the evidence.

---

## What the finding does NOT license

The flip condition as written says that if analytical work cannot be represented
as a change record, "Option A fails and Option B becomes right". Read literally,
the five cases above hand the answer to Option B.

That reading is too fast, and here is the distinction that matters.

Option A's actual protection is in its own second sentence: BrotherDS
"explicitly does NOT build a second project management or delivery framework. It
reads BrotherMode's and BrotherSBE's records rather than keeping its own."

Two different things are bundled in that sentence:

1. **The unit record.** Whether a claim gets its own object.
2. **The delivery framework.** Whether BrotherDS gets its own plan, schedule,
   progress page, task lifecycle, and delivery packet.

The five cases speak only to the first. They say a claim is not a change, which
is a statement about units. They say nothing at all about whether BrotherDS
needs a second project management framework, and the answer to that is plainly
no, on cost grounds that have not changed.

There is also a fact on disk that settles the first half already: BrotherDS has
kept its own unit record since its first commit. A claim is a JSON file with its
own lifecycle, from unexamined through checked and decided to resolved. That is
not a project management framework, it is the unit of the third product, exactly
as a change is the unit of the first two. Nobody proposed that BrotherSBE stop
having changes because BrotherMode has tasks.

---

## The recommendation

**On item 6, project management and the delivery framework: Option A, unchanged.**
BrotherDS builds no plan, no schedule, no second progress page and no delivery
packet. It reads BrotherMode's records. Cost is the deciding argument and the
evidence above does not touch it.

**On the unit: the claim is its own object, and always was.** This is not a
concession to Option B, it is a description of what is already built. It needs
saying out loud only because Option A's wording bundles it with the framework
question and could be read as forbidding it.

**On item 7, value realization tracking: BrotherDS owns it.** This is the part
of the study that changes something, and it comes from the shared chain rather
than from cost.

The founder-authoritative north-star chain ends at VERIFIED REALITY. Its own
status table records that stage as owned by nobody, and the chain document calls
the neighbouring gap the largest structural gap in the chain. Meanwhile
BrotherDS's north star, the Verified Claim Rate, is the only metric in the
triumvirate that measures whether reality agreed with what was said. Those two
facts are the same fact seen from two sides.

Value realization is not a new framework to build. It is the terminal stage of
the chain that already exists and that nobody owns. Giving it to BrotherDS costs
no second record, introduces no reconciliation rule, and fills the hole the
first two products both stop short of.

**First alternative: pure Option B.** BrotherDS owns the analytical delivery
lifecycle end to end. Correct if analysts turn out to need a plan, a schedule and
a delivery packet shaped differently from software work. Costs a second record
and a reconciliation rule between three products.

**Second alternative: pure Option A, including item 7.** Value realization stays
unowned, or is assigned later. Cheapest, and it leaves the chain ending in a
stage nobody holds, which is the state the chain document already flags as its
largest structural gap.

**What would flip the recommendation.** Measurable, at week three of real use:
if analysts start keeping a shadow record of their own, a spreadsheet or a
document tracking analytical work that BrotherMode's records cannot carry, then
Option A's framework half has failed in practice and pure B becomes right. The
count of shadow records is the measurement. Zero means A holds.

**An honest caveat about this recommendation's shape.** Splitting items 6 and 7
and answering them differently is arguably a fourth option rather than a reading
of the three. If the founder reads it that way, it is Option D and it is still
entirely his call. The study's job was to produce the evidence, and the evidence
is the five cases above.

---

## What this study did not do

- It did not test the claim-to-change mapping against BrotherSBE's eight
  assurance concerns, only against BrotherMode's record and passport. A claim
  passing through the assurance concerns is a separate question and is not
  answered here.
- It ran on five claims from one estate on one night. Five is enough to show
  that a mapping fails, since one counterexample does that, and far too few to
  show that any mapping succeeds.
- It did not measure authoring cost, which SPEC.md already names as one of the
  three things that would disprove this product. That measurement is due at
  week three and has not started.
