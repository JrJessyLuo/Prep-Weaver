#!/usr/bin/env python3
"""
diagnose.py
===========
Gold-free diagnostics over a finished run, for deciding WHICH STAGE to revise:

    revise_table           the selected raw tables are wrong (missing / extra)
    revise_relational_plan the target schema, primary keys, or join edges are wrong
    revise_pipeline        the plan is fine but the transformations failed to realise it

NOTHING here reads ground truth. No gold subtables, no gold SQL, no gold column
lists. Everything is computed from: the question, the selected raw tables, the
relational plan we synthesized, the tables the pipeline produced, and the search
telemetry the run already recorded.

    (An earlier draft used the gold SQL's executability as the strongest
    end-to-end signal. It is removed: at deploy time the user supplies a natural
    language question, not SQL. Note that `full_pipeline_bounded._info_need_columns`
    still parses `task["sql"]` — that is a separate leak, not used here.)

THE ATTRIBUTION AXIS
--------------------
The relational plan is a set of ASSERTIONS ("these columns exist", "this is the
primary key", "these two columns join"). The pipeline is an attempt to HONOUR
them. That gives a clean split:

    signals measuring HOW WELL the plan was honoured    -> blame the pipeline
    signals measuring whether the honoured result is
      still internally incoherent                       -> blame the plan
    signals measuring whether the raw inputs could ever
      have supported the plan                           -> blame table selection

The second family must never quote the plan back at itself, or it only verifies
that we copied our own assertions. So every B/C signal below is computed from
frame content and cross-frame relationships, not from the declared schema text.

SIGNAL GROUPS
-------------
  T*  table selection    could these raw inputs support the plan / the question?
  A*  plan fulfilment    did the pipeline deliver what the plan declared?
  B*  result health      is the delivered frame a real table or a shell?
  C*  join health        do the declared keys actually behave like keys?

The three that carry the most weight, and why:

  C2 containment   — strongest single number, by a wide margin. Median best
      containment is 1.000 on edges from value-correct tasks and 0.009 on edges
      from value-wrong ones.

  C4 key_ambiguity  — number of column pairs across two tables whose value
      containment is >= 0.9. Reported ONLY as an explanation for an edge that
      C2 has already shown to be weak. Used as a standalone trigger it fires on
      17 edges of which 15 belong to fully correct tasks, because real tables
      routinely have several joinable pairs (id AND code AND uuid) while the
      declared one works fine. Ambiguity is not itself a failure.

  B1 header_echo   — fraction of cells whose value equals some OTHER column's
      name. A cell holding a column name means the frame is still in
      attribute/value form and the reshape (Pivot/Transpose) never happened.
      Measured at 100% precision on this benchmark: it never fired on a table
      that was actually fine.

  A2/A4 exec_error_rate + terminal score spread — separates "the operator was
      right but the parameters raised" from "the ranker had no information to
      choose with" (all terminal candidates tied at the same score).
"""
from __future__ import annotations

import os
import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# normalisation helpers (kept local so this module has no project dependencies)
# --------------------------------------------------------------------------- #

_WORD = re.compile(r"[a-z0-9]+")
_NULLISH = {"", "nan", "none", "null", "<na>", "n/a", "-"}


def _cf(x: Any) -> str:
    """Casefold to a comparison key: lowercase, strip non-alphanumerics."""
    return re.sub(r"[^a-z0-9]", "", str(x).lower())


def _norm(x: Any) -> str:
    """Normalise a cell value for set comparison: lowercase, collapse spaces."""
    return re.sub(r"\s+", " ", str(x).strip().lower())


def _values(df: pd.DataFrame, col: Any, limit: Optional[int] = None) -> set:
    """Normalised non-null value set of `col`, case-insensitive column lookup."""
    m = {_cf(c): c for c in df.columns}
    real = m.get(_cf(col))
    if real is None:
        return set()
    s = _col(df, real).dropna()
    if limit is not None and len(s) > limit:
        s = s.iloc[:limit]
    return {v for v in (_norm(v) for v in s.astype(str)) if v not in _NULLISH}


def _col(df: pd.DataFrame, col: Any) -> pd.Series:
    """Always a Series: duplicate column labels make `df[c]` a DataFrame."""
    s = df[col]
    return s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s


def _has(df: pd.DataFrame, col: Any) -> bool:
    return _cf(col) in {_cf(c) for c in df.columns}


def _r(x: Any, n: int = 3) -> Any:
    """Round floats for compact, diff-friendly JSON."""
    if isinstance(x, (int, bool)) or x is None:
        return x
    try:
        return round(float(x), n)
    except (TypeError, ValueError):
        return x


# --------------------------------------------------------------------------- #
# T — table selection
# --------------------------------------------------------------------------- #

_STOP = {
    "the", "a", "an", "of", "in", "on", "for", "to", "and", "or", "is", "are",
    "what", "which", "who", "how", "many", "much", "list", "give", "show",
    "find", "please", "name", "names", "with", "that", "have", "has", "there",
    "from", "by", "all", "их", "s", "do", "does", "be", "was", "were", "it",
}


def _table_surface(df: pd.DataFrame, cell_rows: int = 200) -> set:
    """Every token that appears in a table's headers or its sampled cells.

    Cells are included, not just headers, because a target column's name very
    often lives in the DATA (an attribute column's values, a transposed table's
    first column). Judging coverage on headers alone would blame table selection
    for something the pipeline was supposed to expose.
    """
    toks: set = set()
    for c in df.columns:
        toks |= set(_WORD.findall(str(c).lower()))
    head = df.head(cell_rows)
    for c in head.columns:
        for v in _col(head, c).dropna().astype(str).head(cell_rows).tolist():
            if len(str(v)) <= 80:
                toks |= set(_WORD.findall(v.lower()))
    return toks


_LITERAL = re.compile(
    r"'([^']{2,40})'|\"([^\"]{2,40})\"|\b([A-Z][a-zA-Z]{2,})\b|\b(\d{4})\b"
)


def question_literals(question: str) -> List[str]:
    """Quoted strings, capitalised proper nouns, and 4-digit years from the question.

    These are the parts of a question that must appear as DATA somewhere. Unlike
    schema words, a literal cannot be invented by a transformation: if 'Korean'
    is nowhere in any selected table's values, no reshape will conjure it, and
    the table holding it was simply never selected.
    """
    q = question or ""
    out: List[str] = []
    for m in _LITERAL.finditer(q):
        lit = next(g for g in m.groups() if g)
        # A sentence-initial capital is grammar, not a proper noun. Without this
        # guard "Among the ...", "Tell me ...", "Indicates ..." are all reported
        # as ungrounded literals, which fired on 16/43 tasks — almost all wrong.
        if m.group(3) is not None:
            before = q[:m.start()].rstrip()
            if not before or before.endswith((".", "?", "!")):
                continue
        if _norm(lit) not in _STOP:
            out.append(lit)
    # de-duplicate, preserve order
    seen: set = set()
    return [x for x in out if not (_norm(x) in seen or seen.add(_norm(x)))]


def diagnose_tables(question: str,
                    raw_tables: Dict[str, pd.DataFrame],
                    plan: Dict[str, Any],
                    cell_rows: int = 3000) -> Dict[str, Any]:
    """T1-T3: can the SELECTED raw inputs support the plan and the question?

    All three point at `revise_table` when they fire, because they are the only
    signals whose cause lies upstream of both the plan and the pipeline.

    DESIGN NOTE — why there is no "declared column name has no trace in the
    input" check here, even though it is the obvious first idea:
      a column's name very often does NOT exist anywhere in the input. It is
      INVENTED by the transformation. `SplitColumn` names its outputs from
      nothing (`set_info` = 'ALA|...' becomes `setCode`), and `Rename` accounts
      for 23.9% of gold column provenance. A name-trace check therefore fires
      precisely on the tasks that need the most structural work, and blames
      table selection for what is really the pipeline's job. Measured on the 43
      group_a tasks it fired on 15 of them, nearly all false. Only VALUE-level
      evidence (T2) can distinguish "this table was never selected" from "this
      column has not been built yet".
    """
    # T1 — a plan that references a logical table with no selected input.
    # Structural and exact: no thresholds, no name matching.
    declared = {t.get("logical_table") for t in
                (plan.get("gold_tables") or plan.get("tables") or [])}
    missing_inputs = sorted(t for t in declared if t and t not in raw_tables)

    # T2 — question literals absent from every selected table's VALUES.
    # This is the real "wrong tables were selected" evidence.
    lits = question_literals(question)
    value_surface: set = set()
    for df in raw_tables.values():
        head = df.head(cell_rows)
        for c in head.columns:
            for v in _col(head, c).dropna().astype(str).head(cell_rows).tolist():
                s = _norm(v)
                if len(s) <= 80:
                    value_surface.add(s)
                    value_surface |= set(_WORD.findall(s))
    ungrounded_lits = [x for x in lits if _norm(x) not in value_surface
                       and not (set(_WORD.findall(_norm(x))) & value_surface)]
    lit_cov = 1.0 - len(ungrounded_lits) / max(len(lits), 1)

    # Informational only, deliberately NOT used by `heuristic_action`: bag-of-words
    # overlap between question and table surface. It looked attractive but its
    # median on this benchmark is 0.33 even for tasks that are entirely correct,
    # because ordinary English ("tell", "her", "full") never appears in a table.
    surfaces = {k: _table_surface(df) for k, df in raw_tables.items()}
    union = set().union(*surfaces.values()) if surfaces else set()
    q_toks = {w for w in _WORD.findall((question or "").lower())
              if w not in _STOP and len(w) > 2}
    q_missing = sorted(q_toks - union)

    # T3 — selected tables that no edge touches (over-selection).
    edge_tables = set()
    for e in plan.get("join_edges") or []:
        edge_tables |= {e.get("left_table"), e.get("right_table")}
    isolated = [k for k in raw_tables if k not in edge_tables] if len(raw_tables) > 1 else []

    return {
        "T1_plan_tables_without_input": missing_inputs,
        "T1_count": len(missing_inputs),
        "T2_question_literals": lits,
        "T2_literals_absent_from_all_values": ungrounded_lits,
        "T2_literal_grounding": _r(lit_cov),
        "T3_isolated_tables": isolated,
        "info_question_token_coverage": _r(1.0 - len(q_missing) / max(len(q_toks), 1)),
        "info_uncovered_question_tokens": q_missing[:12],
    }


def _plan_columns(table_spec: Dict[str, Any]) -> List[str]:
    """Declared column names, from `column_types` or parsed from CREATE TABLE."""
    ct = table_spec.get("column_types")
    if isinstance(ct, dict) and ct:
        return list(ct)
    sql = table_spec.get("create_table_sql") or ""
    return re.findall(r"`([^`]+)`", sql)


# --------------------------------------------------------------------------- #
# A — plan fulfilment (pipeline side)
# --------------------------------------------------------------------------- #

def diagnose_fulfilment(plan: Dict[str, Any],
                        produced: Dict[str, pd.DataFrame],
                        raw_tables: Dict[str, pd.DataFrame],
                        run: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """A1-A5: how completely, and how cleanly, was the plan realised?"""
    run = run or {}
    per_table: Dict[str, Any] = {}
    unmet_total = declared_total = 0

    for t in plan.get("gold_tables") or plan.get("tables") or []:
        lt = t.get("logical_table")
        cols = _plan_columns(t)
        df = produced.get(lt)
        raw = raw_tables.get(lt)
        declared_total += len(cols)

        if df is None:
            per_table[lt] = {"A1_status": "table_not_produced", "A1_unmet": cols}
            unmet_total += len(cols)
            continue

        unmet = [c for c in cols if not _has(df, c)]
        unmet_total += len(unmet)

        # A5 — provenance. A declared column that was ALREADY a raw header cost
        # the pipeline nothing. If a task needs structural work and almost every
        # column is verbatim, the pipeline handed the input back unchanged — the
        # failure mode where a view echoes the raw headers and coverage (pure
        # string matching) is fooled into passing.
        verbatim = 0
        if raw is not None:
            raw_heads = {_cf(c) for c in raw.columns}
            verbatim = sum(1 for c in cols if _cf(c) in raw_heads)

        chain_rec = (run.get("chains") or {}).get(lt) or {}
        terms = chain_rec.get("terminal_chains") or []
        scores = [c.get("score") for c in terms if isinstance(c.get("score"), (int, float))]

        per_table[lt] = {
            "A1_unmet_declared_columns": unmet,
            "A1_fulfilment": _r(1.0 - len(unmet) / max(len(cols), 1)),
            "A5_verbatim_from_raw_header": verbatim,
            "A5_verbatim_frac": _r(verbatim / max(len(cols), 1)),
            "chain": chain_rec.get("chain"),
            "chain_ok": chain_rec.get("ok"),
            "A3_calls": chain_rec.get("calls"),
            "A3_budget_saturated": (
                None if chain_rec.get("calls") is None or not run.get("budget")
                else bool(chain_rec["calls"] >= run["budget"])
            ),
            # A4 — a flat spread means every surviving candidate looked identical
            # to the layer-1 ranker, so whichever one got picked was arbitrary.
            # This is the PRECONDITION for a ranking error, not a ranking error.
            "A4_terminal_count": len(terms),
            "A4_score_spread": _r(max(scores) - min(scores)) if len(scores) > 1 else 0.0,
            "A4_all_tied": bool(len(scores) > 1 and max(scores) - min(scores) < 1e-9),
            # A4b — distinct op-name chains vs distinct produced frames. Names
            # alone cannot tell a param variant (useful: layer-2 breaks layer-1
            # ties on value overlap) from a true duplicate (wasted budget), so
            # the frame half of `param_fp` is what actually answers it.
            "A4_distinct_chains": len({tuple(c.get("chain") or []) for c in terms}),
            "A4_distinct_frames": len({
                tuple((f or "").split("/")[-1] for f in (c.get("param_fp") or []))
                for c in terms if c.get("param_fp") is not None
            }) or None,
        }

    # A2 — execution errors are the signature of WRONG PARAMETERS specifically:
    # the operator was chosen and invoked, and `robust_execute` raised. Operator
    # selection errors do not raise, they just fail to improve coverage.
    errs = run.get("candidate_errors") or []
    kinds: Dict[str, int] = {}
    for e in errs:
        m = re.match(r"(synth|execute)\s+(\w+):\s*(\w+)", str(e))
        if m:
            kinds[f"{m.group(1)}:{m.group(2)}:{m.group(3)}"] = kinds.get(
                f"{m.group(1)}:{m.group(2)}:{m.group(3)}", 0) + 1

    return {
        "A1_declared_columns": declared_total,
        "A1_unmet_columns": unmet_total,
        "A1_overall_fulfilment": _r(1.0 - unmet_total / max(declared_total, 1)),
        "A2_execution_errors": len(errs),
        "A2_error_kinds": dict(sorted(kinds.items(), key=lambda kv: -kv[1])[:6]),
        "per_table": per_table,
    }


# --------------------------------------------------------------------------- #
# B — result health (plan side); never quotes the declared schema back
# --------------------------------------------------------------------------- #

def diagnose_health(df: pd.DataFrame,
                    declared_types: Optional[Dict[str, str]] = None,
                    cell_rows: int = 300) -> Dict[str, Any]:
    """B1-B4: is this a real table, or a shell that games coverage scoring?"""
    n_rows, n_cols = df.shape
    head = df.head(cell_rows)

    # B1 — header echo. Strongest single signal on this benchmark (100%
    # precision). A cell whose value IS another column's name means the frame is
    # still attribute/value shaped and the reshape never ran.
    names = {_cf(c) for c in df.columns}
    echo = total = 0
    echo_examples: List[str] = []
    for c in head.columns:
        others = names - {_cf(c)}
        for v in _col(head, c).dropna().astype(str).tolist():
            total += 1
            if _cf(v) in others:
                echo += 1
                if len(echo_examples) < 5:
                    echo_examples.append(f"{c}={v!r}")
    echo_frac = echo / max(total, 1)

    # B2 — degeneracy. A 6-row, 17%-non-null frame with field names down the
    # diagonal scored 7/8 on coverage and passed. Density catches what pure
    # string matching cannot.
    density = float(df.notna().to_numpy().mean()) if n_rows and n_cols else 0.0

    # B3 — constant columns are filler; all-unique text columns usually mean the
    # entity grain was misidentified.
    const_cols, allunique_cols = [], []
    for c in df.columns:
        s = _col(df, c).dropna()
        if len(s) == 0:
            const_cols.append(str(c)); continue
        nu = s.astype(str).nunique()
        if nu == 1:
            const_cols.append(str(c))
        elif nu == len(s) and len(s) > 5 and pd.to_numeric(s, errors="coerce").isna().all():
            allunique_cols.append(str(c))

    # B4 — declared numeric but not numeric. `strong_score`'s semantic term gives
    # every NON-numeric column a free pass, so this mismatch is invisible to the
    # ranker and has to be surfaced separately.
    type_mismatch = []
    for col, t in (declared_types or {}).items():
        if not _has(df, col):
            continue
        want_num = any(x in str(t).lower() for x in ("int", "float", "num", "real", "double"))
        if not want_num:
            continue
        m = {_cf(c): c for c in df.columns}[_cf(col)]
        if pd.to_numeric(_col(df, m), errors="coerce").notna().mean() < 0.8:
            type_mismatch.append(str(col))

    return {
        "shape": [int(n_rows), int(n_cols)],
        "B1_header_echo_frac": _r(echo_frac),
        "B1_header_echo_examples": echo_examples,
        "B2_non_null_density": _r(density),
        "B2_degenerate_shape": bool(n_rows <= n_cols or n_rows < 3),
        "B3_constant_columns": const_cols[:8],
        "B3_all_unique_text_columns": allunique_cols[:8],
        "B4_declared_numeric_but_not": type_mismatch,
    }


# --------------------------------------------------------------------------- #
# C — join health.  The 5-way discriminant.
# --------------------------------------------------------------------------- #

def _pk_stats(df: pd.DataFrame, col: Any) -> Dict[str, Any]:
    if not _has(df, col):
        return {"present": False}
    m = {_cf(c): c for c in df.columns}[_cf(col)]
    s = _col(df, m)
    nn = float(s.notna().mean())
    uq = float(s.dropna().astype(str).nunique() / max(s.notna().sum(), 1))
    return {"present": True, "non_null": _r(nn), "unique_ratio": _r(uq),
            "valid": bool(nn >= 0.95 and uq >= 0.95)}


def _containment(a: set, b: set) -> float:
    return len(a & b) / max(len(a), 1)


def diagnose_joins(plan: Dict[str, Any],
                   produced: Dict[str, pd.DataFrame],
                   edges: Sequence[Dict[str, Any]],
                   ambiguity_min_card: int = 8,
                   ambiguity_thresh: float = 0.9) -> Dict[str, Any]:
    """C1-C5 per declared edge, plus the ambiguity scan that separates
    'the pipeline picked the wrong key' from 'the plan cannot be resolved
    structurally at all'."""
    pk_decl = {}
    for t in plan.get("gold_tables") or plan.get("tables") or []:
        pk_decl[t.get("logical_table")] = (t.get("primary_key") or [None])[0]

    out: List[Dict[str, Any]] = []
    for e in edges or []:
        lt, lo = e.get("left_table"), e.get("left_on")
        rt, ro = e.get("right_table"), e.get("right_on")
        ldf, rdf = produced.get(lt), produced.get(rt)

        # C5 — both endpoints materialised at all?
        if ldf is None or rdf is None:
            out.append({"edge": f"{lt}.{lo} <-> {rt}.{ro}",
                        "C5_endpoints_materialised": False,
                        "verdict": "pipeline: endpoint table missing"})
            continue

        lv, rv = _values(ldf, lo), _values(rdf, ro)
        lpk, rpk = _pk_stats(ldf, lo), _pk_stats(rdf, ro)

        # Which side looks like the PK side is decided by measured uniqueness,
        # not by the plan's declaration — otherwise a wrong PK declaration would
        # silently steer the whole diagnosis.
        c_lr, c_rl = _containment(lv, rv), _containment(rv, lv)

        # C3 — join yield. 0 means the domains never meet; >> 1 means fan-out,
        # i.e. the key is not selective enough (usually a missing composite key).
        inter = len(lv & rv)
        yield_ratio = None
        if lv and rv:
            lc = _col(ldf, {_cf(c): c for c in ldf.columns}[_cf(lo)]).astype(str).map(_norm)
            rc = _col(rdf, {_cf(c): c for c in rdf.columns}[_cf(ro)]).astype(str).map(_norm)
            joined = int(pd.Series(lc).isin(set(rc)).sum())
            fan = (lc.value_counts().mean() * rc.value_counts().mean()) if inter else 0.0
            yield_ratio = _r(joined / max(min(len(ldf), len(rdf)), 1))
        else:
            fan = 0.0

        rec = {
            "edge": f"{lt}.{lo} <-> {rt}.{ro}",
            "C5_endpoints_materialised": True,
            "C1_left_key": lpk, "C1_right_key": rpk,
            "C2_containment_l_in_r": _r(c_lr),
            "C2_containment_r_in_l": _r(c_rl),
            "C2_jaccard": _r(len(lv & rv) / max(len(lv | rv), 1)),
            "C3_join_yield": yield_ratio,
            "C3_est_fanout": _r(fan),
            "C4_ambiguity": _key_ambiguity(ldf, rdf, ambiguity_min_card, ambiguity_thresh),
            "declared_pk": {lt: pk_decl.get(lt), rt: pk_decl.get(rt)},
        }
        rec["verdict"] = _edge_verdict(rec)
        out.append(rec)

    return {"edges": out, "n_edges": len(out)}


def _key_ambiguity(ldf: pd.DataFrame, rdf: pd.DataFrame,
                   min_card: int, thresh: float) -> Dict[str, Any]:
    """C4 — how many column pairs would serve equally well as the join key?

    >= 2 means the plan is UNDERSPECIFIED: multiple structurally valid FKs exist
    and only question semantics can choose between them. `bird_feb8f881` is the
    canonical case (`id<->id` AND `uuid<->uuid` both hold). When this fires,
    further pipeline-side repair is provably wasted effort — the fix belongs in
    the plan.
    """
    lcache = {c: _values(ldf, c, limit=2000) for c in ldf.columns}
    rcache = {c: _values(rdf, c, limit=2000) for c in rdf.columns}
    pairs = []
    for lc, lv in lcache.items():
        if len(lv) < min_card:
            continue
        for rc, rv in rcache.items():
            if len(rv) < min_card:
                continue
            c = max(_containment(lv, rv), _containment(rv, lv))
            if c >= thresh:
                pairs.append({"pair": f"{lc}<->{rc}", "containment": _r(c)})
    pairs.sort(key=lambda p: -p["containment"])
    return {"n_viable_pairs": len(pairs), "pairs": pairs[:6]}


def _edge_verdict(rec: Dict[str, Any]) -> str:
    """The C1/C2/C3/C4 discriminant, as a single sentence."""
    l, r = rec["C1_left_key"], rec["C1_right_key"]
    if not l.get("present") or not r.get("present"):
        return "pipeline: declared key column was never materialised"
    best_c = max(rec["C2_containment_l_in_r"], rec["C2_containment_r_in_l"])
    n_viable = rec["C4_ambiguity"]["n_viable_pairs"]
    if best_c < 0.05:
        # ABSTAIN. Near-zero containment has two causes that no gold-free
        # structural signal can separate on this data:
        #   (a) the key really is wrong;
        #   (b) both tables are independent 1000-row samples of much larger
        #       relations, so even a perfect key has no overlap. Measured on the
        #       gold-plan run: 8 of the 34 edges belonging to fully correct tasks
        #       sit here (zip_code<->zip, uuid<->uuid, player_api_id<->...).
        # Format compatibility was tried as a tie-breaker and falsified — the
        # correct and wrong groups overlap completely (correct 0.23-1.0, wrong
        # 0.05-1.0; a wrong edge and a correct edge both scored exactly 1.0).
        # So the verdict is marked undecidable and `heuristic_action` does NOT
        # act on it: only question semantics can resolve it, which is the LLM
        # judge's job, not a threshold's.
        hint = (f"{n_viable} other column pair(s) DO join, so joinable content "
                "exists and the declared columns may be the wrong ones"
                if n_viable >= 1 else
                "no column pair in either table joins at all, so either the key "
                "was built with wrong content or the two samples are disjoint")
        return f"undecidable: declared key domains do not meet ({hint})"
    if best_c < 0.8:
        # Ambiguity is an EXPLANATION for a failing edge, not a failure itself.
        # Checking it before confirming the declared edge is broken was wrong:
        # it fired on 17 edges of which 15 belonged to fully correct tasks,
        # because real relational tables routinely have several joinable column
        # pairs (id AND code AND uuid) while the declared one works fine.
        if n_viable >= 2:
            return (f"plan: underspecified — the declared key only reaches "
                    f"containment {best_c}, and {n_viable} column pairs are "
                    "equally valid; only question semantics can disambiguate")
        return "pipeline: right domain, wrong surface form (case/type/packing)"
    if not l.get("valid") and not r.get("valid"):
        return "plan: neither side is unique — wrong entity grain / composite key needed"
    # Fan-out only indicates a missing key when NEITHER side is unique, i.e. a
    # genuine many-to-many. One-to-many is the normal shape of a foreign key:
    # scoring it as "not selective" flagged 13 edges, every one of them on a
    # fully correct task.
    if (rec["C3_est_fanout"] or 0) > 4 and not l.get("valid") and not r.get("valid"):
        return "plan: key not selective on both sides — composite key likely missing"
    return "ok"


# --------------------------------------------------------------------------- #
# top-level
# --------------------------------------------------------------------------- #

def diagnose(question: str,
             raw_tables: Dict[str, pd.DataFrame],
             plan: Dict[str, Any],
             produced: Dict[str, pd.DataFrame],
             edges: Optional[Sequence[Dict[str, Any]]] = None,
             run: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Full gold-free diagnostic record for one task.

    question    natural language query (NOT SQL)
    raw_tables  {logical_table: DataFrame} as selected by schema linking
    plan        the synthesized relational plan (see relational_plan.py)
    produced    {logical_table: DataFrame} the pipeline materialised
    edges       join edges actually used; defaults to the plan's
    run         optional telemetry: {"budget": int, "candidate_errors": [...],
                "chains": {logical_table: chains.json record}}
    """
    edges = edges if edges is not None else (plan.get("join_edges") or [])
    types = {}
    for t in plan.get("gold_tables") or plan.get("tables") or []:
        types[t.get("logical_table")] = t.get("column_types") or {}

    return {
        "question": question,
        "T_table_selection": diagnose_tables(question, raw_tables, plan),
        "A_plan_fulfilment": diagnose_fulfilment(plan, produced, raw_tables, run),
        "B_result_health": {lt: diagnose_health(df, types.get(lt))
                            for lt, df in produced.items()},
        "C_join_health": diagnose_joins(plan, produced, edges),
    }


# --------------------------------------------------------------------------- #
# heuristic baseline — the number the LLM has to beat
# --------------------------------------------------------------------------- #

def heuristic_action(diag: Dict[str, Any]) -> Dict[str, Any]:
    """Rule-based stage attribution, ordered by how upstream the cause is.

    Exists so that step (2)'s LLM accuracy has a floor to be compared against.
    If the LLM cannot beat this, the diagnostic fields are doing the work and
    the LLM is adding nothing.
    """
    T, A, C = diag["T_table_selection"], diag["A_plan_fulfilment"], diag["C_join_health"]
    B = diag["B_result_health"]

    if T["T1_count"] > 0:
        return {"action": "revise_table",
                "why": f"plan references {T['T1_plan_tables_without_input']} "
                       "with no selected input table"}
    if T["T2_literals_absent_from_all_values"]:
        return {"action": "revise_table",
                "why": "question literal(s) appear in no selected table's values: "
                       f"{T['T2_literals_absent_from_all_values'][:4]}"}

    # Edges marked `undecidable` are deliberately skipped: near-zero containment
    # is produced both by a wrong key and by two disjoint 1000-row samples of the
    # same relation, and no gold-free structural signal separates them (format
    # compatibility was tried and falsified). Guessing here cost more than it
    # gained; the LLM judge, which can read the question, is the right arbiter.
    plan_edges = [e for e in C["edges"] if str(e.get("verdict", "")).startswith("plan")]
    if plan_edges:
        return {"action": "revise_relational_plan", "why": plan_edges[0]["verdict"]}

    for lt, h in B.items():
        if h["B1_header_echo_frac"] > 0.02:
            return {"action": "revise_pipeline",
                    "why": f"{lt}: {h['B1_header_echo_frac']:.1%} of cells hold another "
                           f"column's name — reshape never ran ({h['B1_header_echo_examples'][:2]})"}
        if h["B2_degenerate_shape"] or h["B2_non_null_density"] < 0.3:
            return {"action": "revise_pipeline",
                    "why": f"{lt}: degenerate frame {h['shape']}, density "
                           f"{h['B2_non_null_density']}"}

    if A["A1_unmet_columns"] > 0:
        return {"action": "revise_pipeline",
                "why": f"{A['A1_unmet_columns']}/{A['A1_declared_columns']} declared "
                       "columns were never materialised"}
    pipe_edges = [e for e in C["edges"] if str(e.get("verdict", "")).startswith("pipeline")]
    if pipe_edges:
        return {"action": "revise_pipeline", "why": pipe_edges[0]["verdict"]}
    if A["A2_execution_errors"] > 0:
        return {"action": "revise_pipeline",
                "why": f"{A['A2_execution_errors']} parameter execution error(s)"}
    undecided = [e for e in C["edges"] if str(e.get("verdict", "")).startswith("undecidable")]
    if not any(c.get("chain_ok") is False for c in A["per_table"].values()):
        if undecided:
            return {"action": "no_revision_needed",
                    "why": "no check failed, but "
                           f"{len(undecided)} edge(s) are undecidable without "
                           f"question semantics: {undecided[0]['verdict']}",
                    "low_confidence": True}
        # Nothing fired. Note what this claim is and is not: every gold-free
        # check passed, which is NECESSARY but not SUFFICIENT for correctness —
        # a table can satisfy the plan, be dense, be echo-free and join cleanly
        # and still hold the wrong values. This class exists so accuracy is
        # computable on the tasks that need no revision; it is not a correctness
        # certificate.
        return {"action": "no_revision_needed",
                "why": "all gold-free checks pass: plan fully materialised, "
                       "frames non-degenerate, every declared edge joins"}
    unfinished = [lt for lt, c in A["per_table"].items() if c.get("chain_ok") is False]
    return {"action": "revise_pipeline",
            "why": f"search terminated without a complete plan on {unfinished}"}


# --------------------------------------------------------------------------- #
# rendering for the LLM judge
# --------------------------------------------------------------------------- #

def render_markdown(diag: Dict[str, Any], include_verdicts: bool = True) -> str:
    """Compact markdown for the LLM prompt.

    `include_verdicts=False` strips the rule-based `verdict` strings so you can
    measure whether the LLM is reasoning from the NUMBERS or just copying our
    heuristic. Run the ablation both ways — if accuracy is identical, the LLM is
    not adding judgement and you should ship the heuristic instead.
    """
    L: List[str] = []
    T, A, C = diag["T_table_selection"], diag["A_plan_fulfilment"], diag["C_join_health"]

    L.append("## Table selection")
    L.append(f"- plan tables with no selected input: {T['T1_plan_tables_without_input']}")
    L.append(f"- question literals: {T['T2_question_literals']}")
    L.append(f"- literals found in NO selected table's values: "
             f"{T['T2_literals_absent_from_all_values']} "
             f"(grounding {T['T2_literal_grounding']})")
    L.append(f"- selected tables touched by no edge: {T['T3_isolated_tables']}")

    L.append("\n## Plan fulfilment")
    L.append(f"- declared columns materialised: "
             f"{A['A1_declared_columns'] - A['A1_unmet_columns']}/{A['A1_declared_columns']}")
    L.append(f"- parameter execution errors: {A['A2_execution_errors']} {A['A2_error_kinds']}")
    for lt, p in A["per_table"].items():
        L.append(f"- {lt}: chain={p.get('chain')} ok={p.get('chain_ok')} "
                 f"calls={p.get('A3_calls')} saturated={p.get('A3_budget_saturated')} "
                 f"unmet={p.get('A1_unmet_declared_columns')} "
                 f"verbatim_from_raw={p.get('A5_verbatim_frac')} "
                 f"terminals={p.get('A4_terminal_count')} "
                 f"tied={p.get('A4_all_tied')} "
                 f"distinct_chains={p.get('A4_distinct_chains')} "
                 f"distinct_frames={p.get('A4_distinct_frames')}")

    L.append("\n## Produced table health")
    for lt, h in diag["B_result_health"].items():
        L.append(f"- {lt} shape={h['shape']} density={h['B2_non_null_density']} "
                 f"header_echo={h['B1_header_echo_frac']} {h['B1_header_echo_examples'][:2]} "
                 f"const_cols={h['B3_constant_columns']} "
                 f"type_mismatch={h['B4_declared_numeric_but_not']}")

    L.append("\n## Join health")
    for e in C["edges"]:
        if not e.get("C5_endpoints_materialised"):
            L.append(f"- {e['edge']}: endpoint table missing")
            continue
        L.append(
            f"- {e['edge']}: containment L->R={e['C2_containment_l_in_r']} "
            f"R->L={e['C2_containment_r_in_l']} jaccard={e['C2_jaccard']} "
            f"yield={e['C3_join_yield']} fanout={e['C3_est_fanout']}\n"
            f"    left_key={e['C1_left_key']} right_key={e['C1_right_key']}\n"
            f"    viable_key_pairs={e['C4_ambiguity']['n_viable_pairs']} "
            f"{e['C4_ambiguity']['pairs'][:4]}"
        )
        if include_verdicts:
            L.append(f"    verdict: {e['verdict']}")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# CLI — batch over a finished run
# --------------------------------------------------------------------------- #

AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")


def _load_run(run_pkl: Path) -> Dict[str, Any]:
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from prep_utils import load_run
    return load_run(run_pkl)          # tables.pkl, or the tables/ shard dir


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    ap.add_argument("--run", required=True, type=Path,
                    help="results/*.pkl produced by full_pipeline_bounded")
    ap.add_argument("--spec", required=True, type=Path,
                    help="relational plan jsonl (gold_table_specs.jsonl or a grounded spec)")
    ap.add_argument("--chains", type=Path, default=None,
                    help="matching *_chains.json for A3/A4 telemetry")
    ap.add_argument("--bench-dir", type=Path, default=AUTOP / "nl2sql-bird/dev")
    ap.add_argument("--budget", type=int, default=None,
                    help="the run's --budget, so A3_budget_saturated can be computed")
    ap.add_argument("--out", required=True, type=Path, help="output jsonl")
    ap.add_argument("--markdown-dir", type=Path, default=None,
                    help="also write one .md per task, for pasting into the LLM prompt")
    ap.add_argument("--no-verdicts", action="store_true",
                    help="omit rule-based verdicts from the markdown (ablation)")
    ap.add_argument("--tasks", default=None, help="comma-separated task_id filter")
    args = ap.parse_args(argv)

    run = _load_run(args.run)
    specs = {json.loads(l)["task_id"]: json.loads(l) for l in args.spec.open()}
    chains = json.load(args.chains.open()) if args.chains else {}
    bench = {json.loads(l)["task_id"]: json.loads(l)
             for l in (args.bench_dir / "benchmark.jsonl").open()}

    keep = set(args.tasks.split(",")) if args.tasks else None
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.markdown_dir:
        args.markdown_dir.mkdir(parents=True, exist_ok=True)

    n = 0
    with args.out.open("w") as fh:
        for tid, rec in run.items():
            if keep and tid not in keep:
                continue
            plan, task = specs.get(tid), bench.get(tid)
            if not plan or not task:
                continue

            produced = {k: v for k, v in (rec.get("subtables") or {}).items()
                        if isinstance(v, pd.DataFrame)}
            raw_tables = {}
            for t in plan.get("gold_tables") or []:
                f = t.get("input_file")
                if f and (args.bench_dir / f).exists():
                    raw_tables[t["logical_table"]] = pd.read_pickle(args.bench_dir / f)

            telemetry = {
                "budget": args.budget,
                "candidate_errors": rec.get("candidate_errors") or [],
                "chains": {lt: chains.get(f"{tid}::{lt}", {}) for lt in produced},
            }
            diag = diagnose(task.get("question", ""), raw_tables, plan,
                            produced, rec.get("edges") or [], telemetry)
            diag["task_id"] = tid
            diag["heuristic"] = heuristic_action(diag)
            # carried through only for offline scoring of step (1)'s labels;
            # nothing in the diagnosis reads it.
            diag["_run_label"] = rec.get("label")

            fh.write(json.dumps(diag, ensure_ascii=False, default=str) + "\n")
            if args.markdown_dir:
                (args.markdown_dir / f"{tid}.md").write_text(
                    render_markdown(diag, include_verdicts=not args.no_verdicts))
            n += 1

    print(f"wrote {n} task diagnostics -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
