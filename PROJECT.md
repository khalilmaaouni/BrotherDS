# PROJECT: BrotherDS

Canonical path: `~/Documents/BrotherDS`
Started: 2026-08-12 (scope defined by the founder; nothing built)
Owner: Khalil Maaouni

## What this is

The third product of the triumvirate. BrotherMode governs one person's session.
BrotherSBE governs one change's passage between people. **BrotherDS governs the
question and the answer: what is worth knowing, what the answer is, who it is
for, and whether the answer created value.**

Status as of 2026-08-22: pushed PRIVATE to github.com/khalilmaaouni/BrotherDS,
branch `feature/north-star-chain-and-native-seam` at `8084340`, equal to
origin. PR 1 is OPEN into `v1-claim-receipt`. Last night's commits de-named
the design documents, added master data gates G11 to G14, and wrote the
one-product page. The founder answered four of BrotherDS's six vault
decisions on 2026-08-22: the two seam requests granted, the verified-reality
owner split by unit with the ledger at BrotherDS, and the vault space
proposed at the merge; decisions 1 (the path) and 2 (the boundary question)
are still his. See `docs/ROADMAP-POINTER-2026-08-23.md` for the full record.

Key commands:

```bash
/usr/bin/python3 bds.py selftest              # 32 assertions
/usr/bin/python3 bds.py check claims/x.json   # the ten gates
/usr/bin/python3 bds.py ledger claims/        # the verified claim rate
```

Note the interpreter: `duckdb` is installed under `/usr/bin/python3` (3.9.6) on
this machine, not under `~/.local/bin/python3`.

## Scope, per the founder directive of 2026-08-12

Full text: `docs/SCOPE-2026-08-12-founder-directive.md`. In short, BrotherDS
covers:

1. Data Science
2. Business Science
3. Data Analytics
4. Business Intelligence
5. Business Analysis, upstream of the work rather than after it
6. Project Management and the delivery framework
7. Value realization tracking
8. A feedback loop for self-improvement
9. Assistance to data science individuals and to teams
10. Answers delivered either through humans or through full agentic workflows
11. Integration with the first target estate's data stack
12. Personalization by persona: per role, per objective, per customer
13. Low inference cost, the right delivery method, and the right cost

## The open boundary question, raised 2026-08-12

Items 6 and 7 above (project management, delivery framework, value realization)
overlap with ground BrotherMode and BrotherSBE already hold. That overlap is
NOT resolved and must not be resolved by an implementer. See the directive file
for the three options put to the founder.

## Related projects

- `~/Documents/BrotherModeUp` (BrotherMode, product source)
- `~/Documents/BrotherSBE` (BrotherSBE, product source). Its
  `docs/specs/2026-08-11-analytics-partnership-design.md` holds the contracted
  five-item handoff package from BrotherSBE to BrotherDS.
- `~/Documents/the first target estate` (first target estate; Snowflake-only commercial MVP)
- `~/Documents/BrotherData-Copilot-Spec` (earlier related specification work,
  not yet reconciled with this scope)

## Deliverables so far

| Output | Path | State |
|---|---|---|
| Founder scope directive | `docs/SCOPE-2026-08-12-founder-directive.md` | recorded |
| Identity file | `PROJECT.md` | this file |
| Product spec | `SPEC.md` | written 2026-08-16, includes the reconciliation |
| Three paths, ranked | `OPTIONS.md` | awaiting founder selection |
| Engine | `bds.py` | built, 32 assertions passing |
| Claude Code skill | `skills/brotherds/SKILL.md` | written, not yet installed |
| Progress page | `GANTT.html` | published, one stable link |
| Research | `research/A1` to `A4`, `B1`, `B2` | six files |
| Real claims and receipts | `claims/`, `receipts/` | gitignored, real the pilot estate data |

Open and owned by the founder: which of the three paths; the boundary question
in directive section 3; whether to push to GitHub.
