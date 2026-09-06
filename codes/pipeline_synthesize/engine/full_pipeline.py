#!/usr/bin/env python3
"""
full_pipeline.py
----------------
Whole-task subtable synthesis pipeline (Phase 1 + Phase 2), value-based evaluation, and

Flow, per case:
  1. table_mapping: gold SQL -> for each gold table (input pkl, DB table, full schema,
  2. Phase 1 [parallel]: run the single-table loop per gold table (target = full schema)
  3. Phase 2: build the join graph, fix the anchors (Level 0, PK conditions), then repair
  4. Evaluate: value-based subtable (full/recall) and edge-matched join keys; print and

op-source: gold (mechanism check and ceiling, no LLM) | pipeline (needs OPENAI_API_KEY).
Usage: python3 full_pipeline.py --op-source gold
"""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import os
import sqlglot
from sqlglot import exp

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
for p in (str(HERE), str(ROOT), str(ROOT / "dependency_modeling_react_joint"), str(ROOT / "pipeline_eval")):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_single_ops_type as T
import test_param_synthesis as M
import table_mapping as TM
from schema_spec import SchemaResolver, schema_to_sql
from schema_spec import parse_create_table
from single_table_loop import Loop
from phase2_joinkey import repair_joins, col_values, containment
from eval_react_subtables import fast_norm_series, vmatch, gt_birdspider, score_predictions, norm_values, edge_match

BENCH_DIR = AUTOP / "nl2sql-bird/dev"


# --------------------------------------------------------------------------- #
# VALUE-DOMAIN JOIN-KEY METRIC (ported from eval_two_phase.py so the two runners
# report join_key_full under ONE definition). Name-agnostic: dedup gold edge
# value-domains, cover them one-to-one with our produced key-column domains under
# _oom_vmatch (>=0.8 precision, >=min(2,|gold|) intersection). Replaces the old
# edge_match/pred_edges rollup, which required BOTH endpoints per edge and used a
# different match predicate.
def _oom_norm_values(vals):
    out = set()
    for v in vals or []:
        if v is None:
            continue
        s = str(v).strip()
        if not s or s.lower() in ("nan", "none", "<na>"):
            continue
        try:
            f = float(s)
            s = str(int(f)) if f == int(f) else repr(f)
        except Exception:
            pass
        out.add(s)
    return out


def _oom_vmatch(method_vals, gold_vals):
    method_vals, gold_vals = _oom_norm_values(method_vals), _oom_norm_values(gold_vals)
    if not method_vals or not gold_vals:
        return False
    inter = len(method_vals & gold_vals)
    if inter < min(2, len(gold_vals)):
        return False
    return inter / len(method_vals) >= 0.8


def _dedup_value_domains(domains):
    seen, out = set(), []
    for vals in domains:
        vals = _oom_norm_values(vals)
        if not vals:
            continue
        sig = frozenset(vals)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(vals)
    return out


def _value_domain_jk_frac(pred_keys, gold_domains):
    """Fraction of distinct gold join-key value-domains covered one-to-one by our
    produced key domains (max bipartite matching under _oom_vmatch)."""
    pred = _dedup_value_domains(pred_keys)
    gt = _dedup_value_domains(gold_domains)
    if not gt:
        return None
    match_to_pred = {}

    def dfs(pi, seen):
        for gi, gt_vals in enumerate(gt):
            if gi in seen or not _oom_vmatch(pred[pi], gt_vals):
                continue
            seen.add(gi)
            if gi not in match_to_pred or dfs(match_to_pred[gi], seen):
                match_to_pred[gi] = pi
                return True
        return False

    matched = sum(1 for pi in range(len(pred)) if dfs(pi, set()))
    return matched / len(gt)


def _max_domain_matching_local(pred_domains, gold_domains):
    pred = _dedup_value_domains(pred_domains or [])
    gold = _dedup_value_domains(gold_domains or [])
    match_to_pred = {}

    def dfs(pi, seen):
        for gi, gt_vals in enumerate(gold):
            if gi in seen or not _oom_vmatch(pred[pi], gt_vals):
                continue
            seen.add(gi)
            if gi not in match_to_pred or dfs(match_to_pred[gi], seen):
                match_to_pred[gi] = pi
                return True
        return False

    matched = sum(1 for pi in range(len(pred)) if dfs(pi, set()))
    return matched, len(gold)


def _max_group_matching(pred_groups, gold_groups):
    match_to_pred = {}

    def dfs(pi, seen):
        for gi, gold_group in enumerate(gold_groups):
            if gi in seen:
                continue
            matched, total = _max_domain_matching_local(pred_groups[pi], gold_group)
            if not total or matched < total:
                continue
            seen.add(gi)
            if gi not in match_to_pred or dfs(match_to_pred[gi], seen):
                match_to_pred[gi] = pi
                return True
        return False

    matched = sum(1 for pi in range(len(pred_groups)) if dfs(pi, set()))
    return matched, len(gold_groups)


def _gold_subtable_groups(tid):
    try:
        d = json.loads((AUTOP / "nl2sql-bird/dev/outputs" / f"{tid}.json").read_text())
    except Exception:
        return []
    db_path = d.get("db_path")
    table_columns = d.get("table_columns") or {}
    if not db_path or not Path(db_path).exists():
        return []
    groups = []
    import sqlite3
    con = sqlite3.connect(db_path)
    try:
        for tbl, cols in table_columns.items():
            vals = []
            for c in cols:
                try:
                    rows = con.execute(f'SELECT DISTINCT "{c}" FROM "{tbl}"').fetchall()
                    v = norm_values(x[0] for x in rows)
                    if v:
                        vals.append(v)
                except Exception:
                    pass
            if vals:
                groups.append(vals)
    finally:
        con.close()
    return groups


def _pred_subtable_groups(subs):
    groups = []
    for _lt, (df, _dbt, _pk) in (subs or {}).items():
        vals = []
        for c in df.columns:
            v = fast_norm_series(df[c])
            if v:
                vals.append(v)
        if vals:
            groups.append(vals)
    return groups


def grouped_subtable_score(tid, subs):
    gold_groups = _gold_subtable_groups(tid)
    pred_groups = _pred_subtable_groups(subs)
    if not gold_groups:
        return None, None, 0, 0
    matched, total = _max_group_matching(pred_groups, gold_groups)
    return matched == total, matched / max(total, 1), matched, total


def _cf(x): import re; return __import__("re").sub(r"[^a-z0-9]", "", str(x).lower())


def input_cols(task):
    d = {}
    for i, f in enumerate(task.get("input_table") or []):
        p = BENCH_DIR / f
        if p.exists():
            try: d[f"table_{i+1}"] = set(pd.read_pickle(p).columns)
            except Exception: pass
    return d


def load_external_specs(path: Path | None):
    if not path:
        return {}
    rows = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("task_id"):
                rows[str(row["task_id"])] = row
    return rows


def _norm_name(x):
    import re
    return re.sub(r"[^a-z0-9]", "", str(x or "").lower())


def join_edges_from_spec(spec_row):
    """Parse predicted SQL JOIN equality predicates into logical-table edges.

    The pipeline still needs logical_table ids to locate materialized subtables,
    but we also preserve db_table names so diagnostics and downstream checks can
    compare db_table.column edges without being misled by logical-table order.
    """
    sql = spec_row.get("sql") or spec_row.get("S") or ""
    tables = spec_row.get("gold_tables") or spec_row.get("table_specs") or []
    logical_to_db_early = {str(t.get("logical_table") or ""): str(t.get("db_table") or "")
                           for t in tables}
    # An explicit `join_edges` field is merged with, not substituted for, the edges parsed out
    # of the SQL. Measured on the v3 grounded specs: the explicit edges hit 24 of 50 gold edges
    # and the SQL 27, but the explicit set is a strict SUBSET — union 27, zero edges found only
    # by the explicit field. Preferring it therefore lost 3 real edges for nothing.
    explicit_out = []
    seen = set()
    for e in spec_row.get("join_edges") or []:
        lt, rt = str(e.get("left_table") or ""), str(e.get("right_table") or "")
        lc, rc = str(e.get("left_on") or ""), str(e.get("right_on") or "")
        if not all((lt, rt, lc, rc)) or lt == rt:
            continue
        key = tuple(sorted([(_norm_name(lt), _norm_name(lc)), (_norm_name(rt), _norm_name(rc))]))
        if key in seen:
            continue
        seen.add(key)
        explicit_out.append({"left_table": lt, "left_db_table": logical_to_db_early.get(lt, lt),
                             "left_on": lc, "right_table": rt,
                             "right_db_table": logical_to_db_early.get(rt, rt), "right_on": rc})
    db_to_logical = {}
    alias_to_logical = {}
    logical_to_db = {}
    for t in tables:
        logical = str(t.get("logical_table") or "")
        db_table = str(t.get("db_table") or "")
        if logical:
            alias_to_logical[_norm_name(logical)] = logical
            if db_table:
                logical_to_db[logical] = db_table
        if db_table and logical:
            db_to_logical[_norm_name(db_table)] = logical
    edges = []
    try:
        tree = sqlglot.parse_one(sql, read="sqlite")
        alias_to_db = {}
        for table in tree.find_all(exp.Table):
            name = str(table.name)
            alias = str(table.alias_or_name)
            alias_to_db[_norm_name(alias)] = _norm_name(name)
            alias_to_db[_norm_name(name)] = _norm_name(name)
        for eq in tree.find_all(exp.EQ):
            left, right = eq.left, eq.right
            if not isinstance(left, exp.Column) or not isinstance(right, exp.Column):
                continue
            if not left.table or not right.table:
                continue
            lkey = alias_to_db.get(_norm_name(left.table), _norm_name(left.table))
            rkey = alias_to_db.get(_norm_name(right.table), _norm_name(right.table))
            lt = db_to_logical.get(lkey) or alias_to_logical.get(lkey)
            rt = db_to_logical.get(rkey) or alias_to_logical.get(rkey)
            if lt and rt and lt != rt:
                edges.append({
                    "left_table": lt,
                    "left_db_table": logical_to_db.get(lt, lkey),
                    "left_on": str(left.name),
                    "right_table": rt,
                    "right_db_table": logical_to_db.get(rt, rkey),
                    "right_on": str(right.name),
                })
    except Exception:
        edges = []
    # explicit edges first, then anything the SQL adds on top
    edges = explicit_out + edges
    # de-duplicate while preserving order
    seen, out = set(), []
    for e in edges:
        db_left = (_norm_name(e.get("left_db_table") or e["left_table"]), _norm_name(e["left_on"]))
        db_right = (_norm_name(e.get("right_db_table") or e["right_table"]), _norm_name(e["right_on"]))
        key = tuple(sorted([db_left, db_right]))
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def join_edges_from_gold_output(task_id, mp):
    """Build logical-table join edges from benchmark gold join_keys/set_relations.

    This is an oracle diagnostic path for Stage-3 experiments with gold table
    specifications. It bypasses SQL parsing errors in the predicted/spec SQL but
    still maps DB table names back to the logical tables materialized by Phase 1.
    """
    path = AUTOP / "nl2sql-bird/dev/outputs" / f"{task_id}.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    db_to_logical = {}
    for lt, info in (mp or {}).items():
        db = info.get("db_table")
        if db:
            db_to_logical[_norm_name(db)] = lt
    edges = []
    for item in (data.get("join_keys") or []) + (data.get("set_relations") or []):
        ldb, rdb = item.get("left_table"), item.get("right_table")
        lcol, rcol = item.get("left_column"), item.get("right_column")
        lt = db_to_logical.get(_norm_name(ldb))
        rt = db_to_logical.get(_norm_name(rdb))
        if lt and rt and lt != rt and lcol and rcol:
            edges.append({
                "left_table": lt,
                "left_db_table": ldb,
                "left_on": str(lcol),
                "right_table": rt,
                "right_db_table": rdb,
                "right_on": str(rcol),
                "left_values": item.get("left_values") or [],
                "right_values": item.get("right_values") or [],
                "source": "gold_output",
            })
    seen, out = set(), []
    for e in edges:
        db_left = (_norm_name(e.get("left_db_table") or e["left_table"]), _norm_name(e["left_on"]))
        db_right = (_norm_name(e.get("right_db_table") or e["right_table"]), _norm_name(e["right_on"]))
        key = tuple(sorted([db_left, db_right]))
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def map_task_from_spec(spec_row):
    """Build the mp structure expected by full_pipeline from predicted/minimal specs."""
    edges = join_edges_from_spec(spec_row)
    join_cols = defaultdict(set)
    for e in edges:
        join_cols[e["left_table"]].add(e["left_on"])
        join_cols[e["right_table"]].add(e["right_on"])
    out = {}
    for t in spec_row.get("gold_tables") or spec_row.get("table_specs") or []:
        lt = str(t.get("logical_table") or "")
        csql = t.get("create_table_sql") or ""
        if not lt or not csql:
            continue
        schema, pk = parse_create_table(csql)
        out[lt] = {
            "db_table": str(t.get("db_table") or lt),
            "schema": schema,
            "pk": set(pk),
            "join_cols": sorted(join_cols.get(lt, set())),
            # Carried so synth_one can bind this logical table to the raw file the
            # SPEC names, instead of assuming logical table N is the Nth input.
            "input_file": t.get("input_file"),
        }
    return out, edges


def anchors_for(mp, edges):
    """Pick the anchor (PK side) of every edge; returns {logical_table: pk_col}."""
    anc = {}
    for e in edges:
        l, r = e["left_table"], e["right_table"]
        lpk = l in mp and any(_cf(e["left_on"]) == _cf(c) for c in mp[l]["pk"])
        rpk = r in mp and any(_cf(e["right_on"]) == _cf(c) for c in mp[r]["pk"])
        if lpk: anc[l] = e["left_on"]
        elif rpk: anc[r] = e["right_on"]
        else:
            # No declared PK: take the more unique side as the anchor (not decided at
            anc[r] = e["right_on"]
    return anc


def main():
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("--op-source", choices=["gold", "pipeline", "policy-gold-params"], default="gold")
    ap.add_argument("--model", default="gpt-4o-2024-08-06")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--table-specs", type=Path, default=None, help="Optional JSONL with predicted/minimal schema specs: task_id, sql, gold_tables.")
    ap.add_argument("--tasks", default=None,
                    help="Comma-separated task IDs. Only these tasks are run and evaluated.")
    ap.add_argument("--join-aware-rerank", action="store_true",
                    help="Select among Phase-1 table candidates using planned join overlap before Phase 2 repair.")
    ap.add_argument("--join-rerank-candidates", type=int, default=4,
                    help="Maximum terminal candidates per table considered by --join-aware-rerank.")
    ap.add_argument("--gold-join-edges", action="store_true",
                    help="Use benchmark gold join_keys/set_relations as Phase-2 join edges instead of parsing spec SQL.")
    args = ap.parse_args()

    if args.op_source == "pipeline" and not os.environ.get("OPENAI_API_KEY"):
        ap.error(
            "--op-source pipeline requires OPENAI_API_KEY; without it every "
            "parameter-synthesis candidate fails and the predicted chains are empty"
        )

    btask = T.load_benchmark("nl2sql-bird", "dev", AUTOP)
    external_specs = load_external_specs(args.table_specs)
    default_cids = set(T.load_case_ids(ROOT / "pipeline_eval/cases_group_a_high_ops_union_structural.jsonl", "nl2sql-bird"))
    cids = sorted(set(external_specs) & set(btask) if external_specs else default_cids)
    if args.tasks:
        requested = {task.strip() for task in args.tasks.split(",") if task.strip()}
        unknown = sorted(requested - set(btask))
        if unknown:
            ap.error(f"unknown task IDs: {','.join(unknown)}")
        cids = [task for task in cids if task in requested]
        missing = sorted(requested - set(cids))
        if missing:
            ap.error(f"requested tasks are absent from the selected table specs/case set: {','.join(missing)}")
    R = SchemaResolver()
    loop = Loop(op_source=args.op_source, model=args.model)

    def gold_ops_for(task, lt):
        """Every gold dc_op of this logical table, in order of appearance."""
        out = []
        for op in task.get("dc_ops") or []:
            m = T.OP_WITH_TABLE_RE.search(str(op))
            if m and m.group(2) == lt:
                out.append(str(op))
        return out

    def synth_one(task, lt, info):
        """Phase 1: synthesize one gold table's subtable."""
        idx = int(lt.split("_")[1]) - 1
        files = task.get("input_table") or []
        # BIND_BY_INPUT_FILE (env-gated, default OFF so every previously recorded
        # result keeps its meaning): bind a logical table to the raw file the spec
        # NAMES rather than to the file at its ordinal position. The positional
        # rule holds for the gold specs (0 of 43 tasks permute) but not for
        # synthesized plans: 22 of the 43 plans_v4/grounded_v3 plans number their
        # logical tables in a different order than the benchmark lists the inputs,
        # so 44 of 91 tables were handed the WRONG frame. Verified by declared-
        # schema/frame column overlap, e.g. bird_f9419900 table_2 scores 0.07
        # positionally and 0.67 by input_file.
        f = None
        if os.environ.get("BIND_BY_INPUT_FILE"):
            named = info.get("input_file")
            if named and named in files:
                f = named
        if f is None:
            f = (files or [None] * 99)[idx]
        p = BENCH_DIR / f
        df0 = M.sanitize(pd.read_pickle(p))
        ctx = {"task": task, "logical_table": lt,
               "schema_spec": schema_to_sql(info["schema"], info["pk"]),
               "db_id": task["db_id"], "source": "bird",
               "join_targets": info.get("join_targets") or []}
        tspec = {"create_table_sql": ctx["schema_spec"], "primary_key": sorted(info["pk"]),
                 "column_types": info["schema"], "output_columns": list(info["schema"]),
                 "join_cols": sorted(info.get("join_cols") or []),
                 "join_targets": info.get("join_targets") or []}
        if args.op_source == "gold":
            # Gold ceiling: apply the full ordered gold chain plus the deterministic
            from coverage_policy import plan_next, apply_auto_rename
            df = df0
            for opstr in gold_ops_for(task, lt):
                try:
                    df = M.sanitize(M.robust_execute(df, M.op_str_to_step(opstr)))
                except Exception:
                    pass
            return apply_auto_rename(df, plan_next(df, tspec)["auto_rename"])
        result = loop.run_table(df0, tspec, ctx)
        return result

    def _table_payload(obj):
        if isinstance(obj, dict) and "df" in obj:
            return obj
        return {"df": obj, "chain": [], "ok": False, "terminal_candidates": []}

    def _key_quality(df, col):
        s = _series_casefold(df, col)
        if s is None or len(s) == 0:
            return 0.0
        nn = float(s.notna().mean())
        denom = max(int(s.notna().sum()), 1)
        uq = float(s.dropna().astype(str).nunique() / denom)
        return min(nn, uq)

    def _series_casefold(df, col):
        m = {_cf(c): c for c in df.columns}
        c = m.get(_cf(col))
        if c is None:
            return None
        s = df[c]
        if isinstance(s, pd.DataFrame):
            s = s.iloc[:, 0]
        return s

    def _candidate_join_score(selected, edges, mp):
        # Weighted SUM of subtable coverage + cross-table join-key value overlap.
        # Offline A/B on a FIXED candidate pool (offline_rerank_ab.py) showed this
        # beats both the loop's top-1 baseline (5/9->7/9 subtable, 2/9->6/9 join-key)
        # AND a lexicographic coverage-first variant (which regressed to 6/9, 5/9 —
        # name-based coverage is blind to VALUE correctness, so making it strictly
        # primary picks name-complete-but-value-wrong tables). The join value term
        # must stay additive so it can pull toward value-correct combos.
        score = 0.0
        for lt, payload in selected.items():
            df = payload["df"]
            info = mp.get(lt, {})
            schema = info.get("schema") or {}
            present = {_cf(c) for c in df.columns}
            required = {_cf(c) for c in schema}
            cover = len(required & present) / max(len(required), 1)
            score += 2.0 * cover + 0.25 * float(payload.get("score") or 0.0)
        for e in edges:
            lt, rt = e["left_table"], e["right_table"]
            if lt not in selected or rt not in selected:
                score -= 2.0
                continue
            ldf, rdf = selected[lt]["df"], selected[rt]["df"]
            lv = col_values(ldf, e["left_on"])
            rv = col_values(rdf, e["right_on"])
            if lv is None or rv is None:
                score -= 1.0
                continue
            if not lv or not rv:
                continue
            overlap = len(lv & rv) / max(min(len(lv), len(rv)), 1)
            containment_lr = len(lv & rv) / max(len(lv), 1)
            containment_rl = len(lv & rv) / max(len(rv), 1)
            score += 2.0 * max(overlap, containment_lr, containment_rl)
            score += 0.25 * _key_quality(ldf, e["left_on"])
            score += 0.25 * _key_quality(rdf, e["right_on"])
        return score

    def _join_aware_select(table_results, edges, mp, limit=4):
        from itertools import product
        logical_tables = list(table_results)
        pools = []
        for lt in logical_tables:
            payload = _table_payload(table_results[lt])
            candidates = payload.get("terminal_candidates") or []
            candidates = [{**c, "df": M.sanitize(c["df"])} for c in candidates if isinstance(c, dict) and "df" in c]
            if not candidates:
                candidates = [payload]
            # De-duplicate identical column layouts/chains and keep the local best few.
            seen, uniq = set(), []
            for c in sorted(candidates, key=lambda x: -float(x.get("score") or 0.0)):
                key = (tuple(map(str, c["df"].columns)), tuple(c.get("chain") or []))
                if key in seen:
                    continue
                seen.add(key); uniq.append(c)
                if len(uniq) >= limit:
                    break
            pools.append(uniq)
        best_combo, best_score = None, None
        for combo in product(*pools):
            selected = dict(zip(logical_tables, combo))
            score = _candidate_join_score(selected, edges, mp)
            if best_score is None or score > best_score:
                best_score, best_combo = score, selected
        return best_combo or {lt: _table_payload(v) for lt, v in table_results.items()}

    # EXPOSE callback (Phase 2 structurally missing column) - reuses the loop's one-step
    # Phase 2's EXPOSE branch is NOT implemented. `repair_joins` is written to call this to run a
    # targeted transform that surfaces a missing/broken join column, but there is no such
    # implementation, so passing a stub that returns None made every attempt look like a repair
    # that was tried and failed. Measured over 43 tasks: 44 L1 "UNFIXED" + 18 invalid L0 anchors,
    # 0 EXPOSE calls and 0 successful MATCH repairs — i.e. Phase 2 currently repairs nothing.
    # Passing None instead lets repair_joins say so in the log.
    expose_fn = None

    per_task_subs = {}     # task_id -> {logical_table: (df, db_table, pk)}
    per_task_edges = {}
    for tid in cids:
        task = btask.get(tid)
        if not task: continue
        if tid in external_specs:
            mp, edges = map_task_from_spec(external_specs[tid])
        else:
            mp = TM.map_task(task, R, "bird", input_cols(task))
            edges = [e for e in TM.tol_join_edges(task)
                     if "_join" not in e["left_table"] and "_join" not in e["right_table"]]
        if args.gold_join_edges:
            gold_edges = join_edges_from_gold_output(tid, mp)
            if gold_edges:
                edges = gold_edges
                join_cols = defaultdict(set)
                join_targets = defaultdict(list)
                for e in edges:
                    join_cols[e["left_table"]].add(e["left_on"])
                    join_cols[e["right_table"]].add(e["right_on"])
                    join_targets[e["left_table"]].append({
                        "column": e["left_on"],
                        "other_table": e["right_table"],
                        "other_column": e["right_on"],
                        "other_values": e.get("right_values") or [],
                    })
                    join_targets[e["right_table"]].append({
                        "column": e["right_on"],
                        "other_table": e["left_table"],
                        "other_column": e["left_on"],
                        "other_values": e.get("left_values") or [],
                    })
                for lt, info in mp.items():
                    info["join_cols"] = sorted(join_cols.get(lt, set()))
                    info["join_targets"] = join_targets.get(lt, [])
        # Phase 1, in parallel
        subs = {}
        table_results = {}
        dbt2ops = {}   # db_table -> that logical table's gold op type sequence (diagnostics)
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(synth_one, task, lt, info): (lt, info) for lt, info in mp.items()}
            for fu, (lt, info) in futs.items():
                try:
                    res = fu.result()
                    if args.op_source == "gold":
                        subs[lt] = (M.sanitize(res), info["db_table"], set(info["pk"]))
                    else:
                        table_results[lt] = _table_payload(res)
                        subs[lt] = (M.sanitize(table_results[lt]["df"]), info["db_table"], set(info["pk"]))
                except Exception as exc:
                    print(
                        f"[table-synth-error] {tid}::{lt}: "
                        f"{type(exc).__name__}: {exc}",
                        file=sys.stderr, flush=True,
                    )
                gops = [T.OP_WITH_TABLE_RE.search(str(o)).group(1) for o in (task.get("dc_ops") or [])
                        if T.OP_WITH_TABLE_RE.search(str(o)) and T.OP_WITH_TABLE_RE.search(str(o)).group(2) == lt]
                dbt2ops[info["db_table"].lower()] = gops
        per_task_dbt2ops = getattr(main, "_dbt2ops", None) or {}
        per_task_dbt2ops[tid] = dbt2ops; main._dbt2ops = per_task_dbt2ops
        if args.join_aware_rerank and table_results:
            selected = _join_aware_select(table_results, edges, mp, limit=args.join_rerank_candidates)
            subs = {lt: (M.sanitize(payload["df"]), mp[lt]["db_table"], set(mp[lt]["pk"]))
                    for lt, payload in selected.items()}
            if os.environ.get("DUMP_CALIB"):
                main._join_rerank = getattr(main, "_join_rerank", {})
                main._join_rerank[tid] = {
                    lt: {"chain": payload.get("chain"), "ok": payload.get("ok"),
                         "score": payload.get("score")}
                    for lt, payload in selected.items()
                }
                if os.environ.get("DUMP_TERMINAL_CANDIDATES"):
                    main._terminal_candidates = getattr(main, "_terminal_candidates", {})
                    main._terminal_candidates[tid] = {
                        lt: [
                            {"df": M.sanitize(c["df"]), "chain": c.get("chain"),
                             "ok": c.get("ok"), "score": c.get("score")}
                            for c in ((payload.get("terminal_candidates") or [payload])
                                      if isinstance(payload, dict) else [])
                            if isinstance(c, dict) and "df" in c
                        ]
                        for lt, payload in table_results.items()
                    }
        # Phase 2
        anc = anchors_for(mp, edges)
        subs, log = repair_joins(subs, edges, anc, expose_fn=expose_fn)
        per_task_subs[tid] = subs
        per_task_edges[tid] = (edges, anc)
        # --- DUMP_CALIB (diagnostic, env-gated): capture produced tables + view + edges
        if os.environ.get("DUMP_CALIB"):
            main._calib = getattr(main, "_calib", {})
            main._calib[tid] = {
                "subtables": {lt: v[0] for lt, v in subs.items()},
                "view": {lt: {"column_types": dict(info["schema"]),
                              "primary_key": sorted(info["pk"]),
                              "join_cols": sorted(info.get("join_cols", []))}
                         for lt, info in mp.items()},
                "edges": edges,
                "join_repair_log": log,
            }
            if tid in getattr(main, "_join_rerank", {}):
                main._calib[tid]["join_aware_rerank"] = main._join_rerank[tid]
            if tid in getattr(main, "_terminal_candidates", {}):
                main._calib[tid]["terminal_candidates"] = main._terminal_candidates[tid]

    # ---------------- evaluation ----------------
    import sqlite3
    from collections import Counter as _Ctr
    def _norm(x): import re as _re2; return _re2.sub(r"[^a-z0-9]", "", str(x).lower())
    fail_reasons = _Ctr(); fail_tasks = []; op_blame = _Ctr()

    sub_full = sub_rec = jk_full = jk_rec = 0.0
    grouped_full = grouped_rec = 0.0
    n = njk = ngroup = 0
    for tid in cids:
        gt = gt_birdspider(tid, "nl2sql-bird", "dev", AUTOP)
        if not gt: continue
        subs = per_task_subs.get(tid, {})
        # value-based subtable: pool the column value sets of every subtable
        pred_cols = []
        for lt, (df, dbt, pk) in subs.items():
            for c in df.columns:
                v = fast_norm_series(df[c])
                if v: pred_cols.append(v)
        sc = score_predictions({"cols": pred_cols, "edges": []}, gt)
        gfull, grec, _gmatched, _gtotal = grouped_subtable_score(tid, subs)
        n += 1; sub_full += bool(sc["subtable_full"]); sub_rec += sc["subtable_recall"]
        if gfull is not None:
            ngroup += 1
            grouped_full += bool(gfull)
            grouped_rec += grec
        if os.environ.get("DUMP_CALIB") and tid in getattr(main, "_calib", {}):
            main._calib[tid]["label"] = {"subtable_full": bool(sc["subtable_full"]),
                                         "subtable_recall": sc["subtable_recall"],
                                         "grouped_subtable_full": bool(gfull) if gfull is not None else None,
                                         "grouped_subtable_recall": grec}

        # Diagnosis: when a task scores subtable_full=0, attribute each unmatched gold
        if not sc["subtable_full"]:
            fail_tasks.append(tid)
            d = json.loads((AUTOP / "nl2sql-bird/dev/outputs" / f"{tid}.json").read_text())
            jk = set()
            for e in d.get("join_keys", []) + d.get("set_relations", []):
                jk.add((e.get("left_table"), _norm(e.get("left_column"))))
                jk.add((e.get("right_table"), _norm(e.get("right_column"))))
            # Diagnosis only — scoring above is value-domain and ignores names entirely. Compare
            # table names singular/plural-insensitively: the synthesizer says `members`/`events`/
            # `atoms` where gold says `member`/`event`/`atom`, and the literal comparison charged
            # 27 of 30 failures to "table_not_synthesized", hiding every real reason.
            def _tforms(x):
                s = _norm(x)
                out = {s}
                if s.endswith("ies") and len(s) > 4:
                    out.add(s[:-3] + "y")
                if s.endswith("es") and len(s) > 3:
                    out |= {s[:-2], s[:-1]}
                elif s.endswith("s") and len(s) > 2:
                    out.add(s[:-1])
                else:
                    out |= {s + "s", s + "es"}
                return out

            my_forms = [_tforms(dbt) for _, (df, dbt, pk) in subs.items()]

            def _synthesized(tbl):
                f = _tforms(tbl)
                # plural/singular, or one name embedded in the other: the synthesizer writes
                # `molecule_bonds` for gold's `bond` and `patient_tests` for `Patient`. The table
                # was produced either way; only the label differs, and labels do not score.
                return any(f & m or any(a in b or b in a for a in f for b in m if min(len(a), len(b)) > 3)
                           for m in my_forms)
            try:
                con = sqlite3.connect(d["db_path"])
                for tbl, cols in d.get("table_columns", {}).items():
                    vsets = {}
                    for c in cols:
                        try: vsets[c] = norm_values(x[0] for x in con.execute(f'SELECT DISTINCT "{c}" FROM "{tbl}"').fetchall())
                        except Exception: vsets[c] = set()
                    matched_any = any(v and any(vmatch(pc, v) for pc in pred_cols) for v in vsets.values())
                    for c, v in vsets.items():
                        if not v or any(vmatch(pc, v) for pc in pred_cols): continue
                        if not _synthesized(tbl): fail_reasons["table_not_synthesized"] += 1
                        elif (tbl, _norm(c)) in jk: fail_reasons["join_key_col_miss"] += 1
                        elif not matched_any: fail_reasons["table_synth_but_0col_matched"] += 1
                        else:
                            fail_reasons["other_col_value_miss"] += 1
                            # Look up the gold op sequence of the table that column came
                            gops = (getattr(main, "_dbt2ops", {}).get(tid, {}) or {}).get(tbl.lower(), [])
                            for optype in set(gops):
                                op_blame[optype] += 1
                con.close()
            except Exception: pass
        # VALUE-DOMAIN join key (aligned with eval_two_phase._value_domain_jk_eval):
        # ignore column names, collect the value domains of every join-key column in our
        # subtables as pred_keys, and cover each side of every gold edge with a one-to-one
        # vmatch. Direction-robust: every (table, col) combination is tried, and a missing
        edges, anc = per_task_edges.get(tid, ([], {}))
        pred_keys = []
        for e in edges:
            for tbl, on in ((e["left_table"], e["left_on"]), (e["right_table"], e["right_on"]),
                            (e["left_table"], e["right_on"]), (e["right_table"], e["left_on"])):
                if tbl in subs:
                    v = col_values(subs[tbl][0], on)
                    if v:
                        pred_keys.append(v)
        gold_domains = []
        for ge in gt.get("edges", []):
            if ge.get("left"):
                gold_domains.append(ge["left"])
            if ge.get("right"):
                gold_domains.append(ge["right"])
        jk_frac = _value_domain_jk_frac(pred_keys, gold_domains)
        if jk_frac is not None:
            njk += 1
            jk_rec += jk_frac; jk_full += int(jk_frac >= 0.999)
            if os.environ.get("DUMP_CALIB") and tid in getattr(main, "_calib", {}):
                main._calib[tid].setdefault("label", {})["join_key_full"] = int(jk_frac >= 0.999)
                main._calib[tid]["label"]["join_key_recall"] = jk_frac

    print(f"=== FULL PIPELINE (op-source={args.op_source}) | tasks={n} ===")
    print(f"subtable_full_accuracy : {sub_full/n:.3f}   (bipartite value-domain)")
    print(f"subtable_recall        : {sub_rec/n:.3f}")
    if ngroup:
        print(f"grouped_subtable_full_accuracy : {grouped_full/ngroup:.3f}   (table-group bipartite; tasks: {ngroup})")
        print(f"grouped_subtable_recall        : {grouped_rec/ngroup:.3f}")
    if njk:
        print(f"join_key_full_accuracy : {jk_full/njk:.3f}   (value-domain, aligned w/ eval_two_phase; tasks with keys: {njk})")
        print(f"join_key_recall        : {jk_rec/njk:.3f}")
    print("\nAgainst SOTA_LLM (same 43 tasks, edge matching): subtable_full 0.698 / recall 0.889 | join_key_full 0.419 / recall 0.442")
    print(f"\n=== subtable_full=0 failure diagnosis ({len(fail_tasks)} tasks) ===")
    print(f"  FAIL_TASK_IDS: {','.join(fail_tasks)}")
    for k, v in fail_reasons.most_common():
        print(f"  {k}: {v}")
    print("  gold op types of the tables holding the value-miss columns (whose parameters go wrong most):")
    for k, v in op_blame.most_common():
        print(f"      {k}: {v}")

    # --- DUMP_CALIB (diagnostic, env-gated): persist the labeled calibration set
    if os.environ.get("DUMP_CALIB"):
        import pickle
        calib = getattr(main, "_calib", {})
        outp = os.environ.get("DUMP_CALIB_OUT") or str(
            ROOT / "hardness/pipeline/calib_set.pkl")
        with open(outp, "wb") as f:
            pickle.dump(calib, f)
        print(f"\n[DUMP_CALIB] wrote {len(calib)} tasks -> {outp}")


if __name__ == "__main__":
    main()
