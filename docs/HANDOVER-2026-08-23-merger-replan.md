# Handover 2026-08-23: the merger replan, and what it decides for BrotherDS

Status: rewritten this session (eab3d639, BrotherModeUp, the merger-analysis
session) against the correct head. The previous draft of this document was
written against `8840c2d`, five commits behind the live remote at the time it
was saved, and named that gap without closing it. This rewrite starts from
`8084340`, verified equal to origin below.

Verified this session, commands and output:

```
$ git rev-parse --short HEAD
8084340
$ git ls-remote origin refs/heads/feature/north-star-chain-and-native-seam
8084340...  refs/heads/feature/north-star-chain-and-native-seam
$ /usr/bin/python3 bds.py selftest | tail -1
SELFTEST PASS
```

Repository state: PRIVATE, github.com/khalilmaaouni/BrotherDS, branch
`feature/north-star-chain-and-native-seam` at `8084340`. Pull request 1 is
OPEN into `v1-claim-receipt`. Private-term matches at this head: 30, in two
files (`docs/SCOPE-2026-08-12-founder-directive.md`, 4 matches; and
`research/A3 (its name carries two terms)`, 26 matches, its own filename carrying two
terms), down from 104 in nine files at `8840c2d`. The queue,
`docs/plan/QUEUE.json`, holds 12 items; three changed today
(`verified-reality-owner` moved to done; `passport-consumer-authorised` and
`handoff-wire-format` moved from blocked to queued, each carrying the
founder's decision note).

## The lesson this rewrite exists to record

The previous draft compared its own local checkout against origin, found a
five-commit gap, named the gap in its own text, and then wrote the rest of
the document as if that gap did not matter. It did: the commit it missed,
`8084340`, was titled "The merge into one product, and what it makes
obsolete" and carries `docs/ONE-PRODUCT-2026-08-22.md`, the document the
ADR's round four spends a full section reconciling. A handover written one
commit behind the true head is not a smaller version of the truth; it is
missing the fact that changed the shape of the plan. The rule going forward:
run `git ls-remote origin refs/heads/<branch>` beside `git rev-parse --short
HEAD` in the same verify block, every time, not `rev-parse` alone, and do not
write status prose until the two agree.

## What was decided for BrotherDS on 2026-08-22, the rounds, verbatim

Four rounds, all in the question UI, recorded in
`/Users/khalil.maaouni/Documents/BrotherModeUp/docs/plan/ADR-2026-08-23-one-brother-repository.md`.

**Round one, about 12:0x JST.** BrotherDS: "Yes: separate the internal
context, then public MIT, before it joins (Recommended)." Decision taken: P11
is a precondition of the merge, timing gate condition 3.

**Round two, about 12:1x JST.** The passport's second read-only consumer:
"Yes: authorise the read-only second consumer (Recommended)." The handoff
package wire format: "BrotherSBE writes contracts/handoff-package.v1.json
with a fixture and a test; BrotherDS reads the ratified marker
(Recommended)."

**Round three, about 12:5x JST.** The verified-reality owner: "Split by unit,
ledger owned by BrotherDS (Recommended)." DECIDED: BrotherMode records a
change's outcome, BrotherSBE judges a change's verified reality (N2 stands),
BrotherDS owns the stage's LEDGER, the Verified Claim Rate for claims and a
change-level reopen rate computed from the siblings' records. It judges no
change and writes no change record. The vault spaces: "Propose one space
10-Projects/brother at the merge, keep three until then (Recommended)."
Nothing is created before his yes at the merge.

**Round four, about 13:3x JST.** On which repository governs: "Merge them
under Brother new repo." Read as: the target is a NEW repository named
Brother, built by clean extraction; the three existing repositories are
archived with pointers afterwards. On the seventh gate condition: "Find the
right approach as Fable and handle a harmony between all functions to be
seamless like Superpowers." Read as a delegation: the strongest tier designs
how the three products become one seamless product without breaking the
laws, and decides the gate.

Decisions 1 (which of the three paths in `OPTIONS.md`) and 2 (the boundary
question, directive section 3) are still open; both are named in phase 1
item 1.9 of the roadmap.

## What the one-product page recommended, and how the ADR reconciled it

`docs/ONE-PRODUCT-2026-08-22.md`, this repository's own document, written the
night of 2026-08-22 after the founder said "merge them all under one like
superpower", recommended ONE PRODUCT: a single plugin under the BrotherMode
name, the claim as the general unit for all three (one object with three
subtypes: BrotherMode asserts the work was done as described, BrotherSBE
asserts the change is safe to ship, BrotherDS asserts the number is true),
the seams (the passport, the handoff package, the second-consumer
authorisation) dissolved into ordinary internal structure because a merged
product has no parties, a third-of-the-surface exit criterion before the
first file moves, and its own honest counter-argument: score one claim
against a real outcome before merging, because merging first entangles an
unproven third product with two that already work.

The ADR's round four read that document (unread until the checkout was
fast-forwarded) and did not adopt its packaging. The reconciled shape:

1. **Packaging stays Option B**, decided in round three: three whole plugins
   inside the Brother repository, each installable alone, one marketplace
   file with relative sources, the shape Anthropic's own `claude-code`
   repository and ruflo both use, and the shape a single bundled plugin
   cannot support once write-refusing hooks and a registry are real, which
   BrotherDS, BrotherMode and BrotherSBE together already are.
2. **The harmony layer is the superpowers pattern applied above the
   packaging, not instead of it**: one entry point that routes a person to
   the right capability by what they are doing, one vocabulary (the chain's
   stages, the verdict tuple PASS, FAIL, NO-DATA, and the three-subtype
   assertion object above), and the seams turned into plumbing: the passport
   and the handoff package written and read with no manual step, tested by
   the root runner, invisible to the person using the product. The contracts
   survive as the mechanism; what disappears is the person ever seeing them.
3. **The one-product document's exit criterion is adopted for phase 5**,
   after the merge, not before: the combined surface (19 plus 16 plus 1
   skills, 15 commands, 13 agents today) shrinks by at least a third,
   measured before (P18) and after, by collapsing the four state
   vocabularies first, then the duplicated documents, then the commands that
   exist only because a product needed its own entry.
4. **The counter-argument becomes a promotion gate, not a join gate.**
   BrotherDS joins the repository with the other two so the entry point can
   route to it; its capability is routed as EXPERIMENTAL inside that entry
   point until its first claim is scored against a real outcome
   (`/usr/bin/python3 bds.py ledger` reporting one resolved claim, timing
   gate condition 7). This keeps the merge a move while still answering
   whether the third product earns its place before anyone is told it has.
5. **The freeze**: the entry point is a new public command and phase 5
   deletes commands, both forbidden by the tool-surface freeze until the
   four user journeys pass. The PROPOSED amendment now carries the sentence
   that the merged product's surface is redesigned once, at the merge, then
   frozen again; only the founder can land it.

The flip condition on the whole approach is named in the ADR itself: if the
founder wants the BrotherDS document's shape instead, one plugin, the seams
dissolved in code, Option A returns with the five skill renames and the hook
bundling already named in its rejection, and that is his decision to take in
his own words.

## What is scheduled, phase 2 of the roadmap, this product's rows

All estimates are agent minutes as briefed; the actual range applies
`python3 tools/bm_forecast.py calibrate --clock agent --basis judged`
(median 2.24, n=14) as the calibrated bound and the any-basis run (median
1.39, n=17) as the optimistic bound, not a low end from the same population.

| Item | What | Est | Range | Done-check |
|---|---|---|---|---|
| P3 | The passport's second read-only consumer authorised | 30 | 42 to 67 | the sentence in both contracts; `bds.py passport` no longer capped UNAUTHORISED |
| P4 | The handoff package wire format, written by BrotherSBE | 120 | 167 to 269 | `bds.py handoff <fixture>` not capped at NO-DATA; the schema test green; the meta-test at 0 failures |
| P5 | Passport conformance on the same fixture bytes on all three sides | 60 | 83 to 134 | the three suites print one digest `e6d68b76...` |
| P7 | Release invariant: VERSION, CHANGELOG.md, CHECKSUMS.sha256, `.claude-plugin/plugin.json` | 120 | 167 to 269 | each invariant prints PASS; `verify-install.sh` MISSING 0 MISMATCH 0 in all three |
| P11 | Internal context separated, two files remaining at `8084340` | 45 | 63 to 101 | the private-terms grep prints nothing; SELFTEST PASS |
| P14 | PROJECT.md status current | 15 | 21 to 34 | its status line names the remote, branch, sha and PR 1 |
| P18 | The harmony layer designed, the entry point, one vocabulary, the before-measurement | 120 | 167 to 269 | the design page names the routing table and the before-measurement; the founder has amended the freeze |

Seven items, 510 briefed minutes, roughly 709 to 1142 calibrated. P14 closes
inside this same session, by this same edit to PROJECT.md; P3, P4, P5, P7,
P11 and P18 remain open, and none of their other files were touched this
session beyond the board and this document.

## What is still the founder's

- **Decision 1**, the path: which of the three options in `OPTIONS.md`.
  Still open.
- **Decision 2**, the boundary question: `docs/SCOPE-2026-08-12-founder-
  directive.md` section 3. Still open.
- **PR 1**: OPEN into `v1-claim-receipt`. Its merge is his call; timing gate
  condition 3 (this product's internal context separated, PR 1 resolved)
  reads NOT MET while it stays open.
- **The freeze amendment**: drafted PROPOSED inside the larger
  PRODUCT-DIRECTION amendment in the ADR, landed only by his hand, and
  required before phase 5's entry point can ship without breaking the
  surface freeze.

## The rule that binds before any public tree

The private-terms grep (`git grep -c -i -F -f ~/.brothersbe-private-names --
.`) currently prints two lines summing to 30 matches:
`docs/SCOPE-2026-08-12-founder-directive.md` (4) and `research/A3-vault-
A3 file` (26). That second file's own name carries two of the private
terms. Decision 5 already says yes to public MIT as a precondition, not as a
signal to push now. History carries names forward even after a file is
edited, so the route to public is a clean extraction at a chosen commit,
never a scrub of this tree: both remaining files are rewritten to roles, or
the research file renamed, before this repository's history ever reaches a
public remote.

## Verify

```bash
git rev-parse --short HEAD
git ls-remote origin refs/heads/feature/north-star-chain-and-native-seam
/usr/bin/python3 bds.py selftest
```
