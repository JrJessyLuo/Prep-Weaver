#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASELINES_ROOT = HERE.parent
SHARED_T2P = BASELINES_ROOT / "text-to-pipeline-adapted" / "run_staged.py"
GOLD_SPEC = BASELINES_ROOT / "adapted_gold_spec.py"
BAT_ROOT = BASELINES_ROOT / "BAT-main"
DEFAULT_SELECTION_CACHE_ROOT = BASELINES_ROOT / "adapted-shared" / "table-selection"
DEFAULT_STAGE2_CACHE_ROOT = BASELINES_ROOT / "adapted-shared" / "target-metadata"


def load_shared():
    spec = importlib.util.spec_from_file_location("t2p_adapted_shared", SHARED_T2P)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def load_gold_spec():
    spec = importlib.util.spec_from_file_location("adapted_gold_spec_shared", GOLD_SPEC)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


shared = load_shared()
gold_spec = load_gold_spec()
BATLLMClient = None
MCTSSolver = None
MCTSNode = None
MCTSNodeType = None
BenchmarkExecutionRewardModel = None


def load_bat_backend():
    global BATLLMClient, MCTSSolver, MCTSNode, MCTSNodeType, BenchmarkExecutionRewardModel
    for name in list(sys.modules):
        if name == "src" or name.startswith("src."):
            sys.modules.pop(name, None)
    if str(BAT_ROOT) not in sys.path:
        sys.path.insert(0, str(BAT_ROOT))
    from src.llm import LLMClient as _BATLLMClient
    from src.mcts.mcts import MCTSSolver as _MCTSSolver
    from src.mcts.node import MCTSNode as _MCTSNode, MCTSNodeType as _MCTSNodeType
    from src.mcts.reward import BenchmarkExecutionRewardModel as _BenchmarkExecutionRewardModel
    BATLLMClient = _BATLLMClient
    MCTSSolver = _MCTSSolver
    MCTSNode = _MCTSNode
    MCTSNodeType = _MCTSNodeType
    BenchmarkExecutionRewardModel = _BenchmarkExecutionRewardModel


TARGET_SCHEMA_PROMPT = """
Infer per-table target metadata for adapting BAT to question-conditioned table preparation.

You are given the user question and the selected relevant tables. Produce one target
schema for every selected table. The per-table target schema should describe the
prepared table that BAT should synthesize from that single source table before
cross-table integration. It must preserve join keys and evidence columns needed by
the final answer. Query-specific filtering, aggregation, sorting, and final answer
logic should be placed in answer_code, not in per-table target schemas.

Also infer how the prepared tables should be integrated. Preserve the columns that
participate in that integration in the relevant per-table target_columns. Prefer
semantic foreign-key-like columns with matching names or composite columns that can
be decomposed into matching keys. Do not use generic row identifiers such as id/uuid
as join keys unless the question or table schemas clearly imply that those
identifiers link the selected tables.

The answer_code must explicitly integrate the prepared tables using the inferred join
columns, then apply question-specific filtering/counting/aggregation.

Return JSON only:
{{
  "table_targets": [
    {{
      "table": "table_1",
      "target_table_name": "prepared_table_1",
      "target_columns": ["join_key", "value"],
      "target_description": "..."
    }}
  ],
  "integration_plan": [
    {{"left_table": "prepared_table_1", "left_key": "join_key", "right_table": "prepared_table_2", "right_key": "join_key"}}
  ],
  "answer_code": "target = prepared_table_1.merge(prepared_table_2, ...)"
}}

Question:
{question}

Selected tables:
{selected_context}
""".strip()


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def usage_snapshot_t2p(llm) -> Dict[str, Any]:
    return {
        "input_tokens": int(llm.token_usage.get("prompt_tokens") or 0),
        "output_tokens": int(llm.token_usage.get("completion_tokens") or 0),
        "total_tokens": int(llm.token_usage.get("total_tokens") or 0),
        "llm_calls": int(getattr(llm, "llm_calls", 0) or 0),
    }


def usage_delta_t2p(after: Dict[str, Any], before: Dict[str, Any]) -> Dict[str, Any]:
    return {k: int(after.get(k, 0) or 0) - int(before.get(k, 0) or 0) for k in after}


def usage_snapshot_bat(llm) -> Dict[str, Any]:
    return {
        "input_tokens": int(llm.token_usage.get("prompt_tokens") or 0),
        "output_tokens": int(llm.token_usage.get("completion_tokens") or 0),
        "total_tokens": int(llm.token_usage.get("total_tokens") or 0),
        "llm_calls": int(getattr(llm, "llm_calls", 0) or 0),
    }


def usage_add(*parts: Dict[str, Any]) -> Dict[str, Any]:
    out = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "llm_calls": 0, "time_cost": 0.0}
    for p in parts:
        for k in ("input_tokens", "output_tokens", "total_tokens", "llm_calls"):
            out[k] += int(p.get(k) or 0)
        out["time_cost"] += float(p.get("time_cost") or 0.0)
    return out


def normalize_plan(obj: Dict[str, Any], table_names: List[str], table_dfs: Dict[str, pd.DataFrame] | None = None):
    targets = obj.get("table_targets")
    if not isinstance(targets, list):
        raise ValueError("table_targets must be a list")
    by_name = {}
    for raw in targets:
        name = str(raw.get("table") or "").strip()
        cols = raw.get("target_columns") or []
        if name not in table_names or not isinstance(cols, list) or not cols:
            raise ValueError(f"invalid target metadata for {name!r}")
        by_name[name] = {
            "table": name,
            "target_table_name": str(raw.get("target_table_name") or f"prepared_{name}"),
            "target_columns": [str(c) for c in cols],
            "target_description": str(raw.get("target_description") or ""),
        }
    missing = [name for name in table_names if name not in by_name]
    for name in missing:
        df = table_dfs.get(name) if table_dfs else None
        cols = [str(c) for c in (list(df.columns) if isinstance(df, pd.DataFrame) else [])]
        by_name[name] = {
            "table": name,
            "target_table_name": f"prepared_{name}",
            "target_columns": cols or ["__identity__"],
            "target_description": (
                "No explicit per-table target metadata was produced for this selected table. "
                "Preserve the source table so downstream integration can still use it if needed."
            ),
            "identity_fallback": True,
        }
    answer_code = str(obj.get("answer_code") or "").strip()
    if not answer_code or "target" not in answer_code:
        if "answer" not in answer_code:
            raise ValueError("answer_code must assign target or answer")
    cleaned_lines = []
    for line in answer_code.splitlines():
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            continue
        cleaned_lines.append(line)
    answer_code = "\n".join(cleaned_lines).strip()
    if not answer_code:
        raise ValueError("answer_code is empty after removing imports")
    return [by_name[name] for name in table_names], answer_code


def get_or_generate_stage2_plan(
    *,
    adapter,
    llm,
    benchmark: str,
    task_id: str,
    question: str,
    selected_context: str,
    selected_files: List[str],
    selected_tables: Dict[str, pd.DataFrame],
    stage2_cache_root: Path,
    reasoning_effort: str,
    force_stage2: bool,
) -> tuple[Dict[str, Any], List[Dict[str, Any]], str, Dict[str, Any], bool]:
    prompt = TARGET_SCHEMA_PROMPT.format(question=question, selected_context=selected_context)
    prompt_sha = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    cache_dir = stage2_cache_root / benchmark
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{task_id}.json"
    cached = None
    if cache_path.exists() and not force_stage2:
        cand = json.loads(cache_path.read_text(encoding="utf-8"))
        if (
            cand.get("prompt_sha256") == prompt_sha
            and cand.get("selected_table_files") == selected_files
            and cand.get("model") == llm.model
        ):
            cached = cand
    if cached:
        plan = cached["stage2_plan"]
        table_targets, answer_code = normalize_plan(plan, list(selected_tables), selected_tables)
        return plan, table_targets, answer_code, cached["usage"], True

    before = usage_snapshot_t2p(llm)
    t0 = time.time()
    plan = shared.extract_json(adapter, llm.generate(prompt))
    table_targets, answer_code = normalize_plan(plan, list(selected_tables), selected_tables)
    usage = usage_delta_t2p(usage_snapshot_t2p(llm), before)
    usage["time_cost"] = time.time() - t0
    cache_path.write_text(json.dumps({
        "cache_version": 1,
        "benchmark": benchmark,
        "task_id": task_id,
        "question": question,
        "selected_table_files": selected_files,
        "selected_table_names": list(selected_tables),
        "model": llm.model,
        "reasoning_effort": reasoning_effort,
        "prompt_sha256": prompt_sha,
        "target_metadata_prompt": prompt,
        "stage2_plan": plan,
        "normalized_table_targets": table_targets,
        "normalized_answer_code": answer_code,
        "usage": usage,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return plan, table_targets, answer_code, usage, False


def one_table_schema_context(table_name: str, df: pd.DataFrame, target_meta: Dict[str, Any], sample_rows: int, max_schema_cols: int) -> str:
    source = shared.bounded_table_context({"table_1": df}, sample_rows, max_schema_cols, 200)
    cols = "\n".join(f"- {c}" for c in target_meta["target_columns"])
    return (
        f"Source Tables:\n{source}\n\n"
        f"Target Table:\n**Table Caption:** {target_meta['target_table_name']}\n"
        f"**Columns:**\n{cols}\n\n"
        f"Target Data Description:\n{target_meta['target_description']}"
    )


def solve_bat_target_schema(solver: MCTSSolver, schema_context: str, tables: Dict[str, pd.DataFrame], max_rollout_steps: int):
    solver.best_paths = []
    root = MCTSNode(
        MCTSNodeType.ROOT,
        parent_node=None,
        parent_action=None,
        depth=0,
        table_schema_dict=schema_context,
        table_path=None,
        benchmark_tables=tables,
        task_question=None,
        llm_client=solver.llm_client,
        llm_kwargs=solver.llm_kwargs,
    )
    root.path_nodes = [root]
    for _ in range(max_rollout_steps):
        leaf = solver.select(root)
        if leaf.is_terminal():
            solver.backpropagate(leaf)
            continue
        solver.expand(leaf)
        if not leaf.children:
            continue
        end, _ = solver.simulate(leaf.children[0])
        solver.backpropagate(end)
        if solver.should_terminate():
            break
    ranked = []
    for end in solver.find_all_end_nodes(root):
        score = end.Q / end.N if end.N else 0.0
        if hasattr(end, "final_transformation"):
            ranked.append((score, end))
    ranked.sort(key=lambda x: x[0], reverse=True)
    if not ranked:
        return {"reward": 0.0, "code": [], "execution_error": "no end node"}
    score, end = ranked[0]
    return {
        "reward": float(score),
        "code": end.final_transformation,
        "execution_error": getattr(end, "execution_error", ""),
    }


def prep_function(name: str, lines: List[str]) -> str:
    body = "\n".join("    " + line for line in lines if str(line).strip())
    if not body:
        body = "    target = table_1.copy()"
    return f"""
def {name}(table_1):
{body}
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
""".strip()


def assemble(functions: List[str], selected_original: List[str], answer_code: str, target_names: List[str] | None = None) -> str:
    lines = [
        "import pandas as pd",
        "import numpy as np",
        "",
        *functions,
        "",
    ]
    for i, original in enumerate(selected_original, 1):
        lines.append(f"prepared_table_{i} = _prep_{i}(tables[{original!r}])")
        if target_names and i - 1 < len(target_names):
            alias = str(target_names[i - 1]).strip()
            if alias.isidentifier() and alias != f"prepared_table_{i}":
                lines.append(f"{alias} = prepared_table_{i}")
    lines.extend([
        "",
        answer_code,
        "",
        "_answer_value = None",
        "if 'answer' in locals():",
        "    _answer_value = answer",
        "elif 'target' in locals() and not isinstance(target, pd.DataFrame):",
        "    _answer_value = target",
        "elif 'result' in locals() and not isinstance(result, dict):",
        "    _answer_value = result",
        "elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:",
        "    _answer_value = result['answer']",
        "elif 'target' in locals():",
        "    _answer_value = target",
        "if not isinstance(_answer_value, pd.DataFrame):",
        "    _answer_value = pd.DataFrame({'answer': [_answer_value]})",
        "result = {'answer': _answer_value}",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark_path", required=True)
    ap.add_argument("--benchmark_name", required=True)
    ap.add_argument("--table_dir", required=True)
    ap.add_argument("--model_name", default=None)
    ap.add_argument("--sample_rows", type=int, default=3)
    ap.add_argument("--max_schema_cols", type=int, default=40)
    ap.add_argument("--max_cell_chars", type=int, default=200)
    ap.add_argument("--max_refine", type=int, default=3)
    ap.add_argument("--max_rollout_steps", type=int, default=4)
    ap.add_argument("--max_depth", type=int, default=4)
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
    load_bat_backend()
    llm_config, model_name = adapter.load_llm_config(REPO / "example" / "Text-to-Pipeline-main" / "config/default_config.yaml", args.model_name)
    meta_llm = adapter.LLMClient(llm_config, model_name=model_name)
    meta_llm.reasoning_effort = args.reasoning_effort

    bat_config_path = BAT_ROOT / "src" / "config" / "default.yaml"
    config = yaml.safe_load(bat_config_path.read_text(encoding="utf-8")) or {}
    llm_kwargs = dict(config.get("model_kwargs", {}))
    if args.model_name:
        llm_kwargs["model_name"] = args.model_name
    llm_kwargs.setdefault("n", 1)
    bat_llm = BATLLMClient(model_name=llm_kwargs.get("model_name", "qwen"))
    solver = MCTSSolver(
        max_rollout_steps=args.max_rollout_steps,
        max_depth=args.max_depth,
        exploration_constant=1.0,
        llm_kwargs=llm_kwargs,
        llm_client=bat_llm,
        reward_model=BenchmarkExecutionRewardModel(llm_kwargs),
        logger=logging.getLogger("bat_adapted"),
    )

    result_root = Path(args.result_root)
    if args.use_gold_tables and args.use_gold_specification and args.result_root == str(HERE / "results"):
        result_root = HERE / "results_gold_tables_gold_spec"
    elif args.use_gold_tables and args.result_root == str(HERE / "results"):
        result_root = HERE / "results_gold_tables"
    code_dir = result_root / "codes" / args.benchmark_name
    artifact_dir = result_root / "artifacts" / args.benchmark_name
    record_path = result_root / "records" / f"{args.benchmark_name}.jsonl"
    code_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    rows = read_jsonl(Path(args.benchmark_path))
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
        bat_llm.reset_token_usage()
        usage_by_stage = {}
        started = time.time()
        try:
            candidate_files = item.get("input_table", [])
            candidate_tables = adapter.load_input_tables(candidate_files, table_dir)
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
                max_selected = {"nl2sql-spider": 4, "nl2sql-bird": 4, "beaver": 7, "realdp": 8}.get(args.benchmark_name, len(candidate_tables))
                selection_text = shared.selector_prompt(item.get("question", ""), candidate_files, candidate_tables, 2, max_selected, args.max_schema_cols)
                prompt_sha = hashlib.sha256(selection_text.encode("utf-8")).hexdigest()
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
                    before = usage_snapshot_t2p(meta_llm)
                    t0 = time.time()
                    selection_obj = shared.extract_json(adapter, meta_llm.generate(selection_text))
                    u = usage_delta_t2p(usage_snapshot_t2p(meta_llm), before)
                    u["time_cost"] = time.time() - t0
                    usage_by_stage["table_selection"] = u
                    selected_tmp = shared.normalize_file_selection(selection_obj, candidate_files)
                    cache_path.write_text(json.dumps({
                        "cache_version": 1, "benchmark": args.benchmark_name, "task_id": task_id,
                        "question": item.get("question", ""), "candidate_table_files": candidate_files,
                        "model": meta_llm.model, "reasoning_effort": args.reasoning_effort,
                        "prompt_sha256": prompt_sha, "selector_prompt": selection_text,
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
                plan, table_targets, answer_code, u, _stage2_cached = get_or_generate_stage2_plan(
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
            functions = []
            bat_started = time.time()
            for i, target_meta in enumerate(table_targets, 1):
                df = selected_tables[target_meta["table"]]
                if target_meta.get("identity_fallback"):
                    functions.append(prep_function(f"_prep_{i}", ["target = table_1.copy()"]))
                    continue
                schema_context = one_table_schema_context(target_meta["table"], df, target_meta, args.sample_rows, args.max_schema_cols)
                best = solve_bat_target_schema(solver, schema_context, {"table_1": df}, args.max_rollout_steps)
                functions.append(prep_function(f"_prep_{i}", best.get("code") or []))
            usage_by_stage["pipeline_generation"] = usage_snapshot_bat(bat_llm)
            usage_by_stage["pipeline_generation"]["time_cost"] = time.time() - bat_started
            target_names = [t["target_table_name"] for t in table_targets]
            code_path.write_text(assemble(functions, selected_original, answer_code, target_names), encoding="utf-8")
            total = usage_add(*usage_by_stage.values())
            total["time_cost"] = time.time() - started
            record = {"task_id": task_id, "benchmark": args.benchmark_name, **total, "usage_by_stage": usage_by_stage, "selected_table_indices": selected_indices, "selection_source": "gold" if args.use_gold_tables else "stage1", "specification_source": "gold" if args.use_gold_specification else "stage2"}
            append_jsonl(record_path, record)
            artifact_dir.joinpath(f"{task_id}.json").write_text(json.dumps({
                "task_id": task_id,
                "selection_source": "gold" if args.use_gold_tables else "stage1",
                "specification_source": "gold" if args.use_gold_specification else "stage2",
                "table_targets": table_targets,
                "integration_plan": plan.get("integration_plan"),
                "answer_code": answer_code,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[{pos}/{len(rows)}] {task_id} selected={selected_indices}")
        except Exception as exc:
            total = usage_add(*usage_by_stage.values())
            total["time_cost"] = time.time() - started
            append_jsonl(record_path, {"task_id": task_id, "benchmark": args.benchmark_name, **total, "usage_by_stage": usage_by_stage, "error": f"{type(exc).__name__}: {exc}"})
            print(f"[{pos}/{len(rows)}] {task_id} failed: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
