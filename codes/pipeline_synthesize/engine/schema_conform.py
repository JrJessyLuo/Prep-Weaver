#!/usr/bin/env python3
"""
schema_conform.py — coerce a produced subtable to the type the plan declared
============================================================================

Lives on its own, imported by BOTH `pipeline_synthesize` (which applies it after
join repair) and the scripts `export_for_eval` emits (which the evaluator runs).

WHY IT IS NOT LEFT INSIDE pipeline_synthesize
---------------------------------------------
It was, and the exported scripts therefore did not conform at all: conformance is
not one of the recorded operator `steps`, so replaying the steps reproduced the
PRE-conform frames. `score_subtables` reads tables.pkl and saw the pass;
`eval_all_oom` runs the exported scripts and did not — the same run scored .608
under one and .592 under the other, and every conformance measurement was
invisible to the metric used against the baselines.

Importing `pipeline_synthesize` from the generated scripts would fix that and
cost too much: it pulls in the bounded explore loop and the operator policy model
while the evaluator holds a 50-second alarm over the whole execution. Hence a
module with nothing but pandas behind it.
"""
from __future__ import annotations

import collections
import datetime
import os
import re

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# The relational plan states a TYPE for every target column and nothing in this
# stage ever enforced it. On nl2sql-spider the benchmark ships columns whose
# cells carry literal quote characters — `Paper.year` holds the 6-character
# string `"2000"` while the plan declares `year DOUBLE`, and `Author.author_id`
# holds `"0"` against `author_id DOUBLE`. The value-based scorer compares the
# string, so every such column misses, and because these are frequently the ID
# columns the damage lands hardest on the join keys.
#
# Measured by patching a finished run's tables.pkl and re-scoring it (see
# pipeline_eval/whatif_fixes.py), stripping the quotes alone is worth, with the
# gold plan installed on spider:
#     subtable_full  .650 -> .683      join_key_full  .792 -> .883
# Coercing to the declared type is a superset of that, and it is what the SOTA
# scripts do universally (astype / pd.to_numeric / str.strip) — it was the one
# purely mechanical difference between their output and ours.
#
# WHY IT IS NOT A DETECTOR. The obvious-looking home for this was a new
# `quoted_value_columns` grounding detector next to the other four. It does not
# belong there: those detectors decide the SHAPE of the target schema, and a
# quote around a value changes no column name. The plan was already correct here
# — it said DOUBLE — so nothing upstream needs to learn anything. This is stage 3
# failing to deliver what it was told to deliver.
_NUMERIC_SQL = re.compile(r"\b(INT|INTEGER|BIGINT|SMALLINT|TINYINT|DOUBLE|FLOAT|REAL|"
                          r"DECIMAL|NUMERIC)\b", re.I)
_WRAPPED = re.compile(r'^\s*(["\'])(.*)\1\s*$', re.S)
# En dash, em dash, minus sign, non-breaking hyphen — the corruption substitutes these
# for a plain hyphen in a few cells of a column whose other cells keep the hyphen.
_DASHES = re.compile("[‐‑‒–—―−]")
_WS = re.compile(r"\s+")

# Formats the benchmark's date columns actually use. Order matters only in that the
# first one to parse every non-null cell wins; the column is then rewritten in the
# format the PLURALITY of its own cells already matched.
_DATE_FORMATS = ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
                 "%d %B %Y", "%B %d, %Y", "%d/%m/%Y %H:%M:%S", "%m/%d/%Y %H:%M:%S",
                 "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
                 # Observed as the MINORITY spelling inside otherwise-ISO columns
                 # (spider_f314403d.shipment_date): a 12-hour clock and an
                 # abbreviated month. Without them the column fails closed and
                 # keeps both spellings.
                 "%d/%m/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p",
                 "%b %d, %Y %H:%M:%S", "%B %d, %Y %H:%M:%S", "%b %d, %Y")


def _unwrap(v):
    """`"2000"` -> `2000`. Only a symmetric wrapping pair is removed, so an
    apostrophe inside a name (`O'Brien`) and a quoted phrase inside free text
    are both left alone."""
    if not isinstance(v, str):
        return v
    m = _WRAPPED.match(v)
    return m.group(2) if m else v


def _map_by_value(s: pd.Series, f) -> pd.Series:
    """`s.map(f)` computed once per DISTINCT value instead of once per row.

    Every transform in this module is a pure function of the cell value, so
    evaluating it on the distinct values and gathering the results back is
    exactly equivalent — `factorize` + a numpy take, both vectorised. Beaver
    columns run to millions of rows over a few thousand distinct values, where
    the per-row form dominated the whole conformance pass; on bird/spider the
    two forms agree cell for cell (regression-tested), it is only faster.
    """
    if len(s) < 1000:
        return s.map(f)                     # not worth factorising
    try:
        codes, uniq = pd.factorize(s, use_na_sentinel=True)
    except Exception:
        return s.map(f)
    mapped = np.empty(len(uniq), dtype=object)
    for i, u in enumerate(uniq):
        mapped[i] = f(u)
    missing = codes == -1
    out = np.empty(len(s), dtype=object)
    out[~missing] = mapped[codes[~missing]]
    if missing.any():
        # factorize collapses None / NaN / pd.NA onto one sentinel, so the
        # missing cells must be copied from the original rather than mapped —
        # otherwise a None column would come back as NaN. Every f here returns
        # non-strings unchanged, so passing them through is what map() did too.
        out[missing] = s.to_numpy(dtype=object)[missing]
    return pd.Series(out, index=s.index)


def _tidy(v):
    """Whitespace and dash hygiene: `"History\\tcollection"` -> `History collection`.

    Applied to string-typed targets only. Collapsing runs of whitespace to one space
    and mapping unicode dashes onto the ASCII hyphen are both information-preserving
    for these columns — the benchmark inserts a tab or an en dash into a handful of
    cells of an otherwise uniform column.
    """
    if not isinstance(v, str):
        return v
    return _WS.sub(" ", _DASHES.sub("-", _unwrap(v))).strip()


def _despace_separators(s: pd.Series) -> pd.Series:
    """`90 - APIE - 10` -> `90-APIE-10`, but only where the column says so.

    Same majority principle as the date pass: the corruption pads the separator in a
    few cells of a column whose other cells have none, so the unpadded form is the
    column's own convention. Applied only when a strict majority of the hyphenated
    cells are unpadded — a column that genuinely writes ` - ` everywhere keeps it.
    """
    vals = [v for v in s if isinstance(v, str) and "-" in v]
    if len(vals) < 3:
        return s
    padded = sum(1 for v in vals if re.search(r"\s-|-\s", v))
    if padded == 0 or padded > len(vals) / 2:
        return s
    return _map_by_value(s, lambda v: re.sub(r"\s*-\s*", "-", v) if isinstance(v, str) else v)


def _unify_spelling(s: pd.Series) -> pd.Series:
    """`['Issued','PAID','Paid','iSSued','paid']` -> `['Issued','Paid']`.

    The corruption rewrites the CASE of a few cells, and pads others with
    decoration (`_red_` beside `blue`), inside a column whose values are otherwise
    one small fixed vocabulary. Measured misses that are nothing but this:
        spider_f314403d  ours ['Issued','PAID','Paid','iSSued','paid']  gold ['Issued','Paid']
        spider_7f4820f3  ours ['Red','_red_','blue']                    gold ['blue','red']
    The scorer compares value sets, so five spellings of two values cover neither.

    Same majority rule as the date pass: values that agree once case and padding
    are removed are the SAME value, and the spelling most of the rows use is the
    intended one. Deliberately conservative — a group is only collapsed when its
    members differ by nothing except case and stripped padding, so `US` and `us`
    as genuinely distinct codes are untouched only if they never co-occur with a
    padded variant, which is the best a value-blind rule can do.
    """
    vals = [v for v in s if isinstance(v, str) and v.strip()]
    if len(vals) < 3:
        return s
    groups: dict[str, collections.Counter] = {}
    for v in vals:
        groups.setdefault(v.strip(" _-").casefold(), collections.Counter())[v] += 1
    if not any(len(g) > 1 for g in groups.values()):
        return s          # already uniform: change nothing
    canon = {k: g.most_common(1)[0][0] for k, g in groups.items()}
    return _map_by_value(s, lambda v: canon.get(v.strip(" _-").casefold(), v)
                         if isinstance(v, str) else v)


def _majority_date_format(s: pd.Series):
    """The strftime pattern most of this column's cells already match, or None.

    THE PRINCIPLE, which is what makes this gold-free: the corruption rewrites a FEW
    cells of a column, so the column's own majority IS the intended format. Measured
    cases — `Release_Date` holding `1996/02/27` beside `21 November 1999`, `event_date`
    holding `15/08/2008 22:16:17` beside `2014-07-15 18:18:15.000000` — are minorities
    inside an otherwise consistent column.

    Requires a strict majority AND at least two distinct formats present; a column that
    is already uniform is left alone, and one with no clear winner is too.
    """
    vals = [str(x) for x in s.dropna()][:200]
    if len(vals) < 3:
        return None
    hits = {}
    for fmt in _DATE_FORMATS:
        n = 0
        for v in vals:
            try:
                datetime.datetime.strptime(v.strip(), fmt)
                n += 1
            except Exception:
                pass
        if n:
            hits[fmt] = n
    if len(hits) < 2:
        return None
    best, n = max(hits.items(), key=lambda kv: kv[1])
    return best if n > len(vals) / 2 else None


def conform_to_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """Coerce each column to the type the plan declared for it.

    Conservative on purpose. A numeric cast runs only if EVERY non-null cell
    parses after unwrapping; one unparseable cell means the column is not what
    the plan thinks it is, and silently turning the rest into NaN would destroy
    a column that today merely has the wrong dtype. Failing closed here keeps
    the change strictly non-destructive: a column is either fully conformed or
    untouched.
    """
    if not schema:
        return df
    out = df.copy()
    lower = {str(c).strip().lower(): c for c in out.columns}
    for col, sqltype in schema.items():
        c = lower.get(str(col).strip().lower())
        if c is None:
            continue
        if out[c].dtype != object:
            # Already numeric: quoting and whitespace cannot apply. Do NOT try to
            # narrow float64 to Int64 so that `1` prints as `1` instead of `1.0` —
            # measured twice now, that is worth exactly zero, because the scorer
            # normalises numerics before comparing. A dump that shows `2.0` beside
            # gold's `2` is an artifact of stringifying the frame yourself, not a
            # mismatch the metric sees.
            continue
        s = _map_by_value(out[c], _unwrap)
        if _NUMERIC_SQL.search(str(sqltype) or ""):
            num = pd.to_numeric(s, errors="coerce")
            if num.isna().sum() == s.isna().sum():   # nothing NEW became null
                out[c] = num
                continue
        # Not numeric, or the cast would have lost cells. Three further passes, each
        # fail-closed, each addressing a measured failure class (see failure_triage:
        # CastType 10, StandardizeString 10, StandardizeDatetime 4 of 41 missing ops).
        s = _unify_spelling(_despace_separators(_map_by_value(s, _tidy)))

        # A date column whose cells disagree about their own format.
        fmt = _majority_date_format(s)
        if fmt:
            conv, lost = [], False
            for v in s:
                if v is None or (isinstance(v, float) and pd.isna(v)):
                    conv.append(v)
                    continue
                for f in _DATE_FORMATS:
                    try:
                        conv.append(datetime.datetime.strptime(str(v).strip(), f).strftime(fmt))
                        break
                    except Exception:
                        continue
                else:
                    lost = True
                    break
            if not lost:
                s = pd.Series(conv, index=s.index)

        # `nan` is not a value. The frame carries NaN, the scorer stringifies, and the
        # column reads "nan" against a gold empty string — three of the six tables
        # inspected failed on exactly this and nothing else.
        out[c] = s.where(s.notna(), "")
    return out


