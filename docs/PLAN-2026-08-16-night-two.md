# Night two plan: the full north star, and the native seam to the triumvirate

Session: 2026-08-16, started 01:27 JST. Founder asleep, unattended.
Ask, verbatim: "work overnight to finish the full north star for BrotherDS and
how it integrates natively to the triumvira. /brothersbe to validate things
periodically."

Hard stop 07:00 JST. Spend ceiling 800,000 output tokens, soft stop 500,000.

## What was already true when this session started

Verified by reading, not assumed:

- `SPEC.md` names the north star metric (Verified Claim Rate) and sketches a
  one-table mapping onto the shared chain. That table is eight rows of prose.
- `bds.py` already implements `score` and `ledger`, with outcome states HELD,
  MISSED and UNSCOREABLE. The metric loop is closed in code and reports
  NO-DATA only because no claim has resolved yet.
- There is no `docs/NORTH-STAR-CHAIN.md`. BrotherMode has one, 533 lines,
  founder-authoritative since 2026-08-15.
- There is no stage vocabulary in code. BrotherMode enforces its chain through
  `tools/bm_idle.py` CHAIN_STAGES, where an item naming an unknown stage is a
  hard error rather than a silent pass.
- There is no seam code at all. Nothing reads the change passport, nothing
  reads the BrotherSBE handoff package.
- The boundary question of directive section 3 is open and founder-owned. The
  directive itself asks for "one focused study before any code".

So the gap is not the metric. The gap is that the north star is prose, and the
integration is a table rather than a contract.

## The units, in dependency order

Each unit closes only when its done-check has been run AFTER the last edit and
its output quoted in this file.

### U1. The boundary study
`docs/BOUNDARY-STUDY-2026-08-16.md`. Does analytical work fit a change record
without distortion? That is the founder's own stated flip condition between
Option A and Option B. Produces a recommendation, the first and second
alternative, and what would flip it. It RECOMMENDS; it does not ratify.
Done-check: `grep -c "Option [ABC]" docs/BOUNDARY-STUDY-2026-08-16.md`

### U2. The chain, in code, as a control
`CHAIN_STAGES` in `bds.py`, plus a `stage` command that refuses an unknown
stage name. Mirrors BrotherMode's mechanism rather than inventing a second one.
Done-check: `python3 bds.py selftest`

### U3. The chain document
`docs/NORTH-STAR-CHAIN.md`. Every stage, its owner, its status, the
unconditional human decision points, and what would disprove the whole thing.
An anti-drift assertion makes the document and the code refuse to disagree.
Done-check: `python3 bds.py selftest` (the doc/code drift assertion)

### U4. The passport consumer
`bds.py passport`. Reads `<root>/.sbe/passport.json`, applies BrotherMode's own
hollow-value rule verbatim, reports NO-DATA for what is absent. Reads nothing
else under `.sbe/` and never touches `.brothermode/store.sqlite3`.
Done-check: `python3 bds.py selftest`

### U5. The handoff package reader
`bds.py handoff`. The five-item package BrotherSBE contracted on 2026-08-11.
No wire format was ever ratified, so the shape this reads is PROPOSED and says
so in its own output. Missing items are NO-DATA, never absent-equals-fine.
Done-check: `python3 bds.py selftest`

### U6. The integration document
`docs/TRIUMVIRATE-INTEGRATION.md`. The four seam artifacts, the direction of
travel for each, what each product may and may not read, the shared verdict
vocabulary, and the plain-language terminology map.
Done-check: `python3 bds.py selftest` (the seam-artifact drift assertion)

### U7. Validation
`/brothersbe:verify` and the silent-failure lint, run against the tree after
U2 to U6 have landed. NO-DATA is reported as NO-DATA, never as a pass.
Done-check: `sbe score --strict --strict-soft` output quoted

### U8. Progress page, vault, push
`GANTT.html` regenerated and republished to the SAME artifact URL. Vault
session log and Overview updated. Commits pushed at every green.
Done-check: `git status` clean, `HEAD == @{u}`, artifact URL unchanged

## What this session may not do

- Ratify the boundary question. It is section 3 of a founder directive that
  names itself as founder-owned.
- Choose among the three paths in `OPTIONS.md`.
- Invent a ratified wire format for the BrotherSBE handoff package. A1's own
  warning: assuming a shape "will invent a contract BrotherSBE never ratified,
  which is exactly what this decision was written to prevent".
- Edit BrotherMode or BrotherSBE. Both are separate projects with their own
  canonical roots. Anything they must change is written as a request, not a
  patch applied across a project boundary.

## Status at 01:52 JST

Seven of eight units closed. Each done-check below was run after the last edit
of its unit and its output is quoted.

**U1 CLOSED.** `grep -c "Option [ABC]" docs/BOUNDARY-STUDY-2026-08-16.md` returned
`10`. The study recommends splitting items 6 and 7 and says plainly that this may
read as a fourth option, which is still the founder's to take.

**U2, U3, U4, U5 CLOSED**, all on one check, run last at 01:51 JST:

    $ /usr/bin/python3 bds.py selftest
    SELFTEST PASS

Assertion count went 34 to 56 (`grep -c 'expect(' bds.py`). The chain document
and the CHAIN table are held equal by assertion; the drift control was seen to
fail before the document existed, which is how it was known to work.

**U6 CLOSED.** The isolation control was calibrated by reinjection in a scratch
copy, never in this tree:

    SELFTEST FAIL: this file may not name '.brothermode': it is on the far side of the seam

**U7 CLOSED, and its result is mostly negative.** `sbe verify .` exited 0 and
`sbe score --strict --strict-soft .` exited 1. Of fifteen checks, ONE opened a
file in this repository: silent-failure-lints, PASS on `bds.py`, explicitly
silent about the other 35 files. The four hard gates all returned NO-DATA (no
dossier, no numbers manifest, no ran-receipt). The two FAILs, cache-economy and
correction-latency, are fed by the machine's vault and are not about this code.
**BrotherSBE did not meaningfully validate tonight's work, and saying it did
would reproduce a failure already in the founder's index twice.** The real
control on tonight's work is this product's own selftest.

**U8 CLOSED.** Pushed and verified at three agreeing points:

    HEAD      b5fea8d69eac4a9469b93c20ad85c20b7e9a597a
    upstream  b5fea8d69eac4a9469b93c20ad85c20b7e9a597a
    ls-remote b5fea8d69eac4a9469b93c20ad85c20b7e9a597a

Pull request 1 open at https://github.com/khalilmaaouni/BrotherDS/pull/1, base
`v1-claim-receipt`. Progress page republished to the same artifact URL it has
always had. Bitbucket half BLOCKED, not unverified: the workspace is read-only
over its user limit and only the founder can change that.

## What this session did NOT do, stated plainly

- Did not ratify the boundary question, choose a path, or invent a wire format.
- Did not edit BrotherMode or BrotherSBE. The two things they must agree to are
  written as requests in `docs/TRIUMVIRATE-INTEGRATION.md`.
- Did not measure authoring cost. Still due at week three.
- Did not arm the twice-hourly watchdog cron. The foreign-commit monitor was
  armed and stayed quiet for the whole run; the cron was skipped deliberately because
  this run was one continuous working session rather than a fleet, so its only
  effect would have been to spend the session's own context reporting to a
  sleeping founder. Stated here rather than left as a silent gap.
- Did not run the humanizer over the pull request body. Deliberate, to keep
  context for the progress page and the vault log, and said out loud rather than
  skipped quietly.

## One process near-miss worth keeping

A commit silently did not happen because `grep -c` exits 1 when its count is
zero, and it sat in an `&&` chain ahead of `git add`. The dash scan PASSING is
what broke the chain. Nothing was lost, because the next command printed the old
commit and the discrepancy was visible. Any scan whose success is an empty result
needs `|| true` before it gates anything.
