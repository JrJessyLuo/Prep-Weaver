"""Run a SQL-emitting baseline and capture what it produced.

`tracer.py` watches pandas. A baseline like pneuma emits SQL instead, so
nothing it does passes through pandas at all and that tracer sees an empty run.
Reporting such a method as all-zeros would be wrong in the worst way — it would
read as "it got everything wrong" rather than "we did not measure it" — so the
SQL path is handled here rather than skipped.

    tables   every relation the statements leave behind, read back as DataFrames.
             Input tables are registered as `table_1`..`table_n`, matching the
             names the generated SQL refers to.

    joins    the key columns of every equi-join, taken from the SQL text rather
             than from execution. `ON a.x = b.y` names both sides explicitly,
             which is more than the pandas tracer can recover after a merge has
             collapsed them. Each side is resolved to a real relation and its
             value domain read from the database.

Requires `duckdb`. It is an optional dependency: without it this returns an
error for the task rather than failing the run, and every other method still
scores.
"""

from __future__ import annotations

import contextlib
import re
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd


def _split(statements) -> List[str]:
    """The generated SQL as a list of statements."""
    if isinstance(statements, str):
        return [s for s in (x.strip() for x in statements.split(";")) if s]
    out = []
    for s in statements or []:
        out.extend(x.strip() for x in str(s).split(";") if x.strip())
    return out


def _join_pairs(sql: str) -> List[tuple]:
    """[(left_table, left_col, right_table, right_col), ...] from every equi-join.

    Read off the parse tree, not by executing: `ON a.x = b.y` states both key
    columns, whereas after execution the join has already merged them.
    """
    import sqlglot
    from sqlglot import exp

    pairs = []
    try:
        trees = sqlglot.parse(sql, read="duckdb")
    except Exception:
        return pairs
    for tree in trees:
        if tree is None:
            continue
        # alias -> real relation name, so `a.x` resolves to the table `a` stands for
        alias = {}
        for t in tree.find_all(exp.Table):
            nm = t.name
            al = t.alias_or_name
            if nm:
                alias[al] = nm
                alias[nm] = nm
        for j in tree.find_all(exp.Join):
            on = j.args.get("on")
            if on is None:
                continue
            for eq in [on] if isinstance(on, exp.EQ) else list(on.find_all(exp.EQ)):
                l, r = eq.left, eq.right
                if isinstance(l, exp.Column) and isinstance(r, exp.Column):
                    lt = alias.get(l.table or "", l.table or "")
                    rt = alias.get(r.table or "", r.table or "")
                    if lt and rt:
                        pairs.append((lt, l.name, rt, r.name))
    return pairs


def run_sql(statements, tables: Dict[str, pd.DataFrame],
            timeout: int = 120) -> dict:
    """Execute the generated SQL. Returns {frames, joins, result, error}."""
    try:
        import duckdb
    except ImportError:
        return {"frames": [], "joins": [], "result": None,
                "error": "duckdb is not installed; `pip install duckdb` to score "
                         "SQL baselines"}

    stmts = _split(statements)
    if not stmts:
        return {"frames": [], "joins": [], "result": None, "error": "no statements"}

    con = duckdb.connect(":memory:")
    err = None
    try:
        for name, df in tables.items():
            with contextlib.suppress(Exception):
                con.register(name, df)
        for s in stmts:
            try:
                con.execute(s)
            except Exception as exc:          # a later statement may still work
                err = err or f"{type(exc).__name__}: {exc}"

        # Everything the statements left behind, plus the last SELECT's result.
        frames, by_name = [], {}
        with contextlib.suppress(Exception):
            for (rel,) in con.execute(
                    "SELECT table_name FROM information_schema.tables").fetchall():
                with contextlib.suppress(Exception):
                    df = con.execute(f'SELECT * FROM "{rel}"').fetch_df()
                    by_name[rel] = df
                    frames.append(df)
        result = None
        for s in reversed(stmts):
            if s.lstrip().upper().startswith(("SELECT", "WITH")):
                with contextlib.suppress(Exception):
                    result = con.execute(s).fetch_df()
                    frames.append(result)
                break

        joins = []
        for s in stmts:
            for lt, lc, rt, rc in _join_pairs(s):
                lv = _col_values(by_name, tables, lt, lc)
                rv = _col_values(by_name, tables, rt, rc)
                if lv or rv:
                    joins.append({"left": lv, "right": rv})
    finally:
        with contextlib.suppress(Exception):
            con.close()
    return {"frames": frames, "joins": joins, "result": result, "error": err}


def _col_values(by_name: Dict[str, pd.DataFrame],
                tables: Dict[str, pd.DataFrame], rel: str, col: str) -> List[str]:
    """Values of `rel`.`col`, from a created relation or an input table."""
    df = by_name.get(rel)
    if df is None:
        df = tables.get(rel)
    if df is None:
        return []
    key = re.sub(r"[^a-z0-9]", "", str(col).lower())
    for c in df.columns:
        if re.sub(r"[^a-z0-9]", "", str(c).lower()) == key:
            try:
                s = df[c].dropna()
                if len(s) > 20000:
                    s = s.sample(20000, random_state=0)
                return s.astype(str).drop_duplicates().tolist()
            except BaseException:
                return []
    return []


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Column names as the SQL-generating driver saw them.

    lower-case, every run of non-word characters collapsed to "_", leading and
    trailing separators dropped, and duplicates disambiguated with "_1", "_2".
    Verified against the driver's own captured frames: 19 of 20 sampled tasks
    reproduce them exactly, the twentieth because the driver captured a
    different table for that task.
    """
    seen: Dict[str, int] = {}
    names = []
    for c in df.columns:
        base = re.sub(r"\W+", "_", str(c).strip().lower()).strip("_")
        n = seen.get(base, 0)
        seen[base] = n + 1
        names.append(base if n == 0 else f"{base}_{n}")
    out = df.copy(deep=False)
    out.columns = names
    return out
