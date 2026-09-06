#!/usr/bin/env python3
"""
param_hints.py
--------------
Approach 2: derive parameter candidates for structural ops deterministically from the
table structure (reusing the feature signals). Used as a strong hint for the LLM (hit

split_column_hint(df, schema) -> {source_column, delimiter, n_parts} | None
pivot_hint(df, schema)        -> {index, columns, values} | None
"""
from __future__ import annotations
import re
import pandas as pd

_ATTR_NAMES = {"attribute", "variable", "metric", "key", "type", "code", "field",
               "record_id", "recordid", "stationid", "station_id"}


def _norm(x): return re.sub(r"[^a-z0-9]", "", str(x).lower())


# Both hint functions below are heuristics about a column's SHAPE — does it hold
# packed values, does it look like an attribute-name column — and neither needs
# the whole column to decide. On beaver they were the stage-3 hotspot: pivot_hint
# regex-normalises every DISTINCT value of every object column, and beaver
# columns run to hundreds of thousands of distinct values, while the target
# schema it compares against has a few dozen names. Below the cap the frame is
# untouched, so bird/spider (whose tables are far smaller) are byte-identical.
_HINT_ROW_CAP = 50_000


def _cap(df: pd.DataFrame) -> pd.DataFrame:
    return df.head(_HINT_ROW_CAP) if len(df) > _HINT_ROW_CAP else df


def split_column_hint(df: pd.DataFrame, schema=None):
    """Packed columns: values hold a stable separator and split into a consistent number of
    parts; pure numeric and date columns are excluded. Columns whose NAME itself splits into the target column names are preferred (e.g. format_status -> format+status)."""
    df = _cap(df)
    tgt = {_norm(c) for c in (schema or {})}
    best = None  # (name_match, n_parts, col, delim)
    for c in df.columns:
        s = df[c].astype(str)
        if pd.to_numeric(s, errors="coerce").notna().mean() > 0.9:      # pure numeric column, not packed
            continue
        if pd.to_datetime(s, errors="coerce").notna().mean() > 0.7:      # date column, excluded
            continue
        for d in ["-", "_", "/", "|", ",", " "]:
            frac = s.str.contains(re.escape(d), regex=True).mean()
            if frac > 0.8:
                pl = s.str.split(d).map(len)
                if pl.nunique() == 1 and pl.iloc[0] >= 2:
                    name_parts = {_norm(p) for p in re.split(r"[_\-/ ]", str(c)) if p}
                    nm = len(name_parts & tgt)
                    cand = (nm, int(pl.iloc[0]), str(c), d)
                    if best is None or cand > best:
                        best = cand
    if best is None:
        return None
    return {"source_column": best[2], "delimiter": best[3], "n_parts": best[1]}


def pivot_hint(df: pd.DataFrame, schema: dict):
    """Long table -> Pivot: columns = the attribute column (by naming rule or by matching target column names); values = the data column; index = the remaining keys."""
    df = _cap(df)
    tgt = {_norm(c) for c in (schema or {})}
    cols_cand = None
    # 1) naming rule
    for c in df.columns:
        if _norm(c) in _ATTR_NAMES:
            cols_cand = str(c); break
    # 2) the object column whose values match the most target column names
    if cols_cand is None:
        best_hit = 0
        for c in df.columns:
            if df[c].dtype == object:
                vals = {_norm(v) for v in df[c].astype(str).unique()}
                hit = len(vals & tgt)
                if hit > best_hit:
                    best_hit, cols_cand = hit, str(c)
        if best_hit < 2:
            cols_cand = None
    if cols_cand is None:
        return None
    others = [str(c) for c in df.columns if str(c) != cols_cand]
    val_col = next((c for c in others if _norm(c) in ("value", "val", "values")), None)
    if val_col is None and others:
        val_col = others[-1]
    index = [c for c in others if c != val_col]
    if not index or val_col is None:
        return None
    return {"index": index, "columns": cols_cand, "values": val_col}
