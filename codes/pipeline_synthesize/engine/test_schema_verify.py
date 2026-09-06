#!/usr/bin/env python3
"""
test_schema_verify.py
---------------------
A simple check: for a single-op instance, execute the (gold or LLM) operation on the raw
table, then use react_single_table_runner's own schema_coverage_check to decide whether
the result satisfies the target schema (stop=True means "subtable schema contract pass").

Purpose: see whether these tables pass the verify logic after one op, and if not, what is

Usage:
  python3 test_schema_verify.py                 # with the gold op
  python3 test_schema_verify.py --use-llm-pred  # with the LLM op from param_synth_details.jsonl
"""
from __future__ import annotations
import os
import argparse, json, sys
from pathlib import Path
from collections import Counter

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
AUTOPREP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
for p in (str(HERE), str(ROOT), str(ROOT / "dependency_modeling_react_joint")):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_single_ops_type as T
import test_param_synthesis as M
from table_executor import observation_from_df
from table_specs import schema_coverage_check


def load_full_spec_instances(specs, btask, bench_dir, table_cache, case_ids, infer_classes):
    """Like iter_single_op_instances, but keeps the full table_spec (dict) for schema_coverage_check."""
    out = []
    for rec in specs:
        tid = str(rec.get("task_id") or "")
        if not tid or (case_ids is not None and tid not in case_ids):
            continue
        task = btask.get(tid)
        if not task:
            continue
        ops_by_tbl = T.dc_ops_by_logical_table(task)
        for tspec in (rec.get("table_specs") or rec.get("T") or []):
            tfile = str(tspec.get("table_file") or "")
            if not tfile or not tspec.get("create_table_sql"):
                continue
            lt = T.logical_table_for_file(task, tfile)
            gold_ops = ops_by_tbl.get(lt, [])
            if len(gold_ops) != 1 or gold_ops[0] not in infer_classes:
                continue
            tpath = T.find_table_file(bench_dir, tfile, table_cache)
            if tpath is None:
                continue
            out.append({"task_id": tid, "logical_table": lt, "gold_op": gold_ops[0],
                        "table_path": str(tpath), "table_spec": tspec})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="nl2sql-bird")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--table-specs", type=Path,
                    default=ROOT / "dependency_modeling_react_joint" / "results" / "oracle_v1_group_a_specs.jsonl")
    ap.add_argument("--case-file", type=Path,
                    default=ROOT / "pipeline_eval" / "cases_group_a_high_ops_union_structural.jsonl")
    ap.add_argument("--use-llm-pred", action="store_true",
                    help="use the LLM-generated op from param_synth_details.jsonl instead of gold.")
    ap.add_argument("--output", type=Path, default=HERE / "results" / "schema_verify_details.jsonl")
    args = ap.parse_args()

    from infer import SingleOpInfer
    classes = set(map(str, SingleOpInfer().clf.classes_)) | {"StandardizeDatetime"}
    btask = T.load_benchmark(args.benchmark, args.split, AUTOPREP)
    specs = T.load_jsonl(args.table_specs)
    case_ids = set(T.load_case_ids(args.case_file, args.benchmark)) if args.case_file.exists() else None
    inst = load_full_spec_instances(specs, btask, AUTOPREP / args.benchmark / args.split, {}, case_ids, classes)

    pred_by_task = {}
    if args.use_llm_pred:
        for l in open(HERE / "results" / "param_synth_details.jsonl"):
            r = json.loads(l)
            if r.get("pred_step"):
                pred_by_task[r["task_id"]] = r["pred_step"]

    rows, passed, total = [], Counter(), Counter()
    fail_reasons = Counter()
    for it in inst:
        op = it["gold_op"]; tid = it["task_id"]
        df = M.sanitize(pd.read_pickle(it["table_path"]))
        if args.use_llm_pred:
            step = pred_by_task.get(tid)
            if step is None:
                continue
        else:
            gstr = M.gold_op_str_for_table(btask[tid], it["logical_table"])
            step = M.op_str_to_step(gstr) if gstr else None
            if step is None:
                continue
        try:
            result = M.robust_execute(df.copy(), step)
        except Exception as e:
            rows.append({"task_id": tid, "op": op, "exec_error": str(e)[:100], "stop": False}); total[op] += 1; continue
        obs = observation_from_df(result, top_k=10, cut_col=-1, max_table_len=6000)
        cov = schema_coverage_check(obs, it["table_spec"], {})   # single table: empty joinability
        total[op] += 1; passed[op] += int(bool(cov.get("stop")))
        if not cov.get("stop"):
            fail_reasons[cov.get("reason", "?").split(":")[0]] += 1
        rows.append({"task_id": tid, "op": op, "stop": bool(cov.get("stop")),
                     "reason": cov.get("reason"),
                     "missing_columns": [m["column"] for m in cov.get("missing_columns", [])],
                     "incorrect_column_types": [c.get("column") for c in cov.get("incorrect_column_types", [])],
                     "incorrect_primary_keys": [c.get("column") for c in cov.get("incorrect_primary_keys", [])]})

    N, P = sum(total.values()), sum(passed.values())
    src = "LLM-pred" if args.use_llm_pred else "gold"
    print(f"schema-verify pass ({src} op) : {P}/{N} = {P/N:.3f}" if N else "no instances")
    print("\nper-op:")
    for op in sorted(total):
        print(f"  {op:20s} {passed[op]}/{total[op]}")
    print("\nfail reasons:", dict(fail_reasons))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("\ndetails ->", args.output)


if __name__ == "__main__":
    main()
