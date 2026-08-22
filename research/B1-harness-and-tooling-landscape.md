# B1: Agent-Harness and Analytics-Tooling Landscape (what already exists)

Research date: 2026-08-16. Compiled by the Researcher profile for BrotherDS competitive/reuse scan.
Every row below carries a URL that was actually opened via WebFetch, or a WebSearch result whose
underlying source is named; anything not independently opened is marked so. Where two independent
sources agree, both are cited. Single-sourced claims say so explicitly. No version numbers, plugin
names, or paths are invented; anything not found is written NO-DATA.

Honesty note on method: most of the harness/vendor rows below rest on WebSearch result summaries
(aggregator/blog pages, not the vendor's own page) because a full primary-source open of every one
of the ~30 named products was out of budget for this pass. Six items were independently verified by
opening the primary source directly (dbt MCP, BigQuery data canvas, OSF preregistration, Croissant,
OpenLineage, Elementary, Snowflake Cortex Analyst), those carry "PRIMARY SOURCE OPENED" tags. The
rest carry "AGGREGATOR SOURCE" tags and should be treated as directional, not verified fact, until a
follow-up pass opens the vendor docs directly. This is a real limitation of this research round, not
a claim of completeness.

---

## A. Agent harness ecosystems and their data/analytics extensions

### Claude Code / Claude Agent SDK
- Claude Code ships an official plugin marketplace; a community index (tonsofskills.com, via the
  `ccpi` package manager) lists 471 plugins / 3,069 skills / 347 agents as of the page checked.
  AGGREGATOR SOURCE. Checked 2026-08-16.
  https://github.com/jeremylongshore/claude-code-plugins-plus-skills
- A `dataviz` skill ships in Claude Code itself (no install) for chart/plot/dashboard requests; a
  separate blog post catalogs "35+" community data-science skills (pandas EDA, matplotlib,
  Streamlit, SQL, Jupyter). AGGREGATOR SOURCE, single-sourced. Checked 2026-08-16.
  https://www.aibuilderclub.com/blog/claude-code-for-data-scientists-skills-guide
- A separate marketplace claims a "1,150-skill catalog … for empirical social-science research, econometrics, causal inference, replication" routed by task. AGGREGATOR SOURCE, single-sourced,
  vendor name not independently confirmed. Checked 2026-08-16.
  (surfaced via WebSearch "Claude Code subagents skill for statistics causal inference")
- Claude Agent SDK: built-in Read/Write/Edit/Bash/Glob/Grep/WebSearch/WebFetch, multi-agent
  orchestration, and an "Outcomes" rubric-grading feature for judging agent output against defined
  criteria, relevant as a possible substrate for BrotherDS's own grading, but it is a generic agent
  framework, not a data-trust product. AGGREGATOR SOURCE. Checked 2026-08-16.
  https://agentlas.pro/frameworks/claude-agent-sdk/
- STOPS: none of the above bind a produced number to a query/data-version/method receipt, score a
  forecast against a later outcome, or refuse unsupported causal language. They are execution and
  discovery substrate only.

### OpenAI Codex / ChatGPT agent modes / AgentKit
- OpenAI's own study ("The Shift to Agentic AI: Evidence from Codex," June 2026) reports 70% of
  sampled Codex users made a request equating to 1+ hour of human work, 25% an 8-hour-equivalent
  request, and non-developer usage growing "137x" since Aug 2025. This is adoption/usage data, not
  a data-trust capability. PRIMARY SOURCE (OpenAI's own PDF, linked from search, not independently
  opened this round, treat as AGGREGATOR-adjacent). Checked 2026-08-16.
  https://cdn.openai.com/pdf/5d1e1489-21c0-43e4-9d42-f87efdbf0082/the-shift-to-agentic-ai-evidence-from-codex.pdf
- ChatGPT's "Advanced Data Analysis" / Code Interpreter mode: upload CSV/Excel/PDF, model writes and
  runs Python in a sandbox, returns charts/answers. No receipt, no versioning of the uploaded file,
  no outcome tracking. AGGREGATOR SOURCE. Checked 2026-08-16.
  https://www.buildmvpfast.com/articles/best-llms-2026-guide/data-analysis-ai
- NO-DATA found this round on "AgentKit" as a distinct data-analytics product; searches returned only
  generic Codex-adoption coverage. Not verified to exist as named.

### Cursor / Windsurf / Continue / Aider / Cline / Roo
- Windsurf has been absorbed into "Devin Desktop" (windsurf.com redirects to devin.ai) per one
  aggregator; this is a notable 2026 consolidation if true. AGGREGATOR SOURCE, single-sourced, not
  independently confirmed by opening windsurf.com. Checked 2026-08-16.
  https://memstate.ai/blog/cursor-vs-windsurf-vs-cline-vs-kilo-code-2026
- Cline: open-source, BYO API key, MCP-extensible, terminal/browser execution, general coding agent,
  not a data-science-specific product; no dedicated data-science claims found. AGGREGATOR SOURCE.
  Checked 2026-08-16.
  https://www.morphllm.com/comparisons/cursor-alternatives
- STOPS: none of Cursor/Windsurf/Continue/Aider/Cline/Roo were found (this round) to ship a
  data-trust, provenance, or claim-verification layer of their own, they are general coding agents
  that reach data work only through whatever MCP servers or shell tools the user wires in.

### GitHub Copilot (agents, extensions)
- GitHub Copilot "Agent Mode" plus a July 2026 standalone desktop "Copilot app" (agent-native,
  multi-agent orchestration surface), custom agents in Copilot CLI (June 2026), and browser tools for
  agents in VS Code (GA July 1, 2026). This is a coding/orchestration product, not a data-analytics or
  data-trust product; no data-science-specific claims found. AGGREGATOR SOURCE (Let's Data Science,
  which appears to aggregate GitHub's own changelog). Checked 2026-08-16.
  https://letsdatascience.com/news/github-launches-copilot-app-as-desktop-home-for-ai-agents-287628bd

### Google Gemini CLI / Jules / Colab AI / BigQuery Data Canvas
- BigQuery data canvas: PRIMARY SOURCE OPENED (Google Cloud docs), checked 2026-08-16.
  https://docs.cloud.google.com/bigquery/docs/data-canvas
  - DOES: natural-language search over Knowledge Catalog metadata; generates SQL from prompts for
    "basic to moderately complex queries"; builds a DAG-style visual workflow; produces chart types
    (bar, heat map, line, pie, scatter).
  - STOPS (vendor's own stated limitations): explicitly weak on BigQuery ML/Spark ops, object
    tables/BigLake, nested/repeated fields, complex functions and DATETIME/TIMEZONE types, geomap
    charts. Targeted at data analysts/engineers, not business end-users. No mention of a receipt
    binding a generated number to its exact query/data version, no forecast-scoring, no causal-claim
    guardrail.
- "Jules" was searched for but no connection to BigQuery/Gemini CLI/Data Canvas was found in results
  this round, NO-DATA on that specific linkage. Checked 2026-08-16.

### Databricks Assistant / Genie / Mosaic AI Agent Framework
- Genie family (Genie One, Genie Ontology, Genie Code, Genie Agents), Mosaic AI Agent Framework
  (custom agent framework, Python-level control), "Agent Bricks" (agent dev/eval/deploy/governance
  workflows), Unity AI Gateway (expanded governance layer for model/agent/MCP interactions).
  AGGREGATOR SOURCE. Checked 2026-08-16.
  https://www.databricks.com/blog/announcing-mosaic-ai-agent-framework-and-agent-evaluation
- Databricks' own docs on tuning Genie Agent quality: "typical expectation is that Genie benchmarks
  should be above 80 percent accuracy before you move on to user acceptance testing," and
  acknowledges "a simple single-model text-to-SQL approach fails a lot in production", i.e.
  Databricks' own documentation admits text-to-SQL accuracy is a known, unsolved-by-default problem
  they mitigate with multi-agent design and curated examples, not a receipt or provenance mechanism.
  AGGREGATOR SOURCE quoting Databricks docs; not independently opened this round. Checked 2026-08-16.
  https://docs.databricks.com/aws/en/genie-agents/tune-quality

### Snowflake Cortex Analyst / Snowflake Intelligence
- PRIMARY SOURCE OPENED (Snowflake docs), checked 2026-08-16.
  https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst
  - DOES: NL-to-SQL against Snowflake Semantic Views/YAML semantic models; multi-turn conversation;
    REST API; RBAC/governance integration; does not train on customer data (vendor's own claim).
  - STOPS (vendor's own stated limitations, quoted from the docs): "Cortex Analyst doesn't have
    access to results from previous SQL queries"; "limited to answering questions that can be
    resolved with SQL, does not generate insights for broader business-related queries"; struggles
    "if a conversation includes too many turns or the user shifts intent frequently."
  - No claim-level receipt, no forecast tracking, no causal-language refusal found in the docs opened.
- Snowflake Intelligence and an MCP server (for Salesforce Agentforce/UiPath/Anthropic platform
  connections) are 2026 extensions per aggregator coverage; not independently opened. AGGREGATOR
  SOURCE, single-sourced. Checked 2026-08-16.
  https://www.aegissofttech.com/insights/snowflake-cortex-analyst/

### Microsoft Fabric Copilot / Power BI Copilot
- June 2026: "Copilot in web modeling" can rename tables/columns, create relationships, generate DAX
  measures from NL. May 2026: report-summary shortcut; "Copilot Tooling Format" GA for semantic-model
  metadata (synonyms, descriptions, sample questions) that helps Copilot answer consistently.
  AGGREGATOR SOURCE (Microsoft Fabric Community blog, effectively primary-adjacent since it's
  Microsoft's own community channel, but not independently opened). Checked 2026-08-16.
  https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/Power-BI-June-2026-Feature-Summary/ba-p/5193264
- STOPS: no evidence found of claim-level receipts, forecast-vs-outcome tracking, or causal-language
  guardrails in Power BI/Fabric Copilot coverage this round.

### Notebook-native: Hex Magic / Deepnote AI / marimo / Julius AI / Jupyter AI
- Hex Magic: SQL writing, Python explanation, error debugging, analysis generation layered on Hex's
  SQL-first notebook. Deepnote AI: Jupyter-compatible, collaborative, aimed at pandas/scikit-learn/
  PyTorch workflows. marimo: reproducible Python workflows stored as plain files (git-diffable,
  reactive notebook, relevant as a REUSE candidate for reproducibility, see below). Julius AI:
  upload CSV/connect Sheet, ask in NL, runs Python in a sandbox, returns chart/answer, targeted at
  non-technical users. AGGREGATOR SOURCE (Deepnote's own comparison pages, which are vendor-authored
  but comparing itself to competitors, read with that bias in mind). Checked 2026-08-16.
  https://deepnote.com/compare/juliusai-vs-deepnote and https://julius.ai/articles/ai-tools-for-data-analysis
- STOPS: none of these were found to bind an answer to a data-version/query receipt, track a forecast
  against realized outcome, or refuse causal language.

---

## B. MCP servers relevant to data work

- **dbt MCP server** (dbt Labs, official). PRIMARY SOURCE OPENED (GitHub repo), checked 2026-08-16.
  https://github.com/dbt-labs/dbt-mcp
  - DOES: exposes SQL execution + NL-to-SQL, Semantic Layer queries (metrics/dimensions/entities),
    Discovery API (models/sources/macros/exposures/lineage/health), dbt CLI (build/test/compile/docs),
    Admin API (jobs/runs/projects), code generation (YAML/SQL scaffolding), dbt LSP (column-level
    lineage via the Fusion engine), and product-docs search. Self-hosted or remote/managed flavors.
  - STOPS: the project's own README warns that letting a client run dbt commands through the MCP
    tooling "could modify your data models, sources, and warehouse objects", i.e. it is a capability
    surface, not a safety layer; no built-in claim-receipt or provenance-binding feature found.
  - Second source (dbt Labs blog) confirms same tool categories. Checked 2026-08-16.
    https://www.getdbt.com/blog/mcp
- **DuckDB MCP servers**: multiple independent open-source implementations exist (e.g.
  `ktanaka101/mcp-server-duckdb` on GitHub; MotherDuck's own blog post on MCP+DuckDB). These are
  query/schema-inspection tools, not trust layers. AGGREGATOR + repo listing, not independently
  opened. Checked 2026-08-16.
  https://github.com/ktanaka101/mcp-server-duckdb and https://motherduck.com/blog/faster-data-pipelines-with-mcp-duckdb-ai/
- **BigQuery MCP**: Google now ships "a fully managed remote MCP server (Preview since January 7,
  2026)"; as of March 17, 2026 no separate enablement needed once the BigQuery API is on. Includes a
  `dry_run_query` tool that estimates bytes scanned before executing (useful cost-guard primitive).
  AGGREGATOR SOURCE, single-sourced (Dataworkers), not independently opened. Checked 2026-08-16.
  https://dataworkers.io/resources/mcp-server-bigquery-guide/
- **Snowflake MCP**: Snowflake's official MCP server (early 2025) built on Cortex Analyst and Cortex
  Search, NL-to-SQL, schema browsing, semantic search. AGGREGATOR SOURCE. Checked 2026-08-16.
- **Postgres MCP**: no single official server; Anthropic's original reference Postgres MCP server is
  now archived; Supabase ships its own MCP server for its managed Postgres. AGGREGATOR SOURCE.
  Checked 2026-08-16. https://www.infoworld.com/article/4181843/10-mcp-servers-to-connect-llms-with-databases.html
- **Experiment-tracking / statistics MCP servers**: searches did not surface a maintained, named MCP
  server specifically for MLflow, W&B, or general statistics (e.g. hypothesis testing, power
  analysis) as a standardized MCP tool. NO-DATA for that specific sub-category this round, this is
  itself a signal (see whitespace/reuse below): the trust/stats layer is not yet MCP-native the way
  the warehouse layer is.

---

## C. Data trust / provenance / quality tooling (integrate, don't replace)

- **dbt tests + contracts + semantic layer**: contracts enforce schema before a model builds; tests
  validate semantics/business logic after; the Semantic Layer (MetricFlow) compiles YAML metric
  definitions in git into warehouse SQL at query time, intended to stop different teams handing an
  agent conflicting KPI definitions. One aggregator cites "only 7% of enterprises say their data is
  completely ready for AI." AGGREGATOR SOURCE, single-sourced stat, not independently verified.
  Checked 2026-08-16. https://www.getdbt.com/blog/building-the-agentic-data-stack-a-practical-dbt-guide-for-the-ai-era
- **Great Expectations**: open-source Python framework, explicit codified "expectation suites", code-first, fine-grained. **Soda**: AI-assisted rule authoring, collaborative technical/business
  workflow. **Monte Carlo**: managed, ML-driven anomaly detection, no manual rules required.
  **Elementary**: PRIMARY SOURCE OPENED (vendor site), checked 2026-08-16.
  https://www.elementary-data.com/
  - DOES: dbt-native quality tests, ML-based freshness/volume anomaly detection, column-level
    lineage, incident grouping/alerting, a conversational metadata catalog, and "AI agents" for test
    authoring/triage (vendor's own claim, not independently benchmarked).
  - STOPS: positioned purely as a post-pipeline observability/governance layer, does not do
    transformation, orchestration, ingestion, or BI; no claim-level receipt or decision/outcome
    tracking of the kind BrotherDS is aimed at.
  - Comparison source for Monte Carlo/GX/Soda (AGGREGATOR, single-sourced, not independently opened):
    https://medium.com/@aidelearning/data-observability-in-2026-monte-carlo-vs-great-expectations-vs-soda-a-data-engineers-honest-7c8cab1b68f1
- **OpenLineage / Marquez**: PRIMARY SOURCE OPENED (openlineage.io), checked 2026-08-16.
  https://openlineage.io/getting-started/
  - DOES: standardizes dataset/job/run-level lineage metadata (namespaces, run IDs as UUIDv7,
    input/output dataset relationships, schema, run-state transitions START/COMPLETE).
  - STOPS: explicitly delegates storage and visualization to a separate backend (reference
    implementation: Marquez); the getting-started guide makes no mention of data-quality checking, it is a metadata transport standard, not a quality or trust engine.
- **DataHub / OpenMetadata**: open-source catalogs that *consume* OpenLineage events and render
  navigable lineage graphs; also do discovery/profiling. AGGREGATOR SOURCE, not independently
  opened. Checked 2026-08-16. https://datahub.com/blog/open-source-data-lineage/
- **DVC / MLflow / Weights & Biases**: DVC does dataset versioning + pipeline DAGs; MLflow does
  run-level metrics/artifacts/model registry (open-source, self-hosted, backed by Databricks); W&B is
  managed SaaS experiment tracking (aggregator cites ~$50/user/mo team tier, ~$200k/yr enterprise,
  single-sourced, not verified against W&B's own pricing page this round). Aggregator notes "most
  serious ML platforms run at least two of the three together", additive, not competing. AGGREGATOR
  SOURCE. Checked 2026-08-16.
  https://mljourney.com/model-versioning-strategies-dvc-vs-mlflow-vs-weights-biases/
- **Evidently / whylogs**: searched but not independently opened or found described in the same
  source as Croissant/model cards this round; treat as NO-DATA for a verified 2026 description in
  this pass (they are real, well-known open-source ML-monitoring libraries from prior knowledge, flagged here as UNVERIFIED for 2026 specifics, not confirmed dead or changed).
- **Croissant**: PRIMARY SOURCE OPENED (MLCommons GitHub), checked 2026-08-16.
  https://github.com/mlcommons/croissant
  - DOES: a JSON-LD metadata format built on schema.org's Dataset vocabulary, four layers, metadata,
    resources (file/source docs), structure (raw-to-usable mapping), ML semantics (typical ML uses).
    Spec at v1.0/v1.1, NeurIPS 2024 paper, actively maintained (Apache 2.0, Python 3.10+).
    A "Croissant-RAI" extension adds responsible-AI documentation fields (echoing Datasheets for
    Datasets / Data Cards).
  - STOPS: describes and organizes a dataset; does not do transformation, quality assurance, or
    content moderation, a documentation format, not an enforcement mechanism.
- **Model Cards / Datasheets for Datasets**: confirmed (via the Croissant paper's own framing) as the
  established prior art that Croissant-RAI extends; these remain static documentation templates, not
  live/enforced or receipt-bound to a specific run. UNVERIFIED beyond that framing this round (their
  original papers were not re-opened).

---

## D. Reproducibility / pre-registration practice

- **OSF Preregistration**: PRIMARY SOURCE OPENED (Center for Open Science), checked 2026-08-16.
  https://www.cos.io/initiatives/prereg
  - DOES: creates a timestamped, dated record of a research plan (hypotheses, design, sampling,
    analysis plan) before data collection/analysis, to separate confirmatory from exploratory work
    and curb false positives from post-hoc hypothesis fitting. OSF's template has ~25 questions;
    AsPredicted's shorter template (~8-9 questions) is also hostable directly on OSF.
  - STOPS (explicit, quoted from the source): does **not** verify the analysis was actually run as
    registered, does not monitor execution, does not audit the process, does not prevent selective
    reporting (only makes deviation from plan discoverable if disclosed), and does not guarantee
    methodological quality. Compliance rests on researcher integrity and post-hoc community scrutiny, "a plan, not a prison." This is the single most load-bearing finding for BrotherDS: even the
    gold-standard scientific pre-registration mechanism has NO automated binding between the
    registered plan and what was actually executed.
- **Registered Reports**: peer review of the plan happens before results are seen; a journal-level
  publication format, not a software mechanism. AGGREGATOR SOURCE. Checked 2026-08-16.
- **TRIPOD+AI** (April 2024, per PMC review paper) and **CONSORT-AI**/**SPIRIT-AI** (2020): reporting
  guidelines for how AI prediction models and AI-intervention clinical trials should be *written up*
  after the fact, checklists for authors and reviewers, not runtime enforcement. AGGREGATOR SOURCE
  citing PMC. Checked 2026-08-16.
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12627258/
- **PRISMA-trAIce**: a 2025 extension to PRISMA specifically for transparent reporting when AI is used
  as a tool inside a systematic review (not AI as the object of study). AGGREGATOR SOURCE citing
  JMIR AI. Checked 2026-08-16. https://ai.jmir.org/2025/1/e80247
- **NeurIPS ML Reproducibility Checklist / MLRC track**: PRIMARY-ADJACENT SOURCE (NeurIPS' own blog),
  checked 2026-08-16. https://blog.neurips.cc/2026/05/04/mlrc-2026-reproducibility-as-an-official-track-at-neurips/
  - DOES: standardized ~15-question checklist (Yes/No/NA + justification) submitted with every paper,
    covering reproducibility, ethics, limitations, experimental rigor; a dedicated MLRC track accepts
    replication attempts (including failures to reproduce) as a class of publishable work.
  - STOPS: it is a self-reported checklist at submission time, reviewed by humans during peer review, not an automated or continuously-enforced binding between a paper's claimed number and a
    re-runnable artifact.
- **Papers-with-Code-style artifact evaluation**: not independently found/opened this round in a
  current (2026) form; treat as NO-DATA on current operational status, though the general pattern
  (code+data+leaderboard linkage) is well-established prior art from before this research window.

---

## E. Decision-intelligence / "AI analyst" commercial claims

- **ThoughtSpot Sage/Spotter**: claims conversational NL analytics on top of search-based BI, from
  $25/user/mo (aggregator figure, not verified against ThoughtSpot's own pricing page this round).
  Evidence found: only marketing/aggregator description of the NL-query layer, no independent
  benchmark of accuracy, no receipt mechanism, found this round. AGGREGATOR SOURCE. Checked
  2026-08-16.
- **Julius AI**: claims "chat with your data like a knowledgeable colleague," drop-a-CSV-get-a-chart.
  Evidence found: it runs generated Python in a sandbox and returns output, a code-execution
  convenience layer, not a verification layer; no evidence found of it validating its own numbers,
  versioning input files, or flagging non-causal inference as such. AGGREGATOR SOURCE (Julius's own
  comparison content, vendor-authored). Checked 2026-08-16.
- **ChatGPT Advanced Data Analysis / Code Interpreter**: claims sandboxed Python analysis over
  uploaded files. Evidence found: same, code execution, no provenance/versioning/receipt layer
  found. AGGREGATOR SOURCE. Checked 2026-08-16.
- **Decision-intelligence market framing (Gartner, Domo, Tredence, Cloverpop, aggregator roundups)**:
  the *industry narrative* for 2026 explicitly names the gap BrotherDS targets, one Cloverpop-linked
  source states 2026 will reward "programs that can prove ROI, scale agentic workflows with full
  auditability" and treat "decisions as trackable business activities... captured as structured
  data." This is market commentary describing an unmet need, not a shipped product solving it.
  AGGREGATOR SOURCE, single-sourced per quote. Checked 2026-08-16.
  https://www.tredence.com/blog/decision-intelligence-future-of-data-science
- **Cost of getting this wrong**: one 2026 aggregator cites AI hallucinations costing "global
  businesses about $67.4 billion in 2024" and "$4.4 million" average per major AI error, plus a
  named example of a 25% product-return spike from hallucinated specs. UNVERIFIED, these are
  aggregator-quoted figures whose primary source (a named report) was not opened this round; treat
  as directional market-pain evidence only, not a verified statistic. Checked 2026-08-16.
  https://aihallucinationreport.com/detect-ai-hallucinations-before-they-cost-your-business-billions/

---

## WHITESPACE VERDICT (candidates a-e)

**(a) A claim-level receipt binding a number to its query, data version, method, and stated
uncertainty.** REAL GAP. Nothing found across A-E does this. dbt contracts/tests validate schema and
business rules at build time, not at answer time; BigQuery data canvas and Cortex Analyst generate
SQL but do not emit a receipt object; OpenLineage captures job/run lineage but not "this specific
number came from this exact query against this exact data snapshot with this method and this
confidence interval." Closest partial: OpenLineage's run-level metadata (dataset+job+run IDs, schema)
is the right *shape* of primitive to build a receipt on top of, but it doesn't carry method or
uncertainty.

**(b) Scoring a claim or forecast against the actual outcome later, and keeping the track record.**
REAL GAP. No product found does this. MLflow/W&B/DVC track experiment *runs*, not real-world forecast
outcomes. The 2026 decision-intelligence market commentary (Tredence, Cloverpop) explicitly names
this as an unmet 2026 priority ("treating decisions as trackable business activities"), which is
market validation of the gap, not evidence it's filled.

**(c) Recording the decision a number fed, and the realized business outcome.** REAL GAP,
PARTIALLY NAMED BY decision-intelligence vendors as aspiration. Cloverpop/Domo/Tredence-style
"decision intelligence" platforms claim to move this direction, but no primary source opened this
round demonstrates a shipped, working decision-to-outcome linkage, treat vendor claims as claims,
evidence as absent until a follow-up pass opens a specific vendor's own docs.

**(d) Refusing causal language when the design cannot support it.** REAL GAP. Search surfaced only
academic/research prototypes (e.g. "CausalAgent," "EpiCausalX Agent", both arXiv/medRxiv papers, not
products) attempting automated causal-inference workflows; none were found to implement a
correlational-vs-causal guardrail as a product feature. SR 26-2 (the April 2026 US bank regulator
model-risk guidance) explicitly *excludes* generative/agentic AI from its formal scope per one
aggregator source, i.e. even the regulatory apparatus most likely to mandate this has not yet done
so. This is the sharpest, most defensible whitespace claim in the set.

**(e) Pre-registration of an analysis before it is run.** ALREADY SOLVED (the plan/timestamp part) BY
OSF/AsPredicted, PARTIALLY COVERED for the "before it is run" mechanism. But the verification half of
this candidate (checking the actual analysis matched the registered plan) is a REAL GAP even within
OSF's own stated scope, confirmed directly from the primary source: OSF explicitly does not verify
execution matched the plan. A BrotherDS feature that pre-registers an analysis *and* mechanically
diffs the executed query/method against the registration would sit in unclaimed territory between
OSF (registration only, no verification) and dbt/OpenLineage (execution metadata, no registration
concept).

---

## REUSE LIST (wrap, don't rebuild)

- **OpenLineage** as the run/job/dataset-ID substrate for a claim receipt, it already standardizes
  "which run, which dataset, which schema" as structured events; BrotherDS would add method +
  uncertainty + claim-text binding on top, not reinvent lineage capture.
- **dbt Semantic Layer / contracts** as the "shared vocabulary" layer so a BrotherDS receipt can say
  "this number used the org's contracted `revenue` metric definition," not a bespoke ad hoc one, wrap dbt's governance rather than build a second metrics dictionary.
- **OSF/AsPredicted's registration UX pattern** (timestamped, versioned plan submitted before
  execution) as the interaction model for a pre-registration feature, the mechanism is simple and
  proven; BrotherDS's differentiation is the automated post-hoc diff against dbt/OpenLineage
  execution metadata, which OSF has explicitly declined to build.
- **Croissant / Datasheets-for-Datasets** as the dataset-versioning/documentation metadata shape for
  "data version" inside a claim receipt, instead of inventing a new dataset-description schema.
- **Elementary or Great Expectations** as the upstream data-quality signal feeding into a claim's
  stated uncertainty/confidence, a claim receipt should cite "this data passed/failed these
  freshness and volume checks at query time" by reading their existing test results, not
  re-implementing anomaly detection.
- **NeurIPS's Yes/No/NA-plus-justification checklist pattern** as a lightweight template for a
  "was this analysis design able to support a causal claim" checklist BrotherDS could attach to any
  claim, rather than building a causal-inference engine from scratch.

