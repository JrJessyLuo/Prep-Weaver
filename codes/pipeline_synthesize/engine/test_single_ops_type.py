#!/usr/bin/env python3
from __future__ import annotations

import os
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
AUTOPREP_ROOT = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
HERE = Path(__file__).resolve().parent

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from infer import SingleOpInfer  # noqa: E402


OP_WITH_TABLE_RE = re.compile(r"^(\w+)\((?:[^)]*?)\btable_name\s*=\s*['\"]?(table_\d+)['\"]?", re.S)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def normalize_task_ids(values: list[str] | None) -> set[str] | None:
    if not values:
        return None
    out: set[str] = set()
    for value in values:
        for part in str(value).split(","):
            part = part.strip()
            if part:
                out.add(part)
    return out or None


def logical_table_for_file(task: dict[str, Any], table_file: str) -> str:
    for idx, file_name in enumerate(task.get("input_table") or [], start=1):
        if str(file_name) == str(table_file):
            return f"table_{idx}"
    match = re.search(r"_input_(\d+)\.pkl$", str(table_file))
    if match:
        return f"table_{int(match.group(1)) + 1}"
    return ""


def dc_ops_by_logical_table(task: dict[str, Any]) -> dict[str, list[str]]:
    by_table: dict[str, list[str]] = defaultdict(list)
    for op_text in task.get("dc_ops") or []:
        match = OP_WITH_TABLE_RE.search(str(op_text))
        if not match:
            continue
        op_type, logical_table = match.group(1), match.group(2)
        by_table[logical_table].append(op_type)
    return by_table


def find_table_file(root: Path, file_name: str, cache: dict[str, Path | None]) -> Path | None:
    if file_name in cache:
        return cache[file_name]
    direct = root / file_name
    if direct.exists():
        cache[file_name] = direct
        return direct
    matches = list(root.rglob(file_name))
    out = matches[0] if matches else None
    cache[file_name] = out
    return out


def load_benchmark(benchmark: str, split: str, autoprep_root: Path) -> dict[str, dict[str, Any]]:
    path = autoprep_root / benchmark / split / "benchmark.jsonl"
    rows = load_jsonl(path)
    return {str(row["task_id"]): row for row in rows if row.get("task_id")}


def load_case_ids(case_file: Path | None, benchmark: str) -> list[str]:
    if not case_file or not case_file.exists():
        return []
    ids: list[str] = []
    for row in load_jsonl(case_file):
        if row.get("benchmark") and row.get("benchmark") != benchmark:
            continue
        task_id = row.get("task_id") or row.get("query_id")
        if task_id:
            ids.append(str(task_id))
    return ids


def iter_single_op_instances(
    table_specs: list[dict[str, Any]],
    benchmark_by_task: dict[str, dict[str, Any]],
    benchmark_dir: Path,
    table_cache: dict[str, Path | None],
    task_filter: set[str] | None,
    infer_classes: set[str],
) -> tuple[list[dict[str, Any]], Counter]:
    instances: list[dict[str, Any]] = []
    skipped: Counter = Counter()

    for spec_record in table_specs:
        task_id = str(spec_record.get("task_id") or "")
        if not task_id:
            skipped["missing_task_id"] += 1
            continue
        if task_filter is not None and task_id not in task_filter:
            skipped["task_filter"] += 1
            continue
        task = benchmark_by_task.get(task_id)
        if not task:
            skipped["missing_benchmark_task"] += 1
            continue

        ops_by_table = dc_ops_by_logical_table(task)
        table_specs_list = spec_record.get("table_specs") or spec_record.get("T") or []
        for table_spec in table_specs_list:
            table_file = str(table_spec.get("table_file") or "")
            create_sql = table_spec.get("create_table_sql")
            if not table_file or not create_sql:
                skipped["missing_table_spec_fields"] += 1
                continue
            logical_table = logical_table_for_file(task, table_file)
            if not logical_table:
                skipped["missing_logical_table"] += 1
                continue
            gold_ops = ops_by_table.get(logical_table, [])
            if len(gold_ops) != 1:
                skipped["not_single_gold_op"] += 1
                continue
            gold_op = gold_ops[0]
            if gold_op not in infer_classes:
                skipped[f"unsupported_gold_op::{gold_op}"] += 1
                continue
            table_path = find_table_file(benchmark_dir, table_file, table_cache)
            if table_path is None:
                skipped["missing_table_file"] += 1
                continue
            instances.append(
                {
                    "benchmark": spec_record.get("benchmark"),
                    "split": spec_record.get("split"),
                    "task_id": task_id,
                    "db_id": task.get("db_id"),
                    "source": "bird" if "bird" in str(spec_record.get("benchmark") or benchmark) else "spider",
                    "question": spec_record.get("question") or task.get("question"),
                    "table_file": table_file,
                    "table_path": str(table_path),
                    "logical_table": logical_table,
                    "gold_op": gold_op,
                    "schema_spec": create_sql,
                }
            )
    return instances, skipped


def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    infer = SingleOpInfer(thresh=args.threshold)
    infer_classes = set(str(x) for x in infer.clf.classes_)

    benchmark_dir = args.autoprep_root / args.benchmark / args.split
    benchmark_by_task = load_benchmark(args.benchmark, args.split, args.autoprep_root)
    specs = load_jsonl(args.table_specs)

    case_ids = load_case_ids(args.case_file, args.benchmark) if args.case_file else []
    explicit_ids = normalize_task_ids(args.task_ids)
    task_filter: set[str] | None = None
    if case_ids:
        task_filter = set(case_ids)
    if explicit_ids is not None:
        task_filter = explicit_ids if task_filter is None else task_filter & explicit_ids

    table_cache: dict[str, Path | None] = {}
    instances, skipped = iter_single_op_instances(
        specs,
        benchmark_by_task,
        benchmark_dir,
        table_cache,
        task_filter,
        infer_classes,
    )
    if args.limit is not None:
        instances = instances[: args.limit]

    details: list[dict[str, Any]] = []
    hit_counts = Counter()
    gold_counts = Counter()
    pred_top1_counts = Counter()
    error_counts = Counter()

    for inst in instances:
        row = dict(inst)
        gold = inst["gold_op"]
        gold_counts[gold] += 1
        try:
            align = (None, None) if args.raw_view_schema else (inst.get("db_id"), inst.get("source"))
            out = infer.predict(inst["table_path"], inst["schema_spec"], top_k=max(args.top_k, 3),
                                aggressive_datetime=args.aggressive_datetime,
                                db_id=align[0], source=align[1])
            ranked = out.get("ranked") or []
            ranked_ops = [str(op) for op, _ in ranked]
            top = ranked_ops[: args.top_k]
            row["ranked_topk"] = [[str(op), float(prob)] for op, prob in ranked[: args.top_k]]
            row["top1"] = top[0] if top else None
            row["top2_hit"] = gold in ranked_ops[:2]
            row["top3_hit"] = gold in ranked_ops[:3]
            row["top1_hit"] = bool(top and top[0] == gold)
            row["rank_of_gold"] = ranked_ops.index(gold) + 1 if gold in ranked_ops else None
            pred_top1_counts[row["top1"]] += 1
            for k in (1, 2, 3):
                if gold in ranked_ops[:k]:
                    hit_counts[f"top{k}"] += 1
        except Exception as exc:  # keep evaluation robust over odd table files
            row["error"] = repr(exc)
            error_counts[type(exc).__name__] += 1
        details.append(row)

    n = len(details)
    valid_n = n - sum(error_counts.values())
    per_op: dict[str, Any] = {}
    for op, total in sorted(gold_counts.items()):
        op_rows = [r for r in details if r.get("gold_op") == op and not r.get("error")]
        denom = len(op_rows)
        per_op[op] = {
            "n": total,
            "valid_n": denom,
            "top1": sum(bool(r.get("top1_hit")) for r in op_rows) / denom if denom else None,
            "top2": sum(bool(r.get("top2_hit")) for r in op_rows) / denom if denom else None,
            "top3": sum(bool(r.get("top3_hit")) for r in op_rows) / denom if denom else None,
        }

    summary = {
        "benchmark": args.benchmark,
        "split": args.split,
        "table_specs": str(args.table_specs),
        "case_file": str(args.case_file) if args.case_file else None,
        "total_instances": n,
        "valid_instances": valid_n,
        "top1_accuracy": hit_counts["top1"] / valid_n if valid_n else None,
        "top2_accuracy": hit_counts["top2"] / valid_n if valid_n else None,
        "top3_accuracy": hit_counts["top3"] / valid_n if valid_n else None,
        "gold_op_counts": dict(sorted(gold_counts.items())),
        "pred_top1_counts": dict(sorted(pred_top1_counts.items())),
        "per_op": per_op,
        "skipped_counts": dict(sorted(skipped.items())),
        "error_counts": dict(sorted(error_counts.items())),
    }

    if args.output_details:
        args.output_details.parent.mkdir(parents=True, exist_ok=True)
        with args.output_details.open("w", encoding="utf-8") as f:
            for row in details:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    if args.output_summary:
        args.output_summary.parent.mkdir(parents=True, exist_ok=True)
        args.output_summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate train_infer_single_ops/infer.py on gold single-table single-op cases.")
    parser.add_argument("--benchmark", default="nl2sql-bird")
    parser.add_argument("--split", default="dev")
    parser.add_argument("--autoprep-root", type=Path, default=AUTOPREP_ROOT)
    parser.add_argument(
        "--table-specs",
        type=Path,
        default=PROJECT_ROOT / "dependency_modeling_react_joint" / "results" / "oracle_v1_group_a_specs.jsonl",
        help="JSONL generated by generate_oracle_table_specs.py or generate_table_specs.py.",
    )
    parser.add_argument(
        "--case-file",
        type=Path,
        default=PROJECT_ROOT / "pipeline_eval" / "cases_group_a_high_ops_union_structural.jsonl",
        help="Optional task subset; pass an empty/nonexistent path to evaluate all table specs.",
    )
    parser.add_argument("--task-ids", nargs="*", help="Optional task id filter, comma-separated or space-separated.")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=0.15)
    parser.add_argument("--aggressive-datetime", action="store_true")
    parser.add_argument("--raw-view-schema", action="store_true",
                        help="do NOT expand the view schema into the full DB table schema (expanding is the default, to align with the training distribution).")
    parser.add_argument("--output-details", type=Path, default=HERE / "results" / "single_ops_type_eval_details.jsonl")
    parser.add_argument("--output-summary", type=Path, default=HERE / "results" / "single_ops_type_eval_summary.json")
    args = parser.parse_args()

    summary = evaluate(args)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
