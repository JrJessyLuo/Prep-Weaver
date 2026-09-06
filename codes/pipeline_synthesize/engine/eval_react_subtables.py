#!/usr/bin/env python3
from __future__ import annotations

import os
import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
AUTOPREP_ROOT = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
DEEPPREP_EVAL = Path(os.environ.get(
    "DEEPPREP_EVAL_DIR", ""))
if str(DEEPPREP_EVAL) not in sys.path:
    sys.path.insert(0, str(DEEPPREP_EVAL))


def _lineage():
    """The external DeepPrep lineage tracer, imported on first use.

    It is needed by `trace_code` alone, which scores EXPORTED scripts. This
    module is also on the synthesis path — `phase2_joinkey` imports
    `norm_values` from it for join repair — so importing lineage at module level
    made pipeline synthesis fail outright on any machine without a DeepPrep
    checkout, for a function synthesis never calls. Deferring it keeps scoring
    working where the checkout exists and stops it blocking synthesis where it
    does not.
    """
    import lineage as _l
    return _l


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path or not path.exists():
        return rows
    for line in path.open("r", encoding="utf-8"):
        if line.strip():
            rows.append(json.loads(line))
    return rows


def norm_values(vals) -> set[str]:
    out = set()
    for v in vals:
        if v is None:
            continue
        s = str(v).strip()
        if not s or s.lower() in {"nan", "none", "<na>", "null"}:
            continue
        if len(s) >= 2 and s[0] == s[-1] and s[0] in {'"', "'"}:
            s = s[1:-1].strip()
        try:
            f = float(s)
            s = str(int(f)) if f == int(f) else repr(f)
        except Exception:
            s = s.casefold()
        out.add(s)
    return out


def fast_norm_series(s, max_values: int = 5000) -> set[str]:
    try:
        if isinstance(s, pd.DataFrame):
            s = s.iloc[:, 0]
        s = pd.Series(s).dropna()
        if max_values and len(s) > max_values:
            s = s.sample(max_values, random_state=0)
        return norm_values(s.astype(str).drop_duplicates().tolist())
    except Exception:
        return set()


def vmatch(method_values: set[str], gold_values: set[str]) -> bool:
    if not method_values or not gold_values:
        return False
    inter = len(method_values & gold_values)
    if inter < min(2, len(gold_values)):
        return False
    return inter / len(method_values) >= 0.8


def edge_match(pred: dict[str, set[str]], gold: dict[str, set[str]]) -> bool:
    return (
        vmatch(pred["left"], gold["left"]) and vmatch(pred["right"], gold["right"])
    ) or (
        vmatch(pred["left"], gold["right"]) and vmatch(pred["right"], gold["left"])
    )


def dedup_value_domains(domains):
    seen = set()
    out = []
    for vals in domains or []:
        if not vals:
            continue
        sig = frozenset(vals)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(vals)
    return out


def max_value_domain_matching(pred_domains, gold_domains) -> tuple[int, int]:
    pred_domains = dedup_value_domains(pred_domains)
    gold_domains = dedup_value_domains(gold_domains)
    match_to_pred = {}

    def dfs(pi, seen):
        for gi, gold in enumerate(gold_domains):
            if gi in seen or not vmatch(pred_domains[pi], gold):
                continue
            seen.add(gi)
            if gi not in match_to_pred or dfs(match_to_pred[gi], seen):
                match_to_pred[gi] = pi
                return True
        return False

    matched = 0
    for pi in range(len(pred_domains)):
        if dfs(pi, set()):
            matched += 1
    return matched, len(gold_domains)


def gt_birdspider(task_id: str, benchmark: str, split: str, autoprep_root: Path) -> dict[str, Any] | None:
    path = autoprep_root / benchmark / split / "outputs" / f"{task_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    gt = {"cols": [], "edges": []}
    for edge in data.get("join_keys", []) + data.get("set_relations", []):
        left = norm_values(edge.get("left_values", []))
        right = norm_values(edge.get("right_values", []))
        if left or right:
            gt["edges"].append({"left": left, "right": right})
    db_path = data.get("db_path")
    table_columns = data.get("table_columns", {})
    if db_path and Path(db_path).exists():
        con = sqlite3.connect(db_path)
        try:
            for table, cols in table_columns.items():
                for col in cols:
                    try:
                        vals = con.execute(f'SELECT DISTINCT "{col}" FROM "{table}"').fetchall()
                        value_set = norm_values(row[0] for row in vals)
                        if value_set:
                            gt["cols"].append(value_set)
                    except Exception:
                        pass
        finally:
            con.close()
    return gt


def react_predictions(task_output_path: Path) -> dict[str, Any]:
    data = json.loads(task_output_path.read_text(encoding="utf-8"))
    cols = []
    for table in data.get("prepared_tables", []):
        path = table.get("prepared_subtable_path")
        if not path:
            continue
        try:
            df = pd.read_pickle(path)
        except Exception:
            continue
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)
        for col in df.columns:
            vals = fast_norm_series(df[col])
            if vals:
                cols.append(vals)
    edges = []
    for edge in data.get("join_edges", []):
        try:
            left_df = next(t for t in data.get("prepared_tables", []) if t.get("table_file") == edge.get("left_table"))
            right_df = next(t for t in data.get("prepared_tables", []) if t.get("table_file") == edge.get("right_table"))
            ldf = pd.read_pickle(left_df["prepared_subtable_path"])
            rdf = pd.read_pickle(right_df["prepared_subtable_path"])
            left_vals = fast_norm_series(ldf[edge["left_col"]])
            right_vals = fast_norm_series(rdf[edge["right_col"]])
            if left_vals or right_vals:
                edges.append({"left": left_vals, "right": right_vals})
        except Exception:
            continue
    return {"cols": cols, "edges": edges}


def load_input_tables(task: dict[str, Any], benchmark_dir: Path) -> dict[str, pd.DataFrame]:
    tables = {}
    for idx, file_name in enumerate(task.get("input_table") or [], start=1):
        path = benchmark_dir / file_name
        if not path.exists():
            matches = list(benchmark_dir.rglob(str(file_name)))
            path = matches[0] if matches else path
        if not path.exists():
            continue
        try:
            obj = pd.read_pickle(path)
            df = obj if isinstance(obj, pd.DataFrame) else pd.DataFrame(obj)
            tables[str(file_name)] = df
            tables[f"table_{idx}"] = df
        except Exception:
            continue
    return tables


def baseline_predictions(task: dict[str, Any], benchmark: str, split: str, code_dir: Path, autoprep_root: Path) -> dict[str, Any] | None:
    code_path = code_dir / f"{task['task_id']}.py"
    if not code_path.exists():
        return None
    tables = load_input_tables(task, autoprep_root / benchmark / split)
    try:
        result = _lineage().trace_code(code_path.read_text(encoding="utf-8"), tables, str(code_path))
    except BaseException:
        return None
    cols = []
    for value_set in result.get("any_cols", []):
        vals = norm_values(value_set)
        if vals:
            cols.append(vals)
    for prepared in result.get("prepared", []):
        for value_set in prepared:
            vals = norm_values(value_set)
            if vals:
                cols.append(vals)
    edges = []
    for join in result.get("joins", []):
        left = norm_values(join.get("left", {}).get("values", []))
        right = norm_values(join.get("right", {}).get("values", []))
        if left or right:
            edges.append({"left": left, "right": right})
    return {"cols": cols, "edges": edges}


def score_predictions(pred: dict[str, Any] | None, gt: dict[str, Any] | None) -> dict[str, Any]:
    if not pred or not gt:
        return {
            "subtable_full": False,
            "subtable_recall": 0.0,
            "join_key_full": False,
            "join_key_recall": 0.0,
            "gold_cols": len(gt.get("cols", [])) if gt else 0,
            "gold_edges": len(gt.get("edges", [])) if gt else 0,
        }
    gold_cols = gt.get("cols", [])
    pred_cols = pred.get("cols", [])
    matched_cols, total_cols = max_value_domain_matching(pred_cols, gold_cols)
    gold_edges = gt.get("edges", [])
    pred_edges = pred.get("edges", [])
    matched_edges = sum(1 for gold in gold_edges if any(edge_match(method, gold) for method in pred_edges))
    return {
        "subtable_full": bool(gold_cols) and matched_cols == total_cols,
        "subtable_recall": matched_cols / max(total_cols, 1),
        "join_key_full": matched_edges == len(gold_edges),
        "join_key_recall": matched_edges / max(len(gold_edges), 1),
        "matched_cols": matched_cols,
        "gold_cols": len(gold_cols),
        "matched_edges": matched_edges,
        "gold_edges": len(gold_edges),
    }


def load_benchmark_tasks(benchmark: str, split: str, autoprep_root: Path) -> dict[str, dict[str, Any]]:
    path = autoprep_root / benchmark / split / "benchmark.jsonl"
    return {row["task_id"]: row for row in load_jsonl(path)}


def load_case_groups(path: Path | None) -> dict[str, list[str]]:
    if not path or not path.exists():
        return {}
    out = {}
    for row in load_jsonl(path):
        tid = row.get("task_id") or row.get("query_id")
        if not tid:
            continue
        groups = row.get("case_groups") or row.get("groups") or row.get("tags") or []
        if isinstance(groups, str):
            groups = [groups]
        out[str(tid)] = [str(g) for g in groups] or ["all"]
    return out


def summarize(details: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in details:
        method = row["method"]
        groups = row.get("case_groups") or ["all"]
        for group in ["all"] + groups:
            buckets.setdefault((method, group), []).append(row)
    for (method, group), rows in buckets.items():
        summary.setdefault(method, {})[group] = {
            "n": len(rows),
            "subtable_full_accuracy": sum(bool(r["subtable_full"]) for r in rows) / max(len(rows), 1),
            "subtable_recall": sum(float(r["subtable_recall"]) for r in rows) / max(len(rows), 1),
            "join_key_full_accuracy": sum(bool(r["join_key_full"]) for r in rows) / max(len(rows), 1),
            "join_key_recall": sum(float(r["join_key_recall"]) for r in rows) / max(len(rows), 1),
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate React prepared subtables and predicted join edges.")
    parser.add_argument("--benchmark", default="nl2sql-bird")
    parser.add_argument("--split", default="dev")
    parser.add_argument("--autoprep-root", type=Path, default=AUTOPREP_ROOT)
    parser.add_argument("--react-task-output-dir", type=Path, required=True)
    parser.add_argument("--baseline-code-dir", type=Path, default=None)
    parser.add_argument("--baseline-name", default="baseline")
    parser.add_argument("--case-file", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--details-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    args = parser.parse_args()

    tasks = load_benchmark_tasks(args.benchmark, args.split, args.autoprep_root)
    case_groups = load_case_groups(args.case_file)
    task_ids = list(case_groups) if case_groups else sorted(tasks)
    if args.limit is not None:
        task_ids = task_ids[: args.limit]

    details = []
    for task_id in task_ids:
        task = tasks.get(task_id)
        if not task:
            continue
        gt = gt_birdspider(task_id, args.benchmark, args.split, args.autoprep_root)
        groups = case_groups.get(task_id, ["all"])
        react_path = args.react_task_output_dir / args.benchmark / f"{task_id}.json"
        if react_path.exists():
            score = score_predictions(react_predictions(react_path), gt)
            details.append({"method": "react", "task_id": task_id, "case_groups": groups, **score})
        if args.baseline_code_dir:
            pred = baseline_predictions(task, args.benchmark, args.split, args.baseline_code_dir, args.autoprep_root)
            score = score_predictions(pred, gt)
            details.append({"method": args.baseline_name, "task_id": task_id, "case_groups": groups, **score})

    args.details_output.parent.mkdir(parents=True, exist_ok=True)
    with args.details_output.open("w", encoding="utf-8") as f:
        for row in details:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summarize(details), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(details)} detail records to {args.details_output}")
    print(f"Wrote summary to {args.summary_output}")


if __name__ == "__main__":
    main()
