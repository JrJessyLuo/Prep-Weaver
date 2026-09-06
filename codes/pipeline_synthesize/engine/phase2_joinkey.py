#!/usr/bin/env python3
"""
phase2_joinkey.py
-----------------
Phase 2: after every subtable is synthesized, check and repair the join keys.

Search order (PK->FK topological, each key repaired at most once):
  Level 0: after de-duplication, fix every PK anchor first (present + unique + non-null);
  Level 1: once the anchors are trusted, check containment (FK subset of PK) edge by edge;

Repair ops:
  MATCH class (value level): rule-determined — casefold overlap -> StandardizeString;
                   dtype mismatch -> CastType; an FK packing PK values -> SplitColumn.
  EXPOSE class (structural): a missing key, or a key stuck in the header row -> back to
"""
from __future__ import annotations
import os
import re, sys
from pathlib import Path

ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
for p in (str(ROOT / "pipeline_eval"), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pandas as pd
import numpy as np
from eval_react_subtables import norm_values


def _cf(x): return str(x).strip().casefold()


def _series(df, col):
    """Fetch a column as a Series, case-insensitively; the first on a duplicate name; None when absent."""
    m = {_cf(c): c for c in df.columns}
    if _cf(col) not in m:
        return None
    s = df[m[_cf(col)]]
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    return s


def col_values(df, col):
    """The value set of a column, case-insensitively and normalised. None when the column is absent."""
    s = _series(df, col)
    if s is None:
        return None
    return norm_values(s.dropna().astype(str).tolist())


def pk_valid(df, col):
    """PK conditions: present, unique (>=0.95) and non-null (>=0.95)."""
    s = _series(df, col)
    if s is None:
        return False, "missing"
    nn = s.notna().mean()
    uq = s.dropna().astype(str).nunique() / max(s.notna().sum(), 1)
    if nn < 0.95:
        return False, "null_heavy"
    if uq < 0.95:
        return False, "not_unique"
    return True, "ok"


def containment(fk_df, fk_col, pk_vals):
    """Fraction of FK values that fall inside the PK value set."""
    fv = col_values(fk_df, fk_col)
    if not fv or not pk_vals:
        return 0.0
    return len(fv & pk_vals) / len(fv)


# ---------------- MATCH: rule-based repair (deterministic, no LLM) ----------------
def match_repair(fk_df, fk_col, pk_vals):
    """Try to align fk_col to pk_vals with value-level rules. Returns (repaired_df, op_desc) or (None, None)."""
    m = {_cf(c): c for c in fk_df.columns}
    if _cf(fk_col) not in m:
        return None, None
    col = m[_cf(fk_col)]
    base = containment(fk_df, fk_col, pk_vals)

    cands = []
    # 1) StandardizeString: strip+lower
    d1 = fk_df.copy(); d1[col] = d1[col].map(lambda v: str(v).strip().lower() if pd.notna(v) else v)
    cands.append((d1, "StandardizeString(strip.lower)"))
    # 2) CastType: numeric string -> int (drops a trailing .0 and similar)
    d2 = fk_df.copy()
    num = pd.to_numeric(d2[col], errors="coerce")
    if num.notna().mean() > 0.8:
        d2[col] = num.map(lambda x: str(int(x)) if pd.notna(x) and float(x) == int(x) else x)
        cands.append((d2, "CastType(int)"))
    # 3) SplitColumn: when FK values contain a separator and one part lands in the PK
    for sep in ["-", "_", "/", "|", " "]:
        s = fk_df[col].astype(str)
        if s.str.contains(sep, regex=False).mean() > 0.5:
            for pos in (0, 1, -1):
                d3 = fk_df.copy()
                d3[col] = s.str.split(sep).map(lambda p: p[pos] if len(p) > abs(pos) else None)
                cands.append((d3, f"SplitColumn(sep={sep!r},part={pos})"))

    best_df, best_op, best_c = None, None, base
    for d, desc in cands:
        c = containment(d, fk_col, pk_vals)
        if c > best_c:
            best_c, best_df, best_op = c, d, desc
    return (best_df, f"{best_op} [{base:.2f}->{best_c:.2f}]") if best_df is not None else (None, None)


# ---------------- Phase 2 orchestration ----------------
def repair_joins(subtables: dict, edges: list, anchors: dict, thresh=0.5,
                 expose_fn=None, budget=3):
    """
    subtables: {logical_table: (df, db_table, pk_set)}
    edges: [{'left_table','left_on','right_table','right_on'}, ...]  (excluding _join)
    anchors: {logical_table: pk_col}, the anchors already fixed (the PK side)
    expose_fn: optional callable(df, table_ctx, missing_col)->df, for structurally missing
    Returns: the repaired subtables and a log.
    """
    log = []
    calls = {lt: 0 for lt in subtables}

    def get(lt): return subtables[lt][0]
    def setdf(lt, df): subtables[lt] = (df, subtables[lt][1], subtables[lt][2])

    # ---- Level 0: de-duplicate and repair the anchors ----
    anchor_items = {}   # (lt, col) unique
    for e in edges:
        for side, on in (("left_table", "left_on"), ("right_table", "right_on")):
            lt = e[side]
            if lt in anchors and _cf(anchors[lt]) == _cf(e[on]):
                anchor_items[(lt, e[on])] = True
    for (lt, col) in anchor_items:
        if lt not in subtables:
            log.append(f"L0 anchor {lt}.{col}: missing synthesized table")
            continue
        ok, why = pk_valid(get(lt), col)
        if ok:
            continue
        # Only expose a missing key. A non-unique/null-heavy join column may be
        # valid in one-to-many or composite-key relations; deleting whole rows
        # here destroys query-required non-key values.
        df = get(lt)
        if why == "missing" and expose_fn and calls[lt] < budget:
            df2 = expose_fn(df, subtables[lt], col); calls[lt] += 1
            if df2 is not None: df = df2
        setdf(lt, df)
        note = ("exposed" if pk_valid(df, col)[0] else
                ("kept_non_destructively" if expose_fn else
                 "kept_non_destructively (EXPOSE not implemented)"))
        log.append(f"L0 anchor {lt}.{col}: {why} -> {note}")

    # ---- Level 1: containment per edge, repairing the FK side ----
    for e in edges:
        # The FK side is the non-anchor side
        if e["left_table"] in anchors and _cf(anchors[e["left_table"]]) == _cf(e["left_on"]):
            pk_lt, pk_col, fk_lt, fk_col = e["left_table"], e["left_on"], e["right_table"], e["right_on"]
        else:
            pk_lt, pk_col, fk_lt, fk_col = e["right_table"], e["right_on"], e["left_table"], e["left_on"]
        if pk_lt not in subtables or fk_lt not in subtables:
            continue
        pk_vals = col_values(get(pk_lt), pk_col)
        c = containment(get(fk_lt), fk_col, pk_vals)
        if c >= thresh:
            log.append(f"L1 edge {fk_lt}.{fk_col}->{pk_lt}.{pk_col}: containment {c:.2f} OK")
            continue
        # MATCH rules first
        rdf, desc = match_repair(get(fk_lt), fk_col, pk_vals)
        if rdf is not None and containment(rdf, fk_col, pk_vals) >= thresh:
            setdf(fk_lt, rdf); log.append(f"L1 edge {fk_lt}.{fk_col}: MATCH {desc} OK")
            continue
        # then EXPOSE (structural: Phase 1 predictor + LLM)
        if expose_fn and calls[fk_lt] < budget:
            df2 = expose_fn(get(fk_lt), subtables[fk_lt], fk_col); calls[fk_lt] += 1
            if df2 is not None:
                setdf(fk_lt, df2)
                c2 = containment(get(fk_lt), fk_col, pk_vals)
                log.append(f"L1 edge {fk_lt}.{fk_col}: EXPOSE -> containment {c2:.2f}")
                continue
        why = "UNFIXED" if expose_fn else "UNFIXED (EXPOSE not implemented; only value-level MATCH rules were tried)"
        log.append(f"L1 edge {fk_lt}.{fk_col}->{pk_lt}.{pk_col}: containment {c:.2f} {why}")

    return subtables, log
