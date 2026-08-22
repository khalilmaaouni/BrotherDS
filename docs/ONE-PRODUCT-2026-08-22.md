# Merging the three into one, the way Superpowers is one

Date: 2026-08-22. Status: RECOMMENDATION, written after the founder stated the
goal: "merge them all under one like superpower". It supersedes the three-track
coordination plan written earlier the same day, which assumed three products
coordinating across seams.

Measured, not remembered, on 2026-08-22 from the public repositories:

| | version | skills | commands | agents | licence | visibility |
|---|---|---|---|---|---|---|
| BrotherMode | 3.3.2 | 19 | 15 | 5 | MIT | public |
| BrotherSBE | 3.2.1 | 16 | none | 8 | MIT | public |
| BrotherDS | none | 1 | none | none | MIT | PRIVATE |

---

## 1. The merge is already half done, doctrinally

These are not three philosophies that need reconciling. They are three packagings
of one, and the shared parts were deliberate:

- **One chain.** BrotherMode and BrotherSBE carry the identical north star,
  founder direction 2026-08-15, human intent through to verified reality.
  BrotherDS was built to occupy the same stages rather than add one.
- **One verdict vocabulary.** PASS, FAIL, NO-DATA, where NO-DATA is never a pass
  and never a block. BrotherDS matched that tuple on purpose rather than mint a
  second meaning of verified.
- **One evidence law.** No completion claim without a verifying command run
  after the last edit, with its output quoted. All three enforce it.

What differs is packaging, naming, and four separate state vocabularies that
grew independently. That is merge work, not design work.

## 2. The seams are the tax of being separate, and they disappear

This is the strongest argument for the goal, and it costs me most of last week's
work to say it.

The change passport, the five-item handoff package, the second-consumer
authorisation, the wire-format ratification, the isolation scan that refuses to
let one engine name a path on the far side of the seam: **every one of those
exists only because the products are separate.** They are contracts between
parties. One product has no parties.

Under a merge they collapse into ordinary internal structures. The two
outstanding requests to the sibling products stop being requests, because there
are no siblings. The isolation law stops being a law. A meaningful part of the
BrotherDS seam work becomes obsolete, and pretending otherwise to protect it
would be the exact overclaim this suite exists to refuse.

**What survives the merge** is the substance rather than the plumbing: the
fourteen gates and their refusals, the chain, the claim as a unit, the verdict
tuple, the done-check discipline, and the guided beginner surface.

## 3. The spine: the claim is the general unit, and it was hiding in the third product

The merged product needs one unit or it is a bundle rather than a product. It
already has one, and it came from the smallest of the three.

- BrotherMode asserts **the work was done as described**. A claim about execution.
- BrotherSBE asserts **this change is safe to ship**. A claim about risk.
- BrotherDS asserts **this number is true**. A claim about the world.

Three assertions. Each must carry its evidence, each must state what it does not
establish, and each is settled later by reality rather than by the asserter.
That is one object with three subtypes, not three objects.

The north star generalises with it. **Verified Claim Rate**, the share of
assertions that reality later agreed with, reads correctly for all three: did the
change break, was the work real, did the number hold. BrotherSBE's own north
star already says finished means verified reality and not merge; this gives that
sentence a metric.

**So the merged product's unit is the claim, its verdict is reality's, and the
three current products become three domains of claim, with the gates that domain
earns.** Master data is a fourth such domain (G11 to G14) and it arrived without
needing a fourth product, which is evidence the shape is right.

## 4. The risk that would sink it: concatenation is not consolidation

19 plus 16 plus 1 is 36 skills, 15 commands and 13 agents under one name. That is
a LARGER surface to learn, not a smaller one, and it would make adoption worse
while claiming to make it better.

Superpowers is one thing because it has ONE entry point that routes, not because
its skills sit in one folder. The merge has to delete.

**A merge that does not remove at least a third of the combined surface has
failed**, and that should be a stated exit criterion before the first file moves.
The obvious candidates, from what is already known:

- Four state vocabularies (task lifecycle, fence states, queue-item states, chain
  stages) reduced to the smallest set that still distinguishes real cases.
- Three progress pages and three north star documents reduced to one each.
- The duplicated laws, digests and reference files that say the same thing in
  three houses.
- Every command that exists because a product needed its own entry point.

## 5. What the merge forces into the open

**BrotherDS cannot be moved in as it stands.** It is private and its history
carries 117 client name occurrences, while both siblings are public and MIT. The
standing law is that history binds as well as the working tree, so the route is
a clean extraction of the shippable part into the merged repository, taking the
files and not the history.

That was an optional question yesterday. Under this goal it is a precondition,
and it is cheap: the shippable part is one engine file, the gates, and the
documents that do not name a client.

## 6. Recommended shape

**Promote one name rather than invent a fourth.** BrotherMode's own description
is already the whole chain, "turn an idea into a verified result", while the
other two describe narrower colleagues. It also owns the guided beginner surface
and the higher version. So BrotherMode becomes the umbrella, and assurance and
evidence become capability areas inside it rather than products beside it.

*The alternative worth naming:* a fresh name, on the argument that a merged
product with a new promise deserves one, and that BrotherMode's existing users
would otherwise experience a silent scope change. This costs the recognition
already built and one more migration.

**Sequence, and nothing here is a decision this file may take:**

1. Name the exit criterion first: the combined surface must shrink by a third,
   measured in skills, commands and agents, and it is measured before and after.
2. Extract BrotherDS clean into the umbrella. Files, not history.
3. Collapse the vocabularies, then the documents, then the commands. In that
   order, because the vocabularies are what the documents describe.
4. One entry point that routes, on the Superpowers pattern.
5. Only then, one release.

## 7. The honest counter-argument

Two of these products are near product grade and one has never had a user. A
merge is the most expensive possible way to find out whether the third one was
needed, because it entangles the answer with two things that are already working.

The cheaper order is to answer the BrotherDS question first, with one claim
scored against a real outcome, and merge afterwards from a position of knowing.
Merging first is defensible if the goal is one product regardless of whether the
data science half earns its place, and that is a founder call about what is being
built rather than an engineering judgement about what works.
