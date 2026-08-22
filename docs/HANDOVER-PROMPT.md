# The overnight handover prompt for BrotherDS

Written 2026-08-22 by the session that built the chain, the seam, the de-naming
and the master data gates. Paste the block below as the first message of a fresh
unsupervised session. Everything it needs is in it; it assumes no memory of this
conversation.

---

## PASTE THIS

You are continuing BrotherDS, the third product of a triumvirate, unsupervised
overnight. Read this whole brief before touching anything. /brothersbe
/brothermode

### READ FIRST: the environment is broken in a specific way

macOS TCC denies this machine's `~/Documents` and `~/Downloads` to the Claude
process. `ls` returns "Operation not permitted" and it persists with the sandbox
disabled, so it is the operating system, not the harness. The canonical project
root `~/Documents/BrotherDS` is therefore UNREADABLE. Do not waste the night on
it and do not report it as missing: it exists and is merely unreachable.

Work like this instead, which is verified to work:

    git clone https://github.com/khalilmaaouni/BrotherDS.git $SCRATCH/ds
    cd $SCRATCH/ds && git checkout feature/north-star-chain-and-native-seam
    /usr/bin/python3 bds.py selftest      # must print SELFTEST PASS
    /usr/bin/python3 bds.py backlog       # must print VERDICT PASS

Push to the same branch. The founder pulls later. Note the interpreter:
duckdb is installed under `/usr/bin/python3` (3.9), not under `~/.local/bin`.
`cd` into the clone inside a subshell; the harness resets cwd between commands
and bare `git` calls will fail with a getcwd error, so prefer `git -C <path>`.

### WHERE THE WORK IS

Repository khalilmaaouni/BrotherDS, PRIVATE. Two branches only:
`v1-claim-receipt` (the default, at 24f9534) and
`feature/north-star-chain-and-native-seam` (the live one). PR 1 is open against
the default branch and has been open since 2026-08-15 without being merged.
Merging it is a founder decision; do not merge it yourself.

### THE NORTH STAR, AND THE ONE FACT THAT REFRAMES EVERYTHING

BrotherDS's north star is the VERIFIED CLAIM RATE: of the decision-grade claims
scored against reality, the share whose realised outcome fell inside the
uncertainty stated at the time. It reports NO-DATA today because no claim has
resolved, and that is the honest state rather than a defect.

The shared chain, authoritative from the founder on 2026-08-15 and carried
identically in both sibling repositories, runs: human intent, development
method, BrotherMode, change passport, BrotherSBE's eight concerns, human
decision, release, verified reality. BrotherDS ADDS NO STAGE to it. It stands in
the same stages, for a claim instead of a change, and the mapping lives in
`bds.py`'s CHAIN table with a selftest assertion that refuses to let the table
and `docs/NORTH-STAR-CHAIN.md` disagree.

**THE FACT TO ABSORB BEFORE PLANNING ANYTHING.** Checked on 2026-08-22 with
GitHub code search: BrotherModeUp mentions BrotherDS in ZERO files. BrotherSBE
mentions it in ZERO files. On disk the triumvirate is a DUO plus an orphan. (Do not cite the
"duo spec" as evidence for this: that file is about the two git HOSTS, GitHub
and Bitbucket, and an earlier session misread it. The finding rests on the code
search alone, which is enough.) Every seam this repository has built so far consumes
artifacts the siblings do not know they produce for it, and the integration is
entirely one-sided. Treat any sentence claiming BrotherDS is integrated as
unverified until a sibling repository names it.

### WHAT IS BUILT AND GREEN

`bds.py`, one file, standard library plus duckdb. 73 assertions.

  Ten original gates G1 to G10: empty limits, unknown origin, bare number,
  undesigned causal claim, single-path derivation, wrong accuracy metric,
  a value that no longer reproduces, an incomplete origin protocol, undeclared
  grain, and a contested metric definition.

  Four master data gates G11 to G14, added 2026-08-22 on founder direction of
  2026-08-17: match quality (refuses a resolved-record count with no precision,
  recall and operating point), error asymmetry (refuses a blended F1, and
  requires each error's cost named, because merging two distinct customers and
  missing a duplicate are not the same event), sample frame (a labelled sample
  drawn from the candidate set reads NO-DATA for recall, because it cannot
  contain the pairs blocking never proposed), and survivorship (a merge must
  state which value wins and whether it can be undone; it need not be
  reversible, it must SAY).

  The chain vocabulary and its refusals, the change passport consumer, the
  BrotherSBE handoff reader, the backlog control, and an isolation scan that
  refuses to let this engine name a path on the far side of the seam.

Documents: `SPEC.md`, `docs/NORTH-STAR-CHAIN.md`,
`docs/TRIUMVIRATE-INTEGRATION.md`, `docs/BOUNDARY-STUDY-2026-08-16.md`,
`docs/VALIDATION.md`, `docs/plan/QUEUE.json`, `OPTIONS.md`.

### WHAT TO DO, IN ORDER

Pull from `docs/plan/QUEUE.json`. Every item names the stage it serves and the
check that closes it, and `bds.py backlog` refuses one that does not. Highest
value first:

1. **The charter document.** Founder direction 2026-08-17, still unbuilt: ONE
   HTML document artifact covering BrotherDS's north star, features and
   capabilities, and how it collaborates with BrotherMode and BrotherSBE, with
   master data as a first-class case (dedupe, cleansing, matching, false
   positive and negative detection AND the solutioning). It must cover the
   disciplines generally: data science, business science, MDM science, data
   analytics, business insight, value detection. NAME NO CLIENT. A prior session
   built `BrotherDS-claim-charter.html` and published artifact
   e9112bcb-9fd7-4085-87ff-01dafdb49161 under a DIFFERENT Claude account; it is
   unreadable from the main account. Rebuild rather than block, and reconcile if
   it ever surfaces.
2. **`g5-cross-class-comparison`**, queued. Widen G5 so a dual run can be
   expressed: a SYSTEM derivation paired with a THIRD_PARTY or ELICITED
   comparison against the incumbent artifact somebody already trusts. The
   2026-07-31 red team rated this the highest item in the whole scope with no
   competing vendor. Until it lands the product can answer "is this internally
   reproducible" and cannot answer "does this agree with what the reader
   believes today", which is the question that matters when a number replaces
   one somebody has read for years.
3. **`plugin-surface`**, queued, which unblocks `authoring-cost`, one of the
   three named tests that would disprove this product. It needs a skill
   installed into machine config, so land it at session end, not mid-session.
4. Refresh `GANTT.html` and republish it to the SAME artifact URL,
   c07a5331-edd0-409e-9241-8fb4b2786db4. Never publish it to a new one.

### THE RULES THAT BIND, NON NEGOTIABLE

- **No GitHub Actions.** Founder instruction, direct. None exist in this
  repository. Do not add a workflow file, do not enable Actions, do not propose
  cloud CI. Verification runs locally.
- **No client names.** The design files were de-named on 2026-08-22: use "the
  pilot estate" and "the first target estate". Two files deliberately keep the
  names because they are RECORDS rather than design: the 2026-08-12 founder
  directive and the estate research note. Do not scrub those.
- **This repository can never be made public by scrubbing.** Its history carries
  117 client-name occurrences. The founder's own law says history binds, so the
  route to public is clean extraction into a FRESH repository, never a scrub.
- **No em or en dashes anywhere.** Commas, colons or parentheses.
- **No Anthropic attribution** in any commit, PR body, document or page. Sole
  author: Khalil Maaouni.
- **Never claim done without a verifying command run AFTER the last edit, with
  its output quoted.** NO-DATA is never a pass and never a block.
- Push at every green checkpoint through the github-desktop-push gates.

### KNOWN DEFECTS IN THIS REPOSITORY'S OWN CONTROLS

Stated so the next session does not rediscover them at three in the morning.

- **The dash gate scans removed lines.** Running the dash scan over a whole
  staged diff counts dashes being DELETED as hits, so a commit that removes
  dashes looks like a commit that adds them. Scan added lines only:
  `git show HEAD | grep -E '^\+' | perl -CSD -ne '...'`.
- **A scan whose pass condition is empty output exits nonzero.** `grep -c`
  returns 1 when its count is zero, so a clean dash scan placed in an `&&` chain
  ahead of `git add` silently skips the commit BECAUSE it passed. Separate the
  scan from what it gates with `;` or `|| true`, and print state after any state
  change.
- **`sbe verify` is not this project's validator.** One of its fifteen checks
  opens a file here; the four hard gates return NO-DATA because there is no
  dossier, and that is correct rather than a hole. `docs/VALIDATION.md` records
  why, and the decision not to build a dossier. The selftest is the real
  control.
- **Blind name substitution breaks wrapped lines and filenames.** The
  2026-08-22 de-naming had to be repaired three times: a client name wrapped across two lines, so the replacement landed on
  the first half and orphaned the second; a filename rewritten mid-token, and four
  sentences left starting in lower case. Always re-read the prose after.

### WHAT ONLY THE FOUNDER DECIDES, DO NOT DECIDE THESE

1. Which of the three paths in `OPTIONS.md`.
2. The boundary question, directive section 3. The evidence study is written
   (`docs/BOUNDARY-STUDY-2026-08-16.md`): of five real claims, four cannot be
   keyed to a diff, so his own stated flip condition is met. It recommends
   splitting items 6 and 7 and says plainly that this may read as a fourth
   option. It does not ratify.
3. Who occupies the chain's `verified-reality` stage. NOTE, 2026-08-22:
   BrotherSBE's own north star already sequences that stage as its work
   ("verified reality last, because it is a state computed from the other
   two"), so the 2026-08-16 recommendation that BrotherDS OWN it is superseded.
   See docs/COORDINATED-PLAN-2026-08-22.md: the stage is occupied per unit,
   BrotherSBE for the change, BrotherDS for the claim.
4. Whether the siblings accept the two seam requests, which they currently do
   not know exist.
5. Merging PR 1.

### CLOSE THE SESSION PROPERLY

Session log to the Kay Vault under `10-Projects/brotherds/Sessions/` if
`~/Documents` is reachable by then, otherwise into the repository under `docs/`
and say why. Update `docs/plan/QUEUE.json`. Push. Republish the progress page to
its existing URL. Lead the final report with bad news, quote the command output
behind every number, and name what was not done.
