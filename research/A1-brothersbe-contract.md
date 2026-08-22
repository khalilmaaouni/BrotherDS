# A1: The BrotherSBE contract that BrotherDS must honour

Extracted read-only from `/Users/khalil.maaouni/Documents/Brothersbe` on 2026-08-16.
Every quote below carries its file path and line number, taken from the file
as it exists on disk today. Nothing here is paraphrase presented as quote;
paraphrase is marked as such.

## Priority files: FOUND / ABSENT

- FOUND: `docs/specs/2026-08-11-analytics-partnership-design.md` (235 lines), read in full.
- FOUND: `docs/ECOSYSTEM.md` (189 lines), read in full.
- FOUND: `docs/DIRECTION.md`, read (lines 1-90), the product-identity page one level above the analytics spec.
- FOUND: `docs/ADOPTION.md` (120 lines), read in full. Does NOT contain the six-taxes / buyer-is-reviewer language.
- FOUND: `SKILL.md` (root), spot-read for verdict vocabulary and gate language.
- FOUND: `references/laws-hard-gates.md`, `references/laws-full-digest.md`, `LAWS-REFERENCE.md`, spot-read.
- FOUND: `agents/data-reviewer.md`, `agents/evidence-auditor.md`, `agents/qa-reviewer.md`, read in full.
- FOUND: `tools/sbe_checks.py`, `tools/sbe_gate.py`, `tools/sbe_score.py`, grepped for verdict/state machinery, not read line by line.
- FOUND: `docs/specs/2026-08-11-v3-refocus-and-release-plan.md`, the source of the six-taxes and journey language (not in the priority list but is where those two topics actually live).
- FOUND: `docs/specs/2026-08-15-change-passport-seam.md`, exists, but confirmed it does NOT mention BrotherDS (see "two different seams" note below).
- ABSENT: `design-inputs/` directory does not exist in this repo (`bfs: error: design-inputs: No such file or directory`).
- ABSENT: any file containing the literal phrase "receive/request/run ladder" or "receive, request, run", searched `docs/`, `references/`, `NORTH-STAR.md`, `LAWS-REFERENCE.md`, `docs/ADOPTION.md`, `docs/DIRECTION.md`. Not found anywhere in the repo. If this ladder was described to you as an existing BrotherSBE artifact, it is not written down under that name here; treat any claim about it as unverified.
- ABSENT: any mention of "the first target estate" or "beverage"/"RGM" as a named client use case anywhere in the tracked repo (checked recursively, all file types). The analytics-partnership spec's own worked example is explicitly a synthetic estate, not a named client (see item 7 below).

## 1. The BrotherDS contract in <=10 bullets

- DECIDED. The line: "**BrotherSBE is not the data scientist. It is the colleague who prepares the data, provides the methods and the infrastructure, and validates the results.** A separate product, BrotherDS, will own the science itself and this one will collaborate with it.", `docs/specs/2026-08-11-analytics-partnership-design.md:14-18`
- DECIDED. The rule that names the boundary verbatim: "So the line is: **everything around the model, never the model.**", `docs/specs/2026-08-11-analytics-partnership-design.md:20`
- DECIDED. What BrotherSBE owns on its side of that line: "BrotherSBE owns the data preparation and its contracts, the feature and label pipeline, the evaluation harness, the metric definitions and their misuse guards, reproducibility, and the deployment path. It never chooses a model, never tunes one, and never interprets a business result.", `docs/specs/2026-08-11-analytics-partnership-design.md:22-25`
- DECIDED. Where a modeling decision is needed instead of made: "Where a decision needs domain judgement it emits a decision table (recommendation, first and second alternative, what would flip it) and hands the judgement over.", `docs/specs/2026-08-11-analytics-partnership-design.md:25-27`
- DECIDED. The fifth persona: "Data scientists and analysts join as a FIFTH persona inside the existing star, not as a new star.", `docs/specs/2026-08-11-analytics-partnership-design.md:33-34`. Confirmed a second time in the product-identity page: "The data scientist or analyst, as the fifth persona inside the same star.", `docs/DIRECTION.md:66`
- DECIDED. What reaches the user is code the user owns, not a live connection by default: "A **runnable project folder**, versioned in the user's own repository: SQL that runs in their warehouse, a notebook that runs on their cluster, a metric definitions file, a checks file they can schedule, and a README... Integration is **artifacts first, live connection optional**.", `docs/specs/2026-08-11-analytics-partnership-design.md:52-58`
- DECIDED. Data never leaves the user's environment: "**Personal data never leaves their environment.** Artifacts are schema-only: BrotherSBE emits queries and rules that run where the data lives and reads back aggregates, counts and metrics, never rows.", `docs/specs/2026-08-11-analytics-partnership-design.md:63-65`
- DECIDED. Naming: "**The analytics partnership.** It describes the relationship rather than the technology, and it never implies BrotherSBE does the science.", `docs/specs/2026-08-11-analytics-partnership-design.md:233-234`
- DECIDED (sequencing, not yet built). Building on this design is explicitly gated behind other work and is design-only as of the branch that wrote it: "This delivery produces the design, the decision tables, the metric definitions catalog and the booklet outlines. Building starts the day the four user journeys pass, with no rediscovery.", `docs/specs/2026-08-11-analytics-partnership-design.md:213-215`. So: nothing in this capability area is IMPLEMENTED yet in the ordinary code sense, the whole analytics-partnership content is DECIDED but not built. I checked for a shipped analytics decision table, checks, or skill and found none (searched `references/laws-decision-tables.md`, `agents/`, and `tools/` for analytics-specific names; none exist beyond the two reviewer agents already in the OVERLAP LIST below, which predate and are not analytics-specific).
- DECIDED. Success bar, one concrete outcome: "**a real duplicate rate cut on one estate**, with precision and recall reported against a labelled sample and the figure reproduced by an independent derivation. Breadth of features is not the bar.", `docs/specs/2026-08-11-analytics-partnership-design.md:226-228`

## 2. The handoff package shape

DECIDED (not yet IMPLEMENTED, no code artifact for it exists on disk; it is a design decision only). Verbatim from `docs/specs/2026-08-11-analytics-partnership-design.md:36-48`, heading "## The BrotherDS handoff package, contracted now":

> "Decided now so today's work is not rebuilt when BrotherDS starts. BrotherSBE produces a named package and BrotherDS consumes exactly that:
> 1. The prepared dataset, with its grain, its contract, and its snapshot id.
> 2. The evaluation harness, including the split definition.
> 3. The metric definitions that apply, by name and formula.
> 4. The labelled holdout, with who labelled it and when.
> 5. The open questions BrotherSBE could not answer, stated rather than guessed.
> The two products meet at a document, not at a guess. Anything not in the package is not handed over."

Direction of travel: BrotherSBE → BrotherDS, one way, document-mediated ("meet at a document, not at a guess"). No field names, file format, or serialization are specified anywhere in the repo, no JSON schema, no filename convention for this package exists in `tools/` or `references/`. So while the five-item CONTENT shape is DECIDED, the exact SHAPE (field names, file format) is NOT SPECIFIED beyond that five-item list.

Note on "the seam": there IS a formally specified seam document in this repo, `docs/specs/2026-08-15-change-passport-seam.md`, but it is the BrotherMode <-> BrotherSBE change-passport seam, not a BrotherSBE <-> BrotherDS seam. I grepped it for "BrotherDS" and got zero hits. Do not conflate the two: the change passport is a different, already-partially-implemented contract between the two existing products; the BrotherDS handoff package above is a separate, purely-designed, not-yet-built contract for the third product.

## 3. The evidence receipt / verdict vocabulary, as actually implemented

BOTH (implemented in code, and the same words are used in law/spec prose).

- IMPLEMENTED. Check-level verdict tuple, exact source: `VERDICTS = ("PASS", "FAIL", "NO-DATA")`, `tools/sbe_checks.py:431`.
- IMPLEMENTED. Gate-level verdict set is those three plus a fourth, ranked: `rank = {"FAIL": 0, "NO-DATA": 1, "WAIVED": 2, "PASS": 3}`, `tools/sbe_gate.py:1742`, with the worst verdict across all gates chosen by `min(...)` on that rank, `tools/sbe_gate.py:1743`.
- IMPLEMENTED. Meaning of NO-DATA, stated in the gate code's own comment: "NO-DATA neither blocks nor passes... [it] simply is not told that something was proved when nothing was.", `tools/sbe_gate.py:1667` region (comment) and law text at `references/laws-hard-gates.md:24` (approval gate example): "No approval claim and no APPROVAL file is NO-DATA."
- IMPLEMENTED. Meaning of WAIVED: a gate that would otherwise fail is reported as WAIVED with the reason quoted, and WAIVED never counts as a pass: "a waiver prints as WAIVED, quoting the reason", `tools/sbe_gate.py:208`; "WAIVED is not a pass either", `tools/sbe_gate.py:1667`.
- IMPLEMENTED, narrower scope. `STALE` and `INVALID` exist as reported states, but only inside two specific test/policy paths, not in the core `VERDICTS` tuple: `STALE` appears in `tools/test_sbe_handover.py:544,1160` and `tools/test_sbe_policy.py:410,424`; `INVALID` appears as a tier/check state in `tools/test_sbe_policy.py:267,645,655` (e.g. `check:migration-rehearsal` state `INVALID`, tier `T3` state `INVALID`). These read as states of a policy/tier object, not as one of the four canonical PASS/FAIL/NO-DATA/WAIVED gate verdicts. I could not find a single enum or constant list that includes STALE and INVALID alongside the core four, flag this as unresolved rather than asserting a six-word vocabulary.
- Which script decides them: `tools/sbe_checks.py` defines the base three-verdict contract each individual check returns (with `empty_expect`/`full_expect` parameters, `sbe_checks.py:438-475`); `tools/sbe_gate.py` aggregates checks into gates and adds WAIVED plus the cross-gate worst-verdict ranking (`sbe_gate.py:1601-1743`); `tools/sbe_score.py` is a third script that also emits PASS/FAIL lines for its own scorecard checks (e.g. `sbe_score.py:282,292,330,398,489,514,557,572,596,626,962,975,977,1121,1280,1365,1396,1659`) but does not add new verdict words beyond PASS/FAIL.

**Exact verdict strings, final answer:** `PASS`, `FAIL`, `NO-DATA` (canonical three, `tools/sbe_checks.py:431`), plus `WAIVED` at the gate-aggregation layer (`tools/sbe_gate.py`). `STALE` and `INVALID` exist in the codebase but as narrower policy/tier states, not confirmed as first-class members of the same enum, reported as observed, not asserted as canonical.

## 4. The OVERLAP LIST, what BrotherSBE already covers in data/analysis (BrotherDS must not rebuild)

All IMPLEMENTED (agent definitions and law text on disk today, not just designed).

- Grain discipline: "Every fact model states what one row means. A model whose grain is not written down anywhere is the finding, before any query is read.", `agents/data-reviewer.md:16-17`
- Fan-out / join cardinality checking: "For every join: the expected cardinality, and whether the row count after the join is what that cardinality implies. An aggregation sitting downstream of a potentially multiplying join is Critical until proven otherwise.", `agents/data-reviewer.md:19-20`
- Key and integrity checks (declared keys unique, declared relationships resolve, duplicate source records handled explicitly), `agents/data-reviewer.md:21-23`
- System-of-record determination per entity, and what happens when two sources disagree, `agents/data-reviewer.md:24-25`
- Reconciliation as a hard requirement: "A figure that could reach a decision needs a second derivation that is genuinely independent... State which kind of independence you actually found: structural, semantic, or externally validated.", `agents/data-reviewer.md:26-30`, mechanically enforced by the four-condition manifest check described in `references/laws-hard-gates.md:10` (pinned snapshot_id, textually-different second derivation, a marked re-run, zero drift between the two results).
- Temporal correctness: effective date vs load date, SCD strategy, timezone/business-date definitions, as-of reproducibility, future leakage, `agents/data-reviewer.md:31-34`
- Money semantics: refunds, cancellations, corrections, late-arriving records, currency/rounding, period close, `agents/data-reviewer.md:35-37`
- Freshness and quality: freshness, completeness, validity, uniqueness, consistency, volume checks with ownership and escalation, `agents/data-reviewer.md:38-40`
- Cost and performance: materialization strategy, partitioning/clustering, full-scan detection, incremental vs full refresh, `agents/data-reviewer.md:41-43`
- Migration rehearsal evidence (forward and reverse, row counts before/after a restore) as a hard gate, `references/laws-hard-gates.md:17`, enforced code at `tools/sbe_gate.py` (row-counts/rehearsal gate).
- QA traceability and evidence honesty: requirement-to-test mapping, test class distinction, negative coverage, calibration (does re-injecting the defect make the test fail), stability, environment/data versioning, regression scope, "read the actual test output rather than the summary someone wrote about it", `agents/qa-reviewer.md:13-34`
- Evidence provenance auditing as a dedicated, adversarial, read-only role: origin, commit binding, applicability, internal consistency, resolvability, independence, freshness, trust level, `agents/evidence-auditor.md:16-37`. The analytics spec explicitly routes analytics evidence through this SAME agent rather than minting a new one: "Verification of analytics claims goes to the **existing evidence auditor**, extended with analytics cases: it attacks the labelled set's provenance, the split discipline, and whether the second derivation was genuinely independent. Reusing the strongest control beats minting a new one.", `docs/specs/2026-08-11-analytics-partnership-design.md:171-174`

## 5. The adoption laws (six taxes, buyer-is-reviewer)

DECIDED. Found in `docs/specs/2026-08-11-v3-refocus-and-release-plan.md`, NOT in `docs/ADOPTION.md`.

- Verbatim, six taxes named: "The tax analysis decomposed the adoption cost into six taxes (install, learning, intake, change, risk, social). The strategy charges none of them:", `docs/specs/2026-08-11-v3-refocus-and-release-plan.md:340-341`
- Verbatim, risk tax and reporting mode: "Nothing to install and nothing to learn: the pipeline reports and a page arrives. Reporting mode cannot fail a build, so the risk tax is zero.", `docs/specs/2026-08-11-v3-refocus-and-release-plan.md:343-344`
- Verbatim, buyer is the reviewer: "The buyer is the reviewer. The packet lands on the people whose review time is the constraint; authors follow because the reviewer asks for the packet.", `docs/specs/2026-08-11-v3-refocus-and-release-plan.md:345-346`
- Verbatim, intake tax timing: "The intake tax falls in R1 when the tier becomes computed.", `docs/specs/2026-08-11-v3-refocus-and-release-plan.md:347`
- Verbatim, standing refusals: "The anti-patterns stay refusals by name: no pilot, no training session, no kickoff meeting, no team-wide rollout, no blocking to demonstrate value, no document about the method instead of their problem.", `docs/specs/2026-08-11-v3-refocus-and-release-plan.md:348-350`
- Verbatim, measured proof thresholds: "Proof thresholds, measured not felt: one artifact read to the end unprompted; one unprompted request for a second; a number the system produced quoted in a meeting nobody from this side attended.", `docs/specs/2026-08-11-v3-refocus-and-release-plan.md:351-353`
- Same "reviewer receives a pack, not a request to install" idea restated independently in `docs/DIRECTION.md:84-86`: "Paved road, not forced road. Nothing to install, nothing to learn, no intake before work: the pipeline reports and never blocks, the reviewer receives the Assurance Pack, and authors follow because the reviewer asks for it."
- ABSENT: no phrase "receive/request/run ladder" anywhere in the repo (searched as noted above). If BrotherDS planning assumed this ladder is an existing SBE artifact, that assumption is not backed by anything on disk here.
- ABSENT: "CI in reporting mode" as an exact phrase was not found verbatim; the closest is "Reporting mode cannot fail a build" (`docs/specs/2026-08-11-v3-refocus-and-release-plan.md:344`) and "the pipeline reports and never blocks" (`docs/DIRECTION.md:85`), same concept, different exact wording. Treat "CI in reporting mode" as paraphrase of a real, DECIDED concept, not a verbatim law name.

## 6. Snowflake, Databricks, Tableau, DuckDB, tool mastery, analytics estate

DECIDED, narrow. Only one sentence in the priority spec touches this: "Order follows the ratified tool decision: Snowflake first, then Databricks, then the rest.", `docs/specs/2026-08-11-analytics-partnership-design.md:60-61`. No Tableau or DuckDB mention anywhere in `docs/specs/2026-08-11-analytics-partnership-design.md`, `NORTH-STAR.md`, or `docs/DIRECTION.md`. There is a separate parked item, "tool mastery," referenced by filename only: `docs/plans/PARKING-LOT-tool-mastery.md` and `docs/handover-2026-08-11/06-parking-lot-tool-mastery.md` exist as files (titles only confirmed by `find`, not opened in full, flagging so this is not overclaimed as read). `docs/snowflake-elt.md` also exists as a separate file not opened in full for this pass.

## 7. The first target estate, or a beverage and RGM use case

ABSENT. No occurrence of the first target estate's name anywhere in the tracked repository (recursive search, all files). No occurrence of "beverage" or "RGM" as a named client scenario in `docs/`. The ONLY beverage-flavored content is a deliberately anonymized, synthetic worked example described in the priority spec itself: "Worked examples run on a **generated synthetic estate with planted flaws**: a beverage-distribution shaped dataset with duplicate customers carrying realistic name variations, seasonal demand with promotions, a hierarchy that does not reconcile, and deliberate nulls... Client realities reach the work as **anonymized archetypes in public** with the real mapping held only in the private vault.", `docs/specs/2026-08-11-analytics-partnership-design.md:201-208`. This is a generic beverage-distribution archetype, not a client name, and the text itself states real client mappings are deliberately kept out of this repo and held in the private vault instead.

## Top 3 things that would break BrotherDS if ignored

1. **The line itself.** If BrotherDS builds anything that chooses, tunes, or interprets a model's business result, it violates the founder's own framing decision ("everything around the model, never the model," `docs/specs/2026-08-11-analytics-partnership-design.md:20`) and duplicates work BrotherSBE already claims (data prep, evaluation harness, metric definitions, reproducibility, deployment path, same line, 22-25). BrotherDS's job is the model itself and nothing else on that list.
2. **The handoff package has no wire format yet.** The five-item content list (dataset+grain+snapshot, evaluation harness+split, metric definitions, labelled holdout+provenance, open questions) is DECIDED but there is no schema, filename, or serialization committed anywhere (`docs/specs/2026-08-11-analytics-partnership-design.md:36-48`; confirmed no such schema file exists in `tools/` or `references/`). If BrotherDS assumes a shape (e.g. JSON with specific field names) without going back to the founder to pin it, it will invent a contract BrotherSBE never ratified, which is exactly what this decision was written to prevent ("Decided now so today's work is not rebuilt when BrotherDS starts").
3. **Reusing evidence-auditor, not minting a new verifier.** The spec is explicit that analytics claim verification routes through the EXISTING evidence-auditor agent, extended with analytics-specific attack cases (labelled-set provenance, split discipline, independence of derivations), rather than a new BrotherDS-side verifier (`docs/specs/2026-08-11-analytics-partnership-design.md:171-174`). If BrotherDS builds its own verdict/evidence machinery instead of calling into BrotherSBE's PASS/FAIL/NO-DATA/WAIVED gate contract (`tools/sbe_checks.py:431`, `tools/sbe_gate.py:1742`), the two products will produce two different, unreconciled notions of "verified," which is the precise failure this whole design exists to prevent.
