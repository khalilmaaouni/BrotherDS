# The coordinated plan across the three products

Date: 2026-08-22. Status: RECOMMENDATION. It recommends and does not ratify.
Written in the planning role: no implementation decisions are taken here.

Grounded on the sibling repositories as they actually are on 2026-08-22, read
from GitHub because this machine's Documents folder is denied to the process.
Both siblings are public. Where this plan states a sibling fact, it was read,
not remembered.

---

## 1. The correction this plan opens with

The 2026-08-16 recommendation said BrotherDS should own the chain's
`verified-reality` stage, because the shared chain records that stage as owned
by nobody. **That recommendation was made without reading BrotherSBE's north
star, which was unreachable at the time. It is superseded.**

BrotherSBE's `NORTH-STAR.md` already sequences that stage as its own work:

> "the sequence is forced: readiness first, because it needs no production
> access whatsoever; observation second, gated on that credential; verified
> reality last, because it is a state computed from the other two."

It also already settles the overlap question for the pair:

> "BrotherMode owns provenance, BrotherSBE owns assurance, the passport is the
> contract. Neither implements the other's mechanism."

A second correction, smaller and worth making because it was reported as
evidence: BrotherSBE's "duo spec" is `2026-08-18-bitbucket-duo-spec.md` and is
about the two git HOSTS, GitHub and Bitbucket. It is not a statement that the
two products are a closed pair. The orphan finding below does not rest on it.

---

## 2. The finding that governs everything else

Checked by code search on 2026-08-22: **BrotherModeUp mentions BrotherDS in zero
files. BrotherSBE mentions it in zero files.** Neither sibling's north star, and
neither sibling's roadmap, reserves anything for a third product.

So BrotherDS is not the third leg of a triumvirate on disk. It is a fourth
thing, built against two products that have never heard of it, consuming
artifacts they do not know they produce. Every integration claim it makes today
is one-sided.

This is not a crisis and it is cheap to fix. It is, however, the single fact
that any plan has to start from, because the alternative is designing a seam
with a partner who is not at the table.

---

## 3. The collision, and the resolution that dissolves it

Both BrotherSBE and BrotherDS want the last node of the chain.

They are not asking the same question.

| | unit | the question at `verified-reality` |
|---|---|---|
| BrotherSBE | a change to a system | did the change actually work in production |
| BrotherDS | a claim, one number that reached a decision | did the number turn out to be true |

A change can work perfectly and the number that justified it can still have been
wrong. A number can hold and the change built on it can still have failed. The
two verdicts are independent, and collapsing them into one owner loses whichever
half is not that owner's unit.

**RECOMMENDED RESOLUTION: `verified-reality` is a STAGE, not a component, and it
is occupied per unit rather than owned outright.** BrotherSBE computes the
change verdict from readiness and observation. BrotherDS computes the claim
verdict from an outcome scoring a stated uncertainty. Neither implements the
other's mechanism, which is exactly the rule the pair already applies to
provenance and assurance one node earlier.

This costs nothing to either side. It requires no change to BrotherSBE's
sequencing, no second record, and no reconciliation rule. It extends a settled
principle rather than reopening one.

**What would flip it.** If a single reconciled "did this work" verdict is what a
buyer actually asks for, then one owner is right and BrotherDS's claim verdict
becomes an input to BrotherSBE's rather than a peer of it. That is a market
question, not an architecture question, and it should be answered by asking a
buyer rather than by arguing here.

---

## 4. The coordinated plan, three tracks

The tracks are ordered by what unblocks what. Track A is small and unblocks the
other two, so it goes first even though it is the least interesting.

### TRACK A. Make the third product exist, to the other two. One day.

The cheapest, highest-leverage work in this plan.

- **A1. A cross-reference in each sibling.** BrotherSBE's north star already has
  a "Cross-references owed" section and a precedent for paying one. Add
  BrotherDS to both siblings' chain documents as occupying the same stages for
  the claim unit, with the per-unit resolution above stated in one paragraph.
  Done-check: code search for BrotherDS in each sibling returns non-zero.
- **A2. The passport's second consumer, ratified.** BrotherDS already reads
  `.sbe/passport.json` read-only and never writes it. The seam specification
  lives in the BrotherSBE repository. One sentence permitting a second read-only
  consumer makes a built reader legitimate. Done-check: the seam spec names it.
- **A3. A wire format for the five-item handoff package.** The content was
  contracted 2026-08-11; the field names never were. BrotherDS's reader refuses
  to certify an unratified shape and will keep refusing, correctly, until this
  is done. Done-check: `bds.py handoff` can reach PASS against a real package.

**Everything in Track A is a founder decision or a sibling change. None of it is
BrotherDS's to take unilaterally, which is why it is a request and not a task.**

### TRACK B. BrotherDS earns its own evidence. Two weeks, unblocked by A.

BrotherDS does not need the siblings to become useful, and it should not wait.

- **B1. The charter document.** Founder direction 2026-08-17, still unbuilt: one
  document covering the north star, the features, the capabilities, and the
  collaboration, with master data first class and no client named. This is the
  artifact that makes the product explicable to anyone who is not the founder.
- **B2. Widen G5 for the dual run.** The 2026-07-31 red team rated this the
  highest item in the whole scope with no competing vendor. Until it lands,
  BrotherDS answers "is this internally reproducible" and cannot answer "does
  this agree with what the reader believes today".
- **B3. The plugin surface, then the authoring-cost measurement.** Authoring
  cost is one of the three named tests that would disprove this product, and it
  is measured at week three of real use, not asserted.
- **B4. One claim scored against a real outcome.** The north star reports
  NO-DATA until this happens, and it is the only thing that turns the metric
  from a design into a measurement.

### TRACK C. The publishability question. Founder decision, then one day.

BrotherDS cannot be made public by scrubbing: its history carries 117 client
name occurrences, and the standing law is that history binds as well as the
working tree. Both siblings are already public. If BrotherDS is ever to join
them, the route is a clean extraction of the shippable part into a fresh
repository, done once, deliberately.

This does not block Tracks A or B. It blocks only the day BrotherDS is shown to
anyone outside.

---

## 5. What each product needs from the others, stated as a table

| From | To | What | Blocking |
|---|---|---|---|
| BrotherSBE | BrotherDS | permit a second read-only passport consumer | A2, and the legitimacy of a built reader |
| BrotherSBE | BrotherDS | ratify the handoff package wire format | A3, and `bds.py handoff` ever reaching PASS |
| BrotherDS | both | the per-unit resolution of `verified-reality` | A1, and the coherence of the chain |
| founder | all three | is BrotherDS a product, or a capability of the pair | everything below the top of this plan |

Nothing in this table is technical. All four are decisions.

---

## 6. The honest risk in this plan

**BrotherDS may not deserve to be a third product.** That possibility should be
written down rather than defended against.

The case for it: the claim is a genuinely different unit, four of five real
claims cannot be keyed to a diff, and no amount of change assurance catches a
wrong number when nothing changed.

The case against it: two products are already a lot to explain, both siblings
are near product grade while this one has one open pull request and no user, and
"data science assurance" could be a capability inside BrotherSBE's existing
analytics partnership rather than a separate thing to install, learn and adopt.

The cheapest test of that is Track B4, one claim scored against a real outcome,
because it is the only evidence that the thing this product measures is a thing
anybody wants measured. Nothing in Track A should be spent before somebody
believes the answer to that.
