from __future__ import annotations

import os
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_PROJECT_ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
DEFAULT_AUTOPREP_ROOT = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
DEFAULT_HIGH_OPS_CASES = DEFAULT_PROJECT_ROOT / "dependency_modeling" / "high_ops_single_dependency_cases.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()


def load_jsonl_by_task(path: Path) -> dict[str, dict[str, Any]]:
    return {str(row.get("task_id")): row for row in load_jsonl(path) if row.get("task_id")}


def dependency_logical_tables(reason: str) -> set[str]:
    reason = reason or ""
    out: set[str] = set()
    clauses = re.split(r"(?=(?:On|Within|For|Operations on)\s+table_\d+)", reason)
    positive_markers = [
        "must precede",
        "depends",
        "dependent",
        "required order",
        "order-dependent",
        "non-commutative",
        "not safely swappable",
        "then reads",
        "then depends",
        "before",
        "creates",
        "produces",
    ]
    negative_markers = [
        "independent and swappable",
        "are independent",
        "unrelated",
        "swappable",
    ]
    for clause in clauses:
        tables = set(re.findall(r"\btable_\d+\b", clause))
        if not tables:
            continue
        lowered = clause.lower()
        has_positive = any(marker in lowered for marker in positive_markers)
        has_negative = any(marker in lowered for marker in negative_markers)
        if has_positive and not has_negative:
            out.update(tables)
    return out or set(re.findall(r"\btable_\d+\b", reason))


def logical_table_for_file(task: dict[str, Any], table_file: str) -> str:
    for idx, file_name in enumerate(task.get("input_table") or [], start=1):
        if str(file_name) == str(table_file):
            return f"table_{idx}"
    return ""


def file_for_logical_table(task: dict[str, Any], logical_table: str) -> str | None:
    match = re.match(r"table_(\d+)$", logical_table)
    if not match:
        return None
    idx = int(match.group(1)) - 1
    inputs = task.get("input_table") or []
    if 0 <= idx < len(inputs):
        return str(inputs[idx])
    return None


def find_table_file(root: Path, file_name: str, cache: dict[str, Path | None] | None = None) -> Path | None:
    if cache is not None and file_name in cache:
        return cache[file_name]
    direct = root / file_name
    if direct.exists():
        if cache is not None:
            cache[file_name] = direct
        return direct
    matches = list(root.rglob(file_name))
    out = matches[0] if matches else None
    if cache is not None:
        cache[file_name] = out
    return out


def load_test_task_ids(
    high_ops_cases: Path,
    benchmark: str | None,
    include_cross_table_dependency: bool,
) -> set[str]:
    ids: set[str] = set()
    for row in load_jsonl(high_ops_cases):
        if benchmark and row.get("benchmark") != benchmark:
            continue
        if not bool(row.get("single_table_dependency")):
            continue
        if bool(row.get("cross_table_dependency")) and not include_cross_table_dependency:
            continue
        if row.get("task_id"):
            ids.add(str(row["task_id"]))
    return ids


def load_case_file(path: Path, benchmark: str | None = None) -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}
    if not path or not path.exists():
        return cases
    for row in load_jsonl(path):
        if benchmark and row.get("benchmark") and row.get("benchmark") != benchmark:
            continue
        task_id = row.get("task_id") or row.get("query_id")
        if not task_id:
            continue
        groups = row.get("case_groups") or row.get("groups") or row.get("tags") or []
        if isinstance(groups, str):
            groups = [groups]
        cases[str(task_id)] = {
            "task_id": str(task_id),
            "benchmark": row.get("benchmark"),
            "case_groups": [str(x) for x in groups],
        }
    return cases


def load_case_order(path: Path | None, benchmark: str | None = None) -> list[str]:
    if not path or not path.exists():
        return []
    return list(load_case_file(path, benchmark=benchmark).keys())


def load_schema_linking_selected_tables(path: Path | None, schema_mode: str = "recovered") -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    for row in load_jsonl(path):
        if schema_mode and row.get("schema_mode") != schema_mode:
            continue
        task_id = row.get("task_id")
        if not task_id:
            continue
        files = row.get("relevant_table_files") or (row.get("llm_output") or {}).get("relevant_table_files") or []
        if not files:
            files = [x.get("file_name") for x in row.get("candidate_tables") or [] if x.get("file_name")]
        matches = row.get("table_matches") or (row.get("llm_output") or {}).get("table_matches") or []
        out[str(task_id)] = {
            "selected_table_files": [str(x) for x in files],
            "table_matches": matches,
            "schema_mode": row.get("schema_mode"),
        }
    return out


def build_instances(args) -> list[dict[str, Any]]:
    task_filter: set[str] | None = set(args.task_ids or []) if args.task_ids else None
    case_meta: dict[str, dict[str, Any]] = {}
    case_order: list[str] = []
    if getattr(args, "case_file", None):
        case_meta = load_case_file(args.case_file, benchmark=args.benchmark)
        case_order = list(case_meta.keys())
        case_ids = set(case_meta)
        task_filter = case_ids if task_filter is None else task_filter & case_ids
    schema_selected = load_schema_linking_selected_tables(
        getattr(args, "schema_linking_output", None),
        schema_mode=getattr(args, "schema_linking_mode", "recovered"),
    )
    if args.test:
        test_ids = load_test_task_ids(
            args.high_ops_cases,
            benchmark=args.benchmark,
            include_cross_table_dependency=args.include_cross_table_dependency,
        )
        task_filter = test_ids if task_filter is None else task_filter & test_ids
        dep_desc = (
            "single_table_dependency with or without cross_table_dependency"
            if args.include_cross_table_dependency
            else "single_table_dependency and not cross_table_dependency"
        )
        print(f"--test loaded {len(test_ids)} task IDs ({dep_desc}) from {args.high_ops_cases}")

    benchmark_dir = args.autoprep_root / args.benchmark / args.split
    benchmark_by_task = load_jsonl_by_task(benchmark_dir / "benchmark.jsonl")
    dependency_by_task = load_jsonl_by_task(benchmark_dir / "dependency_summary.jsonl")

    instances: list[dict[str, Any]] = []
    for task_id, task in benchmark_by_task.items():
        if task_filter is not None and task_id not in task_filter:
            continue
        dep = dependency_by_task.get(task_id, {})
        dep_tables = dependency_logical_tables(str(dep.get("single_table_dependency_reason", "")))
        selected_files = schema_selected.get(task_id, {}).get("selected_table_files", [])
        selected_file_set = set(selected_files)
        if selected_files:
            logical_tables = [
                logical_table_for_file(task, table_file)
                for table_file in selected_files
                if logical_table_for_file(task, table_file)
            ]
        elif args.dependency_tables_only and dep_tables:
            logical_tables = sorted(dep_tables, key=lambda x: int(x.split("_")[1]))
        else:
            logical_tables = [f"table_{i}" for i in range(1, len(task.get("input_table") or []) + 1)]

        for logical_table in logical_tables:
            table_file = file_for_logical_table(task, logical_table)
            if not table_file:
                continue
            instances.append(
                {
                    "benchmark": args.benchmark,
                    "split": args.split,
                    "task_id": task_id,
                    "origin_idx": task.get("origin_idx"),
                    "db_id": task.get("db_id"),
                    "question": task.get("question") or task.get("intent") or "",
                    "table_file": table_file,
                    "input_tables": selected_files or [str(x) for x in task.get("input_table") or []],
                    "schema_linking_selected_tables": selected_files,
                    "schema_linking_table_matches": schema_selected.get(task_id, {}).get("table_matches", []),
                    "logical_table": logical_table,
                    "dependency_logical_tables": sorted(dep_tables),
                    "single_table_dependency_reason": dep.get("single_table_dependency_reason", ""),
                    "cross_table_dependency": bool(dep.get("cross_table_dependency_exists", False)),
                    "case_groups": case_meta.get(task_id, {}).get("case_groups", []),
                }
            )

    if case_order:
        order_idx = {task_id: idx for idx, task_id in enumerate(case_order)}
        instances.sort(
            key=lambda item: (
                order_idx.get(str(item.get("task_id")), 10**9),
                int(str(item.get("logical_table", "table_999")).split("_")[-1]),
            )
        )
    task_limit = getattr(args, "task_limit", None)
    if task_limit is not None:
        kept_tasks = set()
        limited: list[dict[str, Any]] = []
        for item in instances:
            tid = str(item.get("task_id"))
            if tid not in kept_tasks:
                if len(kept_tasks) >= task_limit:
                    continue
                kept_tasks.add(tid)
            limited.append(item)
        instances = limited

    if args.limit is not None:
        instances = instances[: args.limit]
    return instances


def record_key(record: dict[str, Any]) -> str:
    return "::".join(
        [
            str(record.get("benchmark", "")),
            str(record.get("split", "")),
            str(record.get("task_id", "")),
            str(record.get("table_file", "")),
        ]
    )


def processed_keys(path: Path) -> set[str]:
    return {record_key(row) for row in load_jsonl(path) if record_key(row)}
