"""
schema_spec.py
--------------
Parsing and synthesis of the target schema.

Two sources:
  (1) at inference time: the caller supplies a schema specification (in the react
      runner's table_spec format: create_table_sql / column_types / primary_key), parsed
  (2) when building training data: synthesized from the benchmark's db_id + SQL via
      spider/bird tables.json, using SchemaResolver (below).

canon type in {int, float, str, date}。
"""
from __future__ import annotations
import json, re

# ---- raw spider/bird schema files (used when building training data) ----
# Ground-truth schemas, used ONLY by the schema-alignment path, which synthesis
# hard-disables (it rewrites a predicted schema into the database's real one).
# Empty unless explicitly configured; the loaders below tolerate missing files.
from engine_paths import SPIDER_TABLES, SPIDER_TEST_TABLES, BIRD_DEV_TABLES


def canon_type(t: str) -> str:
    t = str(t).lower()
    if "int" in t: return "int"
    if any(k in t for k in ["real", "float", "double", "decimal", "numeric", "number"]): return "float"
    if any(k in t for k in ["date", "time"]): return "date"
    return "str"


# ---------------- (1) inference: parse a schema specification ----------------
def parse_create_table(sql: str):
    """CREATE TABLE T (`col` TYPE, ...) -> ({col: canon_type}, pk_set)。"""
    m = re.search(r"\((.*)\)", sql, re.S)
    body = m.group(1) if m else sql
    schema, pk = {}, set()
    for col_def in re.split(r",(?![^(]*\))", body):
        cd = col_def.strip()
        pm = re.match(r"(?i)PRIMARY\s+KEY\s*\(([^)]*)\)", cd)
        if pm:
            pk |= {c.strip(" `\"") for c in pm.group(1).split(",")}
            continue
        cm = re.match(r"[`\"]?(\w+)[`\"]?\s+([A-Za-z]+(?:\([^)]*\))?)", cd)
        if cm:
            schema[cm.group(1)] = canon_type(cm.group(2))
            if re.search(r"(?i)PRIMARY\s+KEY", cd):
                pk.add(cm.group(1))
    return schema, pk


def spec_to_schema(spec: dict):
    """Accept a react-runner-style schema spec and return ({col: canon_type}, pk_set).

    The spec may carry create_table_sql / column_types / output_columns / primary_key.
    column_types wins when present (it is explicit); otherwise parse create_table_sql.
    """
    pk = set(spec.get("primary_key") or [])
    ctypes = spec.get("column_types") or {}
    if ctypes:
        schema = {c: canon_type(t) for c, t in ctypes.items()}
    elif spec.get("create_table_sql"):
        schema, pk2 = parse_create_table(spec["create_table_sql"])
        pk |= pk2
    else:  # only column names, types unknown -> treat every column as str
        schema = {c: "str" for c in (spec.get("output_columns") or [])}
    return schema, pk


# ---------------- (2) training data: synthesize from SQL + tables.json ----------------
class SchemaResolver:
    def __init__(self):
        self.spider, self.bird = {}, {}
        self._load_spider(SPIDER_TABLES); self._load_spider(SPIDER_TEST_TABLES)
        self._load_bird(BIRD_DEV_TABLES)

    def _load_spider(self, path):
        for e in json.load(open(path)):
            names = e["table_names_original"]; pk_idx = set(e.get("primary_keys", []))
            per = {i: {"cols": {}, "pk": set()} for i in range(len(names))}
            for gidx, (tidx, col) in enumerate(e["column_names_original"]):
                if tidx < 0: continue
                per[tidx]["cols"][col] = canon_type(e["column_types"][gidx])
                if gidx in pk_idx: per[tidx]["pk"].add(col)
            self.spider[e["db_id"]] = {nm.lower(): per[i] for i, nm in enumerate(names)}

    def _load_bird(self, path):
        for _, v in json.load(open(path)).items():
            db = v["db_id"]; tn = v["table_name_original"].lower()
            cols = {c: canon_type(t) for c, t in zip(v["column_names_original"], v["column_types"])}
            pk = {c for c in cols if c.lower() in ("id", tn + "id", tn + "_id")}
            self.bird.setdefault(db, {})[tn] = {"cols": cols, "pk": pk}

    @staticmethod
    def _from_tables(sql):
        toks = re.findall(r"\b(?:FROM|JOIN)\s+([`\"\[]?\w+[`\"\]]?)", sql, re.I)
        seen, out = set(), []
        for t in toks:
            t = t.strip("`\"[]").lower()
            if t not in seen: seen.add(t); out.append(t)
        return out

    def resolve(self, db_id, sql, source):
        book = self.bird if source == "bird" else self.spider
        tabs = book.get(db_id)
        if not tabs: return None, None, None
        for t in self._from_tables(sql):
            if t in tabs: return dict(tabs[t]["cols"]), set(tabs[t]["pk"]), t
        if len(tabs) == 1:
            only = next(iter(tabs.values())); return dict(only["cols"]), set(only["pk"]), next(iter(tabs))
        return None, None, None


def sql_view_schema(sql: str, full_schema: dict, pk=frozenset()):
    """Synthesize a view schema from the columns the SQL references that belong to this

    full_schema: this table's complete schema {col: type}, from tables.json.
    Returns ({col: type} subset, pk_in_view). Falls back to the full schema when nothing
    """
    def _n(x): return re.sub(r"[^a-z0-9]", "", str(x).lower())
    norm_to_col = {_n(c): c for c in full_schema}
    # Every identifier token in the SQL (including the col part of alias.col)
    tokens = set()
    for m in re.finditer(r"(?:[A-Za-z_]\w*\s*\.\s*)?([A-Za-z_]\w*)", sql):
        tokens.add(_n(m.group(1)))
    hit = [norm_to_col[t] for t in tokens if t in norm_to_col]
    if not hit:
        return dict(full_schema), set(pk)
    # Keep the full schema's column order
    view = {c: full_schema[c] for c in full_schema if c in hit}
    view_pk = {c for c in pk if c in view}
    return view, view_pk


_DEFAULT_RESOLVER = None


def _get_resolver():
    global _DEFAULT_RESOLVER
    if _DEFAULT_RESOLVER is None:
        _DEFAULT_RESOLVER = SchemaResolver()
    return _DEFAULT_RESOLVER


def expand_view_to_full(view_spec, db_id: str, source: str, resolver: "SchemaResolver | None" = None):
    """Expand the minimal view schema used at inference into the same full DB table schema

    Method: use the view's column names to find the best-covered table in the db_id's
    database, and return that table's full column schema plus primary key. This aligns the

    view_spec: dict (runner table_spec) / CREATE TABLE string / list of column names.
    Returns ({col: canon_type}, pk_set). Falls back to the view itself when no DB table
    """
    R = resolver or _get_resolver()
    # Extract the view's column names
    if isinstance(view_spec, str):
        vcols = list(parse_create_table(view_spec)[0].keys())
    elif isinstance(view_spec, dict):
        vsc, _ = spec_to_schema(view_spec); vcols = list(vsc.keys())
    else:
        vcols = list(view_spec)

    book = R.bird if source == "bird" else R.spider
    tabs = book.get(db_id)
    if not tabs:
        # Fallback: no database schema available, so use the view itself
        if isinstance(view_spec, str):
            return parse_create_table(view_spec)
        if isinstance(view_spec, dict):
            return spec_to_schema(view_spec)
        return {c: "str" for c in vcols}, set()

    want = {re.sub(r"[^a-z0-9]", "", c.lower()) for c in vcols}
    best, best_cov = None, -1
    for _, info in tabs.items():
        cov = len({re.sub(r"[^a-z0-9]", "", c.lower()) for c in info["cols"]} & want)
        if cov > best_cov:
            best_cov, best = cov, info
    if best is None or best_cov <= 0:
        if isinstance(view_spec, str):
            return parse_create_table(view_spec)
        return {c: "str" for c in vcols}, set()
    return dict(best["cols"]), set(best["pk"])


def schema_to_sql(schema: dict, pk=frozenset(), table="T") -> str:
    """{col: canon_type} + pk -> a CREATE TABLE string (for display in an example)."""
    sqlmap = {"int": "INT", "float": "DOUBLE", "date": "DATE", "str": "VARCHAR(255)"}
    cols = [f"`{c}` {sqlmap.get(t, 'VARCHAR(255)')}" for c, t in schema.items()]
    if pk: cols.append(f"PRIMARY KEY ({', '.join(pk)})")
    return f"CREATE TABLE {table} (" + ", ".join(cols) + ");"
