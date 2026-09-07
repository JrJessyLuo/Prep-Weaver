"""Run a SQL-emitting baseline and capture what it produced.

`tracer.py` watches pandas. A baseline like pneuma emits SQL instead, so
nothing it does passes through pandas at all and that tracer sees an empty run.
Reporting such a method as all-zeros would be wrong in the worst way -- it would
read as "it got everything wrong" rather than "we did not measure it" -- so the
SQL path is handled here rather than skipped.

What is scored is NOT "every table the script left behind". It is:

    columns   the base-table columns the statements actually reference, found by
              parsing, plus the columns of each CTE. Replaying the script and
              dumping the whole catalog instead would count the method's own
              scratch and diagnostic tables as prepared output and inflate table
              correctness.

    joins     every equality whose two sides resolve to two different base
              tables, plus semi-joins written as `x IN (SELECT y ...)`. A side
              may be a derived expression (`split_part(...)`), so each side is
              evaluated over its source table rather than read as a column name.

Both are what the reference evaluator's SQL path extracts; this module follows
it so the two agree. Requires `duckdb` and `sqlglot`.
"""

from __future__ import annotations

import contextlib
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd

RESULT_TABLE = "conductor_s_execution"

# The generator emits diagnostic queries that build and drop this table. They
# are not part of the solution, and counting their columns as prepared output
# inflates coverage.
DIAGNOSTIC_TABLES = ("conductor_assumption_check",)

# The producing driver sometimes double-wraps a statement: it prepends
# `CREATE OR REPLACE TABLE "x" AS` to a body that is ALREADY a full
# `CREATE OR REPLACE TABLE x AS ...`. The result is invalid SQL that parses only
# as an opaque command, and all lineage is lost. The artefacts ship that way and
# are left untouched; the redundant prefix is stripped here at read time, which
# is what the reference evaluator does. The lookahead makes this fire only when
# `... AS` is immediately followed by another CREATE, never on a normal chain.
_DOUBLE_CREATE = re.compile(
    r'CREATE\s+OR\s+REPLACE\s+TABLE\s+"?\w+"?\s+AS\s+(?=CREATE\s+OR\s+REPLACE\s+TABLE\b)',
    re.IGNORECASE)

# DuckDB does not take PostgreSQL-style TO_CHAR(x, 'fmt'). Scoring needs value
# presence, not display formatting, so degrade it rather than let the whole
# statement fail.
_TO_CHAR_FMT = re.compile(
    r"TO_CHAR\s*\(\s*([^,()]+(?:\([^)]*\))?[^,]*)\s*,\s*'[^']*'\s*\)", re.IGNORECASE)


def _rewrite_to_char(sql: str) -> str:
    prev = None
    while prev != sql:
        prev = sql
        sql = _TO_CHAR_FMT.sub(r"CAST(\1 AS VARCHAR)", sql)
    return sql


def extract_statements(S) -> List[str]:
    """A list | a python script with embedded SQL | raw SQL -> flat statements."""
    import sqlglot

    if isinstance(S, (list, tuple)):
        blocks = list(S)
    else:
        blocks = [a or b for a, b in
                  re.findall(r"'''(.*?)'''|\"\"\"(.*?)\"\"\"", str(S), re.DOTALL)]
        if not blocks and str(S).strip():
            blocks = [str(S)]

    out = []
    for blk in blocks:
        blk = _rewrite_to_char(_DOUBLE_CREATE.sub("", str(blk)))
        try:
            parsed = sqlglot.parse(blk, read="duckdb")
        except Exception:
            continue
        for one in parsed:
            if one is None:
                continue
            s = _rewrite_to_char(one.sql(dialect="duckdb"))
            if s.strip() and not any(d in s.lower() for d in DIAGNOSTIC_TABLES):
                out.append(s)
    return out


# ---------------------------------------------------------------- duckdb setup

def _qident(x) -> str:
    return '"' + str(x).replace('"', '""') + '"'


def _table_ref(table: str) -> str:
    if isinstance(table, str) and "." in table:
        schema, name = table.split(".", 1)
        return f"{_qident(schema)}.{_qident(name)}"
    return _qident(table)


def _duckdb_safe(df: pd.DataFrame) -> pd.DataFrame:
    """Drop pandas extension string dtypes back to object before registering.

    duckdb does not recognise pandas' `str`/`string` extension dtype and raises
    on register. That failure is caught per table, so the run continues with the
    table simply missing and the method scores zero for reasons that have
    nothing to do with the method. Values are unchanged by the cast.
    """
    bad = [c for c in df.columns
           if isinstance(df[c].dtype, pd.api.extensions.ExtensionDtype)
           and str(df[c].dtype).lower() in ("str", "string")]
    if not bad:
        return df
    out = df.copy()
    for c in bad:
        out[c] = out[c].astype(object)
    return out


def _catalog(con) -> Dict[str, Dict[str, str]]:
    schema: Dict[str, Dict[str, str]] = defaultdict(dict)
    with contextlib.suppress(Exception):
        for ts, t, c in con.execute(
                "SELECT table_schema, table_name, column_name "
                "FROM information_schema.columns").fetchall():
            key = t if ts in (None, "", "main", "temp") else f"{ts}.{t}"
            schema[key][c] = "TEXT"
    return dict(schema)


def _resolve(t, existing):
    if not t or t in existing:
        return t
    m = [e for e in existing if e.split(".")[-1].lower() == str(t).lower()]
    return m[0] if len(m) == 1 else t


def _valueset(con, table, col) -> List[str]:
    try:
        rows = con.execute(
            f"SELECT DISTINCT {_qident(col)} FROM {_table_ref(table)}").fetchall()
        return [r[0] for r in rows if r[0] is not None]
    except Exception:
        return []


# -------------------------------------------------------------- static analysis

def _qualify(tree, schema):
    from sqlglot.optimizer.qualify import qualify
    try:
        return qualify(tree, schema=schema, dialect="duckdb", expand_stars=True,
                       validate_qualify_columns=False)
    except Exception:
        return tree


def _analyze(sql, schema):
    """Parse and fully resolve. optimize() inlines CTEs and qualifies columns to
    base tables, which is what makes CTE-heavy SQL traceable at all."""
    import sqlglot
    tree = sqlglot.parse_one(sql, read="duckdb")
    try:
        from sqlglot.optimizer import optimize
        return optimize(tree, schema=schema, dialect="duckdb")
    except Exception:
        return _qualify(tree, schema)


def _table_key(t) -> str:
    db = t.args.get("db")
    if db:
        return f"{db.name if hasattr(db, 'name') else db}.{t.name}"
    return t.name


def _alias_map(tree) -> Dict[str, str]:
    from sqlglot import exp
    amap: Dict[str, str] = {}
    for t in tree.find_all(exp.Table):
        real = _table_key(t)
        amap[real] = real
        amap[t.name] = real
        if t.alias:
            amap[t.alias] = real
    return amap


def _collect_touched(tree, touched, amap, existing) -> None:
    from sqlglot import exp
    for col in tree.find_all(exp.Column):
        t = _resolve(amap.get(col.table, col.table), existing)
        if t and col.name and col.name != "*":
            touched[t].add(col.name)


def _side_tables(node, amap, existing):
    from sqlglot import exp
    return {t for t in (_resolve(amap.get(c.table, c.table), existing)
                        for c in node.find_all(exp.Column)) if t in existing}


def _side_values(con, side, table) -> List[str]:
    """Evaluate one side of a join condition over its source table.

    A side is often a derived expression rather than a bare column, so it is
    evaluated rather than looked up by name.
    """
    from sqlglot import exp
    node = side.copy()
    for c in node.find_all(exp.Column):
        c.set("table", None)
    expr = _rewrite_to_char(node.sql(dialect="duckdb"))
    try:
        rows = con.execute(
            f"SELECT DISTINCT {expr} FROM {_table_ref(table)}").fetchall()
        return [r[0] for r in rows if r[0] is not None]
    except Exception:
        return []


def _append_join(con, joins, left, right, amap, existing) -> None:
    lt, rt = _side_tables(left, amap, existing), _side_tables(right, amap, existing)
    if len(lt) == 1 and len(rt) == 1 and lt != rt:
        lv = _side_values(con, left, next(iter(lt)))
        rv = _side_values(con, right, next(iter(rt)))
        if lv or rv:
            joins.append({"left": lv, "right": rv})


def _projections(node):
    from sqlglot import exp
    if node is None:
        return []
    if isinstance(node, exp.Subquery):
        node = node.this
    if isinstance(node, exp.Select):
        return list(node.expressions or [])
    sel = node.find(exp.Select) if hasattr(node, "find") else None
    return list(sel.expressions or []) if isinstance(sel, exp.Select) else []


def _semi_join_from_in(con, joins, in_node, amap, existing) -> None:
    """`WHERE outer IN (SELECT inner ...)` is a join key even with no JOIN clause."""
    from sqlglot import exp
    left = in_node.this
    query = (in_node.args.get("query") or in_node.args.get("expression")
             or in_node.expression)
    proj = _projections(query)
    if left is None or not proj:
        return
    right = proj[0]
    if isinstance(right, exp.Alias):
        right = right.this
    _append_join(con, joins, left, right, amap, existing)


def _materialize_ctes(con, tree, existing, cte_tables) -> None:
    """Persist each `WITH x AS (...)` as a table.

    Join keys frequently live on CTE-derived columns; without this they point at
    names that are not queryable and the key is lost. CTEs are defined in
    dependency order, so materializing in order lets later ones see earlier ones.
    """
    from sqlglot import exp
    with_ = tree.find(exp.With)
    if not with_:
        return
    for cte in with_.expressions:
        name, query = cte.alias, cte.this
        if not name or query is None:
            continue
        with contextlib.suppress(Exception):
            con.execute(f'CREATE OR REPLACE TABLE "{name}" AS '
                        f'{query.sql(dialect="duckdb")}')
            existing.add(name)
            cte_tables.add(name)


# --------------------------------------------------------------------- entry

def run_sql(statements, tables: Dict[str, pd.DataFrame],
            timeout: int = 120) -> dict:
    """Execute the generated SQL. Returns {frames, joins, result, error}.

    `frames` is one single-column frame per referenced base column and per CTE
    column, not the catalog: see the module docstring.
    """
    try:
        import duckdb           # noqa: F401
        import sqlglot          # noqa: F401
        from sqlglot import exp
    except ImportError as exc:
        return {"frames": [], "joins": [], "result": None,
                "error": f"{exc}; `pip install duckdb sqlglot` to score SQL baselines"}

    stmts = extract_statements(statements)
    if not stmts:
        return {"frames": [], "joins": [], "result": None, "error": "no statements"}

    import duckdb
    con = duckdb.connect(":memory:")
    err = None
    frames: List[pd.DataFrame] = []
    joins: List[dict] = []
    result = None
    try:
        for name, df in (tables or {}).items():
            try:
                tmp = "__src_" + re.sub(r"[^A-Za-z0-9_]", "_", str(name))
                con.register(tmp, _duckdb_safe(df))
                con.execute(f"CREATE OR REPLACE TABLE {_table_ref(name)} "
                            f"AS SELECT * FROM {_qident(tmp)}")
            except Exception as exc:
                err = err or f"register {name}: {type(exc).__name__}: {exc}"

        # 1. replay in order; a later statement may work after an earlier failure
        for s in stmts:
            try:
                cur = con.execute(s)
                if s.lstrip().lower().startswith(("select", "with")):
                    result = cur.fetchdf()
            except Exception as exc:
                err = err or f"{type(exc).__name__}: {exc}"
        with contextlib.suppress(Exception):
            result = con.execute(f'SELECT * FROM "{RESULT_TABLE}"').fetchdf()

        # 2. static extraction against the materialized catalog
        schema = _catalog(con)
        existing = set(schema)
        touched: Dict[str, set] = defaultdict(set)
        cte_tables: set = set()

        for s in stmts:
            try:
                raw = _qualify(sqlglot.parse_one(s, read="duckdb"), schema)
                raw_amap = _alias_map(raw)
            except Exception:
                raw, raw_amap = None, {}
            if raw is not None:
                # Semi-joins are read off the un-optimized tree: optimize() can
                # rewrite `a IN (SELECT b ...)` into a join against a synthetic
                # CTE, which hides the base-table relationship entirely.
                _materialize_ctes(con, raw, existing, cte_tables)
                for node in raw.find_all(exp.In):
                    _semi_join_from_in(con, joins, node, raw_amap, existing)
            try:
                tree = _analyze(s, schema)
            except Exception:
                continue
            amap = _alias_map(tree)
            _collect_touched(tree, touched, amap, existing)
            for eq in tree.find_all(exp.EQ):
                _append_join(con, joins, eq.this, eq.expression, amap, existing)

        # 3. one frame per referenced base column, plus every CTE column. A CTE
        #    column is a prepared column too (`split_part(...) AS setcode` exists
        #    nowhere else); value matching is asymmetric, so an aggregate or
        #    mixed column cannot match a gold column and inflate coverage.
        for t, cols in touched.items():
            if t not in existing:
                continue
            for c in cols:
                vs = _valueset(con, t, c)
                if vs:
                    frames.append(pd.DataFrame({f"{t}.{c}": vs}))
        full = _catalog(con)
        for t in cte_tables:
            for c in full.get(t, {}):
                vs = _valueset(con, t, c)
                if vs:
                    frames.append(pd.DataFrame({f"{t}.{c}": vs}))
    finally:
        with contextlib.suppress(Exception):
            con.close()

    return {"frames": frames, "joins": joins, "result": result, "error": err}


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
