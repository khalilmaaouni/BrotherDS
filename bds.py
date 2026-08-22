#!/usr/bin/env python3
"""BrotherDS: every number that reaches a decision carries its proof.

A claim is one number that reaches a decision. This tool re-derives it, applies
the refusals, and writes a receipt. It never decides that a claim is true; it
decides whether the claim is PROVEN, DISPROVEN, or UNEXAMINED, and reality
decides the rest later via `score`.

    python3 bds.py new      RGM-014 claims/rgm-014.json   scaffold a claim
    python3 bds.py author   claims/rgm-014.json           write one from key=value stdin
    python3 bds.py check    claims/rgm-014.json           run the ten gates
    python3 bds.py receipt  claims/rgm-014.json [out.md]  the page a human reads
    python3 bds.py register claims/rgm-014.json           make its metric definition the reference
    python3 bds.py score    claims/rgm-014.json 8123 "ops lead" 2026-09-30
    python3 bds.py ledger   claims/                       the verified claim rate
    python3 bds.py chain                                  the stages, and what each stands in
    python3 bds.py stage    outcome                       is this a stage an item may serve
    python3 bds.py passport [.sbe/passport.json]          consume BrotherMode's change passport
    python3 bds.py handoff  [.sbe/handoff.json]           consume BrotherSBE's handoff package
    python3 bds.py backlog  [docs/plan/QUEUE.json]        every item against the chain
    python3 bds.py selftest

Verdicts are PASS, FAIL, NO-DATA, matching the BrotherSBE tuple exactly.
NO-DATA is never a pass and never a block.

Requires: duckdb, only for claims whose origin is SYSTEM. Every other origin
runs on the standard library alone.
"""
import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path

PASS, FAIL, NODATA = "PASS", "FAIL", "NO-DATA"

# The five origins. A claim that does not name one cannot be checked, because
# the questions that interrogate a warehouse query are not the questions that
# interrogate an expert's judgement.
ORIGINS = {
    "SYSTEM": "a query against a governed source system",
    "THIRD_PARTY": "an external or vendor dataset, carrying its own provenance",
    "ELICITED": "expert judgement, captured through a structured protocol",
    "ASSUMPTION": "stated and unverified, requiring sensitivity analysis",
    "HYPOTHESIS": "explicitly untested; may inform a test, may not alone decide",
}

# Words that assert one thing made another thing happen. Any of these in a
# statement demands a design that can license the assertion.
CAUSAL_TOKENS = (
    "caused", "causes", "drove", "drives", "driven by", "led to", "leads to",
    "resulted in", "results in", "incremental", "incrementality", "lift",
    "uplift", "boosted", "boosts", "impact of", "effect of", "due to",
    "because of", "attributable", "thanks to", "responsible for",
)

# Designs that can license a causal claim, each with the assumption it rests on.
CAUSAL_DESIGNS = {
    "rct": "treatment assignment is random, so groups differ only by chance",
    "randomised_holdout": "the held-out group was randomly chosen and untreated",
    "geo_experiment": "treated and control geographies were randomly assigned",
    "switchback": "treatment periods were randomised and carryover is bounded",
    "difference_in_differences": "treated and control trends were parallel before treatment",
    "synthetic_control": "the weighted donor pool tracks the treated unit pre-treatment",
    "event_study": "no other event coincides with the studied event",
    "regression_discontinuity": "units cannot precisely manipulate the running variable",
    "instrumental_variable": "the instrument affects the outcome only through the treatment",
}


def _fmt(v):
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        # A whole-numbered float is a quantity, not a measurement. Rendering
        # 1050000.0 as 1.05e+06 in a receipt a person reads is a defect.
        if v == int(v) and abs(v) >= 1000:
            return "{:,}".format(int(v))
        return ("%.6g" % v)
    if isinstance(v, int):
        return "{:,}".format(v)
    return str(v)


def _expand(p):
    return Path(os.path.expanduser(str(p)))


class Finding(object):
    """One gate result. `gate` names the rule, `verdict` is the tuple value."""

    def __init__(self, gate, verdict, detail):
        self.gate = gate
        self.verdict = verdict
        self.detail = detail

    def line(self):
        return "%-8s %-26s %s" % (self.verdict, self.gate, self.detail)


# ---------------------------------------------------------------- source state

def source_state(path):
    """Identity of the data a claim was computed against.

    Size and mtime, not a content hash: hashing a 191MB warehouse on every check
    costs seconds for a property that size-and-mtime already detects in practice.
    ponytail: swap in a content hash if a source is ever rewritten in place at
    identical size, which is the one case this misses.
    """
    p = _expand(path)
    if not p.exists():
        return None
    st = p.stat()
    return {"path": str(p), "bytes": st.st_size, "mtime": int(st.st_mtime)}


# ---------------------------------------------------------------- derivations

def run_sql(db_path, sql):
    import duckdb  # imported lazily so non-SYSTEM claims need no dependency
    con = duckdb.connect(str(_expand(db_path)), read_only=True)
    try:
        row = con.execute(sql).fetchone()
    finally:
        con.close()
    if row is None:
        return None
    return row[0]


def evaluate_derivations(claim):
    """Run every derivation and return (value_paths, findings).

    A derivation either RECOMPUTES THE CLAIMED VALUE or it is a supporting fact.
    Only the first kind may be compared, and conflating them is how a month count
    ends up being checked against a percentage. Mark a supporting query with
    "computes_value": false; the default is true.

    Two independent paths to the same number is the whole point. One path is
    NO-DATA on independent re-derivation, not a pass: it proves the query runs,
    not that the number is right.
    """
    findings = []
    ev = claim.get("evidence") or {}
    derivations = ev.get("derivations") or []
    db = ev.get("source")

    if not derivations:
        findings.append(Finding("G5.rederivation", NODATA,
                                "no derivation given; nothing was recomputed"))
        return [], findings

    if db and source_state(db) is None:
        findings.append(Finding("G5.rederivation", FAIL,
                                "source does not exist: %s" % db))
        return [], findings

    value_paths, supporting = [], []
    for d in derivations:
        try:
            v = run_sql(db, d["sql"])
        except Exception as exc:  # a broken query is a FAIL, never a skip
            findings.append(Finding("G5.rederivation", FAIL,
                                    "derivation '%s' raised %s: %s"
                                    % (d.get("name", "?"), type(exc).__name__, exc)))
            return value_paths, findings
        pair = (d.get("name", "?"), v)
        (value_paths if d.get("computes_value", True) else supporting).append(pair)

    for n, v in supporting:
        findings.append(Finding("G5.supporting", PASS,
                                "%s = %s (context, not compared)" % (n, _fmt(v))))

    if not value_paths:
        findings.append(Finding("G5.rederivation", NODATA,
                                "no derivation recomputes the claimed value; "
                                "every query given is supporting context"))
    elif len(value_paths) == 1:
        findings.append(Finding("G5.rederivation", NODATA,
                                "one derivation only ('%s'); the number was "
                                "recomputed but not independently corroborated"
                                % value_paths[0][0]))
    else:
        distinct = set(_fmt(v) for _, v in value_paths)
        if len(distinct) == 1:
            findings.append(Finding("G5.rederivation", PASS,
                                    "%d independent derivations agree at %s"
                                    % (len(value_paths), _fmt(value_paths[0][1]))))
        else:
            expl = claim.get("expected_derivation_gap")
            detail = "derivations disagree: " + ", ".join(
                "%s=%s" % (n, _fmt(v)) for n, v in value_paths)
            if expl:
                findings.append(Finding("G5.rederivation", NODATA,
                                        detail + " | gap declared expected: " + expl))
            else:
                findings.append(Finding("G5.rederivation", FAIL, detail))
    return value_paths, findings


def evaluate_comparison(claim, value_paths):
    """The dual run: a SYSTEM derivation paired with a THIRD_PARTY or ELICITED
    comparison against the incumbent artifact somebody already trusts.

    This answers a different question than G5.rederivation. Rederivation asks
    "is this internally reproducible" by running two SQL paths against one
    governed source. A comparison cannot be SQL against that source by
    definition, since the whole point is a second, independent, non-system
    read (a vendor panel, an expert's number, a spreadsheet). So this is not a
    third SQL path: it is the claim's own recomputed value, held up against a
    value that was never a query at all.

    No comparison block: this function returns nothing and the SQL-only path
    is exactly as it was before this existed.
    """
    ev = claim.get("evidence") or {}
    comp = ev.get("comparison")
    if not comp:
        return []

    cls = comp.get("class")
    if cls not in ("THIRD_PARTY", "ELICITED"):
        return [Finding("G5.comparison", FAIL,
                        "comparison.class must be THIRD_PARTY or ELICITED, got %r"
                        % cls)]

    missing = [f for f in ("incumbent", "incumbent_value", "tolerance")
               if not _answered(comp.get(f))]
    if missing:
        return [Finding("G5.comparison", NODATA,
                        "comparison missing %s" % ", ".join(missing))]

    proto_required = PROTOCOL_REQUIRED.get(cls, [])
    proto = comp.get("protocol") or {}
    proto_missing = [k for k in proto_required if not _answered(proto.get(k))]
    if proto_missing:
        return [Finding("G5.comparison", NODATA,
                        "%s comparison protocol incomplete, missing: %s"
                        % (cls, ", ".join(proto_missing)))]

    if not value_paths:
        return [Finding("G5.comparison", NODATA,
                        "the system side recomputed no value; nothing to "
                        "compare the incumbent against")]
    system_value = value_paths[0][1]

    try:
        drift = abs(float(system_value) - float(comp["incumbent_value"]))
        tol = float(comp["tolerance"])
    except (TypeError, ValueError):
        return [Finding("G5.comparison", FAIL,
                        "incumbent_value and tolerance must be numeric, got "
                        "%r and %r" % (comp.get("incumbent_value"), comp.get("tolerance")))]

    detail = ("system %s vs %s incumbent (%s) %s, drift %s, tolerance %s"
             % (_fmt(system_value), cls, comp["incumbent"],
                _fmt(comp["incumbent_value"]), _fmt(drift), _fmt(tol)))
    if drift <= tol:
        return [Finding("G5.comparison", PASS, "agrees: " + detail)]
    return [Finding("G5.comparison", FAIL, "disagrees: " + detail)]


# ---------------------------------------------------------------------- gates

def gate_origin(claim):
    o = claim.get("origin")
    if o not in ORIGINS:
        return Finding("G2.origin", FAIL,
                       "origin must be one of %s, got %r"
                       % (", ".join(sorted(ORIGINS)), o))
    return Finding("G2.origin", PASS, "%s (%s)" % (o, ORIGINS[o]))


def gate_not_established(claim):
    """Field four. It may never be empty. A claim asserting that nothing is
    unexamined is the precise lie this whole product exists to prevent."""
    ne = claim.get("not_established")
    if not ne:
        return Finding("G1.not_established", FAIL,
                       "empty; every claim has limits and they must be written down")
    if not isinstance(ne, list):
        return Finding("G1.not_established", FAIL, "must be a list of statements")
    return Finding("G1.not_established", PASS,
                   "%d limit(s) declared" % len(ne))


def gate_uncertainty(claim):
    u = claim.get("uncertainty")
    if not isinstance(u, dict) or "kind" not in u:
        return Finding("G3.uncertainty", FAIL,
                       "missing; give an interval and its method, or state "
                       "kind=NOT_ESTABLISHED with a reason")
    kind = u["kind"]
    if kind == "NOT_ESTABLISHED":
        if not u.get("why"):
            return Finding("G3.uncertainty", FAIL,
                           "NOT_ESTABLISHED requires 'why'")
        return Finding("G3.uncertainty", NODATA,
                       "not established: %s" % u["why"])
    if "interval" not in u or "method" not in u:
        return Finding("G3.uncertainty", FAIL,
                       "kind=%s requires 'interval' and 'method'" % kind)
    return Finding("G3.uncertainty", PASS,
                   "%s %s by %s" % (kind, u["interval"], u["method"]))


def gate_causal(claim):
    text = (claim.get("statement") or "").lower()
    hits = [t for t in CAUSAL_TOKENS if t in text]
    if not hits:
        return Finding("G4.causal", PASS, "no causal assertion in the statement")

    if claim.get("origin") == "HYPOTHESIS":
        return Finding("G4.causal", NODATA,
                       "causal wording (%s) permitted because the claim is "
                       "declared a HYPOTHESIS; it may not alone reach a decision"
                       % ", ".join(hits))

    design = claim.get("design") or {}
    kind = design.get("kind")
    if kind not in CAUSAL_DESIGNS:
        return Finding("G4.causal", FAIL,
                       "statement asserts causation (%s) but names no valid "
                       "design; one of: %s"
                       % (", ".join(hits), ", ".join(sorted(CAUSAL_DESIGNS))))
    if not design.get("assumption_test"):
        return Finding("G4.causal", FAIL,
                       "design '%s' rests on: %s. No assumption_test given, so "
                       "the assumption is asserted, not checked"
                       % (kind, CAUSAL_DESIGNS[kind]))
    return Finding("G4.causal", PASS,
                   "%s; assumption '%s' tested by %s"
                   % (kind, CAUSAL_DESIGNS[kind], design["assumption_test"]))


def gate_value_matches(claim, values, computed_metrics=None):
    """Does the number the claim states still come back?

    For an accuracy claim the stated value IS the metric, so the thing to
    compare against is the metric this tool just computed, not a warehouse
    query. Getting this wrong is what made an earlier version check a WAPE
    against a month count.
    """
    recorded = claim.get("value")
    if recorded is None:
        return Finding("G7.value", NODATA, "claim records no value")

    acc = claim.get("accuracy") or {}
    named = acc.get("reported_metric")
    if named and computed_metrics and named in computed_metrics:
        got, source = computed_metrics[named], "recomputed %s" % named
    elif values:
        got, source = values[0][1], "warehouse"
    else:
        return Finding("G7.value", NODATA, "nothing recomputed to compare against")

    tol = claim.get("tolerance", 0)
    try:
        drift = abs(float(got) - float(recorded))
        ok = drift <= float(tol)
    except (TypeError, ValueError):
        ok = (_fmt(got) == _fmt(recorded))
        drift = None
    if ok:
        return Finding("G7.value", PASS,
                       "recorded %s reproduces (%s)" % (_fmt(recorded), source))
    return Finding("G7.value", FAIL,
                   "recorded %s, %s returns %s%s"
                   % (_fmt(recorded), source, _fmt(got),
                      "" if drift is None else " (drift %s)" % _fmt(drift)))


def _norm_definition(text):
    """Whitespace and case are not definition differences. Anything else is."""
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def definition_registry(path):
    p = _expand(path)
    if not p.exists():
        return {}
    with open(p) as fh:
        return json.load(fh)


def gate_definition(claim, registry_path):
    """Do two people mean the same thing by the same word?

    This exists because reproduction was never the hard problem. A number can
    re-derive perfectly from its own query and still disagree with the number
    somebody else computed under the same name, because the two definitions
    differ. Gates G5 and G7 cannot see that; only a registry across claims can.

    First use of a metric name is NO-DATA, not PASS: one claim defines nothing,
    it only proposes. Disagreement is a FAIL that names the claim it collides
    with, so the argument is about the definition rather than about the numbers.
    """
    m = claim.get("metric")
    if not m or not m.get("name"):
        return Finding("G10.definition", NODATA,
                       "no metric name declared, so this number cannot be "
                       "compared with anyone else's number of the same name")
    name = m["name"]
    text = m.get("definition")
    if not text:
        return Finding("G10.definition", FAIL,
                       "metric '%s' is named but not defined; a name without a "
                       "definition is exactly what drifts between teams" % name)

    reg = definition_registry(registry_path)
    mine = _norm_definition(text)
    prior = reg.get(name)

    if prior is None:
        return Finding("G10.definition", NODATA,
                       "first recorded use of metric '%s'; nothing to disagree "
                       "with yet. Run 'bds register' to make this the reference"
                       % name)
    if _norm_definition(prior.get("definition")) == mine:
        return Finding("G10.definition", PASS,
                       "metric '%s' matches the definition registered by %s"
                       % (name, prior.get("claim_id", "?")))
    return Finding("G10.definition", FAIL,
                   "metric '%s' is defined differently here than in claim %s. "
                   "Two numbers under one name. Registered: %r. This claim: %r"
                   % (name, prior.get("claim_id", "?"),
                      prior.get("definition"), text))


def register_definition(claim, registry_path):
    m = claim.get("metric") or {}
    if not m.get("name") or not m.get("definition"):
        print("claim declares no named-and-defined metric; nothing to register")
        return 1
    p = _expand(registry_path)
    reg = definition_registry(p)
    name = m["name"]
    prior = reg.get(name)
    if prior and _norm_definition(prior.get("definition")) != _norm_definition(m["definition"]):
        print("REFUSED. Metric %r is already registered by claim %s with a "
              "different definition.\n  registered: %s\n  yours:      %s\n"
              "Resolve which definition is correct with the other author. "
              "Overwriting silently is the drift this registry exists to stop."
              % (name, prior.get("claim_id", "?"), prior.get("definition"),
                 m["definition"]))
        return 1
    reg[name] = {"definition": m["definition"],
                 "claim_id": claim.get("id"),
                 "source": m.get("definition_source", "not stated")}
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as fh:
        json.dump(reg, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print("registered %r from claim %s in %s" % (name, claim.get("id"), p))
    return 0


def gate_grain(claim):
    """At what level was this computed, and is that level actually unique?

    A number without its grain cannot be interpreted, and a grain that is not
    unique in the source is how a join fans out. This gate exists because the
    first analysis run against the pilot warehouse grouped by product_id alone,
    and product_id turned out to cover 24 different pack sizes.
    """
    g = claim.get("grain")
    if not g:
        return [Finding("G9.grain", FAIL,
                        "no grain declared; state the level this number was "
                        "computed at (per order line, per venue, per month)")]
    out = [Finding("G9.grain", PASS, str(g))]

    sql = claim.get("grain_uniqueness_sql")
    if not sql:
        out.append(Finding("G9.uniqueness", NODATA,
                           "grain is declared but not verified; give "
                           "grain_uniqueness_sql returning the number of "
                           "duplicate key groups"))
        return out
    db = (claim.get("evidence") or {}).get("source")
    try:
        dupes = run_sql(db, sql)
    except Exception as exc:
        out.append(Finding("G9.uniqueness", FAIL,
                           "grain check raised %s: %s" % (type(exc).__name__, exc)))
        return out
    if dupes:
        out.append(Finding("G9.uniqueness", FAIL,
                           "%s key group(s) are not unique at the declared "
                           "grain; any join on this key fans out" % _fmt(dupes)))
    else:
        out.append(Finding("G9.uniqueness", PASS,
                           "declared key is unique in the source"))
    return out


# What each non-SYSTEM origin's protocol must answer. Shared by gate_origin_
# protocol (the claim's own origin) and evaluate_comparison (a comparison's
# origin class), because the questions that interrogate a vendor dataset are
# the same questions whether the vendor dataset IS the claim or is standing
# next to a SYSTEM claim as its incumbent comparison.
PROTOCOL_REQUIRED = {
    "THIRD_PARTY": ["provider", "collection_method", "coverage", "known_biases"],
    "ELICITED": ["expert_role", "elicitation_protocol", "calibration_question",
                 "seed_score"],
    "ASSUMPTION": ["stated_by", "sensitivity_range", "sensitivity_result"],
    "HYPOTHESIS": ["test_that_would_settle_it", "cost_of_being_wrong"],
    "SYSTEM": [],
}


def gate_origin_protocol(claim):
    """Each origin is interrogated by its own question set. A missing answer is
    NO-DATA, which is honest, not a failure. A wrong-shaped answer is a FAIL."""
    o = claim.get("origin")
    p = claim.get("protocol") or {}
    required = PROTOCOL_REQUIRED.get(o, [])

    if not required:
        return Finding("G8.protocol", PASS, "SYSTEM claims are interrogated by "
                                            "re-derivation, not by protocol")
    missing = [k for k in required if not p.get(k)]
    if missing:
        return Finding("G8.protocol", NODATA,
                       "%s protocol incomplete, missing: %s"
                       % (o, ", ".join(missing)))
    return Finding("G8.protocol", PASS,
                   "%s protocol complete (%s)" % (o, ", ".join(required)))


# ----------------------------------------------------------------- accuracy

def choose_metric(actual):
    """Refuse MAPE where it is undefined or dominated by small denominators.

    Hyndman and Koehler: percentage errors are undefined at zero and put a
    heavier penalty on over-forecasting than under-forecasting. The standard
    replacement when the series contains near-zero values is WAPE (also called
    MAD-Mean), which divides total absolute error by total actual.
    """
    mean = sum(abs(a) for a in actual) / float(len(actual))
    smallest = min(abs(a) for a in actual)
    if smallest == 0:
        return "WAPE", "MAPE is undefined: the actual series contains a zero"
    if smallest < 0.1 * mean:
        return "WAPE", ("MAPE refused: smallest actual (%s) is under 10%% of the "
                        "mean (%s), so a few small denominators would dominate "
                        "the average" % (_fmt(smallest), _fmt(mean)))
    return "MAPE", "no near-zero denominators; MAPE is safe here"


def errors(actual, predicted):
    n = len(actual)
    ae = [abs(a - p) for a, p in zip(actual, predicted)]
    mae = sum(ae) / float(n)
    rmse = math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / float(n))
    wape = sum(ae) / float(sum(abs(a) for a in actual))
    out = {"n": n, "MAE": mae, "RMSE": rmse, "WAPE": wape}
    if min(abs(a) for a in actual) > 0:
        out["MAPE"] = sum(abs((a - p) / float(a)) for a, p in zip(actual, predicted)) / float(n)
    return out


def naive_baseline(history, horizon):
    """Last observed value, carried forward. The floor any forecast must beat.

    Not seasonal naive: that needs at least two full cycles of history, and
    claiming it on less is the error this product exists to catch.
    """
    return [history[-1]] * horizon


def gate_accuracy(claim):
    """Returns (findings, computed_metrics). Every metric is reported, not just
    the one the claim happens to name, because the gap between them is often
    the finding."""
    a = claim.get("accuracy")
    if not a:
        return [Finding("G6.accuracy", PASS, "not a predictive claim")], {}
    actual, predicted = a.get("actual"), a.get("predicted")
    if not actual or not predicted or len(actual) != len(predicted):
        return [Finding("G6.accuracy", NODATA,
                        "predictive claim with no matched actual/predicted pairs; "
                        "accuracy is asserted, not measured")], {}

    findings = []
    metric, why = choose_metric(actual)
    e = errors(actual, predicted)
    reported = a.get("reported_metric", "")
    shown = ", ".join("%s=%.1f%%" % (k, 100 * e[k])
                      for k in ("WAPE", "MAPE") if k in e)
    if metric == "WAPE" and "MAPE" in reported:
        findings.append(Finding("G6.accuracy", FAIL,
                                "claim reports MAPE. %s Use WAPE = %.1f%%"
                                % (why, 100 * e["WAPE"])))
    else:
        findings.append(Finding("G6.accuracy", PASS,
                                "%s (safe metric here: %s, %s)" % (shown, metric, why)))

    hist = a.get("history")
    if not hist:
        findings.append(Finding("G6.baseline", NODATA,
                                "no history given, so no baseline could be "
                                "computed; an accuracy figure without a baseline "
                                "says nothing about skill"))
    else:
        base = naive_baseline(hist, len(actual))
        be = errors(actual, base)
        ratio = e["MAE"] / be["MAE"] if be["MAE"] else float("inf")
        if ratio < 1:
            findings.append(Finding("G6.baseline", PASS,
                                    "beats naive: MASE-style ratio %.2f "
                                    "(model MAE %s vs naive %s)"
                                    % (ratio, _fmt(e["MAE"]), _fmt(be["MAE"]))))
        else:
            findings.append(Finding("G6.baseline", FAIL,
                                    "does NOT beat carrying the last value "
                                    "forward: ratio %.2f (model MAE %s vs naive "
                                    "%s). The forecast has no demonstrated skill"
                                    % (ratio, _fmt(e["MAE"]), _fmt(be["MAE"]))))

    if hist and len(hist) < 24:
        findings.append(Finding("G6.seasonality", NODATA,
                                "%d periods of history: fewer than two full "
                                "yearly cycles, so seasonality cannot be "
                                "established and no seasonal claim may be made"
                                % len(hist)))
    return findings, e


# --------------------------------------------------------------------- check

# --------------------------------------------------------- master data

# Wording that can only mean entity resolution. Deliberately tight: "match" on
# its own is far too common a word to hang a refusal on, so only phrases that
# cannot mean anything else are listed.
MDM_WORDING = re.compile(
    r"\b(duplicates?|duplicated|dedup\w*|deduplicat\w*|golden record|"
    r"master record|entity resolution|record linkage|survivorship|"
    r"single customer view|"
    r"match(?:ing|ed)?\s+(?:record|entity|entities|customer|product)\w*|"
    r"merg\w+\s+(?:record|entity|entities|customer)\w*)\b", re.I)

MERGE_WORDING = re.compile(
    r"\b(merg\w+|survivorship|golden record|master record)\b", re.I)

# Where the labelled pairs were drawn from. This is the whole difference
# between a recall figure and a guess: a sample drawn from the candidate set a
# blocker produced cannot contain the pairs that blocker never proposed, so
# recall measured on it is an upper bound being reported as a fact.
FRAMES = ("full_cross_product", "stratified_sample", "candidate_set")


def _num01(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and 0.0 <= v <= 1.0


def gate_master_data(claim):
    """G11 to G14, the refusals master data work earns.

    A dedupe or match claim that says how many records it resolved, and nothing
    about how many it resolved WRONGLY, is the master data overclaim. It is the
    same shape as an accuracy figure with no baseline, and it is more dangerous,
    because the errors here are not symmetric: merging two distinct customers is
    usually irreversible and visible to that customer, while missing a duplicate
    is cheap and caught on the next run. One blended score hides exactly that.
    """
    text = " ".join(str(claim.get(k, "")) for k in
                    ("statement", "question", "decision"))
    m = claim.get("match")
    if not MDM_WORDING.search(text) and not m:
        return []           # not a master data claim; these gates say nothing

    out = []
    if not isinstance(m, dict) or not m:
        out.append(Finding("G11.match_quality", FAIL,
                           "the statement asserts entity resolution but the "
                           "claim carries no match block, so how much was "
                           "resolved wrongly is unstated"))
        return out

    # G11: the count is not the claim. The error rates are.
    missing = [k for k in ("precision", "recall", "threshold")
               if m.get(k) is None]
    if missing:
        out.append(Finding("G11.match_quality", FAIL,
                           "match block missing %s. A resolved-record count "
                           "without both error rates, at a stated operating "
                           "point, is the master data overclaim"
                           % ", ".join(missing)))
    elif not (_num01(m["precision"]) and _num01(m["recall"])):
        out.append(Finding("G11.match_quality", FAIL,
                           "precision and recall must be proportions between "
                           "0 and 1; got %r and %r"
                           % (m.get("precision"), m.get("recall"))))
    else:
        out.append(Finding("G11.match_quality", PASS,
                           "precision %.3f, recall %.3f at threshold %s"
                           % (m["precision"], m["recall"], m["threshold"])))

    # G12: the two errors do not cost the same, so they are never blended.
    blended = [k for k in ("f1", "f_measure", "accuracy") if m.get(k) is not None]
    have_both = m.get("precision") is not None and m.get("recall") is not None
    if blended and not have_both:
        out.append(Finding("G12.error_asymmetry", FAIL,
                           "%s reported without precision and recall. A single "
                           "blended score averages a false merge against a "
                           "missed duplicate, which are not the same event"
                           % ", ".join(blended)))
    else:
        costs = [k for k in ("false_positive_cost", "false_negative_cost")
                 if not _answered(m.get(k))]
        if costs:
            out.append(Finding("G12.error_asymmetry", FAIL,
                               "missing %s. Naming what each error costs is "
                               "what makes an operating point a decision "
                               "rather than a preference" % ", ".join(costs)))
        else:
            out.append(Finding("G12.error_asymmetry", PASS,
                               "both error costs named separately"))

    # G13: recall is only as honest as the frame its sample was drawn from.
    ls = m.get("labelled_sample")
    if not isinstance(ls, dict) or not ls:
        out.append(Finding("G13.sample_frame", FAIL,
                           "no labelled sample, so precision and recall were "
                           "computed against nothing that was checked by hand"))
    else:
        gaps = [k for k in ("n", "frame", "labelled_by", "labelled_on")
                if not _answered(ls.get(k))]
        if gaps:
            out.append(Finding("G13.sample_frame", FAIL,
                               "labelled sample missing %s" % ", ".join(gaps)))
        elif ls.get("frame") not in FRAMES:
            out.append(Finding("G13.sample_frame", FAIL,
                               "frame %r is not one of %s"
                               % (ls.get("frame"), ", ".join(FRAMES))))
        elif ls.get("frame") == "candidate_set":
            out.append(Finding("G13.sample_frame", NODATA,
                               "the sample was drawn from the candidate set, "
                               "which cannot contain the pairs blocking never "
                               "proposed. Precision survives this; RECALL does "
                               "not, and is an upper bound rather than a rate"))
        else:
            out.append(Finding("G13.sample_frame", PASS,
                               "%s labelled pairs drawn from the %s"
                               % (_fmt(ls["n"]), ls["frame"])))

    # G14: a merge is a one-way door unless somebody says otherwise.
    if MERGE_WORDING.search(text) or m.get("kind") == "merge":
        gaps = []
        if not _answered(m.get("survivorship")):
            gaps.append("survivorship")
        if m.get("reversible") is None:
            gaps.append("reversible")
        if gaps:
            out.append(Finding("G14.survivorship", FAIL,
                               "a merge claim must state %s. Which value wins "
                               "decides what is destroyed, and whether it can "
                               "be undone decides how bad a wrong merge is"
                               % " and ".join(gaps)))
        elif m.get("reversible") is False:
            out.append(Finding("G14.survivorship", PASS,
                               "survivorship stated, and the claim says the "
                               "merge is NOT reversible: a wrong merge here "
                               "cannot be undone"))
        else:
            out.append(Finding("G14.survivorship", PASS,
                               "survivorship stated and the merge is reversible"))
    return out


GATES = (gate_origin, gate_not_established, gate_uncertainty,
         gate_causal, gate_origin_protocol)


DEFAULT_REGISTRY = "definitions.json"


def check(claim, registry_path=DEFAULT_REGISTRY):
    findings = []
    for g in GATES:
        findings.append(g(claim))
    findings.append(gate_definition(claim, registry_path))
    findings.extend(gate_grain(claim))
    findings.extend(gate_master_data(claim))
    values = []
    if claim.get("origin") == "SYSTEM":
        values, dfind = evaluate_derivations(claim)
        findings.extend(dfind)
        findings.extend(evaluate_comparison(claim, values))
    acc_findings, metrics = gate_accuracy(claim)
    findings.append(gate_value_matches(claim, values, metrics))
    findings.extend(acc_findings)

    if any(f.verdict == FAIL for f in findings):
        verdict = FAIL
    elif any(f.verdict == NODATA for f in findings):
        verdict = NODATA
    else:
        verdict = PASS
    return verdict, findings, values


def print_check(claim, verdict, findings):
    """The page `check` prints, shared with `author` so a newly authored claim
    is shown its own G-gate result rather than a second, drifting copy of this
    text."""
    print("claim   %s" % claim.get("id"))
    print("        %s" % claim.get("statement"))
    print("")
    for f in findings:
        print("  " + f.line())
    print("")
    print("VERDICT %s" % verdict)
    if verdict == NODATA:
        print("        NO-DATA is not a pass and not a block. Something the "
              "claim needs was never measured.")


# ------------------------------------------------------------------- receipt

def receipt(claim, verdict, findings):
    L = []
    A = L.append
    A("# Claim receipt: %s" % claim.get("id", "(no id)"))
    A("")
    A("**%s**" % claim.get("statement", ""))
    A("")
    A("| field | value |")
    A("|---|---|")
    A("| Value | %s %s |" % (_fmt(claim.get("value")), claim.get("unit", "")))
    A("| Origin | %s |" % claim.get("origin"))
    A("| Question it answers | %s |" % claim.get("question", "NOT STATED"))
    A("| Decision it feeds | %s |" % claim.get("decision", "NOT STATED"))
    A("| Verdict | **%s** |" % verdict)
    A("")
    ev = claim.get("evidence") or {}
    if ev.get("source"):
        st = source_state(ev["source"])
        A("## Source")
        if st:
            A("`%s`  \nbytes %s, mtime %s" % (st["path"], _fmt(st["bytes"]), st["mtime"]))
        else:
            A("`%s` (MISSING)" % ev["source"])
        A("")
    if ev.get("derivations"):
        A("## Derivations")
        for d in ev["derivations"]:
            A("**%s**" % d.get("name", "?"))
            A("```sql")
            A(d["sql"].strip())
            A("```")
        A("")
    A("## Gates")
    A("```")
    for f in findings:
        A(f.line())
    A("```")
    A("")
    A("## What was NOT established")
    for item in (claim.get("not_established") or ["(nothing declared, which is itself a failure)"]):
        A("- %s" % item)
    A("")
    if claim.get("known_defects_in_source"):
        A("## Known defects in the source")
        for item in claim["known_defects_in_source"]:
            A("- %s" % item)
        A("")
    if claim.get("how_it_was_found"):
        A("## How this was found")
        A(claim["how_it_was_found"])
        A("")
    o = claim.get("outcome")
    A("## Verified against reality")
    if o and o.get("actual") is not None:
        A("Actual: %s. Recorded %s. Error %s."
          % (_fmt(o["actual"]), _fmt(claim.get("value")),
             _fmt(abs(float(o["actual"]) - float(claim.get("value"))))))
        A("")
        A("Verified on %s by %s." % (o.get("observed_on", "?"), o.get("observed_by", "?")))
    else:
        A("NOT YET. This claim has not been scored against what actually happened. "
          "A gate verdict is a statement about proof; only an outcome is a "
          "statement about the world.")
    return "\n".join(L)


# ------------------------------------------------------------------ selftest

def selftest():
    """Every gate must be able to reach a verdict, and must refuse what it
    claims to refuse. A gate that cannot fail is not a control."""
    ok = True

    def expect(cond, msg):
        if not cond:
            print("SELFTEST FAIL: %s" % msg)
        return bool(cond)

    base = {"id": "T", "statement": "Volume was 100 units.", "value": 100,
            "origin": "SYSTEM", "uncertainty": {"kind": "NOT_ESTABLISHED", "why": "census"},
            "not_established": ["nothing checked"]}

    # G1 refuses an empty not_established
    c = dict(base); c["not_established"] = []
    ok &= expect(gate_not_established(c).verdict == FAIL, "G1 must fail on empty")
    ok &= expect(gate_not_established(base).verdict == PASS, "G1 must pass when declared")

    # G2 refuses an unknown origin
    c = dict(base); c["origin"] = "VIBES"
    ok &= expect(gate_origin(c).verdict == FAIL, "G2 must fail unknown origin")

    # G3 refuses a bare number
    c = dict(base); c.pop("uncertainty")
    ok &= expect(gate_uncertainty(c).verdict == FAIL, "G3 must fail missing uncertainty")
    ok &= expect(gate_uncertainty(base).verdict == NODATA, "G3 NOT_ESTABLISHED is NO-DATA")

    # G4 refuses causal wording with no design, permits it under HYPOTHESIS
    c = dict(base); c["statement"] = "The banner drove incremental orders."
    ok &= expect(gate_causal(c).verdict == FAIL, "G4 must fail undesigned causal claim")
    c2 = dict(c); c2["origin"] = "HYPOTHESIS"
    ok &= expect(gate_causal(c2).verdict == NODATA, "G4 hypothesis is NO-DATA not FAIL")
    c3 = dict(c); c3["design"] = {"kind": "difference_in_differences",
                                 "assumption_test": "pre-trend test"}
    ok &= expect(gate_causal(c3).verdict == PASS, "G4 must pass a designed claim")
    c4 = dict(c); c4["design"] = {"kind": "difference_in_differences"}
    ok &= expect(gate_causal(c4).verdict == FAIL, "G4 must fail untested assumption")

    # G6 refuses MAPE on near-zero denominators
    m, _ = choose_metric([100.0, 100.0, 0.5])
    ok &= expect(m == "WAPE", "choose_metric must refuse MAPE near zero")
    m, _ = choose_metric([100.0, 110.0, 90.0])
    ok &= expect(m == "MAPE", "choose_metric must allow MAPE when safe")

    # G6 must catch a forecast that loses to the naive baseline
    c = dict(base)
    c["accuracy"] = {"history": [100.0] * 12, "actual": [100.0, 100.0],
                     "predicted": [130.0, 70.0]}
    fs, metrics = gate_accuracy(c)
    ok &= expect(any(f.gate == "G6.baseline" and f.verdict == FAIL for f in fs),
                 "G6 must fail a forecast worse than naive")

    # G6 must refuse seasonality on short history
    ok &= expect(any(f.gate == "G6.seasonality" and f.verdict == NODATA for f in fs),
                 "G6 must refuse seasonality under 24 periods")

    # G7 must check a stated accuracy figure against the recomputed metric.
    # Regression fixture: SKU-FCST-003 originally claimed MAPE 0.47 when the true
    # value was 0.6322, because only the first month had been computed by hand.
    c7 = {"value": 0.47, "accuracy": {"reported_metric": "MAPE",
                                      "actual": [35460.0, 33078.0, 37779.0],
                                      "predicted": [52209.3, 57785.5, 63361.6]}}
    _, m7 = gate_accuracy(c7)
    ok &= expect(abs(m7["MAPE"] - 0.6322) < 1e-3, "MAPE fixture must be 0.6322")
    ok &= expect(gate_value_matches(c7, [], m7).verdict == FAIL,
                 "G7 must fail a stated metric that does not match the computed one")
    c7ok = dict(c7); c7ok["value"] = m7["MAPE"]
    ok &= expect(gate_value_matches(c7ok, [], m7).verdict == PASS,
                 "G7 must pass when the stated metric matches")

    # G5.comparison: the dual run, a SYSTEM derivation paired with a
    # THIRD_PARTY or ELICITED comparison against the incumbent artifact.
    # value_paths is passed in directly rather than run through evaluate_
    # derivations, so this needs no duckdb and no database file, exactly the
    # promise that non-SYSTEM machinery costs nothing in dependencies.
    def cmp_claim(**overrides):
        c = {"evidence": {"comparison": dict(
            {"class": "THIRD_PARTY", "incumbent": "the ops team's spreadsheet",
             "incumbent_value": 101, "tolerance": 5,
             "protocol": {"provider": "regional distributor", "coverage": "national",
                          "collection_method": "monthly manual export",
                          "known_biases": "excludes cash sales"}},
            **overrides)}}
        return c

    # the old SQL-only claim (no comparison block at all) is unaffected
    ok &= expect(evaluate_comparison({"evidence": {"source": "x"}}, [("q", 100)]) == [],
                 "no comparison block: G5.comparison says nothing, the SQL-only "
                 "path is unchanged")

    # agrees within tolerance: PASS
    f = evaluate_comparison(cmp_claim(), [("q", 100)])
    ok &= expect(len(f) == 1 and f[0].gate == "G5.comparison" and f[0].verdict == PASS,
                 "G5.comparison must pass when system and incumbent agree "
                 "within the stated tolerance")

    # disagrees beyond tolerance: FAIL
    f = evaluate_comparison(cmp_claim(incumbent_value=500), [("q", 100)])
    ok &= expect(len(f) == 1 and f[0].verdict == FAIL,
                 "G5.comparison must fail when system and incumbent disagree "
                 "beyond the stated tolerance")

    # missing tolerance: NO-DATA naming the field
    no_tol = cmp_claim(); no_tol["evidence"]["comparison"].pop("tolerance")
    f = evaluate_comparison(no_tol, [("q", 100)])
    ok &= expect(len(f) == 1 and f[0].verdict == NODATA and "tolerance" in f[0].detail,
                 "G5.comparison must refuse a missing tolerance as NO-DATA, "
                 "naming the field")

    # missing incumbent description: NO-DATA naming the field
    no_inc = cmp_claim(); no_inc["evidence"]["comparison"].pop("incumbent")
    f = evaluate_comparison(no_inc, [("q", 100)])
    ok &= expect(len(f) == 1 and f[0].verdict == NODATA and "incumbent" in f[0].detail,
                 "G5.comparison must refuse a missing incumbent description as "
                 "NO-DATA, naming the field")

    # missing protocol field for the comparison's own class: NO-DATA naming it
    no_proto = cmp_claim(); no_proto["evidence"]["comparison"]["protocol"].pop("provider")
    f = evaluate_comparison(no_proto, [("q", 100)])
    ok &= expect(len(f) == 1 and f[0].verdict == NODATA and "provider" in f[0].detail,
                 "G5.comparison must refuse an incomplete comparison protocol "
                 "as NO-DATA, naming the missing field")

    # invalid class: FAIL, not silently accepted
    bad_cls = cmp_claim(**{"class": "VIBES"})
    f = evaluate_comparison(bad_cls, [("q", 100)])
    ok &= expect(len(f) == 1 and f[0].verdict == FAIL,
                 "G5.comparison must fail an unknown comparison class")

    # no system value to compare against yet: NO-DATA, not a silent skip
    f = evaluate_comparison(cmp_claim(), [])
    ok &= expect(len(f) == 1 and f[0].verdict == NODATA,
                 "G5.comparison must refuse to compare against nothing "
                 "recomputed on the system side")

    # `check` itself must reach a verdict on the pairing, not refuse the non-
    # SQL path. A SYSTEM claim with one SQL derivation and a comparison that
    # agrees must show both G5.rederivation (single path, NO-DATA) and
    # G5.comparison (PASS) rather than the comparison being invisible.
    dual = dict(base)
    dual["grain"] = "one row per month"
    dual["evidence"] = {"derivations": [{"name": "warehouse rollup",
                                         "sql": "select 100"}],
                        "comparison": {"class": "ELICITED",
                                      "incumbent": "the regional lead's estimate",
                                      "incumbent_value": 100, "tolerance": 0,
                                      "protocol": {"expert_role": "regional lead",
                                                  "elicitation_protocol": "structured interview",
                                                  "calibration_question": "known benchmark quantity",
                                                  "seed_score": 0.8}}}
    dual["value"] = None  # SQL derivation is stubbed by the test below, not run
    dual_findings = evaluate_comparison(dual, [("stub", 100)])
    ok &= expect(dual_findings[0].verdict == PASS,
                 "a SYSTEM claim's ELICITED comparison must reach PASS, "
                 "proving the pairing is checkable end to end")

    # G9 must refuse a claim with no declared grain
    c9 = dict(base)
    ok &= expect(gate_grain(c9)[0].verdict == FAIL, "G9 must fail missing grain")
    c9["grain"] = "one row per month"
    gf = gate_grain(c9)
    ok &= expect(gf[0].verdict == PASS, "G9 must pass a declared grain")
    ok &= expect(gf[1].verdict == NODATA, "G9 unverified grain is NO-DATA")

    # errors() arithmetic, checked by hand
    e = errors([100.0, 200.0], [110.0, 180.0])
    ok &= expect(abs(e["MAE"] - 15.0) < 1e-9, "MAE must be 15")
    ok &= expect(abs(e["WAPE"] - 30.0 / 300.0) < 1e-9, "WAPE must be 0.1")

    # G10 must refuse a named metric with no definition, and must catch two
    # different definitions under one name. This is the gate that answers
    # "a definition is not a file"; reproduction gates cannot see it.
    import tempfile
    tmp = tempfile.mkdtemp()
    reg = os.path.join(tmp, "definitions.json")
    ok &= expect(gate_definition({}, reg).verdict == NODATA,
                 "G10 with no metric is NO-DATA")
    ok &= expect(gate_definition({"metric": {"name": "gmv"}}, reg).verdict == FAIL,
                 "G10 must fail a named metric with no definition")
    ca = {"id": "A", "metric": {"name": "gmv", "definition": "gross, before cancellations"}}
    ok &= expect(gate_definition(ca, reg).verdict == NODATA,
                 "G10 first use is NO-DATA, not PASS")
    register_definition(ca, reg)
    ok &= expect(gate_definition(ca, reg).verdict == PASS,
                 "G10 must pass an identical definition")
    ok &= expect(gate_definition({"id": "A", "metric": {"name": "gmv",
                 "definition": "GROSS,  Before Cancellations"}}, reg).verdict == PASS,
                 "G10 must ignore case and whitespace")
    cb = {"id": "B", "metric": {"name": "gmv", "definition": "net, after cancellations"}}
    ok &= expect(gate_definition(cb, reg).verdict == FAIL,
                 "G10 must fail two definitions under one name")
    ok &= expect(register_definition(cb, reg) == 1,
                 "register must refuse to overwrite a conflicting definition")

    # score: a claim with no stated interval can never be HELD, only UNSCOREABLE.
    # This is what keeps the north star from rewarding people for saying nothing.
    sp = os.path.join(tmp, "s.json")
    cs = {"id": "S", "value": 100, "uncertainty": {"kind": "interval", "interval": [90, 110]},
          "not_established": ["x"]}
    score(dict(cs), sp, 95, "t", "d")
    ok &= expect(json.load(open(sp))["outcome"]["state"] == "HELD", "score inside is HELD")
    score(dict(cs), sp, 200, "t", "d")
    ok &= expect(json.load(open(sp))["outcome"]["state"] == "MISSED", "score outside is MISSED")
    cu = {"id": "U", "value": 100,
          "uncertainty": {"kind": "NOT_ESTABLISHED", "why": "census"}}
    score(dict(cu), sp, 95, "t", "d")
    ok &= expect(json.load(open(sp))["outcome"]["state"] == "UNSCOREABLE",
                 "a claim stating no interval is UNSCOREABLE, never HELD")

    # a whole-numbered float must render as a quantity, not in scientific notation
    ok &= expect(_fmt(1050000.0) == "1,050,000", "_fmt must not print 1.05e+06")

    # The ledger must never drop a claim silently. A rate computed over an
    # unstated subset is the failure this whole product refuses.
    ldir = os.path.join(tmp, "ledger")
    os.makedirs(ldir)
    with open(os.path.join(ldir, "good.json"), "w") as fh:
        json.dump({"id": "G", "statement": "fine"}, fh)
    with open(os.path.join(ldir, "broken.json"), "w") as fh:
        fh.write("{not json at all")
    import io as _io
    import contextlib as _ctx
    buf = _io.StringIO()
    with _ctx.redirect_stdout(buf):
        ledger(ldir)
    out = buf.getvalue()
    ok &= expect("UNREADABLE" in out and "broken.json" in out,
                 "ledger must name a claim file it could not read")
    ok &= expect("1 of 2 claim files" in out,
                 "ledger must state how many claims the rate actually covers")

    # `author`: a claim reaches disk only as a side effect of the CLI, never
    # by hand-editing JSON. Each assertion below is a refusal it must make.
    adir = os.path.join(tmp, "authored")
    os.makedirs(adir)
    full_input = (
        "id=RGM-014\n"
        "statement=Weekly orders for wholesaler segment A were 8123.\n"
        "value=8123\n"
        "unit=orders\n"
        "origin=ASSUMPTION\n"
        "question=What is this week's order volume for the incentive model?\n"
        "decision=Sets the base the incentive payout is a percentage of.\n"
        "grain=one row per calendar week, whole segment\n"
        "uncertainty.kind=NOT_ESTABLISHED\n"
        "uncertainty.why=stated by the ops lead, not yet reconciled to a system\n"
        "not_established=No reconciliation was run against the order system.\n"
        "not_established=Returns after the week close were not checked.\n"
    )
    ap = os.path.join(adir, "rgm-014.json")
    buf = _io.StringIO()
    with _ctx.redirect_stdout(buf):
        rc = author(ap, full_input)
    ok &= expect(rc == 0, "author must accept a complete claim: %s" % buf.getvalue())
    ok &= expect(os.path.exists(ap), "author must write the claim file")
    written = json.load(open(ap))
    ok &= expect(written["value"] == 8123 and isinstance(written["value"], int),
                 "author must coerce a whole-numbered value to an int")
    ok &= expect(written["not_established"] ==
                 ["No reconciliation was run against the order system.",
                  "Returns after the week close were not checked."],
                 "repeated not_established= lines must become an ordered list")
    ok &= expect(written["uncertainty"] ==
                 {"kind": "NOT_ESTABLISHED",
                  "why": "stated by the ops lead, not yet reconciled to a system"},
                 "dotted keys must nest exactly what was written, nothing hand-added")
    v, findings, _ = check(written, os.path.join(adir, DEFAULT_REGISTRY))
    ok &= expect(v != FAIL, "a claim `author` accepts must not FAIL `check`: %s"
                 % "; ".join(f.line() for f in findings))

    buf2 = _io.StringIO()
    with _ctx.redirect_stdout(buf2):
        rc2 = author(os.path.join(adir, "missing-unit.json"),
                     full_input.replace("unit=orders\n", ""))
    ok &= expect(rc2 == 2, "author must refuse a claim missing a required field")
    ok &= expect("unit" in buf2.getvalue(),
                 "author must name the missing field, not just refuse silently")
    ok &= expect(not os.path.exists(os.path.join(adir, "missing-unit.json")),
                 "author must write nothing when validation fails")

    # G11 to G14, master data. Each assertion is a refusal the gate must make;
    # a gate that cannot fail is not a control.
    def mdm(**kw):
        c = dict(base); c["statement"] = "We removed 12,000 duplicate customers."
        if kw: c["match"] = kw
        return c

    def verd(c, gate):
        for f in gate_master_data(c):
            if f.gate.startswith(gate): return f.verdict
        return None

    ok &= expect(gate_master_data(base) == [],
                 "the master data gates say nothing about a non-master-data claim")
    ok &= expect(verd(mdm(), "G11") == FAIL,
                 "G11 must refuse entity-resolution wording with no match block")
    full = dict(precision=0.94, recall=0.87, threshold=0.85,
                false_positive_cost="two distinct customers merged",
                false_negative_cost="a duplicate survives to the next run",
                labelled_sample=dict(n=500, frame="full_cross_product",
                                     labelled_by="data steward", labelled_on="2026-08-20"))
    ok &= expect(verd(mdm(**full), "G11") == PASS, "G11 passes a complete match block")
    c = dict(full); c.pop("recall")
    ok &= expect(verd(mdm(**c), "G11") == FAIL, "G11 must refuse a count with no recall")
    c = dict(full); c["precision"] = 94
    ok &= expect(verd(mdm(**c), "G11") == FAIL,
                 "G11 must refuse a precision that is not a proportion")
    c = dict(full); c.pop("precision"); c.pop("recall"); c["f1"] = 0.90
    ok &= expect(verd(mdm(**c), "G12") == FAIL,
                 "G12 must refuse a blended F1 standing in for both error rates")
    c = dict(full); c.pop("false_positive_cost")
    ok &= expect(verd(mdm(**c), "G12") == FAIL,
                 "G12 must refuse an operating point with no cost named for each error")
    c = dict(full); c.pop("labelled_sample")
    ok &= expect(verd(mdm(**c), "G13") == FAIL,
                 "G13 must refuse error rates computed against nothing hand-checked")
    c = dict(full); c["labelled_sample"] = dict(full["labelled_sample"], frame="candidate_set")
    ok &= expect(verd(mdm(**c), "G13") == NODATA,
                 "G13 reads a candidate-set frame as NO-DATA: blocking's misses are invisible to it")
    c = dict(full); c["labelled_sample"] = dict(full["labelled_sample"], frame="vibes")
    ok &= expect(verd(mdm(**c), "G13") == FAIL, "G13 must refuse an unknown sample frame")
    merge = dict(base); merge["statement"] = "Merging these customer records is safe."
    merge["match"] = dict(full)
    ok &= expect(verd(merge, "G14") == FAIL,
                 "G14 must refuse a merge that states neither survivorship nor reversibility")
    merge["match"] = dict(full, survivorship="most recent non-null per field", reversible=False)
    ok &= expect(verd(merge, "G14") == PASS,
                 "G14 passes an irreversible merge that SAYS it is irreversible")

    # The chain is a control only if it refuses something. A stage the chain
    # does not hold is a hard error; the stage a person owns is refused by name.
    ok &= expect(stage_check("outcome").verdict == PASS, "a real stage passes")
    ok &= expect(stage_check("shipping").verdict == FAIL, "an unknown stage fails")
    ok &= expect(stage_check("decision-taken").verdict == FAIL,
                 "the stage a person takes may not be served by an item")
    ok &= expect(stage_check("").verdict == NODATA, "an unnamed stage is NO-DATA")
    ok &= expect(all(occ for name, occ in CHAIN if name not in UNSERVABLE),
                 "every servable stage must stand in a shared stage")
    ok &= expect(dict(CHAIN)["verified-reality"] == ("verified-reality",),
                 "the chain must end in the shared stage nobody else owns")

    # The document and the code may not disagree about the chain. This mirrors
    # BrotherMode's own schema-versus-doc anti-drift test rather than trusting
    # two copies of one contract to stay equal by attention.
    _doc = os.path.join(os.path.dirname(os.path.abspath(__file__)), CHAIN_DOC)
    try:
        ok &= expect(chain_from_doc(_doc) == CHAIN,
                     "%s and CHAIN must not drift" % CHAIN_DOC)
    except (IOError, OSError, ValueError) as exc:
        ok &= expect(False, "chain document unreadable: %s" % exc)

    # The passport consumer. Absence is NO-DATA, padding is a FAIL, and 0 and
    # False are real answers rather than emptiness.
    pp = os.path.join(tmp, "passport.json")
    ok &= expect(read_passport(os.path.join(tmp, "nothing.json"))[0] == NODATA,
                 "an undeposited passport is NO-DATA")
    full = dict((f, "stated") for f in PASSPORT_FIELDS)
    with open(pp, "w") as fh:
        json.dump(full, fh)
    ok &= expect(read_passport(pp)[0] == PASS, "a complete passport passes")
    padded = dict(full); padded["whatWasRun"] = ""
    with open(pp, "w") as fh:
        json.dump(padded, fh)
    ok &= expect(read_passport(pp)[0] == FAIL,
                 "a field padded to look filled is a FAIL, not an absence")
    partial = dict(full); partial.pop("whatWasDone")
    with open(pp, "w") as fh:
        json.dump(partial, fh)
    ok &= expect(read_passport(pp)[0] == NODATA,
                 "an honestly omitted field is NO-DATA, not a FAIL")
    ok &= expect(_answered(0) and _answered(False),
                 "0 and False are answers; only absence is absence")
    ok &= expect(not _answered("   ") and not _answered([]),
                 "whitespace and an empty list read as absence")

    # MERGE-P5: the canonical passport fixture, byte-identical across all
    # three repositories, pins to one recorded sha256. A byte drifting in the
    # copy must redden this suite, not pass silently.
    _fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "examples", "change-passport.v1.canonical.json")
    _fixture_sha = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "examples", "change-passport.v1.canonical.sha256")
    with open(_fixture, "rb") as fh:
        _fixture_bytes = fh.read()
    _digest = hashlib.sha256(_fixture_bytes).hexdigest()
    print("passport canonical fixture sha256 %s" % _digest[:8])
    with open(_fixture_sha) as fh:
        _recorded = fh.read().strip()
    ok &= expect(_digest == _recorded,
                 "examples/change-passport.v1.canonical.json drifted from the "
                 "recorded digest in examples/change-passport.v1.canonical.sha256")
    ok &= expect(read_passport(_fixture)[0] == PASS,
                 "bds.py passport must parse the canonical fixture")

    # The handoff package. It may never certify a shape nobody ratified.
    hp = os.path.join(tmp, "handoff.json")
    ok &= expect(read_handoff(os.path.join(tmp, "none.json"))[0] == NODATA,
                 "an undelivered handoff package is NO-DATA")
    pkg = {"dataset": {"grain": "one row per order line", "contract": "c",
                       "snapshot_id": "s"},
           "evaluation_harness": {"split": "time-based"},
           "metric_definitions": [{"name": "gmv", "formula": "sum(x)"}],
           "labelled_holdout": {"labelled_by": "ops lead", "labelled_on": "2026-08-01"},
           "open_questions": []}
    with open(hp, "w") as fh:
        json.dump(pkg, fh)
    ok &= expect(read_handoff(hp)[0] == NODATA,
                 "a complete package with no ratified shape is still NO-DATA")
    pkg["ratified"] = True
    with open(hp, "w") as fh:
        json.dump(pkg, fh)
    ok &= expect(read_handoff(hp)[0] == PASS,
                 "a complete package passes once its shape is ratified")
    short = json.loads(json.dumps(pkg)); short["dataset"].pop("snapshot_id")
    with open(hp, "w") as fh:
        json.dump(short, fh)
    ok &= expect(read_handoff(hp)[0] == NODATA,
                 "an item carried without its required parts is NO-DATA")

    # The backlog is what turns the chain from a document into a control. Until
    # something reads a queue and refuses an item serving no stage, the stage
    # vocabulary is a discipline. Each assertion below is a refusal it must make.
    bq = os.path.join(tmp, "queue.json")
    ok &= expect(read_backlog(os.path.join(tmp, "noqueue.json"))[0] == NODATA,
                 "an absent backlog is NO-DATA, not a pass")
    good = [{"id": "A", "title": "t", "state": "queued", "stage": "outcome",
             "check": "bds.py ledger claims/"}]
    with open(bq, "w") as fh:
        json.dump(good, fh)
    ok &= expect(read_backlog(bq)[0] == PASS, "a well formed backlog passes")
    for bad, why in (
            ({"id": "B", "state": "queued", "stage": "shipping", "check": "c"},
             "an item serving a stage the chain lacks is refused"),
            ({"id": "C", "state": "queued", "stage": "decision-taken", "check": "c"},
             "an item claiming the stage a person takes is refused"),
            ({"id": "D", "state": "queued", "stage": "outcome"},
             "an item naming no check is refused"),
            ({"id": "E", "state": "done-ish", "stage": "outcome", "check": "c"},
             "an item in a state this queue does not have is refused")):
        with open(bq, "w") as fh:
            json.dump([bad], fh)
        ok &= expect(read_backlog(bq)[0] == FAIL, why)
    with open(bq, "w") as fh:
        json.dump([], fh)
    ok &= expect(read_backlog(bq)[0] == NODATA, "an empty backlog is NO-DATA")

    # The project's own queue must satisfy the rule the engine enforces on any
    # other. A control its author's own file cannot pass is a control nobody
    # will keep.
    _own_queue = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              DEFAULT_QUEUE)
    ok &= expect(read_backlog(_own_queue)[0] == PASS,
                 "this project's own %s must pass the backlog check" % DEFAULT_QUEUE)

    # The isolation law as a control rather than a discipline: this file may not
    # name any path on the far side of the seam. Reaching across to fill a
    # missing field is the failure the seam exists to prevent, and a rule with
    # no file behind it is not a control.
    #
    # The needles are assembled from pieces rather than written whole, because a
    # scan whose own pattern appears in the text it scans reports a hit it
    # created. That exact mistake cost this project a false credential alarm on
    # its first night.
    _src = open(os.path.abspath(__file__)).read()
    for _needle in ("." + "brothermode", ".sbe/" + "tasks", ".sbe/" + "evidence",
                    "store." + "sqlite3"):
        ok &= expect(_needle not in _src,
                     "this file may not name %r: it is on the far side of the "
                     "seam" % _needle)

    # The integration document names the fields this code reads. If the code
    # grows a field and the document does not, the document is stale and says
    # something untrue about the seam.
    _seam_doc = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "docs/TRIUMVIRATE-INTEGRATION.md")
    try:
        _seam = open(_seam_doc).read()
        for _name in PASSPORT_FIELDS + tuple(i for i, _ in HANDOFF_ITEMS):
            ok &= expect(_name in _seam,
                         "the integration document must name %s" % _name)
    except (IOError, OSError) as exc:
        ok &= expect(False, "integration document unreadable: %s" % exc)

    print("SELFTEST PASS" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


# ------------------------------------------------------------------- the chain

# BrotherDS's own stage vocabulary, and the shared north-star stage each one
# occupies. Four stage and state vocabularies already coexist across the other
# two products, and reusing the wrong one by string-matching corrupts data
# silently, so this list is BrotherDS's own and is never compared to another
# product's enum by name.
#
# The right-hand column is what makes the integration native rather than
# adjacent. Every BrotherDS stage names the shared stage it STANDS IN, so the
# third product occupies the same chain the other two occupy, for a different
# unit. It adds no stage to the chain.
#
# docs/NORTH-STAR-CHAIN.md carries this same table, and selftest refuses to let
# the document and the code disagree.
CHAIN = (
    ("question",         ("intent",)),
    ("design",           ("method",)),
    ("provenance",       ("provenance",)),
    ("receipt",          ("passport",)),
    ("refusals",         ("required-proof", "evidence-integrity")),
    ("human-decision",   ("human-decision",)),
    ("decision-taken",   ()),
    ("outcome",          ("production-observation",)),
    ("verified-reality", ("verified-reality",)),
)

# A person takes the decision, exactly as a host performs the release. No
# backlog item of this product may claim to serve it. BrotherMode leaves
# `release` out of its servable stages for that reason; this is the same
# refusal, for the claim rather than for the change.
UNSERVABLE = ("decision-taken",)

STAGES = tuple(s for s, _ in CHAIN)
SERVABLE = tuple(s for s in STAGES if s not in UNSERVABLE)

CHAIN_DOC = "docs/NORTH-STAR-CHAIN.md"


def chain_from_doc(path):
    """Parse the ```chain block out of the chain document.

    Returns the same shape as CHAIN. Raises if the block is missing, because a
    document that lost its own contract is a defect, not a NO-DATA.
    """
    text = open(_expand(path)).read()
    lines = text.splitlines()
    try:
        start = lines.index("```chain")
    except ValueError:
        raise ValueError("no ```chain block in %s" % path)
    rows = []
    for line in lines[start + 1:]:
        if line.strip() == "```":
            return tuple(rows)
        if not line.strip():
            continue
        ours, _, shared = line.partition("->")
        shared = shared.strip()
        occupies = () if shared == "NONE" else tuple(
            s.strip() for s in shared.split(",") if s.strip())
        rows.append((ours.strip(), occupies))
    raise ValueError("unterminated ```chain block in %s" % path)


def stage_check(name):
    """An item naming a stage the chain does not hold is a hard error, never a
    silent pass. An item naming the stage a person owns is refused by name."""
    if not name:
        return Finding("stage", NODATA, "no stage named; the item does not say "
                                        "which part of the chain it serves")
    if name in UNSERVABLE:
        return Finding("stage", FAIL,
                       "%s is taken by a person, not by this product. No item "
                       "may serve it." % name)
    if name not in STAGES:
        return Finding("stage", FAIL, "%r is not a stage of this chain. Known: %s"
                       % (name, ", ".join(SERVABLE)))
    occupies = dict(CHAIN)[name]
    return Finding("stage", PASS, "%s, standing in the shared stage %s"
                   % (name, ", ".join(occupies)))


# --------------------------------------------------------------------- seams

# BrotherMode's hollow-value rule, adopted verbatim rather than reinvented:
# an empty string, a whitespace-only string, an empty list or null all read as
# ABSENCE on the consuming side. 0 and False are real answers.
def _answered(v):
    if v is None:
        return False
    if isinstance(v, bool) or isinstance(v, int) or isinstance(v, float):
        return True
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, tuple, dict)):
        return len(v) > 0
    return True


_RANK = {FAIL: 0, NODATA: 1, PASS: 2}


def _worst(verdicts):
    return min(verdicts, key=lambda v: _RANK[v]) if verdicts else NODATA


# The five fields of the change passport, exact spelling from the producing
# side. BrotherDS reads this deposit and nothing else under .sbe/: no tasks,
# no evidence directory, no store. Reaching across the seam to fill a field is
# the failure the seam exists to prevent, and a field this deposit does not
# carry is a defect in the passport, never a licence to read execution state.
PASSPORT_FIELDS = ("whatWasDone", "whoDidIt", "whatWasRun",
                   "whatWasNotEstablished", "whereItCameFrom")


def read_passport(path=".sbe/passport.json"):
    """Consume the change passport. Absence is NO-DATA; padding is a FAIL."""
    p = _expand(path)
    if not p.exists():
        return NODATA, [Finding("passport", NODATA,
                                "no deposit at %s. Nothing was handed over." % path)]
    try:
        with open(p) as fh:
            deposit = json.load(fh)
    except Exception as exc:
        return FAIL, [Finding("passport", FAIL,
                              "deposit at %s exists and cannot be read: %s"
                              % (path, exc))]
    findings = []
    for field in PASSPORT_FIELDS:
        if field not in deposit:
            findings.append(Finding("passport." + field, NODATA,
                                    "absent. The producing side omits what it "
                                    "cannot establish honestly."))
        elif not _answered(deposit[field]):
            findings.append(Finding("passport." + field, FAIL,
                                    "present but empty. A field padded to look "
                                    "filled breaks the producing side's own rule."))
        else:
            findings.append(Finding("passport." + field, PASS, "carried"))
    return _worst([f.verdict for f in findings]), findings


# The five-item handoff package BrotherSBE contracted on 2026-08-11. The CONTENT
# is decided; no wire format was ever ratified. This reader therefore proposes a
# shape and can never certify it, which is why `ratified` caps the verdict below.
HANDOFF_ITEMS = (
    ("dataset", ("grain", "contract", "snapshot_id")),
    ("evaluation_harness", ("split",)),
    ("metric_definitions", ()),
    ("labelled_holdout", ("labelled_by", "labelled_on")),
    ("open_questions", ()),
)


def read_handoff(path=".sbe/handoff.json"):
    """Consume the BrotherSBE handoff package. The shape is PROPOSED, so the
    best verdict this reader can reach is NO-DATA until a shape is ratified."""
    p = _expand(path)
    if not p.exists():
        return NODATA, [Finding("handoff", NODATA,
                                "no package at %s. Anything not in the package "
                                "is not handed over." % path)]
    try:
        with open(p) as fh:
            pkg = json.load(fh)
    except Exception as exc:
        return FAIL, [Finding("handoff", FAIL,
                              "package at %s exists and cannot be read: %s"
                              % (path, exc))]
    findings = []
    for item, required in HANDOFF_ITEMS:
        if item not in pkg:
            findings.append(Finding("handoff." + item, NODATA, "absent"))
            continue
        # open_questions is the one field where an explicit empty list is a real
        # answer (none were open), so the hollow rule is waived for it by name.
        if item == "open_questions":
            if not isinstance(pkg[item], list):
                findings.append(Finding("handoff." + item, FAIL,
                                        "must be a list, stated rather than guessed"))
            else:
                findings.append(Finding("handoff." + item, PASS,
                                        "%d stated" % len(pkg[item])))
            continue
        if not _answered(pkg[item]):
            findings.append(Finding("handoff." + item, FAIL, "present but empty"))
            continue
        missing = [k for k in required
                   if not _answered((pkg[item] or {}).get(k)
                                    if isinstance(pkg[item], dict) else None)]
        if missing:
            findings.append(Finding("handoff." + item, NODATA,
                                    "carried, but without %s" % ", ".join(missing)))
        else:
            findings.append(Finding("handoff." + item, PASS, "carried"))
    verdict = _worst([f.verdict for f in findings])
    if verdict == PASS and not pkg.get("ratified"):
        verdict = NODATA
        findings.append(Finding("handoff.ratified", NODATA,
                                "every item is carried, but no wire format for "
                                "this package has been ratified. This reader "
                                "will not certify a contract nobody signed."))
    return verdict, findings


# -------------------------------------------------------------------- backlog

# BrotherDS's OWN queue-item vocabulary. The same four words appear in
# BrotherMode's idle checker for its own queue, and that is where the
# resemblance stops: this list is never compared to another product's enum, by
# string or otherwise. Four stage and state vocabularies already coexist across
# the triumvirate and reusing one by string-matching is how they corrupt.
ITEM_STATES = ("queued", "in_flight", "done", "blocked")

DEFAULT_QUEUE = "docs/plan/QUEUE.json"


def read_backlog(path=DEFAULT_QUEUE):
    """Every item names the stage it serves and the check that closes it.

    This is what turns the chain from a document into a control: until
    something reads a backlog and refuses an item that serves no stage of the
    chain, the stage vocabulary is a discipline rather than a rule.
    """
    p = _expand(path)
    if not p.exists():
        return NODATA, [Finding("backlog", NODATA,
                                "no queue at %s. Nothing was offered to check." % path)]
    try:
        with open(p) as fh:
            items = json.load(fh)
    except Exception as exc:
        return FAIL, [Finding("backlog", FAIL,
                              "queue at %s exists and cannot be read: %s" % (path, exc))]
    if not isinstance(items, list):
        return FAIL, [Finding("backlog", FAIL, "queue must be a list of items")]
    if not items:
        return NODATA, [Finding("backlog", NODATA, "queue is empty")]

    findings, depth = [], 0
    for i, item in enumerate(items):
        label = "backlog[%s]" % (item.get("id") if isinstance(item, dict) else i)
        if not isinstance(item, dict):
            findings.append(Finding(label, FAIL, "item is not an object"))
            continue
        state = item.get("state")
        if state not in ITEM_STATES:
            findings.append(Finding(label, FAIL, "state %r is not one of %s"
                                    % (state, ", ".join(ITEM_STATES))))
        elif state == "queued":
            depth += 1
        stage = stage_check(item.get("stage"))
        if stage.verdict != PASS:
            findings.append(Finding(label + ".stage", stage.verdict, stage.detail))
        # An item with no done-check is the item that rots. Done items are past
        # the question; blocked ones are waiting on somebody, and both still owe
        # the check that would close them.
        if not _answered(item.get("check")):
            findings.append(Finding(label, FAIL,
                                    "names no check that would close it"))
    if not findings:
        findings.append(Finding("backlog", PASS,
                                "%d item(s), every one naming a stage of this "
                                "chain and a check that closes it" % len(items)))
    findings.append(Finding("backlog.depth",
                            PASS if depth else NODATA,
                            "%d item(s) queued and unblocked" % depth))
    return _worst([f.verdict for f in findings]), findings


# ----------------------------------------------------------------------- cli

def load(path):
    with open(_expand(path)) as fh:
        return json.load(fh)


def print_chain():
    """The chain, and the shared stage each of its stages stands in."""
    print("BrotherDS occupies the shared north-star chain. It adds no stage.")
    print("")
    for name, occupies in CHAIN:
        if name in UNSERVABLE:
            where = "a person takes this; no item may serve it"
        else:
            where = "stands in: " + ", ".join(occupies)
        print("  %-18s %s" % (name, where))
    print("")
    print("%d stages, %d of them servable by an item of work."
          % (len(STAGES), len(SERVABLE)))
    return 0


def _report_seam(title, verdict, findings):
    print(title)
    print("")
    for f in findings:
        print("  " + f.line())
    print("")
    print("VERDICT %s" % verdict)
    if verdict == NODATA:
        print("        NO-DATA is not a pass and not a block. Something the "
              "seam should carry was never handed over.")
    return 1 if verdict == FAIL else 0


TEMPLATE = {
    "id": "CHANGE-ME-001",
    "statement": "State the claim in one sentence, in the words a decision maker would use.",
    "value": 0,
    "unit": "",
    "origin": "SYSTEM",
    "question": "What decision does this number serve? If none, it is not a claim, it is trivia.",
    "decision": "What changes depending on the answer?",
    "grain": "The level this number was computed at. One row per what?",
    "evidence": {
        "source": "~/path/to/your.duckdb",
        "derivations": [
            {"name": "first route to the number", "sql": "select ..."},
            {"name": "a genuinely independent second route", "sql": "select ..."},
            {"name": "context only", "sql": "select ...", "computes_value": False}
        ]
    },
    "uncertainty": {
        "kind": "NOT_ESTABLISHED",
        "why": "Say why there is no interval. If you can state one, replace this "
               "with kind, interval and method instead."
    },
    "not_established": [
        "What this claim does not settle. This list may never be empty.",
        "A reviewer reads it to know where to spend their attention."
    ]
}


def scaffold(claim_id, dest):
    """Write a claim skeleton. The comments live in the placeholder text itself,
    because a template whose guidance sits in a separate document gets filled in
    without the guidance."""
    t = dict(TEMPLATE)
    t["id"] = claim_id
    p = _expand(dest)
    if p.exists():
        print("refusing to overwrite %s" % p)
        return 1
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as fh:
        json.dump(t, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote %s" % p)
    print("Fill it in, then: python3 bds.py check %s" % dest)
    print("")
    print("The five origins, pick the honest one:")
    for k, v in sorted(ORIGINS.items()):
        print("  %-12s %s" % (k, v))
    return 0


# The fields a claim cannot be checked without, per gates G1, G2, G3 and G9.
# `author` refuses to write a file missing any of these, instead of writing a
# claim that then hits its first FAIL only when someone runs `check` on it.
REQUIRED_FIELDS = ("id", "statement", "value", "unit", "origin",
                   "question", "decision", "grain")


def _parse_author_input(text):
    """key=value lines, stdlib only, no JSON typed by hand.

    A dotted key (uncertainty.kind) nests one level. The key `not_established`
    may repeat; each line becomes one list entry. The key `evidence.derivation`
    may repeat too, each line shaped `name|sql` or `name|sql|context` (the
    third field marks a supporting query that does not compute the value).
    Blank lines and lines starting with # are skipped.
    """
    claim = {}
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError("line %d has no '=': %r" % (lineno, raw))
        key, value = (part.strip() for part in line.split("=", 1))
        if not key:
            raise ValueError("line %d has an empty key: %r" % (lineno, raw))
        if key == "not_established":
            claim.setdefault("not_established", []).append(value)
        elif key == "evidence.derivation":
            parts = [p.strip() for p in value.split("|")]
            if len(parts) < 2 or not parts[0] or not parts[1]:
                raise ValueError("line %d: evidence.derivation needs "
                                 "name|sql, got %r" % (lineno, raw))
            d = {"name": parts[0], "sql": parts[1]}
            if len(parts) > 2 and parts[2].lower() == "context":
                d["computes_value"] = False
            claim.setdefault("evidence", {}).setdefault("derivations", []).append(d)
        elif "." in key:
            # Nests to any depth (evidence.comparison.protocol.provider=...),
            # not just one level, because the comparison block needs three.
            parts = key.split(".")
            node = claim
            for part in parts[:-1]:
                if not isinstance(node.get(part), dict):
                    node[part] = {}
                node = node[part]
            node[parts[-1]] = value
        else:
            claim[key] = value
    return claim


def _author_errors(claim):
    """Validate before writing. Nothing here is silently defaulted: a missing
    or malformed field is named and the write is refused."""
    errors = []
    for field in REQUIRED_FIELDS:
        v = claim.get(field)
        if v is None or (isinstance(v, str) and not v.strip()):
            errors.append("missing required field: %s" % field)

    if claim.get("value") is not None:
        try:
            f = float(claim["value"])
        except (TypeError, ValueError):
            errors.append("value must be numeric, got %r" % claim["value"])
        else:
            claim["value"] = int(f) if f == int(f) else f

    origin = claim.get("origin")
    if origin is not None and origin not in ORIGINS:
        errors.append("origin must be one of %s, got %r"
                      % (", ".join(sorted(ORIGINS)), origin))

    # The dual-run comparison, if the author chose to authored one. Missing
    # incumbent/incumbent_value/tolerance/protocol fields are not refused here:
    # `check` reports those as NO-DATA by name, same as any other origin's
    # protocol. Only the enum and the numeric shape are hard errors, matching
    # how origin and value are treated above.
    comp = (claim.get("evidence") or {}).get("comparison")
    if comp:
        cls = comp.get("class")
        if cls is not None and cls not in ("THIRD_PARTY", "ELICITED"):
            errors.append("evidence.comparison.class must be THIRD_PARTY or "
                          "ELICITED, got %r" % cls)
        for f in ("incumbent_value", "tolerance"):
            if comp.get(f) is not None:
                try:
                    v = float(comp[f])
                except (TypeError, ValueError):
                    errors.append("evidence.comparison.%s must be numeric, "
                                  "got %r" % (f, comp[f]))
                else:
                    comp[f] = int(v) if v == int(v) else v

    ne = claim.get("not_established")
    if ne is None:
        errors.append("missing required field: not_established (repeat "
                      "'not_established=...' at least once)")
    elif not isinstance(ne, list) or not ne:
        errors.append("not_established must be a non-empty list")

    u = claim.get("uncertainty")
    if not isinstance(u, dict) or "kind" not in u:
        errors.append("missing required field: uncertainty.kind (plus "
                      "uncertainty.why, or uncertainty.interval and "
                      "uncertainty.method)")
    elif u["kind"] == "NOT_ESTABLISHED":
        if not u.get("why"):
            errors.append("uncertainty.kind=NOT_ESTABLISHED requires uncertainty.why")
    elif "interval" not in u or "method" not in u:
        errors.append("uncertainty.kind=%s requires uncertainty.interval "
                      "and uncertainty.method" % u["kind"])
    elif isinstance(u["interval"], str):
        try:
            lo, hi = (float(x) for x in u["interval"].split(","))
        except ValueError:
            errors.append("uncertainty.interval must be 'lo,hi', got %r"
                          % u["interval"])
        else:
            u["interval"] = [lo, hi]

    return errors


def author(dest, stdin_text):
    """Write a claim from key=value lines on stdin: authoring a claim as a
    side effect of doing the analysis, never by hand-editing JSON."""
    p = _expand(dest)
    if p.exists():
        print("refusing to overwrite %s" % p)
        return 1
    try:
        claim = _parse_author_input(stdin_text)
    except ValueError as exc:
        print("REFUSED: %s" % exc)
        return 2

    errors = _author_errors(claim)
    if errors:
        print("REFUSED, %d problem(s), nothing written:" % len(errors))
        for e in errors:
            print("  - %s" % e)
        return 2

    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as fh:
        json.dump(claim, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote %s" % p)
    print("")

    registry = os.path.join(os.path.dirname(_expand(dest)) or ".", DEFAULT_REGISTRY)
    verdict, findings, _ = check(claim, registry)
    print_check(claim, verdict, findings)
    return 1 if verdict == FAIL else 0


def score(claim, path, actual, observed_by, observed_on):
    """Let reality grade the claim.

    A claim whose uncertainty was NOT_ESTABLISHED can never be HELD or MISSED,
    only UNSCOREABLE. That is deliberate: the north star counts claims that
    stated what they expected and were right. Declining to state an interval
    keeps you out of the denominator, and out of the numerator too.
    """
    u = claim.get("uncertainty") or {}
    recorded = claim.get("value")
    err = None
    if recorded is not None:
        try:
            err = float(actual) - float(recorded)
        except (TypeError, ValueError):
            err = None

    if u.get("kind") == "NOT_ESTABLISHED" or "interval" not in u:
        state = "UNSCOREABLE"
        why = ("no interval was stated, so there is nothing for reality to fall "
               "inside or outside. This claim cannot count toward the verified "
               "claim rate.")
    else:
        lo, hi = u["interval"][0], u["interval"][1]
        inside = float(lo) <= float(actual) <= float(hi)
        state = "HELD" if inside else "MISSED"
        why = "actual %s %s the stated interval [%s, %s]" % (
            _fmt(actual), "fell inside" if inside else "fell outside",
            _fmt(lo), _fmt(hi))

    claim["outcome"] = {"actual": actual, "observed_by": observed_by,
                        "observed_on": observed_on, "state": state,
                        "why": why, "error": err}
    with open(_expand(path), "w") as fh:
        json.dump(claim, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print("claim   %s" % claim.get("id"))
    print("        %s" % claim.get("statement"))
    print("")
    print("  recorded  %s" % _fmt(recorded))
    print("  actual    %s" % _fmt(actual))
    if err is not None:
        print("  error     %s" % _fmt(err))
    print("  observed  %s by %s" % (observed_on, observed_by))
    print("")
    print("OUTCOME %s" % state)
    print("        %s" % why)
    return 0


def ledger(directory):
    """The north star, computed. Verified claim rate is held over resolved,
    where resolved means the claim stated an interval AND an outcome arrived."""
    d = _expand(directory)
    rows, counts = [], {"HELD": 0, "MISSED": 0, "UNSCOREABLE": 0, "OPEN": 0}
    unreadable = []
    for p in sorted(d.glob("*.json")):
        if p.name == DEFAULT_REGISTRY:
            continue
        try:
            with open(p) as fh:
                c = json.load(fh)
        except (ValueError, IOError) as exc:
            # Never skip a claim silently. A rate computed over an unstated
            # subset is the exact failure this product refuses, and it would be
            # sitting inside the function that computes the north star.
            unreadable.append((p.name, "%s: %s" % (type(exc).__name__, exc)))
            continue
        o = c.get("outcome") or {}
        state = o.get("state", "OPEN")
        counts[state] = counts.get(state, 0) + 1
        rows.append((c.get("id", p.stem), state, c.get("statement", "")[:64]))

    print("%-12s %-12s %s" % ("CLAIM", "OUTCOME", "STATEMENT"))
    for r in rows:
        print("%-12s %-12s %s" % r)
    print("")
    if unreadable:
        print("UNREADABLE, excluded from every count below:")
        for name, why in unreadable:
            print("  %-28s %s" % (name, why))
        print("  The rate that follows is computed over %d of %d claim files. "
              "Fix these before trusting it." % (len(rows), len(rows) + len(unreadable)))
        print("")
    resolved = counts["HELD"] + counts["MISSED"]
    print("open %d, unscoreable %d, resolved %d"
          % (counts["OPEN"], counts["UNSCOREABLE"], resolved))
    if resolved == 0:
        print("")
        print("VERIFIED CLAIM RATE  NO-DATA")
        print("        No claim has both stated an interval and been scored "
              "against a real outcome. The north star has no numerator and no")
        print("        denominator yet. This is the honest state, not a zero.")
        return 0
    rate = counts["HELD"] / float(resolved)
    print("")
    print("VERIFIED CLAIM RATE  %.0f%%  (%d held of %d resolved)"
          % (100 * rate, counts["HELD"], resolved))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]

    if cmd == "selftest":
        return selftest()

    if cmd == "new":
        if len(argv) < 3:
            print("usage: bds.py new <CLAIM-ID> [path.json]")
            return 2
        claim_id = argv[2]
        dest = argv[3] if len(argv) > 3 else "claims/%s.json" % claim_id.lower()
        return scaffold(claim_id, dest)

    if cmd == "author":
        if len(argv) < 3:
            print("usage: python3 bds.py author <dest.json>   "
                  "(reads key=value lines from stdin)")
            return 2
        return author(argv[2], sys.stdin.read())

    if cmd == "ledger":
        return ledger(argv[2] if len(argv) > 2 else "claims")

    if cmd == "chain":
        return print_chain()

    if cmd == "stage":
        f = stage_check(argv[2] if len(argv) > 2 else "")
        print(f.line())
        return 1 if f.verdict == FAIL else 0

    if cmd == "passport":
        return _report_seam("CHANGE PASSPORT, consumed from BrotherMode",
                            *read_passport(argv[2] if len(argv) > 2
                                           else ".sbe/passport.json"))

    if cmd == "handoff":
        return _report_seam("HANDOFF PACKAGE, consumed from BrotherSBE",
                            *read_handoff(argv[2] if len(argv) > 2
                                          else ".sbe/handoff.json"))

    if cmd == "backlog":
        return _report_seam("BACKLOG, every item against the chain",
                            *read_backlog(argv[2] if len(argv) > 2
                                          else DEFAULT_QUEUE))

    if len(argv) < 3:
        print("usage: bds.py %s <claim.json>" % cmd)
        return 2
    path = argv[2]
    claim = load(path)

    if cmd == "register":
        return register_definition(claim, os.path.join(
            os.path.dirname(_expand(path)) or ".", DEFAULT_REGISTRY))

    if cmd == "score":
        rest = argv[3:]
        if not rest:
            print("usage: bds.py score <claim.json> <actual> [observed_by] [observed_on]")
            return 2
        actual = float(rest[0])
        by = rest[1] if len(rest) > 1 else "not stated"
        on = rest[2] if len(rest) > 2 else "not stated"
        return score(claim, path, actual, by, on)

    registry = os.path.join(os.path.dirname(_expand(path)) or ".", DEFAULT_REGISTRY)
    verdict, findings, _ = check(claim, registry)

    if cmd == "check":
        print_check(claim, verdict, findings)
        return 1 if verdict == FAIL else 0

    if cmd == "receipt":
        out = receipt(claim, verdict, findings)
        dest = argv[3] if len(argv) > 3 else None
        if dest:
            with open(_expand(dest), "w") as fh:
                fh.write(out + "\n")
            print("wrote %s" % dest)
        else:
            print(out)
        return 0

    print("unknown command %r" % cmd)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
