#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.util
import json
import os
import re
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
# Point at your DeepPrep checkout; there is no sensible default.
DEEPPREP_ROOT = Path(os.environ.get("DEEPPREP_ROOT", ""))
BASELINES_ROOT = HERE.parent
T2P_SHARED = BASELINES_ROOT / "text-to-pipeline-adapted" / "run_staged.py"
BAT_ADAPTED = BASELINES_ROOT / "bat-adapted" / "run_staged.py"
GOLD_SPEC = BASELINES_ROOT / "adapted_gold_spec.py"
DEFAULT_SELECTION_CACHE_ROOT = BASELINES_ROOT / "adapted-shared" / "table-selection"
DEFAULT_STAGE2_CACHE_ROOT = BASELINES_ROOT / "adapted-shared" / "target-metadata"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


shared = load_module("t2p_adapted_shared", T2P_SHARED)
bat_shared = load_module("bat_adapted_shared", BAT_ADAPTED)
gold_spec = load_module("adapted_gold_spec_for_deepprep", GOLD_SPEC)


@contextmanager
def pushd(path: Path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def clear_src_modules() -> None:
    for name in list(sys.modules):
        if name == "src" or name.startswith("src.") or name == "app" or name.startswith("app.") or name == "_values" or name.startswith("_values."):
            sys.modules.pop(name, None)


def load_deepprep_backend():
    clear_src_modules()
    root = str(DEEPPREP_ROOT)
    sys.path = [
        p for p in sys.path
        if p != root
        and "Text-to-Pipeline-main" not in p
        and "BAT-main" not in p
    ]
    sys.path.insert(0, root)
    importlib.invalidate_caches()
    with pushd(DEEPPREP_ROOT):
        from src.data import DataPool, Task
        from src.framework.mcts import MCTSFramework
        from src.tools.helper import Config
        from src.tools.helper.gpt_inference import USAGE_TRACKER
    return DataPool, Task, MCTSFramework, Config, USAGE_TRACKER


def schema_payload(target_meta: Dict[str, Any]) -> Dict[str, Any]:
    cols = {}
    desc = str(target_meta.get("target_description") or "")
    for col in target_meta["target_columns"]:
        cols[str(col)] = {
            "description": f"Column required in the prepared table. {desc}".strip(),
            "requirements": [],
        }
    return {
        "Task Description": (
            f"{desc}\n\n"
            "Prepare this single source table according to the target columns. "
            "Preserve columns needed by later integration."
        ),
        "Column Schema": cols,
    }


def usage_from_deepprep_tracker(tracker) -> Dict[str, Any]:
    try:
        snap = tracker.snapshot()
    except Exception:
        snap = {}
    return {
        "input_tokens": int(snap.get("prompt_tokens") or snap.get("input_tokens") or 0),
        "output_tokens": int(snap.get("completion_tokens") or snap.get("output_tokens") or 0),
        "total_tokens": int(snap.get("total_tokens") or 0),
        "llm_calls": int(snap.get("llm_calls") or snap.get("calls") or 0),
    }


def usage_from_debug_file(path: Path) -> Dict[str, Any]:
    out = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "llm_calls": 0, "time_cost": 0.0}
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            out["input_tokens"] += int(row.get("prompt_tokens") or row.get("input_tokens") or 0)
            out["output_tokens"] += int(row.get("completion_tokens") or row.get("output_tokens") or 0)
            out["total_tokens"] += int(row.get("total_tokens") or 0)
            out["llm_calls"] += int(row.get("llm_calls") or row.get("calls") or 0)
            out["time_cost"] += float(row.get("wall_time_sec") or row.get("time_cost") or 0.0)
    return out


def inject_schema(DataPool, benchmark: str, split: str, pseudo_task_id: str, source_file: str, payload: Dict[str, Any]) -> None:
    DataPool.tbl_schema_description.setdefault(benchmark, {}).setdefault(split, {})[pseudo_task_id] = payload
    DataPool.origin_case.setdefault(benchmark, {}).setdefault(split, {})[pseudo_task_id] = {
        "task_id": pseudo_task_id,
        "input_table": [source_file],
        "target_table": None,
        "question": None,
    }


def strip_deepprep_script_to_body(script_text: str) -> str:
    lines = []
    started = False
    for line in script_text.splitlines():
        if re.match(r"^table_\d+\s*=\s*input_tables\[", line):
            started = True
        if not started:
            continue
        if line.startswith("import ") or line.startswith("from "):
            continue
        lines.append(line)
    if not lines:
        lines = ["table_1 = input_tables['table_1'].copy()", "result = {'table_1': table_1}"]
    return "\n".join(lines)


def deepprep_script_to_function(name: str, script_text: str) -> str:
    body = strip_deepprep_script_to_body(script_text)
    indented = "\n".join("    " + line if line.strip() else "" for line in body.splitlines())
    return f"""
def {name}(table_1):
    input_tables = {{'table_1': table_1}}
{indented}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
""".strip()


def run_deepprep_table(
    DataPool,
    Task,
    MCTSFramework,
    Config,
    USAGE_TRACKER,
    *,
    benchmark: str,
    split: str,
    task_id: str,
    source_file: str,
    target_meta: Dict[str, Any],
    debug_root: Path,
    max_steps: int | None,
) -> tuple[str, Dict[str, Any], Dict[str, Any]]:
    pseudo_task_id = task_id
    inject_schema(DataPool, benchmark, split, pseudo_task_id, source_file, schema_payload(target_meta))

    old_debug = os.environ.get("DS_AGENT_DEBUG_DIR")
    os.environ["DS_AGENT_DEBUG_DIR"] = str(debug_root)
    started = time.time()
    try:
        with pushd(DEEPPREP_ROOT):
            cfg = Config.load_base_config()
            if max_steps is not None:
                cfg.set("mcts_max_steps", max_steps)
            framework = MCTSFramework(cfg=cfg, log_file=f"deepprep_adapted_{task_id}")
            trial = framework.run(Task(id=pseudo_task_id, inp_tbl_names=[source_file], tgt_tbl_name="", tgt_tbl_description=True, split=split))
            combined_path = debug_root / pseudo_task_id / "combined_execution.py"
            if not combined_path.exists():
                raise FileNotFoundError(f"DeepPrep did not export {combined_path}")
            script_text = combined_path.read_text(encoding="utf-8")
            usage = usage_from_debug_file(debug_root / pseudo_task_id / "usage.jsonl")
            if not usage["llm_calls"]:
                usage = usage_from_deepprep_tracker(USAGE_TRACKER)
            usage["time_cost"] = usage.get("time_cost") or (time.time() - started)
            artifact = {
                "pseudo_task_id": pseudo_task_id,
                "matched": getattr(trial, "matched", False),
                "combined_execution": str(combined_path),
                "best_chain": [str(op) for op in ((trial.recording.get("best_chain") or [None])[-1] or [])],
            }
            return script_text, usage, artifact
    finally:
        if old_debug is None:
            os.environ.pop("DS_AGENT_DEBUG_DIR", None)
        else:
            os.environ["DS_AGENT_DEBUG_DIR"] = old_debug


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark_path", required=True)
    ap.add_argument("--benchmark_name", required=True)
    ap.add_argument("--table_dir", required=True)
    ap.add_argument("--model_name", default=None)
    ap.add_argument("--sample_rows", type=int, default=3)
    ap.add_argument("--max_schema_cols", type=int, default=40)
    ap.add_argument("--max_cell_chars", type=int, default=200)
    ap.add_argument("--max_steps", type=int, default=None)
    ap.add_argument("--max_tasks", type=int, default=None)
    ap.add_argument("--task_ids", nargs="*")
    ap.add_argument("--reasoning_effort", default="minimal")
    ap.add_argument("--result_root", default=str(HERE / "results"))
    ap.add_argument("--selection_cache_root", default=str(DEFAULT_SELECTION_CACHE_ROOT))
    ap.add_argument("--stage2_cache_root", default=str(DEFAULT_STAGE2_CACHE_ROOT))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--force-selection", action="store_true")
    ap.add_argument("--force-stage2", action="store_true")
    ap.add_argument("--use-gold-tables", action="store_true",
                    help="skip Stage 1 and use benchmark gold relevant tables")
    ap.add_argument("--use-gold-specification", action="store_true",
                    help="skip Stage 2 and use benchmark dc_ops/output metadata as gold target metadata")
    args = ap.parse_args()

    adapter = shared.load_adapter(REPO / "example" / "Text-to-Pipeline-main")
    llm_config, model_name = adapter.load_llm_config(REPO / "example" / "Text-to-Pipeline-main" / "config/default_config.yaml", args.model_name)
    meta_llm = adapter.LLMClient(llm_config, model_name=model_name)
    meta_llm.reasoning_effort = args.reasoning_effort
    DataPool, Task, MCTSFramework, Config, USAGE_TRACKER = load_deepprep_backend()

    result_root = Path(args.result_root)
    if args.use_gold_tables and args.use_gold_specification and args.result_root == str(HERE / "results"):
        result_root = HERE / "results_gold_tables_gold_spec"
    elif args.use_gold_tables and args.result_root == str(HERE / "results"):
        result_root = HERE / "results_gold_tables"
    code_dir = result_root / "codes" / args.benchmark_name
    artifact_dir = result_root / "artifacts" / args.benchmark_name
    debug_root = result_root / "deepprep_debug_logs"
    record_path = result_root / "records" / f"{args.benchmark_name}.jsonl"
    code_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    debug_root.mkdir(parents=True, exist_ok=True)

    rows = bat_shared.read_jsonl(Path(args.benchmark_path))
    if args.task_ids:
        wanted = set(args.task_ids)
        rows = [r for r in rows if r.get("task_id") in wanted]
    if args.max_tasks is not None:
        rows = rows[:args.max_tasks]

    table_dir = Path(args.table_dir)
    for pos, item in enumerate(rows, 1):
        task_id = item["task_id"]
        code_path = code_dir / f"{task_id}.py"
        if code_path.exists() and not args.force:
            continue
        meta_llm.reset_token_usage()
        usage_by_stage: Dict[str, Dict[str, Any]] = {}
        started = time.time()
        try:
            candidate_files = item.get("input_table", [])
            candidate_tables = adapter.load_input_tables(candidate_files, table_dir)
            max_selected = {"nl2sql-spider": 4, "nl2sql-bird": 4, "beaver": 7, "realdp": 8}.get(args.benchmark_name, len(candidate_tables))
            if args.use_gold_tables:
                selected_indices = shared.gold_indices(item, args.benchmark_name)
                selection_obj = {
                    "relevant_table_files": [candidate_files[i] for i in selected_indices]
                }
                usage_by_stage["table_selection"] = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "llm_calls": 0,
                    "time_cost": 0.0,
                }
            else:
                selector = shared.selector_prompt(item.get("question", ""), candidate_files, candidate_tables, 2, max_selected, args.max_schema_cols)
                prompt_sha = hashlib.sha256(selector.encode("utf-8")).hexdigest()
                cache_dir = Path(args.selection_cache_root) / args.benchmark_name
                cache_dir.mkdir(parents=True, exist_ok=True)
                cache_path = cache_dir / f"{task_id}.json"
                cached = None
                if cache_path.exists() and not args.force_selection:
                    cand = json.loads(cache_path.read_text(encoding="utf-8"))
                    if cand.get("prompt_sha256") == prompt_sha and cand.get("candidate_table_files") == candidate_files and cand.get("model") == meta_llm.model:
                        cached = cand
                if cached:
                    selection_obj = cached["selection_decision"]
                    usage_by_stage["table_selection"] = cached["usage"]
                else:
                    before = bat_shared.usage_snapshot_t2p(meta_llm)
                    t0 = time.time()
                    selection_obj = shared.extract_json(adapter, meta_llm.generate(selector))
                    u = bat_shared.usage_delta_t2p(bat_shared.usage_snapshot_t2p(meta_llm), before)
                    u["time_cost"] = time.time() - t0
                    usage_by_stage["table_selection"] = u
                    selected_tmp = shared.normalize_file_selection(selection_obj, candidate_files)
                    cache_path.write_text(json.dumps({
                        "cache_version": 1, "benchmark": args.benchmark_name, "task_id": task_id,
                        "question": item.get("question", ""), "candidate_table_files": candidate_files,
                        "model": meta_llm.model, "reasoning_effort": args.reasoning_effort,
                        "prompt_sha256": prompt_sha, "selector_prompt": selector,
                        "selection_decision": selection_obj, "selected_table_indices": selected_tmp,
                        "selected_table_files": [candidate_files[i] for i in selected_tmp],
                        "usage": u,
                    }, ensure_ascii=False, indent=2), encoding="utf-8")

                selected_indices = shared.normalize_file_selection(selection_obj, candidate_files)
            selected_original = [f"table_{i + 1}" for i in selected_indices]
            selected_files = [candidate_files[i] for i in selected_indices]
            selected_tables = {f"table_{i + 1}": candidate_tables[orig] for i, orig in enumerate(selected_original)}
            selected_context = shared.bounded_table_context(selected_tables, args.sample_rows, args.max_schema_cols, args.max_cell_chars)

            if args.use_gold_specification:
                plan, table_targets, answer_code = gold_spec.target_metadata_gold_stage2(
                    item, selected_tables, table_dir
                )
                u = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "llm_calls": 0, "time_cost": 0.0}
            else:
                plan, table_targets, answer_code, u, _stage2_cached = bat_shared.get_or_generate_stage2_plan(
                    adapter=adapter,
                    llm=meta_llm,
                    benchmark=args.benchmark_name,
                    task_id=task_id,
                    question=item.get("question", ""),
                    selected_context=selected_context,
                    selected_files=selected_files,
                    selected_tables=selected_tables,
                    stage2_cache_root=Path(args.stage2_cache_root),
                    reasoning_effort=args.reasoning_effort,
                    force_stage2=args.force_stage2,
                )
            usage_by_stage["target_metadata_generation"] = u

            functions: List[str] = []
            deepprep_artifacts = []
            pipeline_usages = []
            for i, target_meta in enumerate(table_targets, 1):
                pseudo_task_id = f"{task_id}__deepprep_adapted_{i}"
                if target_meta.get("identity_fallback"):
                    functions.append(f"""
def _prep_{i}(table_1):
    return table_1.copy()
""".strip())
                    pipeline_usages.append({"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "llm_calls": 0, "time_cost": 0.0})
                    deepprep_artifacts.append({"pseudo_task_id": pseudo_task_id, "identity_fallback": True})
                    continue
                script_text, pipe_usage, artifact = run_deepprep_table(
                    DataPool, Task, MCTSFramework, Config, USAGE_TRACKER,
                    benchmark=args.benchmark_name,
                    split="dev",
                    task_id=pseudo_task_id,
                    source_file=selected_files[i - 1],
                    target_meta=target_meta,
                    debug_root=debug_root,
                    max_steps=args.max_steps,
                )
                functions.append(deepprep_script_to_function(f"_prep_{i}", script_text))
                pipeline_usages.append(pipe_usage)
                deepprep_artifacts.append(artifact)
            usage_by_stage["pipeline_generation"] = bat_shared.usage_add(*pipeline_usages)

            target_names = [t["target_table_name"] for t in table_targets]
            code_path.write_text(bat_shared.assemble(functions, selected_original, answer_code, target_names), encoding="utf-8")
            total = bat_shared.usage_add(*usage_by_stage.values())
            total["time_cost"] = time.time() - started
            bat_shared.append_jsonl(record_path, {
                "task_id": task_id,
                "benchmark": args.benchmark_name,
                **total,
                "usage_by_stage": usage_by_stage,
                "selected_table_indices": selected_indices,
                "selection_source": "gold" if args.use_gold_tables else "stage1",
                "specification_source": "gold" if args.use_gold_specification else "stage2",
            })
            artifact_dir.joinpath(f"{task_id}.json").write_text(json.dumps({
                "task_id": task_id,
                "selection_source": "gold" if args.use_gold_tables else "stage1",
                "specification_source": "gold" if args.use_gold_specification else "stage2",
                "selected_table_indices": selected_indices,
                "selected_table_files": selected_files,
                "table_targets": table_targets,
                "integration_plan": plan.get("integration_plan"),
                "answer_code": answer_code,
                "deepprep_artifacts": deepprep_artifacts,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[{pos}/{len(rows)}] {task_id} selected={selected_indices}")
        except Exception as exc:
            total = bat_shared.usage_add(*usage_by_stage.values())
            total["time_cost"] = time.time() - started
            bat_shared.append_jsonl(record_path, {
                "task_id": task_id,
                "benchmark": args.benchmark_name,
                **total,
                "usage_by_stage": usage_by_stage,
                "error": f"{type(exc).__name__}: {exc}",
            })
            print(f"[{pos}/{len(rows)}] {task_id} failed: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
