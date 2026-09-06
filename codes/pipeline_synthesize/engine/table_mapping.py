#!/usr/bin/env python3
"""
table_mapping.py
----------------
Scale-up, step one: from benchmark.jsonl, map each query's gold input tables to DB

- gold table = the logical table (table_N) referenced by tol_ops Join / dc_ops; the other
- mapping: tol_ops Join(table_N, on=col) -> input_{N-1} has column col;
        which DB table does col belong to (decided with tables.json) -> that DB table is
  Fallback: score the overlap between the transformed table's columns and each candidate
- join keys: taken from the gold SQL's JOIN..ON and from tol_ops Join(left_on,right_on).

map_task(task, resolver) -> {logical_table: {db_table, schema, pk, join_cols}}
"""
from __future__ import annotations
import os
import re, sys
from pathlib import Path

ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
for p in (str(ROOT / "dependency_modeling_react_joint"), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

from schema_spec import SchemaResolver


def _norm(x): return re.sub(r"[^a-z0-9]", "", str(x).lower())


def sql_tables(sql: str) -> list[str]:
    """Table names after FROM/JOIN in the SQL (subqueries included), de-duplicated in order."""
    out, seen = [], set()
    for m in re.finditer(r"\b(?:FROM|JOIN)\s+([`\"\[]?\w+[`\"\]]?)", sql, re.I):
        t = m.group(1).strip("`\"[]")
        if t.lower() not in seen:
            seen.add(t.lower()); out.append(t)
    return out


def tol_join_edges(task) -> list[dict]:
    """Extract (left_table, left_on, right_table, right_on) from tol_ops Join."""
    edges = []
    for op in task.get("tol_ops") or []:
        if not op.startswith("Join"):
            continue
        d = {}
        for k in ("left_table", "right_table", "left_on", "right_on"):
            m = re.search(rf'{k}\s*=\s*"([^"]+)"', op)
            if m:
                d[k] = m.group(1)
        if {"left_table", "right_table", "left_on", "right_on"} <= set(d):
            edges.append(d)
    return edges


def _db_tables_for(resolver, db_id, source):
    return (resolver.bird if source == "bird" else resolver.spider).get(db_id, {})


def map_task(task, resolver, source="bird", input_cols=None) -> dict:
    """input_cols: optional {logical_table: set(columns of that input table)}, the content fallback for ambiguous cases."""
    db_id = task["db_id"]
    tabs = _db_tables_for(resolver, db_id, source)                 # {db_table_lower: {cols, pk}}
    cand_names = [t for t in sql_tables(task["sql"]) if t.lower() in tabs]  # tables in the SQL that exist in the database
    edges = tol_join_edges(task)

    # Collect the gold logical tables and their join columns (excluding _join intermediates)
    logical_cols: dict[str, set] = {}
    for e in edges:
        for side, on in (("left_table", "left_on"), ("right_table", "right_on")):
            lt = e[side]
            if "_join" in lt:
                continue
            logical_cols.setdefault(lt, set()).add(e[on])

    def owners(col, used):
        return [t for t in cand_names if t.lower() not in used
                and _norm(col) in {_norm(c) for c in tabs[t.lower()]["cols"]}]

    def content_pick(lt, avail):
        """Content fallback: the candidate DB table whose columns overlap the input's most."""
        ic = {_norm(c) for c in (input_cols or {}).get(lt, set())}
        if not ic:
            return None
        best, bs = None, -1
        for t in avail:
            s = len(ic & {_norm(c) for c in tabs[t.lower()]["cols"]})
            if s > bs:
                bs, best = s, t
        return best if bs > 0 else None

    out, used = {}, set()
    pending = dict(logical_cols)
    # Constraint propagation: repeatedly assign tables with a unique candidate; when stuck,
    while pending:
        progressed = False
        for lt in list(pending):
            cands = set()
            for col in pending[lt]:
                cands |= set(owners(col, used))
            if len(cands) == 1:
                t = cands.pop()
                out[lt] = t; used.add(t.lower()); del pending[lt]; progressed = True
        if progressed:
            continue
        # Nothing uniquely assignable -> use the content fallback on the first pending one,
        lt = next(iter(pending))
        cands = set()
        for col in pending[lt]:
            cands |= set(owners(col, used))
        pick = content_pick(lt, cands) or (sorted(cands)[0] if cands else None)
        if pick is None:
            del pending[lt]
        else:
            out[lt] = pick; used.add(pick.lower()); del pending[lt]

    return {lt: {"db_table": t, "schema": dict(tabs[t.lower()]["cols"]),
                 "pk": set(tabs[t.lower()]["pk"]), "join_cols": sorted(logical_cols[lt])}
            for lt, t in out.items()}


# ---------------- validation: against the oracle spec's file->columns ----------------
if __name__ == "__main__":
    import json
    import test_single_ops_type as T
    AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
    btask = T.load_benchmark("nl2sql-bird", "dev", AUTOP)
    specs = {r["task_id"]: r for r in T.load_jsonl(
        ROOT / "dependency_modeling_react_joint/results/oracle_v1_group_a_specs.jsonl")}
    cids = sorted(set(T.load_case_ids(
        ROOT / "pipeline_eval/cases_group_a_high_ops_union_structural.jsonl", "nl2sql-bird")))
    R = SchemaResolver()

    from schema_spec import parse_create_table
    tot = ok = 0
    for tid in cids:
        task = btask.get(tid)
        if not task:
            continue
        mp = map_task(task, R, "bird")
        # oracle spec: table_file -> the columns of create_table_sql (the gold mapping reference)
        sp = specs.get(tid)
        spec_cols = {}
        for ts in (sp.get("table_specs") if sp else []) or []:
            tf = ts.get("table_file"); csql = ts.get("create_table_sql")
            if tf and csql:
                idx = re.search(r"_input_(\d+)\.pkl", tf)
                if idx:
                    spec_cols[f"table_{int(idx.group(1))+1}"] = set(_norm(c) for c in parse_create_table(csql)[0])
        for lt, spc in spec_cols.items():
            if lt not in mp:
                continue  # this logical table is not in a join (no tol edge); not scored here
            tot += 1
            mapped = {_norm(c) for c in mp[lt]["schema"]}
            covered = spc <= mapped   # the mapped DB table columns should be a superset of the spec columns
            ok += int(covered)
            if not covered:
                print(f"  MISMATCH {tid} {lt}: db_table={mp[lt]['db_table']} spec_cols={spc-mapped} not covered")
    print(f"\nMapping validation (spec columns covered by the mapped table): {ok}/{tot}")
