# A4: prior-work reconciliation for tonight's BrotherDS design (2026-08-16)

Comparing SPEC.md (tonight) against BrotherData-Copilot-Spec (2026-07-31, red-teamed) and the first target estate (whitepaper 2026-08-12, fleet green team 2026-07-14, founder directive 2026-08-12). Read-only. Quotes are verbatim with file paths.

## SURVIVORS (WHAT-SURVIVES.md, 2026-07-31 red team verdict)

1. **"The trust mechanism... it is 'the only component that answers a failure the customer's own corpus demonstrates rather than asserts', it is mechanical, it is cheap... It is also the only item in the whole scope with no competing vendor identified."** (`decision/WHAT-SURVIVES.md:12-16`), **IGNORED.** Tonight's nine gates check reproduction of a single number against a single source (G5, G7). The prior mechanism is a *dual-run comparator whose right side changes across a lifecycle* (incumbent Excel, then own history), `decision/MECHANISM-V2.md:1-38`. Tonight's SPEC.md never cites this design or reuses its phased-comparator shape.

2. **"The semantic and metric layer specified against an interface... 'the one design decision in the scope that survives either outcome of the October gate'."** (`decision/WHAT-SURVIVES.md:18-19`), **IGNORED.** Tonight's SPEC.md has no semantic/metric-layer concept at all; a claim binds directly to SQL against DuckDB. No interface abstraction for a future Snowflake/Databricks seam.

3. **"The disproving test, specifically the condition 'the reader wants the Excel anyway'."** (`decision/WHAT-SURVIVES.md:20-22`), **IGNORED.** Tonight's SPEC.md has no disproving test or failure-condition-before-building discipline for BrotherDS itself.

4. **"Catalog and label remediation, narrowly scoped to the executive report set... `ULTRAPLAN.md:49`, 80 percent by week 6."** (`decision/WHAT-SURVIVES.md:23-25`), **IGNORED.** Tonight's G9 (grain/key uniqueness) is a related mechanical check but is not connected to this measured, dated the first target estate remediation target.

## CONTRADICTIONS, most severe first

1. **The definition problem is unaddressed.** Prior finding, quoted as the headline of the whole prior corpus: **"A definition is not a file. The one thing the architecture unifies is the one thing that was never the problem."** (`proposals/SPEC-v2.md:37-38`), resting on ADR-0001 verbatim: **"Gold modelling... happen here [Databricks]"** vs **"the semantic layer, Power BI, and the agent and question-answering surfaces [happen in Snowflake]"** (`proposals/SPEC-v2.md:44-52`). Tonight's SPEC.md G5/G7 gates only check that **"a stated value... reproduces"** from **one source** (`SPEC.md:141,166`), reproduction, not cross-definition agreement across surfaces. Tonight's design solves the reproduction problem the prior work explicitly says was never the hard one, and is silent on the definition-drift problem the prior work says is the actual one.

2. **Prior north star vs tonight's north star are different measurements of different things.** Tonight: **"Verified Claim Rate... the share of decision-grade claims... whose realised outcome fell inside the uncertainty they stated"** (`SPEC.md:31-33`), an outcome-scored, months-to-resolve metric. The first target estate's whitepaper, titled a north star for the same estate: **"Every number that reaches the CCO carries a traceable answer to 'where did this come from and who checked it', produced by the same agents that generate it, without a single byte of data leaving the Snowflake account."** (`whitepaper/the first target estate-Verified-Delivery-North-Star.md:12-14`), a point-in-time provenance guarantee, not an outcome-resolution rate. Both are RED-TEAMED/PROPOSED for their own estates but neither cites the other; if BrotherDS ever reports into the first target estate it will need to state which north star governs there.

3. **Unit is close but not identical.** Prior unit of value: **"P3 is not a separate product. It is P1's unit of value."** (`redgreen/green-P3-P4-P5-P6.md:53`), a retired report/receipt reconciled by dual-run, i.e. a **metric/report**, PROPOSED not ratified. Tonight's unit: **"BrotherDS takes the CLAIM as its unit: one number that reaches a decision"** (`SPEC.md:27`), narrower and more atomic, any number, not just a catalogued report metric. Not a direct contradiction, but tonight's design does not acknowledge the prior unit existed or say why "claim" supersedes "metric/report."

## PRIOR UNIT and PRIOR NORTH STAR

- Prior unit: no single ratified name; closest is **"unit of value"** = a metric/report under dual-run comparison (`redgreen/green-P3-P4-P5-P6.md:53,161,567`), RED/GREEN-TEAMED, not founder-ratified.
- Prior north star (BrotherData-Copilot-Spec corpus): **none found.** Grep for "north star" across the whole spec tree returns zero hits.
- the first target estate north star (separate estate, same triumvirate): quoted above, `whitepaper/the first target estate-Verified-Delivery-North-Star.md:12-14`. PROPOSED (whitepaper, not code).

## the first target estate GROUND TRUTH

- Estate = Snowflake-only commercial MVP, CCO + Commercial Leadership, agentic-first, JP/EN, VERIFIED (`PROJECT.md:8-9`, `whitepaper/...md:37-38`).
- Surface = Cortex Analyst, Cortex Search, Cortex Agents, semantic views, dbt model contracts, data metric functions, Snowflake Trail, VERIFIED, each capability in `fleet/03_green_team.md` carries a checked URL (rows 1-14 of Task 1 table).
- Personas = CCO/CLT aggregate, KAM/merchandiser disaggregate, VERIFIED (`whitepaper/...md:33-34`, `fleet/03_green_team.md:76-81`).
- Dates: checkpoint gate Oct 16 2026, December executive release, VERIFIED across `fleet/03_green_team.md:99-113` and `SCOPE-V2.md:81,169`.
- Data residency: no data leaves the Snowflake account; Tokyo (ap-northeast-1) primary region; cross-region inference has documented no-egress, no-persistence language, VERIFIED (`fleet/03_green_team.md:61`, `whitepaper/...md:272`).
- **Asset numbers, checked against the task's stated figures:** **800 reports total... 319 key reports detailed (exactly 319 CSV data rows); 123 executive-tagged (38.6 percent)**, CONFIRMED VERIFIED and correctly stated in the task; source explicitly says these **"supersede... The 848, 364, 142 and 214 figures used in every deck"** (`SCOPE-V2.md:138-145`).
- Databricks-vs-Snowflake ground truth is UNSETTLED, not a single fact: the infrastructure plan (2026-07-28) describes a two-plane Databricks-plus-Snowflake bridge under ADR-0001, **status "Proposed (27 July 2026)"**, gated 2026-10-16 (`SCOPE-V2.md:76-81`), while the later the first target estate whitepaper (2026-08-12) states the MVP itself is **"Snowflake-only"** (`PROJECT.md:8`, `whitepaper/...md:37`). Both are ASSERTED as current in their own documents; neither supersedes the other explicitly in the files read.

## WOULD DUPLICATE

- **PASS/FAIL/NO-DATA verdict vocabulary and gate framing**, already existed and was already inherited from BrotherSBE by the prior spec (`proposals/SPEC-v2.md:108`, `decision/PROGRAM-LOOPS.md:19`, `proposals/CANDIDATES.md:45`). Tonight's bds.py reimplements this vocabulary rather than importing/reusing BrotherSBE's existing gate engine (not verified against bds.py's code, flagged for direct check).
- **Cross-definition/cross-surface agreement testing**, the prior "definition compiler" + cross-surface agreement test (`proposals/SPEC-v2.md:66-90`) is the mechanism tonight's design would eventually need to build to close the definition-drift gap named above; building it fresh later duplicates design work already red-teamed once.
- **Native Snowflake data-quality mechanisms** (DMFs for freshness/null/duplicate/row-count, dbt model contracts, Snowflake Trail) are explicitly catalogued as "leverage rather than rebuild" for the first target estate (`whitepaper/...md:161-179`). If BrotherDS's G6/G9-style checks are ever pointed at the first target estate's Snowflake data rather than the pilot estate's DuckDB, reimplementing freshness/null/duplicate checks would duplicate these GA-native features.
- **Catalog/label remediation** (WHAT-SURVIVES survivor #4, scoped to the first target estate's 123 executive-tagged reports, 80% by week 6 target) overlaps with what a future BrotherDS G9 grain/key-uniqueness sweep would do if pointed at the same report set.
- **Five evidence classes (SYSTEM/THIRD_PARTY/ELICITED/ASSUMPTION/HYPOTHESIS)**, grepped across the entire prior corpus, no match found. This appears to be a genuine, non-duplicative addition in tonight's design.

## OPEN FOUNDER QUESTIONS (gathered, none answered here)

1. `decision/FOUNDER-GATES.md`: Gate 1 (is the answer to the original brief "no, and here is what instead"), Gate 2 (does the forgeable-receipt fix need founder sign-off), Gate 3 (the pilot estate first or the first target estate first, tonight's SPEC.md answers this de facto by piloting on the pilot estate, but does not cite the gate), Gate 4 (run the cheapest disproving test before building).
2. `SCOPE-V2.md:169`: Databricks-vs-Snowflake platform question for the wider first-target-estate architecture, "a real decision with a dated gate on 2026-08-31", that date is 15 days from today (2026-08-16) and appears still open.
3. `docs/SCOPE-2026-08-12-founder-directive.md` section 3, THE OPEN BOUNDARY QUESTION: does BrotherDS own project-management/delivery/value-realization itself (Option B), read BrotherMode's/BrotherSBE's records instead (Option A, recommended), or restructure all three products (Option C)? **Explicitly unresolved, founder-owned, must be answered "before any code."** Tonight's SPEC.md's "Boundaries" section acts consistently with Option A (consumes BrotherSBE's verdict, does not rebuild it, `SPEC.md:184-187`) but never states this or cites the directive.
4. `PROJECT.md:57-58` (the first target estate): same open item, restated: "The relationship between this programme and BrotherDS's delivery framework is an unresolved founder decision."
5. `docs/SCOPE-2026-08-12-founder-directive.md:128-130`: **"The relationship to `~/Documents/BrotherData-Copilot-Spec` has not been reconciled... may contain decisions that contradict or duplicate this directive."** This is the exact task this file completes; it should be read as answering that outstanding item, not as new information.
6. Value realization tracking (directive item 7), not mentioned anywhere in tonight's SPEC.md; still open.

## The 3 things that should most change tonight's design

1. **Tonight's gates solve reproduction, not definition drift.** The prior red-teamed corpus's central, hardest-won finding is that reproduction was never the real problem, cross-surface/cross-team definition agreement was. G5/G7 as written do not touch this. If BrotherDS ever operates anywhere two teams can define the same metric differently (which is the first target estate's exact stated risk), tonight's nine gates will pass a claim that is internally reproducible but organizationally contested.
2. **The open boundary question (directive section 3) is live and tonight's SPEC.md silently picks a side.** SPEC.md's "Boundaries" section reads as Option A but never says so, never cites the founder directive, and never notes that Option A was a *recommendation*, not a founder ratification.
3. **The first target estate is the founder-named one, but tonight's SPEC.md pilots exclusively on the pilot estate DuckDB with no acknowledgment of the first target estate's native GA mechanisms (DMFs, dbt contracts, Snowflake Trail) that a Snowflake-facing version of the nine gates would need to interoperate with, not duplicate.** The reasoning for the pilot estate-first exists in the prior corpus ("build the trust mechanism against the pilot estate... because that is where the evidence is", `decision/WHAT-SURVIVES.md:101-103`) but tonight's SPEC.md does not cite it, so the sequencing looks unmotivated rather than deliberate.
