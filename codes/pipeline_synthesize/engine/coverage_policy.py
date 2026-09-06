#!/usr/bin/env python3
"""
coverage_policy.py
------------------
Classify a schema_coverage_check result by error type, decide whether the single-table
stage MUST continue, and for the deterministically fixable cases (transpose index

Policy, three tiers:
  - blocking (continue now): the VALUES of a required schema column do not appear in the
  - deferred (leave to integration / final cleaning): dtype mismatch, join-key overlap.
  - deterministic-fix (a Rename, no LLM): the values are already there under the wrong
       * a transposed index column row_id -> the key column the schema wants
       * a casing-only difference (circuitId -> circuitID)

Public result:
  plan_next(result_df, table_spec, joinability={}) -> dict
     status: "complete" | "deterministic_fix" | "needs_generation"
     auto_rename: {old:new}   # deterministic fixes, directly executable, no LLM
     blocking_missing: [...]  # genuinely missing structure; a next op must be generated
     deferred: {dtype:[...], join_keys:[...]}  # not blocking at the single-table stage
"""
from __future__ import annotations
import re as _re
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
for p in (str(ROOT / "dependency_modeling_react_joint"), str(ROOT)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pandas as pd
from table_executor import observation_from_df
from table_specs import schema_coverage_check


def _cf(x): return str(x).strip().casefold()


_LIST_DELIMS = (",", "|", ";")


def list_cell_delimiter(s) -> str | None:
    """The delimiter joining a VARIABLE-length list of atomic tokens inside each cell.

    A join key holding `a,b,c,...` cannot be joined on — the rows must be exploded first. The
    coverage check cannot see this, because Explode leaves the column NAME untouched: on
    bird_8d39e1b3 the spec asked for `link_to_member`, the raw table already had a column of
    that name, so the search stopped with calls=0 and never tried anything.

    Variable part count is what separates an Explode target from a fixed-arity packed column
    (SplitColumn's job). The atomicity guards keep prose out — `rulings.text` and `AboutMe` are
    full of commas, but their fragments are long and contain spaces.
    """
    try:
        v = s.dropna().astype(str)
    except Exception:
        return None
    if len(v) < 3:
        return None
    for d in _LIST_DELIMS:
        n = v.str.count(_re.escape(d))
        if (n >= 1).mean() <= 0.8 or n.nunique() <= 2:
            continue
        parts = [p.strip() for cell in v.head(50) for p in cell.split(d)]
        parts = [p for p in parts if p]
        if len(parts) < 6 or max(len(p) for p in parts) > 40:
            continue
        if sum(" " in p for p in parts) / len(parts) > 0.2:
            continue
        if len({len(p) for p in parts}) > 12:
            continue
        return d
    return None


def plan_next(result_df: pd.DataFrame, table_spec: dict, joinability: dict | None = None) -> dict:
    joinability = joinability or {}
    cols = [str(c) for c in result_df.columns]
    cf_map = {_cf(c): c for c in cols}

    cov = schema_coverage_check(observation_from_df(result_df, 10, -1, 6000), table_spec, joinability)
    if not cov.get("has_spec"):
        return {"status": "needs_generation", "reason": "no spec", "auto_rename": {}, "blocking_missing": [], "deferred": {}}

    required = cov.get("target_columns", [])
    missing = [m["column"] for m in cov.get("missing_columns", [])]

    auto_rename: dict[str, str] = {}
    blocking: list[str] = []
    row_id_col = cf_map.get("row_id")

    for col in missing:
        # 1) casing-only difference -> deterministic rename
        if _cf(col) in cf_map and cf_map[_cf(col)] != col:
            auto_rename[cf_map[_cf(col)]] = col
            continue
        # 2) the transposed index column row_id carries this key's values -> rename it
        #    Conditions: row_id exists, the required column looks like a key (a PK or an
        pk_cols = {_cf(c) for c in (table_spec.get("primary_key") or [])}
        looks_key = (_cf(col) in pk_cols) or _cf(col).endswith("id")
        if row_id_col and looks_key and row_id_col not in auto_rename:
            auto_rename[row_id_col] = col
            row_id_col = None   # row_id can only be claimed once
            continue
        # 3) genuinely missing structure
        blocking.append(col)

    # REVERTED — a join column holding a list per cell is genuinely unfinished (Explode leaves
    # the column NAME untouched, so coverage cannot see it), and gating on it did make
    # bird_8d39e1b3::table_2 find Explode. But plan_next runs on every INTERMEDIATE frame of the
    # search, not just the final table: validating the detector on the 91 produced tables showed
    # 1 hit, while the live run changed 11 chains and cost subtable_full 28/43 -> 25/43 for
    # join_key_full 23/43 -> 24/43. `list_cell_delimiter` is kept below for reuse if this is ever
    # retried against the FINAL state only.

    deferred = {
        "dtype": [c.get("column") for c in cov.get("incorrect_column_types", [])],
        "join_keys": [c.get("this_table_column") or c.get("column") for c in cov.get("incorrect_join_keys", [])],
    }

    if not blocking and not auto_rename:
        status = "complete" if cov.get("stop") else "deferred_only"  # only deferred items (dtype/join) remain
    elif blocking:
        status = "needs_generation"
    else:
        status = "deterministic_fix"     # a deterministic Rename is all that is needed

    return {"status": status, "auto_rename": auto_rename, "blocking_missing": blocking,
            "deferred": deferred, "coverage_stop": bool(cov.get("stop"))}


def apply_auto_rename(df: pd.DataFrame, auto_rename: dict) -> pd.DataFrame:
    return df.rename(columns=auto_rename).copy() if auto_rename else df


if __name__ == "__main__":
    # Run over the 32 single-op instances and count the verdicts under this policy
    import test_param_synthesis as M, test_single_ops_type as T, test_schema_verify as V
    from infer import SingleOpInfer
    from collections import Counter
    cls = set(map(str, SingleOpInfer().clf.classes_)) | {"StandardizeDatetime"}
    AP = M.AUTOPREP
    btask = T.load_benchmark("nl2sql-bird", "dev", AP)
    specs = T.load_jsonl(M.ROOT / "dependency_modeling_react_joint/results/oracle_v1_group_a_specs.jsonl")
    cids = set(T.load_case_ids(M.ROOT / "pipeline_eval/cases_group_a_high_ops_union_structural.jsonl", "nl2sql-bird"))
    inst = V.load_full_spec_instances(specs, btask, AP / "nl2sql-bird/dev", {}, cids, cls)

    stat = Counter(); after_fix_ok = 0
    for it in inst:
        g = M.gold_op_str_for_table(btask[it["task_id"]], it["logical_table"])
        step = M.op_str_to_step(g) if g else None
        if not step:
            continue
        try:
            res = M.robust_execute(M.sanitize(pd.read_pickle(it["table_path"])).copy(), step)
        except Exception:
            continue
        plan = plan_next(res, it["table_spec"])
        stat[plan["status"]] += 1
        # After applying the deterministic renames, is the structure complete (only deferred left)?
        if plan["auto_rename"]:
            res2 = apply_auto_rename(res, plan["auto_rename"])
            plan2 = plan_next(res2, it["table_spec"])
            if not plan2["blocking_missing"]:
                after_fix_ok += 1
    print("Verdicts under this policy (32 gold single-op instances):")
    for k, v in stat.most_common():
        print(f"  {k}: {v}")
    print(f"\n  of the deterministic_fix cases, structure completed by the Rename: {after_fix_ok}")
    print("\nReading:")
    print("  complete           = the schema is satisfied after one op; nothing follows")
    print("  deferred_only      = only dtype/join items remain; done for the single-table stage")
    print("  deterministic_fix  = the values are in place; only a deterministic Rename is missing (no LLM)")
    print("  needs_generation   = a column is genuinely missing; another op must be generated")
