#!/usr/bin/env python3
"""
repair_context.py
=================
Given a localized action, assemble the evidence and constraints the re-invoked
stage gets — and check, offline and for free, whether that evidence could have
supported a correct repair at all.

    from prep_utils.repair_context import build_context, coverage
    text = build_context("revise_relational_plan", diag=..., plan=..., link=...,
                         chains=..., tried=[...])

    python3 repair_context.py --inter <intermedidate_results/<bm>> --coverage

TWO RULES THAT SHAPE EVERY BLOCK
--------------------------------
1. Constraints are NEGATIVE or CONDITIONAL, never prescriptive. "Declare an edge
   between table_1 and table_2; these column pairs are known to join" preserves
   the stage's judgement. "Set the edge to code<->set_code" turns it into an
   executor — and would be wrong here anyway: on bird_058b8e3b `code<->set_code`
   and `keyruneCode<->set_code` both have containment 1.00, so the structure
   cannot choose and only the question can.

2. Failed directions are mandatory, not optional. Without them a loop that
   rolled back re-proposes the same repair, and the round budget is spent
   oscillating.

WHAT EACH ACTION IS TOLD, AND WHY
---------------------------------
revise_table (re-runs schema linking, then everything downstream)
    * the full candidate pool with the RECOVERED headers schema linking used,
      selected ones marked. Without the pool "a table is missing" is
      unfalsifiable — the stage cannot name a replacement.
    * question literals present in NO selected table. The only positive evidence
      that a needed table is absent.
    * produced columns that look like foreign keys and resolve against a
      NON-selected candidate. This is the actionable form: it names the table.
    * previously selected table sets that failed.

revise_relational_plan (re-runs the plan, then pipeline synthesis)
    * declared columns no operator chain could build (A1_unmet). The plan is
      about to be rebuilt and must not ask for them again unchanged.
    * per declared edge: measured containment, and the ranked column pairs that
      DO join, computed on the produced tables and on the raw tables. C4 already
      computes these and nothing consumed them until now.
    * what the synthesizer demonstrably CAN produce, from the terminal candidate
      pool. Synthesis re-runs after this stage, so a plan that declares
      unbuildable columns fails the same way twice.
    * previously declared edges with their measured containment.

revise_pipeline (re-runs synthesis for named tables only)
    * which tables are at fault, and which declared columns they missed.
    * the chains already tried for those tables, with the columns each produced,
      so the search does not re-derive them. The pool is small — 203 of 302
      tables finished with a single distinct candidate — so "what was tried" is
      short and worth stating exactly.
    * whether the needed values are visible in the raw table at all, which
      separates "the search failed" from "the plan asked for something the data
      cannot supply".

TESTING THE EVIDENCE, CHEAPLY, BEFORE SPENDING ON RUNS
------------------------------------------------------
Repair success is bounded above by evidence COVERAGE: if the correct answer is
not in the evidence, no model can pick it, and an A/B on repair outcomes would
be measuring the wrong thing. `coverage()` answers that offline against gold,
with no LLM call:

    revise_table            is every gold table in the candidate pool?
    revise_relational_plan  is the gold join key pair among the ranked pairs
                            offered for that edge?
    revise_pipeline         do the raw tables visibly contain the values of the
                            columns the chain failed to produce?

Coverage is a ceiling, not a prediction — it says a correct repair was
*available*, never that the stage will find it. Run it first: a block whose
coverage is low is a block to fix before any repair experiment is worth its cost.
"""
from __future__ import annotations

import os
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd

ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
for _p in (str(ROOT), str(ROOT / "construct_training_data")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import diagnose as D                                               # noqa: E402

ACTIONS = ("revise_table", "revise_relational_plan", "revise_pipeline")


# --------------------------------------------------------------------------- #
# shared blocks
# --------------------------------------------------------------------------- #

def _col_values(df: "pd.DataFrame", col: Any, n: int = 4, width: int = 22) -> str:
    try:
        v = list(dict.fromkeys(df[col].dropna().astype(str).tolist()[:400]))[:n]
    except Exception:
        return ""
    return ", ".join(x[:width] + ("…" if len(x) > width else "") for x in v)


def _candidate_tables(link: Dict[str, Any], bench_dir: Optional[Path] = None,
                      limit: int = 24, val_cols: int = 8,
                      max_dropped: int = 60) -> str:
    """The pool, with SAMPLE VALUES — not headers alone.

    Headers alone are close to useless on this benchmark, which is the whole
    reason `schema_profiler` exists. Three of the failing cases make the point:

        bird_2d3826a9_input_1   columns ['id','variable','value'] — a transposed
                                table whose `id` column holds the original FIELD
                                NAMES ('birthday','first_name','height'). Nothing
                                in the header says it is about players.
        bird_6ca266b1_input_0   columns ['fz_id','jd_lx'] — obfuscated, but the
                                values 'TR420_6_10=' end in '=' for a double bond,
                                which is exactly what the question asks about.
        bird_496c969d_input_1   44 columns of lab codes, recovered to 21 names
                                that drop the one the question names.

    In each case the deciding evidence is in the cells. Listing only column names
    asks the model to choose between tables it cannot read, and it reliably picks
    the one with the friendliest NAME instead — a clean DB table like
    `european_football_2_Team.pkl` over the transposed file that actually holds
    the ratings. 14 of 24 failures are exactly that substitution.
    """
    cands = link.get("candidates") or []
    if not cands:
        return f"  (pool not recorded; currently selected: {link.get('selected_tables')})"
    sel = set(link.get("selected_tables") or [])
    out = []
    for c in cands:
        f, cols = c.get("file_name"), c.get("headers") or []
        extra = f" ...+{len(cols) - limit}" if len(cols) > limit else ""
        out.append(f"  [{'SELECTED' if f in sel else 'not selected'}] {f}\n"
                   f"      columns: {cols[:limit]}{extra}")
        if bench_dir is None:
            continue
        p = Path(bench_dir) / str(f)
        if not p.exists():
            continue
        try:
            df = pd.read_pickle(p)
        except Exception:
            continue
        # Only the names recovery LOST, not the whole raw header row. Recovery
        # renames as well as drops, so echoing every raw name would repeat ~half
        # the list under a second heading; the first pass paid for that in
        # attention and lost 4 correctly-selected tables to it.
        seen = {re.sub(r"[^a-z0-9]", "", str(x).lower()) for x in cols}
        dropped = [str(x) for x in df.columns
                   if re.sub(r"[^a-z0-9]", "", str(x).lower()) not in seen]
        if dropped and len(cols) < df.shape[1]:
            # The whole list, not a preview. Truncating at 24 is what kept
            # bird_496c969d broken: its question asks about `anti-SSA`, `SSA`
            # sits 30th among the names recovery dropped, and the cut fell just
            # short of it. These lists are only emitted for tables where
            # recovery lost columns, so the cost is bounded and paid exactly
            # where the deciding name is likely to be hiding.
            out.append(f"      raw column names recovery did NOT keep "
                       f"({len(cols)} names returned for {df.shape[1]} columns): "
                       f"{dropped[:max_dropped]}"
                       + (f" ...+{len(dropped) - max_dropped} more"
                          if len(dropped) > max_dropped else ""))
        out.append(f"      shape: {df.shape}")
        for rc in list(df.columns)[:val_cols]:
            out.append(f"        {str(rc)[:28]} = {_col_values(df, rc) or '(empty)'}")
        if df.shape[1] > val_cols:
            out.append(f"        ...+{df.shape[1] - val_cols} more columns")
    return "\n".join(out)


def _tried(tried: Sequence[Dict[str, Any]]) -> str:
    """Failed directions. Their absence is what makes a loop oscillate."""
    if not tried:
        return "  (nothing tried yet)"
    return "\n".join(
        f"  - {t.get('action')}: {t.get('what')}"
        + (f"  -> measured {t['measured']}" if t.get("measured") else "")
        + "  (rolled back, do not repeat)"
        for t in tried)


def _viable_pairs(diag: Dict[str, Any]) -> Dict[str, List[dict]]:
    return {e.get("edge"): ((e.get("C4_ambiguity") or {}).get("pairs") or [])
            for e in (diag.get("C_join_health") or {}).get("edges", [])}


def raw_key_pairs(raw_tables: Dict[str, pd.DataFrame], left: str, right: str,
                  min_card: int = 5, thresh: float = 0.5) -> List[dict]:
    """Ranked joinable column pairs on the RAW tables.

    C4 runs on the PRODUCED tables, which is the right input when the pipeline
    is at fault. When the PLAN is at fault the produced tables may be shaped
    wrongly, and the pairs computed on them inherit that. Same routine, raw
    input — the plan is being rewritten against the sources, so that is what it
    should see.
    """
    ldf, rdf = raw_tables.get(left), raw_tables.get(right)
    if ldf is None or rdf is None:
        return []
    return (D._key_ambiguity(ldf, rdf, min_card, thresh) or {}).get("pairs", [])


# --------------------------------------------------------------------------- #
# per-action context
# --------------------------------------------------------------------------- #

def _fmt_plan(plan: Dict[str, Any], limit: int = 16) -> str:
    """The declared target schema and edges, as the plan stated them."""
    out = []
    for t in plan.get("gold_tables") or []:
        sql = t.get("create_table_sql") or ""
        # Strip the PRIMARY KEY clause before harvesting backticks, or every key
        # column is listed twice.
        body = re.sub(r"PRIMARY\s+KEY\s*\([^)]*\)", "", sql, flags=re.I)
        cols = re.findall(r"`([^`]+)`", body)
        extra = f" ...+{len(cols) - limit}" if len(cols) > limit else ""
        out.append(f"  {t.get('logical_table')} (from {t.get('input_file')})\n"
                   f"    declared columns: {cols[:limit]}{extra}")
    edges = [f"{e.get('left_table')}.{e.get('left_on')} <-> "
             f"{e.get('right_table')}.{e.get('right_on')}"
             for e in (plan.get("join_edges") or [])]
    out.append(f"  declared join edges: {edges or 'none'}")
    return "\n".join(out)


def _sample_rows(df: "pd.DataFrame", rows: int = 3, cols: int = 12,
                 width: int = 20) -> str:
    """A few rows of a materialised table, narrow enough to read."""
    if df is None or len(df) == 0:
        return "      (empty)"
    sub = df.iloc[:rows, :cols]
    head = " | ".join(str(c)[:width] for c in sub.columns)
    extra = f"   ...+{df.shape[1] - cols} more columns" if df.shape[1] > cols else ""
    lines = [f"      {head}{extra}"]
    for _, r in sub.iterrows():
        lines.append("      " + " | ".join(
            ("" if pd.isna(v) else str(v))[:width] for v in r))
    return "\n".join(lines)


def _materialized(produced: Dict[str, Any], diag: Dict[str, Any]) -> str:
    out = []
    per = (diag.get("A_plan_fulfilment") or {}).get("per_table") or {}
    for lt, df in (produced or {}).items():
        unmet = (per.get(lt) or {}).get("A1_unmet_declared_columns") or []
        out.append(f"    {lt}  shape={getattr(df, 'shape', None)}"
                   + (f"   declared but not produced: {unmet}" if unmet else ""))
        out.append(_sample_rows(df))
    return "\n".join(out) or "    (nothing was materialised)"


def _join_keys(diag: Dict[str, Any]) -> str:
    edges = (diag.get("C_join_health") or {}).get("edges", [])
    if not edges:
        return "    (the plan declared no join edge at all)"
    return "\n".join(
        f"    {e.get('edge')}   containment L->R {e.get('C2_containment_l_in_r')}"
        f"  R->L {e.get('C2_containment_r_in_l')}   {e.get('verdict')}"
        for e in edges)


def _symptom(diag: Dict[str, Any], produced: Dict[str, Any]) -> str:
    """A factual statement of what the current selection led to.

    Deliberately NOT a diagnosis of which table to add. An earlier version of
    this block asserted "column X resolves into non-selected table Y", derived
    from value containment. It fired on 19 of 32 tasks, named the actually
    missing table in 8, and its firing did not correlate with a successful
    repair (1 of those 8 repaired, against 4 of 11 where it named the wrong
    table). Integer id columns contain one another all over this benchmark, so
    the rule mostly produced confident wrong pointers. What survives here is the
    observable consequence; the choice is left to the model.
    """
    bits = []
    per = (diag.get("A_plan_fulfilment") or {}).get("per_table") or {}
    unmet = sorted({c for v in per.values()
                    for c in (v.get("A1_unmet_declared_columns") or [])})
    if unmet:
        bits.append(f"columns the plan declared but nothing could build: {unmet[:8]}")
    edges = (diag.get("C_join_health") or {}).get("edges", [])
    if not edges and len(produced or {}) <= 1:
        bits.append("only one table was materialised and no join was possible, "
                    "so nothing could be related to anything else")
    weak = [e.get("edge") for e in edges
            if max(e.get("C2_containment_l_in_r") or 0,
                   e.get("C2_containment_r_in_l") or 0) < 0.5]
    if weak:
        bits.append(f"declared edges whose keys barely overlap: {weak}")
    t = diag.get("T_table_selection") or {}
    if t.get("T2_literals_absent_from_all_values"):
        bits.append("values named in the question appear in none of the selected "
                    f"tables: {t['T2_literals_absent_from_all_values'][:6]}")
    return "\n".join(f"  - {b}" for b in bits) or \
        "  - the tables were materialised but the result did not answer the question"


def _subquestion_audit(link: Dict[str, Any], bench_dir: Optional[Path],
                       n_cols: int = 6) -> str:
    """The selector's OWN decomposition, put next to what each table really holds.

    Schema linking already emits, per selected table, the part of the question it
    is supposed to answer. On the failures that decomposition is consistently
    RIGHT — bird_3f3aba77 correctly asked for "payment amounts made by those
    students" — and what goes wrong is the binding: it hung that requirement on
    `student_club_income.pkl`, whose values are `source = Dues / Fundraising /
    School Appropriation`, i.e. money coming IN. The requirement and the refuting
    evidence were both already in our artefacts, on opposite sides of a join
    nobody made.

    So this block asks nothing new of the model. It restates what the model
    itself claimed each table would supply, and shows the cells that table
    actually produced, so the claim can be checked rather than assumed.
    """
    subq = link.get("subquestions") or {}
    if not subq:
        return "  (the selector recorded no per-table subquestions)"
    out = []
    for f, qs in subq.items():
        out.append(f"  {f}")
        for q in list(qs)[:3]:
            out.append(f"      claimed to answer: {q}")
        p = Path(bench_dir) / str(f) if bench_dir else None
        if p is None or not p.exists():
            continue
        try:
            df = pd.read_pickle(p)
        except Exception:
            continue
        out.append(f"      what it actually holds ({df.shape[0]}x{df.shape[1]}):")
        for c in list(df.columns)[:n_cols]:
            out.append(f"        {str(c)[:26]} = {_col_values(df, c, n=3) or '(empty)'}")
    return "\n".join(out)


def _ctx_revise_table(diag, plan, link, chains, task_id, raw_tables,
                      bench_dir=None, produced=None) -> str:
    return f"""The table selection below was judged wrong: the tables that were
built from it cannot supply what the question asks for, or cannot be joined so
as to answer it. Check each claim you made against what the table actually
contains, then choose again from the full candidate pool.

CURRENT SELECTION
  {link.get('selected_tables')}

WHAT YOU SAID EACH SELECTED TABLE WOULD ANSWER, AND WHAT IT ACTUALLY CONTAINS
{_subquestion_audit(link, bench_dir)}

RELATIONAL PLAN BUILT ON IT
{_fmt_plan(plan)}

MATERIALISED TABLES (what the pipeline actually produced)
{_materialized(produced or {}, diag)}

JOIN KEYS THAT RESULTED
{_join_keys(diag)}

WHAT THIS SELECTION LED TO
{_symptom(diag, produced or {})}

FULL CANDIDATE POOL (choose from these; `columns` are the recovered names, and
where recovery returned fewer names than the table has columns the names it lost
are listed separately — a column the question asks about may appear only there)
{_candidate_tables(link, bench_dir)}

HARD CONSTRAINTS
  - keep the tables already carrying values the question needs
  - a table only satisfies a requirement if its CELLS show it; a plausible column
    name is not evidence, and a plausible file name is not evidence
  - the new selection must make the missing information above obtainable"""


def _declared_by_source(plan: Dict[str, Any]) -> str:
    """The declared schema keyed by SOURCE FILE, with the logical name secondary.

    Not by `logical_table`. Our plan and the gold plan disagree on the numbering
    on 6 of the 12 tasks in this class, so anything that reasons about "table_1"
    across two plans is comparing different tables. Keying on the file removes
    the trap from the prompt itself.
    """
    out = []
    for t in plan.get("gold_tables") or []:
        sql = t.get("create_table_sql") or ""
        body = re.sub(r"PRIMARY\s+KEY\s*\([^)]*\)", "", sql, flags=re.I)
        m = re.search(r"PRIMARY\s+KEY\s*\(([^)]*)\)", sql, flags=re.I)
        pk = [x.strip(' `"') for x in m.group(1).split(",")] if m else []
        out.append(f"  {t.get('input_file')}   (called {t.get('logical_table')} in this plan)\n"
                   f"      declared columns: {re.findall(r'`([^`]+)`', body)}\n"
                   f"      declared primary key: {pk or 'none'}")
    return "\n".join(out) or "  (the plan declares no table)"


def _source_contents(plan: Dict[str, Any], raw_tables: Dict[str, Any],
                     bench_dir: Optional[Path], n_cols: int = 16) -> str:
    """What each SOURCE table actually holds, so "can any column carry X?" is
    checkable rather than guessed."""
    out = []
    for t in plan.get("gold_tables") or []:
        lt, f = t.get("logical_table"), t.get("input_file")
        df = (raw_tables or {}).get(lt)
        if df is None and bench_dir and f:
            p = Path(bench_dir) / f
            if p.exists():
                try:
                    df = pd.read_pickle(p)
                except Exception:
                    df = None
        if df is None:
            continue
        out.append(f"  {f}  ({df.shape[0]} rows x {df.shape[1]} columns)")
        for c in list(df.columns)[:n_cols]:
            out.append(f"      {str(c)[:28]:<28} = {_col_values(df, c, n=4) or '(empty)'}")
        if df.shape[1] > n_cols:
            out.append(f"      ...+{df.shape[1] - n_cols} more columns")
    return "\n".join(out) or "  (no source table could be read)"


def _plan_cols_by_lt(plan: Dict[str, Any]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for t in plan.get("gold_tables") or []:
        sql = t.get("create_table_sql") or ""
        body = re.sub(r"PRIMARY\s+KEY\s*\([^)]*\)", "", sql, flags=re.I)
        out[t.get("logical_table")] = re.findall(r"`([^`]+)`", body)
    return out


def _q_tokens(question: str) -> set:
    """Plain tokens from the question. No hand-written expansions.

    An earlier version expanded specific words — `where` also matched
    `building`/`room`, `frequency` also matched `freq`, `who` also matched
    `player`. Every one of those expansions names a column that appears in the 12
    tasks this action is scored on (`building`/`room` in bird_474ecddc, `freq_part*`
    in bird_94ff6607, `player_name` in bird_83d15f3a). A hint list written from the
    evaluation set measures the list, not the method.
    """
    raw = re.sub(r"([a-z])([A-Z])", r"\1 \2", question or "")
    return {t for t in re.split(r"[^A-Za-z0-9]+", raw.lower()) if len(t) > 2}


def _tok_overlap(a: str, toks: set) -> bool:
    parts = set(re.split(r"[^a-z0-9]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", str(a)).lower()))
    parts = {p for p in parts if len(p) > 2}
    return bool(parts & toks)


def _plan_repair_brief(question: str, plan: Dict[str, Any],
                       raw_tables: Dict[str, Any],
                       diag: Dict[str, Any]) -> str:
    """Gold-free intent hints for revising the relational plan.

    This does not compare to gold. It asks whether the current declared schema has
    a column that can carry each requirement in the form the question needs.
    """
    cols_by_lt = _plan_cols_by_lt(plan)
    qtok = _q_tokens(question)
    out: List[str] = []

    for t in plan.get("gold_tables") or []:
        lt, f = t.get("logical_table"), t.get("input_file")
        declared = cols_by_lt.get(lt, [])
        dcf = {D._cf(c) for c in declared}
        raw = raw_tables.get(lt)
        if raw is None:
            continue
        raw_cols = [str(c) for c in raw.columns]
        raw_cf = {D._cf(c): str(c) for c in raw_cols}

        # A whole semantic value is often scored as ONE value domain, so a plan
        # that declares only its pieces can satisfy every name while carrying none
        # of the required domain.
        #
        # Derived from the data, not from a list. The previous version hard-coded
        # `{year, month, day}`, the candidate whole-column names
        # `{date, datereceived, receiveddate, eventdate}`, and the prefixes
        # `uuidpart` / `freqpart`. `date_received` is bird_2bc5bfed's gold column
        # and `uuid_part*` is bird_ea61a71a's declaration — i.e. the rules named
        # the answers of the tasks being scored, and `carrier_fragmented` then
        # fired on exactly 1 of 12 (that one task) and 0 of 67 healthy ones.
        # A rule that fires on one evaluation case is a memorised case.
        #
        # The general form: a SOURCE column whose name is a prefix of two or more
        # DECLARED column names has been split by the plan.
        for rc in raw_cols:
            stem = D._cf(rc)
            if len(stem) < 3 or stem in dcf:
                continue
            parts = [c for c in declared
                     if D._cf(c) != stem and D._cf(c).startswith(stem)]
            if len(parts) >= 2:
                out.append(
                    f"  - carrier_fragmented on {f}: the source column `{rc}` is "
                    f"declared only as the pieces {parts[:6]}. If the question or a "
                    f"join needs the complete value, declare `{rc}` itself; if it "
                    "needs only a piece, leave this alone.")

        # Question-named source fields that are absent from the plan.
        missing_named = []
        for c in raw_cols:
            n = D._cf(c)
            if n in dcf:
                continue
            if _tok_overlap(c, qtok):
                missing_named.append(c)
        if missing_named:
            out.append(
                f"  - carrier_missing on {f}: question terms match source columns "
                f"{missing_named[:8]}, but these are not declared. Allowed edit: add "
                "only the columns needed by the question, not the whole source schema.")

    # Edge repair: show raw-level alternatives, not just produced-level pairs.
    for e in (plan.get("join_edges") or []):
        lt, rt = e.get("left_table"), e.get("right_table")
        if not lt or not rt:
            continue
        pairs = raw_key_pairs(raw_tables, lt, rt, min_card=5, thresh=0.5)
        current = f"{lt}.{e.get('left_on')} <-> {rt}.{e.get('right_on')}"
        if pairs:
            out.append(
                f"  - join_key_candidates for declared edge {current}: raw tables "
                f"also contain joinable pairs {pairs[:6]}. Allowed edit: change "
                "the join key only if the current key cannot carry the relationship "
                "the question needs.")

    if not (plan.get("join_edges") or []) and len(raw_tables) >= 2:
        lts = list(raw_tables)[:4]
        for i, lt in enumerate(lts):
            for rt in lts[i + 1:]:
                pairs = raw_key_pairs(raw_tables, lt, rt, min_card=5, thresh=0.7)
                if pairs:
                    out.append(
                        f"  - join_edge_missing candidate: {lt} and {rt} have raw "
                        f"joinable pairs {pairs[:4]}. Allowed edit: add an edge only "
                        "if the question requires relating these two source files.")

    if not out:
        return ("  (no focused carrier/key defect detected; apply THE TEST below. "
                "If every question requirement has a declared value carrier, return "
                "plan_at_fault=false.)")
    return "\n".join(out)


def _ctx_revise_plan(diag, plan, link, chains, task_id, raw_tables, bench_dir=None, produced=None) -> str:
    """Evidence for rewriting a relational plan.

    WHAT THIS PROMPT DELIBERATELY DOES NOT SAY
    ------------------------------------------
    Comparing our plans against the gold plans on nl2sql-bird dev, four obvious
    structural differences turn out to be worthless as repair signals, because
    they occur just as often in the tasks that came out CORRECT:

        difference                              revise_plan   no_revision_needed
        under-declaration (a gold column absent)   0.92             0.88
        primary key differs                        0.58             0.55
        over-decomposition (1 gold col -> N)       0.25             0.31
        table set differs                          0.17             0.11

    Telling the model "your plan is missing columns" is therefore true of 88% of
    the plans that worked, and sends it chasing harmless differences. The block
    below never says it.

    The one refinement that does separate the classes is whether the omitted
    column is one the QUESTION names: 0.583 on this class against 0.309 on the
    rest (OR 3.14, Fisher p = 0.101, n = 12 — directional, not significant). That
    is what "THE TEST" encodes, and it is also why "no change" is an allowed
    answer: 5 of the 12 have no visible defect at all, and a repair action that
    must always change something will damage plans that were already fine.
    """
    a = diag.get("A_plan_fulfilment") or {}
    per = a.get("per_table") or {}
    unmet = {lt: v.get("A1_unmet_declared_columns") or []
             for lt, v in per.items() if v.get("A1_unmet_declared_columns")}
    pairs = _viable_pairs(diag)

    edges = []
    for e in (diag.get("C_join_health") or {}).get("edges", []):
        name = e.get("edge")
        ranked = pairs.get(name) or []
        edges.append(
            f"  declared: {name}\n"
            f"    measured containment  L->R {e.get('C2_containment_l_in_r')}  "
            f"R->L {e.get('C2_containment_r_in_l')}\n"
            f"    verdict: {e.get('verdict')}\n"
            f"    column pairs that DO join (produced tables, by containment):\n"
            + ("\n".join(f"      {p['pair']}  {p['containment']}" for p in ranked[:6])
               or "      (none above threshold)"))

    buildable = []
    for lt in (plan.get("gold_tables") or []):
        name = lt.get("logical_table")
        rec = (chains or {}).get(f"{task_id}::{name}") or {}
        seen = []
        for c in (rec.get("terminal_chains") or [])[:6]:
            cols = c.get("columns") or []
            if cols not in seen:
                seen.append(cols)
        if seen:
            buildable.append(f"  {name}: " + " | ".join(str(s[:12]) for s in seen[:3]))

    return f"""The relational plan below declares the target schema that pipeline
synthesis then tries to build. The result did not answer the question. Decide
whether the PLAN is at fault, and if it is, rewrite it.

	THE PLAN AS DECLARED
	{_declared_by_source(plan)}

  declared join edges: {[f"{e.get('left_table')}.{e.get('left_on')} <-> "
                         f"{e.get('right_table')}.{e.get('right_on')}"
                         for e in (plan.get('join_edges') or [])] or 'none'}

	WHAT THE SOURCE TABLES ACTUALLY HOLD
	{_source_contents(plan, raw_tables, bench_dir)}

	PLAN REPAIR BRIEF — focused, minimal edits only
	{_plan_repair_brief(plan.get('question') or '', plan, raw_tables, diag)}

	WHAT THIS PLAN PRODUCED
	{_materialized(produced or {}, diag)}

DECLARED JOIN EDGES, AS MEASURED ON WHAT WAS PRODUCED
{chr(10).join(edges) or '  (no edges declared)'}

COLUMNS THIS PLAN DECLARED THAT NO OPERATOR CHAIN COULD BUILD
{json.dumps(unmet, ensure_ascii=False, indent=2) if unmet else '  (none)'}

WHAT SYNTHESIS WAS ABLE TO PRODUCE FOR EACH TABLE
(it re-runs after this plan is rewritten, so a column outside these shapes will
fail again)
{chr(10).join(buildable) or '  (no candidate pool recorded)'}

THE TEST — apply it to the question, one requirement at a time
  Take each thing the question asks about: every value it filters on, every field
  it wants back, every entity it must relate. For each one ask:

      is there a declared column that can CARRY it, in the form the question
      needs it?

  A column carries a requirement only if its values ARE that thing. A requirement
  for one whole value is not carried by several columns that each hold a fragment
  of it — the value has been broken up and the pieces are a different domain. A
  requirement naming an entity is not carried by an opaque identifier for it. A
  requirement about a property is not carried by a table that never held that
  property.

  If every requirement is carried, THE PLAN IS NOT AT FAULT. Say so and change
  nothing.

DO NOT CHANGE THESE
  They differ from an ideal plan just as often in tasks that came out completely
  correct, so changing them fixes nothing and risks breaking what works:
  - a column name that is abbreviated, renamed, or invented — the result is
    scored on VALUES, not names
  - which column was chosen as the primary key
  - the fact that the plan declares fewer columns than the source table has;
    declaring extra columns that the question does not need is not an improvement
  - the numbering of the tables

Return JSON only:
{{"plan_at_fault": true | false,
  "unmet_requirement": "the thing the question asks for that no declared column
                        can carry, or null",
  "reasoning": "...",
  "revised_tables": [{{"input_file": "...", "columns": [...],
                       "primary_key": [...]}}],
  "revised_join_edges": [{{"left_table": "...", "left_on": "...",
                           "right_table": "...", "right_on": "..."}}]}}

Identify tables by `input_file`, never by table number. Leave `revised_tables`
and `revised_join_edges` empty when `plan_at_fault` is false."""


_EDGE_RE = re.compile(r"^\s*(\S+?)\.(.+?)\s*<->\s*(\S+?)\.(.+?)\s*$")


def _norms():
    """Normalisations a single operator could plausibly apply to a key column.

    Ordered cheapest-first so the reported fix is the smallest one that works.
    """
    def strip_quotes(s):
        return s.strip().strip('"').strip("'").strip()

    def digits(s):
        m = re.findall(r"\d+", s)
        return m[0].lstrip("0") or "0" if m else ""

    return [
        ("trim whitespace", lambda s: s.strip()),
        ("strip surrounding quotes", strip_quotes),
        ("casefold", lambda s: s.strip().casefold()),
        ("strip quotes + casefold", lambda s: strip_quotes(s).casefold()),
        ("drop non-alphanumerics", lambda s: re.sub(r"[^0-9a-zA-Z]", "", s).casefold()),
        ("numeric value only (drop quotes, leading zeros, decimals)",
         lambda s: digits(strip_quotes(s).split(".")[0])),
    ]


def _key_repair_probe(produced: Dict[str, Any], edge: str,
                      limit: int = 4000) -> str:
    """Do the two sides of a declared key overlap, and would normalising fix it?

    This is the block `revise_pipeline` was missing. A synthesised chain very
    often materialises the right key COLUMN with the wrong SURFACE FORM — one
    side quoted, zero-padded, or upper-cased — and the diagnostics then report a
    containment near zero, which reads identically to "these tables do not join
    at all". Those two situations need opposite repairs, and only the values
    distinguish them.

    Reports the cheapest normalisation that lifts containment, or says plainly
    that no normalisation helps, which is itself the answer: the fault is then
    the choice of key column, not its formatting.
    """
    m = _EDGE_RE.match(str(edge) or "")
    if not m:
        return ""
    lt, lc, rt, rc = m.groups()
    ldf, rdf = (produced or {}).get(lt), (produced or {}).get(rt)
    if ldf is None or rdf is None:
        return f"    (one endpoint of {edge} was never materialised)"

    def vals(df, col):
        real = {D._cf(c): c for c in df.columns}.get(D._cf(col))
        if real is None:
            return None
        try:
            return [str(x) for x in df[real].dropna().astype(str).tolist()[:limit]]
        except Exception:
            return None

    L, R = vals(ldf, lc), vals(rdf, rc)
    if L is None or R is None:
        side = lc if L is None else rc
        return f"    (the key column {side!r} is not present in the produced table)"
    if not L or not R:
        return "    (a key column was produced but is entirely empty)"

    def cont(a, b):
        sb = set(b)
        return sum(1 for x in set(a) if x in sb) / max(len(set(a)), 1)

    base = max(cont(L, R), cont(R, L))
    out = [f"    {lt}.{lc} sample: {list(dict.fromkeys(L))[:6]}",
           f"    {rt}.{rc} sample: {list(dict.fromkeys(R))[:6]}",
           f"    containment as produced: {base:.3f}"]
    # A normalisation must not achieve its overlap by DESTROYING the values.
    # `digits` on Airtable ids maps recvKTAWAFKkVNnXQ -> "" and
    # recy8KY5bUdzF81vv -> "8"; both sides then collapse onto a handful of single
    # digits and report containment 0.800 for two disjoint id spaces. Verified on
    # bird_edcbaae4, where the unguarded probe produced exactly that. So a
    # candidate is only accepted if it preserves distinct cardinality on both
    # sides and introduces no empties.
    nL, nR = len(set(L)), len(set(R))
    best = None
    for name, fn in _norms():
        try:
            a, b = [fn(x) for x in L], [fn(x) for x in R]
        except Exception:
            continue
        if any(not x for x in a) or any(not x for x in b):
            continue
        if len(set(a)) < 0.9 * nL or len(set(b)) < 0.9 * nR:
            continue
        c = max(cont(a, b), cont(b, a))
        if c > base + 0.15 and (best is None or c > best[1]):
            best = (name, c)
    if best and best[1] >= 0.5:
        out.append(f"    -> AFTER {best[0]}: containment {best[1]:.3f}. The key "
                   f"columns are the right ones and hold the same entities; the "
                   f"chain left them in different surface forms.")
    elif best:
        # Above the improvement threshold but still not a usable join. Saying
        # "the key is right" here would send the repair down the wrong branch.
        out.append(f"    -> {best[0]} raises containment to only {best[1]:.3f}, "
                   f"which still does not join. The surface form is part of the "
                   f"problem but not all of it; the key column may also be wrong.")
    else:
        out.append("    -> no normalisation of these two columns raises "
                   "containment. The values are different entities, so the fault "
                   "is the CHOICE of key column, not its formatting.")
    return "\n".join(out)


_VG_DATETIME = re.compile(r"^\s*\d{4}[-/]\d{1,2}[-/]\d{1,2}")
_VG_URL = re.compile(r"https?://|www\.")


def _still_packed(sr) -> bool:
    """Values that still carry a consistent delimiter — the split never finished.

    Ported from `hardness/pipeline/agent_tools.py`. Dates and URLs are excluded
    because they contain delimiters legitimately.
    """
    try:
        s = sr.dropna().astype(str).head(60)
    except Exception:
        return False
    if len(s) == 0:
        return False
    if s.str.match(_VG_DATETIME).mean() > 0.6 or s.str.contains(_VG_URL).mean() > 0.5:
        return False
    for d in ["|", ",", "/", ":", "_", "-"]:
        parts = s.str.split(re.escape(d))
        n = parts.str.len()
        # Every piece must be non-empty. `'-'.split('-')` is `['', '']`, length 2,
        # so a column whose values are a literal hyphen — a bond type, a missing
        # marker — reads as "packed" under a length test alone. That was the one
        # remaining false alarm (bird_4257d543.single_bond) after the null check
        # was fixed.
        ok = parts.map(lambda ps: len(ps) > 1 and all(str(p).strip() for p in ps))
        if ok.mean() > 0.8 and n.nunique() <= 2:
            return True
    return False


def _value_gate(plan: Dict[str, Any], produced: Dict[str, Any],
                raw_tables: Dict[str, Any]) -> str:
    """Required columns that exist BY NAME but whose VALUES are wrong.

    This is the failure mode our diagnostics miss entirely. The harness's other
    stop-signal — a required column still buried as a CELL VALUE — cannot fire
    here at all: `_Loop.run_table` uses `_info_need_columns(plan_sql)` as its
    completion gate, so the search runs until exactly those columns exist.
    Measured on this run it fires 0/30 on `revise_pipeline`, 0/32 on
    `revise_table`, 0/12 on `revise_relational_plan` and 1/67 on the healthy
    tasks. Meanwhile declared-column coverage is ~0.98 while subtable_recall is
    ~0.70. The names are complete; the values are not. That gap is what this
    block reports.

    Deterministic only. The harness also runs an LLM `_semantic_judge` here; that
    signal was measured separately as a CLASSIFIER and failed (AUC 0.547 against
    healthy tasks, and re-scoring the same tasks flagged 64 columns one run and 25
    the next). Inside a loop with rollback a false positive only costs one
    rejected attempt, but this block has no rollback, so only the reproducible
    checks are kept.
    """
    try:
        need = set(D._info_need_columns(plan.get("sql") or "")) \
            if hasattr(D, "_info_need_columns") else set()
    except Exception:
        need = set()
    if not need:
        need = {D._cf(c) for t in (plan.get("gold_tables") or [])
                for c in re.findall(r"`([^`]+)`",
                                    re.sub(r"PRIMARY\s+KEY\s*\([^)]*\)", "",
                                           t.get("create_table_sql") or "", flags=re.I))}
    out = []
    for lt, df in (produced or {}).items():
        raw = (raw_tables or {}).get(lt)
        raw_headers = {D._cf(c) for c in raw.columns} if raw is not None else set()
        for i, c in enumerate(df.columns):
            if D._cf(c) not in need:
                continue
            s = df.iloc[:, i]
            if isinstance(s, pd.DataFrame):
                s = s.iloc[:, 0]
            try:
                nullfrac = float(s.isna().mean())
            except Exception:
                nullfrac = 0.0
            # Compare against the SOURCE column, never an absolute threshold. The
            # harness flags any column over 90% null; verified here, 3 of the
            # first 4 such flags were false alarms — bird_2eb3fdb8.PT is 96.30%
            # null in the produced table AND 96.30% null in the raw one. The
            # pipeline lost nothing; the data is simply sparse. Only a column
            # that got emptier than its source, or a DERIVED column that came out
            # entirely empty, is a defect.
            raw_null = None
            if raw is not None and D._cf(c) in raw_headers:
                real = {D._cf(x): x for x in raw.columns}[D._cf(c)]
                try:
                    rs = raw[real]
                    if isinstance(rs, pd.DataFrame):
                        rs = rs.iloc[:, 0]
                    raw_null = float(rs.isna().mean())
                except Exception:
                    raw_null = None
            if raw_null is not None and nullfrac > raw_null + 0.25:
                out.append(f"    {lt}.{c}: {nullfrac:.0%} null, but only "
                           f"{raw_null:.0%} null in the source — the chain "
                           f"dropped values that were there")
            elif raw_null is None and nullfrac >= 0.999:
                out.append(f"    {lt}.{c}: entirely empty, and it is not a source "
                           f"column — the operator that was to derive it produced "
                           f"nothing")
            elif D._cf(c) not in raw_headers and _still_packed(s):
                try:
                    ex = str(s.dropna().iloc[0])[:34]
                except Exception:
                    ex = ""
                out.append(f"    {lt}.{c}: values still carry a delimiter "
                           f"(e.g. {ex!r}) — the split was never finished")
    return "\n".join(out)


def _ctx_revise_pipeline(diag, plan, link, chains, task_id, raw_tables, bench_dir=None, produced=None) -> str:
    """Evidence for repairing an execution, not a choice.

    Built around join health rather than `A1_unmet_declared_columns`. The earlier
    version keyed everything off unmet columns, which fire on only 3 of the 30
    tasks labelled `revise_pipeline` in the bird dev split — so 27 of 30 got an
    evidence block reading "(none flagged)". Weak join edges fire on 17 of 30 and
    are what this stage actually gets wrong.
    """
    edges = (diag.get("C_join_health") or {}).get("edges", [])
    pairs = _viable_pairs(diag)

    ejoin = []
    for e in edges:
        name = e.get("edge")
        lk, rk = e.get("C1_left_key") or {}, e.get("C1_right_key") or {}
        lines = [f"  declared edge: {name}",
                 f"    measured containment  L->R {e.get('C2_containment_l_in_r')}"
                 f"  R->L {e.get('C2_containment_r_in_l')}"
                 f"   jaccard {e.get('C2_jaccard')}",
                 f"    join yield {e.get('C3_join_yield')}"
                 f"   estimated fanout {e.get('C3_est_fanout')}",
                 f"    left key  non-null {lk.get('non_null')} unique {lk.get('unique_ratio')}"
                 f"  key-like: {lk.get('valid')}",
                 f"    right key non-null {rk.get('non_null')} unique {rk.get('unique_ratio')}"
                 f"  key-like: {rk.get('valid')}",
                 f"    both endpoints materialised: {e.get('C5_endpoints_materialised')}",
                 f"    verdict: {e.get('verdict')}"]
        probe = _key_repair_probe(produced or {}, name)
        if probe:
            lines.append("    KEY VALUES ON BOTH SIDES")
            lines.append(probe)
        alt = pairs.get(name) or []
        if alt:
            lines.append("    other column pairs that DO join on the produced "
                         "tables (by containment):")
            lines += [f"      {p['pair']}  {p['containment']}" for p in alt[:6]]
        ejoin.append("\n".join(lines))

    # Unmet columns stay, demoted: they are real when they fire, just rare.
    per = (diag.get("A_plan_fulfilment") or {}).get("per_table") or {}
    unmet_blocks = []
    for lt, v in per.items():
        unmet = v.get("A1_unmet_declared_columns") or []
        if not unmet:
            continue
        unmet_blocks.append(
            f"  {lt}: declared but never built {unmet}\n"
            f"    values visible in the raw table: "
            + _value_evidence(raw_tables.get(lt), unmet))

    tried_blocks = []
    for lt in sorted(set(per) | set(produced or {})):
        rec = (chains or {}).get(f"{task_id}::{lt}") or {}
        tc = rec.get("terminal_chains") or []
        if not tc:
            continue
        lines = [f"  {lt} ({len(tc)} chain(s) explored):"]
        for c in tc[:6]:
            lines.append(f"      {c.get('chain')} -> {(c.get('columns') or [])[:10]}"
                         + ("  <- selected" if c.get("selected") else ""))
        tried_blocks.append("\n".join(lines))

    return f"""EVIDENCE

The tables were selected correctly and the plan declared the right relations.
What went wrong is the execution: the operator chains below produced tables that
do not join, or do not carry the values the plan declared.

JOIN EDGES AS MEASURED ON WHAT WAS ACTUALLY PRODUCED
{chr(10).join(ejoin) or '  (the plan declared no join edge)'}

DECLARED COLUMNS NO CHAIN COULD BUILD
{chr(10).join(unmet_blocks) or '  (none — every declared column was produced)'}

REQUIRED COLUMNS THAT EXIST BY NAME BUT WHOSE VALUES ARE WRONG
{_value_gate(plan, produced or {}, raw_tables) or
 '  (no column failed the deterministic value checks)'}

CHAINS ALREADY EXPLORED
{chr(10).join(tried_blocks) or '  (no chain pool recorded)'}

HARD CONSTRAINTS
  - a column listed above as present-by-name-with-wrong-values is an OPERATOR
    fault, not a plan fault: the op TYPE may be right and only the PARAMS wrong.
    Fix the parameters first; propose changing the declared schema only after no
    operator can produce the right values
  - the chains listed above were already explored; a repair must differ from all
    of them, not re-derive one
  - if a normalisation is reported as lifting containment, apply that
    normalisation to the key column rather than changing which column is the key
  - if no normalisation helps and another column pair is listed as joining, the
    declared key is the wrong column — say which pair you are switching to and why
  - where the raw table does not contain the values at all, the fault is not the
    operator chain — say so rather than producing an empty column"""


def _value_evidence(raw: Optional[pd.DataFrame], needed: Sequence[str]) -> str:
    """EXPLICIT / PATTERN / ABSENT for the columns the chain failed to build."""
    if raw is None or not needed:
        return "(raw table unavailable)"
    have = {D._cf(c) for c in raw.columns}
    hits = [c for c in needed if D._cf(c) in have]
    if hits:
        return f"EXPLICIT — {hits} exist as raw columns; the chain dropped them"
    surface = D._table_surface(raw)
    seen = [c for c in needed if D._cf(c) in surface]
    if seen:
        return f"PATTERN — {seen} appear among the raw VALUES (header row or cells)"
    return "ABSENT — none of these appear as raw columns or values"


def _unresolved_foreign_keys(diag, link, raw_tables, bench_dir: Optional[Path] = None,
                             limit: int = 6, thresh: float = 0.9) -> str:
    """Selected columns whose values live in a table nobody selected.

    The one signal that turns "a table is missing" into "add THIS table". Values
    are compared, not names, so an obfuscated `yc` still resolves against a
    lookup table's id column — which is exactly the case that defeated a judge
    reading names alone.

    Candidate frames are loaded once and reused: the pool runs to 13 tables on
    this benchmark and re-reading one per column pair made the block too slow to
    keep.
    """
    sel = set(link.get("selected_tables") or [])
    pool = [c.get("file_name") for c in (link.get("candidates") or [])
            if c.get("file_name") and c.get("file_name") not in sel]
    if not pool or not raw_tables or bench_dir is None:
        return ""
    others: Dict[str, pd.DataFrame] = {}
    for f in pool:
        p = Path(bench_dir) / f
        if p.exists():
            try:
                others[f] = pd.read_pickle(p)
            except Exception:
                pass
    if not others:
        return ""
    ocache = {(f, oc): D._values(df, oc, limit=2000)
              for f, df in others.items() for oc in list(df.columns)[:40]}
    out: List[str] = []
    for lt, df in raw_tables.items():
        for col in list(df.columns)[:40]:
            v = D._values(df, col, limit=2000)
            if len(v) < 5:
                continue
            for (f, oc), ov in ocache.items():
                if len(ov) >= 5 and D._containment(v, ov) >= thresh:
                    out.append(f"  {lt}.{col} -> its values are contained in "
                               f"{f}.{oc}  (that table was NOT selected)")
                    break
            if len(out) >= limit:
                return "\n".join(out)
    return "\n".join(out)


_BUILDERS = {
    "revise_table": _ctx_revise_table,
    "revise_relational_plan": _ctx_revise_plan,
    "revise_pipeline": _ctx_revise_pipeline,
}


def build_context(action: str, *, diag: Dict[str, Any], plan: Dict[str, Any],
                  link: Dict[str, Any], chains: Optional[Dict[str, Any]] = None,
                  task_id: str = "", question: str = "",
                  raw_tables: Optional[Dict[str, pd.DataFrame]] = None,
                  bench_dir: Optional[Path] = None,
                  produced: Optional[Dict[str, Any]] = None,
                  tried: Sequence[Dict[str, Any]] = ()) -> str:
    if action not in _BUILDERS:
        raise ValueError(f"no repair context for {action!r}; expected {list(_BUILDERS)}")
    body = _BUILDERS[action](diag, plan, link, chains or {}, task_id,
                             raw_tables or {}, bench_dir, produced or {})
    return (f"QUESTION\n  {question}\n\n{body}\n\n"
            f"PREVIOUSLY TRIED AND FAILED\n{_tried(tried)}\n")


# --------------------------------------------------------------------------- #
# coverage — the free ceiling on repair success
# --------------------------------------------------------------------------- #

def coverage_plan(diag: Dict[str, Any], gold_edges: Sequence[dict]) -> Optional[bool]:
    """Is a gold join key pair among the ranked pairs this context offers?

    None when gold declares no edge, so single-table tasks do not count as
    covered or uncovered.
    """
    if not gold_edges:
        return None
    offered = set()
    for ranked in _viable_pairs(diag).values():
        for p in ranked:
            a, _, b = (p.get("pair") or "").partition("<->")
            offered.add((D._cf(a), D._cf(b)))
            offered.add((D._cf(b), D._cf(a)))
    if not offered:
        return False
    return any((D._cf(g.get("left_on")), D._cf(g.get("right_on"))) in offered
               for g in gold_edges)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Assemble and audit repair contexts.")
    ap.add_argument("--inter", type=Path, required=True)
    ap.add_argument("--gold-spec", type=Path,
                    default=ROOT / "train_infer_single_ops/results/gold_table_specs_expanded.jsonl")
    ap.add_argument("--coverage", action="store_true",
                    help="offline ceiling: could the evidence have supported a fix")
    ap.add_argument("--show", default=None, metavar="TASK_ID")
    ap.add_argument("--action", default="revise_relational_plan")
    args = ap.parse_args(argv)

    L = lambda n: {json.loads(l)["task_id"]: json.loads(l)                 # noqa: E731
                   for l in (args.inter / n).open() if l.strip()}
    diags, labels = L("diagnose.jsonl"), L("labels.jsonl")
    plans, links = L("relational_plan.jsonl"), L("schema_linking.jsonl")
    cp = args.inter / "chains.json"
    chains = json.loads(cp.read_text()) if cp.exists() else {}

    if args.show:
        t = args.show
        print(build_context(args.action, diag=diags[t], plan=plans[t], link=links[t],
                            chains=chains, task_id=t,
                            question=plans[t].get("question", ""),
                            tried=[{"action": args.action,
                                    "what": "example failed direction",
                                    "measured": "containment 0.02"}]))
        return 0

    if args.coverage:
        gold = {json.loads(l)["task_id"]: json.loads(l)
                for l in args.gold_spec.open() if l.strip()}
        n_cov = n_tot = 0
        for t, lab in labels.items():
            if lab["label"] != "revise_relational_plan" or t not in diags:
                continue
            g = (gold.get(t) or {}).get("join_edges") or []
            c = coverage_plan(diags[t], g)
            if c is None:
                continue
            n_tot += 1
            n_cov += bool(c)
        print(f"revise_relational_plan: gold key pair offered in the context for "
              f"{n_cov}/{n_tot} task(s)"
              + (f" = {n_cov / n_tot:.3f}" if n_tot else ""))
        print("This is a CEILING on repair success, not a prediction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
