# BrotherDS: three paths for the next 90 days

Written 2026-08-16, overnight, for Khalil to read on waking. Built from the
actual files: bds.py read in full, the five claims in claims/, the five
research files in research/, docs/SCOPE-2026-08-12-founder-directive.md, the
The first target estate's PROJECT.md, and the prior spec at ~/Documents/BrotherData-Copilot-Spec
(decision/WHAT-SURVIVES.md and proposals/SPEC-v2.md). Nothing is described
that was not opened.

Two sentences of ground truth first. The tool that exists proved its worth
tonight by REFUSING and by FINDING, not by certifying: five real claims, zero
passes, two genuine failures (a forecast 2.88x worse than doing nothing, a
causal claim with no design), one real defect (product_id merges draft beer
with bottled beer across 2,350 ids). And the code has one telling gap: bds.py
line 11 advertises a `score` command, but main() implements only check,
receipt, and selftest, so the half that lets reality judge a claim, the north
star itself, is not built.

---

## The one-page summary

| | Option 1: THE CLOSED LOOP | Option 2: THE NIGHT AUDITOR | Option 3: THE OPEN REFEREE |
|---|---|---|---|
| The bet | Trust comes from one complete loop, claim to reality, run on real work until the ledger speaks | Trust comes fastest from defects found in numbers already believed, no behaviour change asked | The receipt format itself is the product; strangers adopt it in public |
| Wedge | The claim | The defect | The standard |
| First user | Khalil, on the pilot estate FY2027 plan numbers | Khalil, sweeping the three unexamined lakehouse databases | A stranger from the plugin marketplace |
| Of the 13 scope items, serves now | 1, 2, 3, 7 (in embryo), 8 (in embryo), 9, 10, 13 | The trust slice of 1 and 3 only | None directly this quarter |
| Boundary question presumed | Option A | None; survives A, B or C unchanged | Option A; broken by C |
| Mid-October the first target estate proof | Neutral, with one sized assist | Helps, modestly | Competes |
| Ledger (north star) | Starts day one, thin | Deferred the whole quarter | Deferred indefinitely |
| The single measurement | 10 or more claims scored against arrived reality by day 90, ledger page live | 3 or more confirmed defects that forced a correction to a filed or presented number | One external user files a claim receipt on their own data, unprompted |
| Rank | 1 | 2 | 3 |

---

## The wider ground every option now stands on

**The 2026-08-12 directive is thirteen items, not one.** Tonight's decisions
narrow V1 to the claim, the gates, and the reality loop; they do not delete
the other items. Each option below states which items it serves now, which it
defers, and which it refuses. Numbering used throughout: 1 data science, 2
business science, 3 data analytics, 4 business intelligence, 5 business
analysis upstream, 6 project management and delivery framework, 7 value
realization tracking, 8 self-improvement loop, 9 assistance to individuals
and teams, 10 human or agentic delivery, 11 the first target estate stack integration, 12
personalization by persona, 13 low inference cost.

**The open boundary question stays open.** Directive section 3 puts items 6
and 7 on ground BrotherMode and BrotherSBE already hold, offers three
resolutions (A: BrotherDS owns the question and reads the other two's
records; B: BrotherDS owns the analytical delivery lifecycle end to end; C:
restructure the triumvirate), and says an implementer must not answer it.
Nothing below answers it. Each option states which resolution it presumes, so
your one choice settles both questions at once. Option 1 additionally
delivers the one focused study the directive itself says the decision needs:
whether analytical work can be represented as a change record without
distortion. A study, not a verdict.

**the first target estate is Snowflake-only, agentic-first, bilingual, with a mid-October
proof roughly eight weeks out.** Its native surface already ships Cortex
Analyst, Cortex Search, Cortex Agents, semantic views, dbt model contracts,
data metric functions and Snowflake Trail. None of the options below builds
natural-language-to-SQL, a semantic layer, search, or cost metering: Cortex
and Snowflake budgets own those. What Cortex does not do, confirmed against
its own docs in research/B1, is exactly the BrotherDS thesis: no receipt
binding a number to its query, data version, method and uncertainty; no
scoring of a claim against the later outcome; no refusal of causal language.
The estate's recorded constraints bind every option: data never leaves the
environment (bds.py already fits: it runs where the data lives and its
receipts carry SQL, aggregates and verdicts, never rows), the dominant fear
is a confidently wrong number in front of leadership (the founder's own
words, a month before tonight), and per-persona answers must reconcile or
the first month-end disagreement destroys the product.

**The prior spec strengthens tonight's direction; it does not contradict
it.** The red-teamed v2 at ~/Documents/BrotherData-Copilot-Spec concluded
that the trust mechanism is "the only component that answers a failure the
customer's own corpus demonstrates rather than asserts" and the only item
with no competing vendor, and recommended proving it against the pilot estate's figures
"because that is where the evidence is". That is an independent, month-old
endorsement of the receipt wedge and the pilot estate proof bed. The same red team
killed the Excel-elimination promise, the Gemba rail, matching-before-
ADR-0004, and standalone ranked-insight packaging; no option below rebuilds
any of them. One inconsistency to surface rather than resolve: that spec and
ADR-0001 describe a dual Databricks-plus-Snowflake estate with an October
gate, while your 2026-08-12 directive records the commercial MVP as
Snowflake-only. If Snowflake-only is now the whole story, the spec's
cross-surface agreement test has nothing to test (its own failure condition
3) and the piece of it that survives is the publication-gate and trust
mechanism, which is the same shape as the BrotherDS receipt. The two lines
of work then converge, and their relationship is a founder decision the
directive already flags as unreconciled. One line from you settles it.

---

## Shared mechanics (settled tonight, common to all three)

- The nine gates, five origins, and PASS / FAIL / NO-DATA stay as built; the
  tuple already matches BrotherSBE's (tools/sbe_checks.py:431, per A1).
- The BrotherSBE handoff package has decided content and no wire format on
  disk (A1). Every option PROPOSES a format to you and builds nothing
  against it until you ratify.
- BrotherMode has no plugin point (A2). Every option registers BrotherDS in
  tools/toolkit_routes.json, the one data-driven surface, and edits no core
  file. VERIFIED REALITY is the one chain stage nobody owns; BrotherDS
  `score` is proposed as its owner, as a decision, never as an edit.
- LLMs author and flag; deterministic code verifies (decision 12; B2 Block
  5: 6 to 35 percent task reliability on exactly this work). This is also
  how item 13 is served: gates cost no inference.
- Repo goes under git, GitHub main. The Bitbucket half of the two-host law
  is BLOCKED today (workspace read-only, standing blocker), so parity ships
  as a host-neutral script proven locally and the Bitbucket run is recorded
  BLOCKED, not silently skipped.

---

## Option 1: THE CLOSED LOOP (recommended)

**The bet.** A number-trust product earns belief the same way it asks
numbers to earn it: make a claim, state its uncertainty, let reality arrive,
show the ledger. The 90 days go to running that loop end to end on real the pilot estate
decisions until the ledger has entries, however few.

### Thirteen-item map
Serves now: 1, 2 and 3 (the science and analytics of real claims), 7 in
embryo (every claim names the decision it feeds; scoring the outcome IS
value realization tracking at claim grain), 8 in embryo (scored outcomes
feed back into gate thresholds), 9 (one individual first), 10 (agentic
workflow with the four human decision points intact), 13 (deterministic
verification, bounded LLM authoring). Defers: 4, 5 (partially served by the
mandatory question and decision fields on every claim), 11 (offer artifact
only, integration after ratification), 12 (with its shape named: per-persona
answers reconcile through a gate proving disaggregate sums to aggregate, a
BrotherDS-native check, deferred not dropped). Refuses forever: building a
second project management or delivery framework, under boundary Option A,
which this option presumes: the ledger reads BrotherMode and BrotherSBE
records, it never keeps its own work-state.

### What it builds, in phases

**Phase 1, days 1 to 14: close the loop in code, make authoring cheap.**
- Implement `score` in bds.py: ingest an outcome (actual, observed_on,
  observed_by), compute the error, record whether the claim held inside its
  stated uncertainty. A claim whose uncertainty is NOT_ESTABLISHED can be
  scored for error but never counts as VERIFIED: there is no band to hold
  inside. Deliberate pressure toward stating uncertainty.
- A ledger command producing one page of counts, never percentages of tiny
  samples: registered, scored, held. Plain JSON stays in claims/.
- Package as a host harness plugin: a `bds-claim` skill that makes authoring
  a SIDE EFFECT of analysis. The analyst asks a question; the session writes
  the SQL, files the claim with derivations, grain and not_established
  populated; bds.py gates it; the receipt lands beside the answer. Nobody
  hand-writes JSON.
- Done-check: selftest 17 for 17 plus a score block, plus one full loop on a
  fixture claim: register, inject outcome, score.

**Phase 2, days 15 to 45: real the pilot estate decisions, start the clock.**
- Register forward-looking claims NOW for the pilot estate months elapsed in the world
  but not yet loaded (warehouse ends 2026-03; the raw archive tarball of
  2026-08-14 exists at the lakehouse). Register before extraction,
  timestamps in the claim, source_state recorded before and after the load.
  Data unseen is the honest equivalent of future data, and the receipt
  proves the order of events. This is how the north star reports in weeks.
- Re-run the FY2027 plan questions (the GMV base, the forecastability
  verdicts NET-FCST-002 and SKU-FCST-003 opened) through the plugin so every number
  in that plan carries a receipt.
- Week 3: time three claims end to end. This number decides survival (see
  the kill attempt).

**Phase 3, days 46 to 90: widen inside the loop, and the proposals.**
- The defect sweep, expressed as claims: GRAIN-005's own not_established
  list names the next job, the same key-integrity interrogation on the three
  unexamined lakehouse databases including a retail analysis database.
  Option 2 lives inside Option 1 as one phase, at claim discipline.
- Score everything whose reality has arrived; publish the ledger page.
- Three one-page papers for you: (a) the claim JSON as candidate wire format
  for the BrotherSBE package (it already carries the dataset with grain and
  snapshot, metric names, and open questions; it lacks the evaluation
  harness and labelled holdout, and says so); (b) BrotherDS `score` as owner
  of VERIFIED REALITY; (c) the boundary study the directive names: can
  analytical work be a change record without distortion.
- The the first target estate offer artifact: one page, tool unnamed per the vault law,
  offering to re-derive one recurring figure someone re-checks by hand,
  aimed at BLANK 1, the item the first target estate proposal says everything waits on.
  You deliver it, not the tool.

### What it refuses to build, and why the refusal is the point
No connectors (Snowflake included) this quarter: the pilot data is DuckDB on
this machine and a connector before ratified seams is a festival-of-features
vector. No NL-to-SQL, semantic layer, search or metering: Cortex and
Snowflake budgets own those and rebuilding them is dead on arrival. No
causal estimation engines: G4 refuses undesigned causal language, it does
not compute effects. No elicitation tooling beyond the protocol fields. No
BrotherSBE package consumer and no BrotherMode core edits before
ratification. No public marketing. No second delivery framework, ever,
under boundary A.

### Mid-October stance
Neutral, with one sized assist. Phases 2 and 3 run largely by agents, so
the founder-time draw is small and scheduled around the October lane. The
assist: a worked receipt on real the pilot estate figures plus the BLANK 1 offer is
evidence for the October trust narrative (the estate's recorded fear is a
confidently wrong number in front of leadership; the receipt is the
counter-artifact), without putting BrotherDS on the October critical path.
Nothing in this option must land before October for October to succeed.

### First user, first hour
The operator opens the host harness in the project directory and asks a real
question from the estate it is used on: what is the revenue base and what growth
is plausible. The session
does the analysis, files each number as a claim, gates it, and answers with
receipts beside the numbers. The hour ends with the ledger page showing
what was claimed, what reality will check, and when.

### The single measurement
By day 90: ten or more decision-grade claims scored against arrived
reality, on the ledger page, verified count beside scored count. Zero
scored claims by day 90 means the loop never closed and the option failed.

### Honest cost
Forecloses estate breadth this quarter: nothing runs inside the first target estate systems.
Three risks. Authoring cost: tonight's five claims took a full expert
session; if the plugin cannot cut a claim to minutes this collapses into
ceremony, the decorative record the first target estate proposal warns about. Data
cadence: if no new the pilot estate month can be loaded within 45 days, the ledger
starves. And one person is analyst and judge; reality-scoring is the design
answer (decision 3), but the optics remain until an outside user exists.

### The north-star silence
Answered head on: claim before load, score on load produces honestly
scored claims within weeks. Until then the page reports proxies labelled as
proxies: claims registered, gate-clean rate. Never the north star's name on
a proxy number.

---

## Option 2: THE NIGHT AUDITOR

**The bet.** Nobody asked for receipts, but everybody hates being wrong in
front of others; so the 90 days go to finding defects in numbers already
believed, each filed with proof, and the receipt discipline rides in behind
the pain relief.

### Thirteen-item map
Serves now: the trust slice of items 1 and 3 only. Defers everything else.
Refuses: item 6 construction (no delivery machinery of any kind). Boundary
presumption: none; it survives A, B or C unchanged, which is part of its
appeal as a hedge while you decide.

### What it builds, in phases
- Days 1 to 21: harden the interrogation that found GRAIN-005 into runnable
  sweeps: key uniqueness at declared grain, fan-out detection, many-to-many
  mapping discovery, structural-break scan on monthly series,
  reconciliation of any figure appearing in two places. Deterministic SQL
  over DuckDB, stdlib plus duckdb, every finding filed as a claim with two
  derivations.
- Days 22 to 50: sweep the three unexamined lakehouse databases, then the
  the pilot estate media-kit numbers against the warehouse (the vault records the filed
  ads model wrong by a factor of two once already). Each confirmed defect
  becomes a memo with receipts.
- Days 51 to 90: the first target estate offer aimed at BLANK 1: one recurring
  hand-checked figure, re-derived twice, defect or clean bill either way.
  Plus the same three one-page papers as Option 1.

### Mid-October stance
Helps, modestly. The BLANK 1 re-derivation and the sweep of
a retail analysis database (already on this machine, no data
movement) feed the October trust narrative directly, and the prior spec's
red team explicitly endorsed proving the trust mechanism on the pilot estate figures.
It does not touch the October build itself.

### First user, first hour
Khalil runs one command against a retail analysis database and
reads a defect memo or a clean bill, every finding carrying two
derivations. No new habits, no JSON, no ceremony.

### The single measurement
Three or more confirmed defects that forced a correction to a filed or
presented number by day 90. GRAIN-005 is the existence proof.

### Honest cost
Sharpest 30-day path, weakest 90-day one. Boundary collision: grain, fan-
out, keys and reconciliation are on BrotherSBE's implemented overlap list
(A1 section 4); as a product identity this rebuilds a sibling's claimed
ground and stands in a crowded market (Elementary, Great Expectations,
Soda, per B1). The north star stays silent all quarter: day 91 starts the
real product from zero. And defects run out: a finite estate, no loop, no
second act.

### The north-star silence
Not addressed, by design. The quarter measures defects found; verified
claim rate reports NO-DATA with that reason.

---

## Option 3: THE OPEN REFEREE

**The bet.** The claim receipt is a format the way lineage events are a
format; publish it MIT with a reference checker and let stranger adoption
prove the whitespace B1 confirmed is real.

### Thirteen-item map
Serves now: none of the thirteen directly this quarter; item 9 only at a
distance. That sentence is most of the verdict. Boundary presumption: A,
and actively broken by C (restructuring reopens ratified ground while a
public standard is being marketed).

### What it builds, in phases
Days 1 to 30: polish bds.py into a documented reference implementation;
write the claim-format spec; a worked example on shipped synthetic data
with planted flaws. Days 31 to 60: plugin on the marketplace, README
onboarding, the five the pilot estate claims anonymised as showcase. Days 61 to 90:
respond to whoever shows up.

### What it refuses to build
Real analysis on real estates, connectors, the ledger. The refusal is the
point only if the format is the moat.

### Mid-October stance
Competes. It spends founder attention on strangers in exactly the eight
weeks the October proof needs it, and contributes nothing to that date.

### First user, first hour
A stranger installs the plugin, runs selftest, runs the worked example,
files a first claim on their own CSV or DuckDB file.

### The single measurement
One external user files a claim receipt on their own data, unprompted,
within 90 days (the same unprompted-adoption bar BrotherSBE uses).

### Honest cost
A quarter spent on an audience that does not yet exist, while both
existing products record zero measured adoption (A3). The gates stop
improving because no real data flows. The north star can never report:
strangers' outcomes never arrive. It inverts the settled landing order
(decision 9: build on the pilot estate, offer the first target estate later) and competes with a dated
commitment. The right second-year move; as a first move it is the
festival-of-features failure wearing a licence file.

---

## Recommendation: 1. Closed Loop, 2. Night Auditor, 3. Open Referee

The Closed Loop wins because it is the only option that starts the clock
on the metric you chose. VERIFIED CLAIM RATE needs claims registered
before their reality arrives; every week without a scored claim is a week
the product cannot say what it is. The code makes the same argument from
the other side: check, receipt and the gates exist and passed their trial
tonight; score does not exist at all. The unbuilt half is the half you
named the north star, so the 90 days go there. The prior spec seals it:
an independent red team, a month ago, on the first target estate,
concluded the trust mechanism is the one component with no competing
vendor and told you to prove it on the pilot estate figures. That is this option.

The Auditor comes second, folded into the Closed Loop as Phase 3: the
defect wedge is real (GRAIN-005 proved it in one night) but as an identity
it rebuilds BrotherSBE's implemented ground and leaves the north star
silent for a quarter. The Referee comes third: publishing a standard
before one user has a track record argues the whitespace instead of
occupying it.

## The attempt to kill the favourite

The strongest case against the Closed Loop is authoring cost. Tonight's
five claims consumed a full expert session; twenty claims at that cost is
the quarter gone on JSON, and a receipt system nobody can afford to feed
becomes the decorative record the first target estate vault notes warn about. The
design answer is authoring as a side effect of analysis; the honest
answer is that this is unproven, so it is measured in week 3 with a named
flip condition below. Second attack: n will be small, three scored claims
prove little. Accepted: the ledger reports counts, never percentages, per
the standing progress-page law. Small honest numbers beat silent big
ones, which is the product's own thesis applied to itself. Third attack:
the thirteen-item directive makes any one-loop V1 look narrow. But
tonight's decisions chose the claim as the unit and reality as the judge;
the loop is the smallest thing that honours all twenty answers, and the
map above shows eight of thirteen items served or seeded rather than one.

## What would change my mind

- If you pick boundary Option B, the Closed Loop does not flip, it
  expands: the ledger becomes the analytical delivery record. Only C
  forces a redesign, and C is the directive's own least-favoured path.
- If the first target estate's BLANK 1 gets filled soon (a named recurring hand-checked
  figure with a remembered occasion it was wrong), the Auditor jumps to
  first: a real outside user with felt pain beats an internal loop.
- If the week-3 measurement shows a claim still costs more than 30
  minutes through the plugin, fall back to the Auditor, which needs no
  authoring.
- If no new the pilot estate month can be loaded within 45 days, the ledger starves
  and the Auditor becomes the only option with fuel.
- If October pressure spikes and the founder-time budget shrinks to near
  zero, run the Auditor's days 1 to 21 only, because its sweep is the
  cheapest artifact that still feeds the October trust narrative.
