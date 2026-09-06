#!/usr/bin/env python3
"""Staged adaptation of Text-to-Pipeline for retrieval-based table QA.

Stages:
  1. select relevant tables from retrieved candidates;
  2. jointly write one preparation specification per selected table plus answer code;
  3. generate one Text-to-Pipeline chain per table, then assemble all prepared tables.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
import logging
import re
import sys
import textwrap
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DEFAULT_T2P_ROOT = HERE.parent / "Text-to-Pipeline-main"
DEFAULT_SELECTION_CACHE_ROOT = HERE.parent / "adapted-shared" / "table-selection"
sys.path.insert(0, str(HERE.parent))
import adapted_gold_spec

# A capability guide aligned with novel_prep's benchmark dc_ops action space.
# Query-specific filtering/aggregation/sorting belongs in answer_code, not in the
# per-table preparation specifications.
PREPARATION_CAPABILITIES = """
- Value/type normalization: CastType, StandardizeString, StandardizeDatetime.
  The benchmark's high-level Normalize operation should be described precisely
  as the needed type conversion or string/datetime normalization.
- Schema and projection: Rename, DropColumn. SelectCol may be used only as
  deterministic final projection to keep expected columns after preparation.
- Packed or composite columns: SplitColumn, Concatenate.
- Structural reshaping: Transpose, Pivot, Stack, WideToLong, Explode.
- Multi-table integration: Join and Union. State every join key and join type.
- Do not use row-level query-answering operations in per-table preparation:
  Filter, DropNulls, Deduplicate, Sort, TopK, GroupBy, Count, and
  CalculateStatistic are outside the benchmark dc_ops space here.
- Do not use CodeGeneration for the adapted baseline operation space.
""".strip()

ALLOWED_PREP_OPS = {
    "Transpose", "Pivot", "Stack", "WideToLong", "Explode",
    "Rename", "SplitColumn", "Concatenate", "StandardizeString",
    "StandardizeDatetime", "CastType", "DropColumn", "SelectCol",
}


def load_adapter(t2p_root: Path):
    path = t2p_root / "run_benchmark_text2pipeline.py"
    sys.path.insert(0, str(t2p_root))
    spec = importlib.util.spec_from_file_location("t2p_existing_adapter", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import existing Text-to-Pipeline adapter: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_json(adapter, response: Any) -> Dict[str, Any]:
    obj = adapter.extract_json(response)
    if not isinstance(obj, dict):
        raise ValueError("Expected a JSON object")
    return obj


def selector_prompt(
    question: str, candidate_files: List[str], candidate_tables: Dict[str, pd.DataFrame],
    min_selected: int, max_selected: int, max_schema_cols: int,
) -> str:
    blocks = []
    for index, (filename, df) in enumerate(zip(candidate_files, candidate_tables.values()), 1):
        headers = [str(col) for col in list(df.columns)[:max_schema_cols]]
        omitted = len(df.columns) - len(headers)
        note = f"\n   note: {omitted} columns were omitted from this preview." if omitted else ""
        blocks.append(
            f"{index}. file_name: {filename}\n"
            f"   columns: [{', '.join(headers)}]{note}"
        )
    tables_text = "\n\n".join(blocks)
    return f"""
You are performing schema linking for a data-preparation benchmark.

Given a user question and a set of candidate input table files, identify the minimal
set of table files needed to answer the question. The number of selected tables may
range from {min_selected} to {max_selected}.

Your tasks:
1. Select the relevant table files based on the full question.
2. Ensure that the selected tables collectively preserve the important semantics of
   the question.
   Do not select a table only because it already contains the requested output
   columns. Also include the table(s) that encode the question condition, such as a
   department/person/category/date filter, and the bridge/lookup tables needed to
   connect that condition to the requested output attributes.
3. Include lookup tables needed to resolve a named literal in the question (for
   example, a place/product/person name) to the ID used by another selected table.
   Do not guess that a word or Roman numeral in the literal is itself an ID or level.
4. Include a bridge table when it is required to connect two semantic source tables.
   A table may be relevant because it supplies the integration path even when it does
   not contain the requested final output column.
5. Be careful with generic words in the question such as set, group, class, type,
   table, record, item, or collection. Do not select a table merely because its file
   name matches such a generic word. Prefer the table that contains the named entity
   condition column (for example name/faceName/title) and the foreign-key-like join
   column needed to connect to the measured table.

Question:
{question}

Candidate table files:
{tables_text}

Return only valid JSON:
{{"relevant_table_files": ["..."]}}
""".strip()


def specification_prompt(question: str, selected_context: str) -> str:
    return f"""
You are Stage 2 of a staged data preparation system. Examine ALL selected tables
together, but produce a separate natural-language preparation specification for
EVERY table. Each specification must describe only transformations applied to that
one table before integration. Preserve source/destination columns, type conversions,
split delimiters, reshape identifiers/value columns, filters, and expected output
columns. Jointly reason about join relationships so both sides prepare compatible
keys, and state the intended partner/key relationship in the relevant specifications.

Assume the selected tables are the relevant tables for answering the question. Do
not say that the question is impossible, that a selected table is not usable, that
there is no link, or that the final answer should be empty because information is
missing. If the relationship is indirect, infer the most plausible join path from
column names, table names, foreign-key-like identifiers, entity-name columns, and
sample values, then make that path explicit in the per-table specifications and
answer_code.

Prefer preserving rows in each per-table preparation. Do not put narrow
question-specific value filters into a per-table specification unless the sampled
values clearly prove the exact value/coding scheme. For entity names, department
names, category labels, or natural-language phrases, keep the evidence columns and
apply robust filtering after full-table integration in answer_code. If a filter is
needed, describe broad case-insensitive matching over plausible columns and include
a fallback that preserves rows rather than producing an empty prepared table.

The downstream Text-to-Pipeline stage supports the following preparation
capabilities. Use this catalog to avoid omitting an important preparation step and
to keep each specification expressible, but do not select an exact operator chain:
{PREPARATION_CAPABILITIES}

Also write `answer_code`: executable pandas statements that answer the question
using ONLY prepared_table_1, prepared_table_2, ... corresponding to table_1,
table_2, .... This code runs after all per-table pipelines. It may perform joins,
unions, filtering, aggregation, sorting, and projection, and MUST assign the final
DataFrame to `target`. Do not read `tables`, do not repeat per-table cleaning, do
not import modules, and do not wrap the code in markdown. Do not create placeholder
null columns to represent missing information, and do not intentionally return an
empty DataFrame. The answer_code must integrate the prepared tables and produce the
best answer according to the selected evidence. When a value/category filter yields
no rows, relax the filter using broader case-insensitive matching or fall back to
the integrated rows most plausibly connected to the question instead of returning
an empty target.

When relational integration is required, join the full prepared tables first and
apply question-specific filtering, aggregation, sorting, TopK/Limit, and final
projection to the integrated result afterward. Do not reduce either side to only
the currently matching key values before its merge. Use explicit pandas `merge`
calls with named `on` or `left_on`/`right_on` keys so the integration relationships
remain auditable in the executable pipeline.

Every selected prepared table that supplies information or a relational link for the
answer must participate in this full-table integration. Build one integrated
DataFrame by explicitly merging all such tables before computing minima/maxima or
other row-reducing conditions. Do not use `isin`, `map`, scalar/list membership, or
precomputed key subsets as a substitute for a cross-table merge. For example, to
answer a question about the entity with the earliest date, first merge the complete
date table with the complete relationship/entity tables, then sort the integrated
rows by date and take the first row.

Return JSON only:
{{
  "table_specifications": [
    {{
      "table": "table_1",
      "preparation_specification": "Precise natural-language instructions for table_1...",
      "expected_output_columns": ["join_key", "value"]
    }}
  ],
  "answer_code": "target = prepared_table_1.merge(prepared_table_2, ...)"
}}

Return exactly one specification for every selected table. A no-op specification is
allowed only when the table is already ready AND still participates in the final
answer or integration path. `answer_code` is the only place where cross-table Join
or Union is executed.

Question:
{question}

Selected tables:
{selected_context}
""".strip()


def normalize_stage2_plan(obj: Dict[str, Any], table_names: List[str]) -> tuple[List[Dict[str, Any]], str]:
    raw_specs = obj.get("table_specifications")
    if not isinstance(raw_specs, list):
        raise ValueError("table_specifications must be a list")
    by_name: Dict[str, Dict[str, Any]] = {}
    for raw in raw_specs:
        if not isinstance(raw, dict):
            raise ValueError("each table specification must be an object")
        name = str(raw.get("table") or "").strip()
        text = str(raw.get("preparation_specification") or "").strip()
        if name not in table_names or name in by_name or not text:
            raise ValueError(f"invalid or duplicate specification for {name!r}")
        by_name[name] = {
            "table": name,
            "preparation_specification": text,
            "expected_output_columns": raw.get("expected_output_columns") or [],
        }
    missing = [name for name in table_names if name not in by_name]
    if missing:
        raise ValueError(f"missing table specifications: {missing}")
    answer_code = str(obj.get("answer_code") or "").strip()
    if not answer_code or "target" not in answer_code:
        raise ValueError("answer_code must assign the final DataFrame to target")
    if re.search(r"(^|\n)\s*(import|from)\s+", answer_code):
        raise ValueError("answer_code must not import modules")
    return [by_name[name] for name in table_names], answer_code


def answer_refinement_prompt(
    question: str, prepared_context: str, answer_code: str, error: str,
) -> str:
    return f"""
Revise only the integration/answer code for a staged table-preparation system.
All per-table pipelines have already executed successfully. Use only the actual
prepared_table_1, prepared_table_2, ... schemas shown below. Explicitly merge every
prepared table needed for information or a relational link before filtering,
aggregation, sorting, or TopK. Do not use isin/map as a substitute for a merge.
Assign the final DataFrame to `target`. Do not import modules or use markdown.
If the previous execution produced an empty or zero-column DataFrame, revise the
code by relaxing value/category filters, using broader case-insensitive matching
over plausible evidence columns, or falling back to the most plausible integrated
rows. Do not intentionally return an empty target.

Question:
{question}

Previous answer_code:
{answer_code}

Execution error:
{error}

Actual prepared tables:
{prepared_context}

Return JSON only:
{{"answer_code": "..."}}
""".strip()


def normalize_selection(obj: Dict[str, Any], n_tables: int) -> List[int]:
    raw = obj.get("selected_table_indices")
    if not isinstance(raw, list):
        raise ValueError("selected_table_indices must be a list")
    out: List[int] = []
    for value in raw:
        idx = int(value)
        if idx < 0 or idx >= n_tables:
            raise ValueError(f"selected table index {idx} outside [0, {n_tables})")
        if idx not in out:
            out.append(idx)
    if not out:
        raise ValueError("the selector returned no tables")
    return out


def normalize_file_selection(obj: Dict[str, Any], candidate_files: List[str]) -> List[int]:
    raw = obj.get("relevant_table_files")
    if not isinstance(raw, list):
        raise ValueError("relevant_table_files must be a list")
    exact = {str(name): i for i, name in enumerate(candidate_files)}
    basenames: Dict[str, List[int]] = {}
    for i, name in enumerate(candidate_files):
        basenames.setdefault(Path(str(name)).name, []).append(i)
    selected: List[int] = []
    for value in raw:
        name = str(value)
        idx = exact.get(name)
        if idx is None:
            matches = basenames.get(Path(name).name, [])
            if len(matches) != 1:
                raise ValueError(f"selected file is not a unique candidate: {name!r}")
            idx = matches[0]
        if idx not in selected:
            selected.append(idx)
    if not selected:
        raise ValueError("the selector returned no table files")
    return selected


def normalize_name(value: str) -> str:
    name = str(value).split("#sep#")[-1]
    name = Path(name).stem
    return re.sub(r"[^a-z0-9]", "", name.lower())


def gold_indices(item: Dict[str, Any], benchmark: str) -> List[int]:
    files = item.get("input_table") or []
    if benchmark in {"nl2sql-spider", "nl2sql-bird"}:
        count = int(item.get("relevant_table_num") or 0)
        return list(range(min(count, len(files))))
    gold = {normalize_name(x) for x in (item.get("gold_tables") or [])}
    return [i for i, filename in enumerate(files) if normalize_name(filename) in gold]


def selection_metrics(selected: List[int], gold: List[int]) -> Dict[str, Any]:
    pred_set, gold_set = set(selected), set(gold)
    overlap = len(pred_set & gold_set)
    precision = overlap / len(pred_set) if pred_set else 0.0
    recall = overlap / len(gold_set) if gold_set else None
    f1 = None if recall is None else (2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return {
        "gold_table_indices": gold,
        "table_precision": precision,
        "table_recall": recall,
        "table_f1": f1,
        "table_exact_match": pred_set == gold_set,
    }


def remap_code(code: str, selected_indices: List[int]) -> str:
    mapping = {
        f"table_{local + 1}": f"table_{original + 1}"
        for local, original in enumerate(selected_indices)
    }
    marker = "import numpy as np\n"
    preamble = (
        "\n# Stage-1 table-selection mapping: local pipeline names -> retrieved candidates.\n"
        f"SELECTED_TABLE_MAPPING = {mapping!r}\n"
        "_selected_tables = {local: tables[source] for local, source in SELECTED_TABLE_MAPPING.items()}\n"
    )
    if marker not in code:
        raise ValueError("Unexpected generated-code wrapper")
    code = code.replace(marker, marker + preamble, 1)
    code = code.replace("for _name, _df in tables.items():", "for _name, _df in _selected_tables.items():")
    code = code.replace("tables.get(", "_selected_tables.get(")
    return code


def assemble_code(
    bodies: List[str], chains: List[List[Dict[str, Any]]], answer_code: str,
    source_table_names: List[str],
) -> str:
    """Compose independent one-table pipelines and the Stage-2 answer program."""
    blocks = [
        "import pandas as pd",
        "import numpy as np",
        "",
        "# Per-table Text-to-Pipeline chains, retained for auditability.",
        f"TEXT2PIPELINE_CHAINS = {chains!r}",
    ]
    for i, (body, source_name) in enumerate(zip(bodies, source_table_names), 1):
        function_body = "df = _source.copy()\n" + body + "\nreturn result"
        blocks.extend([
            "",
            f"def _prepare_table_{i}(_source):",
            textwrap.indent(function_body, "    "),
            "",
            f"prepared_table_{i} = _prepare_table_{i}("
            f"tables.get({source_name!r}, pd.DataFrame()))",
        ])
    blocks.extend([
        "",
        "# Stage-2 program over the prepared tables.",
        answer_code,
        "",
        "if isinstance(target, pd.Series):",
        "    target = target.to_frame().reset_index(drop=True)",
        "elif isinstance(target, (list, tuple)):",
        "    target = pd.DataFrame(target)",
        "elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):",
        "    target = pd.DataFrame(target)",
        "elif not isinstance(target, pd.DataFrame):",
        "    target = pd.DataFrame({'answer': [target]})",
        "",
        "result = {'answer': target}",
        "",
    ])
    return "\n".join(blocks)


def passthrough_body() -> str:
    """Conservative one-table fallback when Text2Pipeline cannot ground a chain.

    The fallback is intentionally weak: it only preserves the selected raw table.
    This keeps the task in the evaluation denominator and lets lineage scoring
    credit any subtable/join-key evidence that survived, without fabricating a
    successful preparation pipeline.
    """
    return "result = df.copy()"


def fallback_answer_code(n_tables: int) -> str:
    """Executable fallback when Stage-2 answer_code cannot assemble a target."""
    lines = [
        "_frames = []",
    ]
    for i in range(1, n_tables + 1):
        lines.extend([
            f"if isinstance(prepared_table_{i}, pd.DataFrame) and not prepared_table_{i}.empty:",
            f"    _tmp = prepared_table_{i}.copy()",
            f"    _tmp['__prepared_table__'] = 'prepared_table_{i}'",
            "    _frames.append(_tmp)",
        ])
    lines.extend([
        "target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()",
    ])
    return "\n".join(lines)


def execute_pipeline_output(code: str, tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    import numpy as np
    env: Dict[str, Any] = {"pd": pd, "np": np, "tables": tables}
    exec(code, env, env)
    wrapped = env.get("result")
    output = wrapped.get("answer") if isinstance(wrapped, dict) else wrapped
    if not isinstance(output, pd.DataFrame):
        raise ValueError("one-table pipeline did not produce a DataFrame")
    return output


def logger_for(path: Path) -> logging.Logger:
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("text_to_pipeline_adapted")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(path, mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    return logger


def usage_snapshot(llm) -> Dict[str, int]:
    return {
        "input_tokens": int(llm.token_usage.get("prompt_tokens", 0)),
        "output_tokens": int(llm.token_usage.get("completion_tokens", 0)),
        "total_tokens": int(llm.token_usage.get("total_tokens", 0)),
        "llm_calls": int(llm.llm_calls),
    }


def usage_delta(after: Dict[str, int], before: Dict[str, int]) -> Dict[str, int]:
    return {key: after[key] - before[key] for key in after}


def total_usage(usage_by_stage: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "input_tokens": sum(int(stage.get("input_tokens", 0)) for stage in usage_by_stage.values()),
        "output_tokens": sum(int(stage.get("output_tokens", 0)) for stage in usage_by_stage.values()),
        "total_tokens": sum(int(stage.get("total_tokens", 0)) for stage in usage_by_stage.values()),
        "llm_calls": sum(int(stage.get("llm_calls", 0)) for stage in usage_by_stage.values()),
        "time_cost": sum(float(stage.get("time_cost", 0.0)) for stage in usage_by_stage.values()),
    }


def bounded_table_context(
    tables: Dict[str, pd.DataFrame], sample_rows: int, max_schema_cols: int,
    max_cell_chars: int,
) -> str:
    """Serialize schemas and samples without allowing nested/long cells to explode prompts."""
    blocks = []
    for table_name, df in tables.items():
        frame = df.iloc[:, :max_schema_cols]
        columns = list(frame.columns)
        counts: Dict[tuple[str, str], int] = {}
        display_columns: List[str] = []
        schema = []
        for position, col in enumerate(columns):
            key = (type(col).__name__, repr(col))
            counts[key] = counts.get(key, 0) + 1
            duplicate_count = sum(
                1 for other in columns
                if type(other).__name__ == key[0] and repr(other) == key[1]
            )
            duplicate = (
                f", duplicate occurrence {counts[key]} of {duplicate_count}"
                if duplicate_count > 1 else ""
            )
            display = f"position {position}, label={repr(col)}, label_type={type(col).__name__}{duplicate}"
            display_columns.append(display)
            schema.append(f"- {display}, dtype={frame.dtypes.iloc[position]}")
        sample = []
        for _, row in frame.head(sample_rows).iterrows():
            item = {}
            for i, display_col in enumerate(display_columns):
                value = str(row.iloc[i])
                if len(value) > max_cell_chars:
                    value = value[:max_cell_chars] + f"... <{len(value) - max_cell_chars} chars omitted>"
                item[f"display only: {display_col}"] = value
            sample.append(item)
        blocks.append(
            f"Table: {table_name}\n"
            f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n"
            f"Columns:\n{chr(10).join(schema)}\n"
            f"Sample rows:\n{json.dumps(sample, ensure_ascii=False, indent=2)}"
        )
    return "\n\n".join(blocks)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--benchmark_path", required=True)
    ap.add_argument("--benchmark_name", required=True)
    ap.add_argument("--table_dir", required=True)
    ap.add_argument("--t2p_root", default=str(DEFAULT_T2P_ROOT))
    ap.add_argument("--config", default=None)
    ap.add_argument("--model_name", default=None)
    ap.add_argument("--sample_rows", type=int, default=3)
    ap.add_argument("--max_schema_cols", type=int, default=40)
    ap.add_argument("--max_cell_chars", type=int, default=200)
    ap.add_argument("--max_refine", type=int, default=3)
    ap.add_argument("--reasoning_effort", default="minimal",
                    choices=["minimal", "low", "medium", "high"],
                    help="reasoning effort for GPT-5/o-series calls")
    ap.add_argument("--max_tasks", type=int, default=None)
    ap.add_argument("--task_ids", nargs="*")
    ap.add_argument("--skip_task_ids", nargs="*",
                    help="task ids to skip during resume, useful for Beaver OOM cases")
    ap.add_argument("--result_root", default=str(HERE / "results"))
    ap.add_argument("--selection_cache_root", default=str(DEFAULT_SELECTION_CACHE_ROOT),
                    help="shared table-identification cache reusable by adapted baselines")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--force-selection", action="store_true",
                    help="ignore and refresh a matching shared table-selection cache entry")
    ap.add_argument("--use-gold-tables", action="store_true",
                    help="skip Stage 1 and use benchmark gold relevant tables")
    ap.add_argument("--use-gold-specification", action="store_true",
                    help="skip Stage 2 and use benchmark dc_ops/output metadata as gold specification")
    args = ap.parse_args()

    t2p_root = Path(args.t2p_root)
    adapter = load_adapter(t2p_root)
    config_path = Path(args.config) if args.config else t2p_root / "config/default_config.yaml"
    llm_config, model_name = adapter.load_llm_config(config_path, args.model_name)
    llm = adapter.LLMClient(llm_config, model_name=model_name)
    llm.reasoning_effort = args.reasoning_effort

    result_root = Path(args.result_root)
    if args.use_gold_tables and args.use_gold_specification and args.result_root == str(HERE / "results"):
        result_root = HERE / "results_gold_tables_gold_spec"
    elif args.use_gold_tables and args.result_root == str(HERE / "results"):
        result_root = HERE / "results_gold_tables"
    code_dir = result_root / "codes" / args.benchmark_name
    artifact_dir = result_root / "artifacts" / args.benchmark_name
    record_path = result_root / "records" / f"{args.benchmark_name}.jsonl"
    selection_cache_dir = Path(args.selection_cache_root) / args.benchmark_name
    code_dir.mkdir(parents=True, exist_ok=True)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    selection_cache_dir.mkdir(parents=True, exist_ok=True)
    logger = logger_for(result_root / "logs" / f"{args.benchmark_name}.log")

    rows = read_jsonl(Path(args.benchmark_path))
    if args.task_ids:
        wanted = set(args.task_ids)
        rows = [r for r in rows if r.get("task_id") in wanted]
    if args.skip_task_ids:
        skipped = set(args.skip_task_ids)
        rows = [r for r in rows if r.get("task_id") not in skipped]
    if args.max_tasks is not None:
        rows = rows[:args.max_tasks]

    table_dir = Path(args.table_dir)
    for position, item in enumerate(rows, 1):
        task_id = item["task_id"]
        code_path = code_dir / f"{task_id}.py"
        artifact_path = artifact_dir / f"{task_id}.json"
        if code_path.exists() and artifact_path.exists() and not args.force:
            logger.info("[%d/%d] skip %s", position, len(rows), task_id)
            continue
        # LLMClient accumulates usage by default. Reset here so every record is a
        # true per-query total suitable for eval_all_oom.py cost aggregation.
        llm.reset_token_usage()
        started = time.time()
        record: Dict[str, Any] = {"task_id": task_id, "benchmark": args.benchmark_name}
        usage_by_stage: Dict[str, Dict[str, Any]] = {}
        selection_obj = None
        selected_indices = None
        table_specs = None
        answer_code = None
        local_table_names: List[str] = []
        per_table_chains: List[List[Dict[str, Any]]] = []
        pipeline_responses: Dict[str, List[str]] = {}
        try:
            candidate_files = item.get("input_table", [])
            candidate_tables = adapter.load_input_tables(candidate_files, table_dir)
            max_selected = {
                "nl2sql-spider": 4, "nl2sql-bird": 4,
                "beaver": 7, "realdp": 8,
            }.get(args.benchmark_name, len(candidate_tables))
            min_selected = 2

            selection_cache_path = selection_cache_dir / f"{task_id}.json"
            if args.use_gold_tables:
                selected_indices = gold_indices(item, args.benchmark_name)
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
                selection_cache_status = "gold"
            else:
                selection_text = selector_prompt(
                    item.get("question", ""), candidate_files, candidate_tables,
                    min_selected, max_selected, args.max_schema_cols,
                )
                prompt_sha256 = hashlib.sha256(selection_text.encode("utf-8")).hexdigest()
                cached_selection = None
                if selection_cache_path.exists() and not args.force_selection:
                    try:
                        candidate = json.loads(selection_cache_path.read_text(encoding="utf-8"))
                        if (
                            candidate.get("prompt_sha256") == prompt_sha256
                            and candidate.get("candidate_table_files") == candidate_files
                            and candidate.get("model") == llm.model
                        ):
                            cached_selection = candidate
                    except Exception:
                        cached_selection = None
                if cached_selection:
                    selection_obj = cached_selection["selection_decision"]
                    usage_by_stage["table_selection"] = cached_selection["usage"]
                    selection_cache_status = "reused"
                else:
                    stage_before = usage_snapshot(llm)
                    selection_started = time.time()
                    selection_obj = extract_json(adapter, llm.generate(selection_text))
                    selection_usage = usage_delta(usage_snapshot(llm), stage_before)
                    selection_usage["time_cost"] = time.time() - selection_started
                    usage_by_stage["table_selection"] = selection_usage
                    selection_cache_status = "created"
                selected_indices = normalize_file_selection(selection_obj, candidate_files)
                if not cached_selection:
                    selection_cache_path.write_text(json.dumps({
                        "cache_version": 1,
                        "benchmark": args.benchmark_name,
                        "task_id": task_id,
                        "question": item.get("question", ""),
                        "candidate_table_files": candidate_files,
                        "model": llm.model,
                        "reasoning_effort": args.reasoning_effort,
                        "prompt_sha256": prompt_sha256,
                        "selector_prompt": selection_text,
                        "selection_decision": selection_obj,
                        "selected_table_indices": selected_indices,
                        "selected_table_files": [candidate_files[i] for i in selected_indices],
                        "usage": usage_by_stage["table_selection"],
                    }, ensure_ascii=False, indent=2), encoding="utf-8")
            metrics = selection_metrics(selected_indices, gold_indices(item, args.benchmark_name))
            record.update({**metrics, "selected_table_indices": selected_indices})
            selected_original = [f"table_{i + 1}" for i in selected_indices]
            selected_tables = {
                f"table_{local + 1}": candidate_tables[original]
                for local, original in enumerate(selected_original)
            }
            selected_context = bounded_table_context(
                selected_tables, args.sample_rows, args.max_schema_cols,
                args.max_cell_chars,
            )

            local_table_names = list(selected_tables)
            if args.use_gold_specification:
                spec_obj, table_specs, answer_code = adapted_gold_spec.text2pipeline_gold_stage2(
                    item, selected_tables, table_dir
                )
                usage_by_stage["preparation_specification"] = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "llm_calls": 0,
                    "time_cost": 0.0,
                }
            else:
                stage_before = usage_snapshot(llm)
                specification_started = time.time()
                spec_prompt = specification_prompt(item.get("question", ""), selected_context)
                spec_obj = None
                table_specs = None
                answer_code = None
                previous_spec_error = ""
                for _ in range(args.max_refine + 1):
                    prompt = spec_prompt
                    if previous_spec_error:
                        prompt = (
                            f"{spec_prompt}\n\n"
                            "Your previous Stage 2 JSON was invalid for this evaluator:\n"
                            f"{previous_spec_error}\n"
                            "Return corrected JSON only. In particular, answer_code must not "
                            "contain import/from statements, markdown, or placeholder empty "
                            "targets, and it must assign the final DataFrame to target."
                        )
                    spec_obj = extract_json(adapter, llm.generate(prompt))
                    try:
                        table_specs, answer_code = normalize_stage2_plan(
                            spec_obj, local_table_names
                        )
                        break
                    except Exception as exc:
                        previous_spec_error = f"{type(exc).__name__}: {exc}"
                if table_specs is None or answer_code is None:
                    raise ValueError(previous_spec_error or "invalid Stage 2 plan")
                usage_by_stage["preparation_specification"] = usage_delta(
                    usage_snapshot(llm), stage_before
                )
                usage_by_stage["preparation_specification"]["time_cost"] = (
                    time.time() - specification_started
                )

            per_table_chains: List[List[Dict[str, Any]]] = []
            per_table_bodies: List[str] = []
            per_table_rewards: List[float] = []
            per_table_errors: List[str] = []
            per_table_fallbacks: List[bool] = []
            per_table_outputs: List[pd.DataFrame] = []
            pipeline_responses: Dict[str, List[str]] = {}
            stage_before = usage_snapshot(llm)
            pipeline_started = time.time()
            for table_spec in table_specs:
                table_name = table_spec["table"]
                table_df = selected_tables[table_name]
                # Text2Pipeline sees exactly one input table in this call. Rename it
                # locally so its built-in table_1/index-0 convention stays truthful.
                one_table = {"table_1": table_df}
                one_context = bounded_table_context(
                    one_table, args.sample_rows, args.max_schema_cols,
                    args.max_cell_chars,
                )
                previous_error = ""
                previous_chain = ""
                best_reward = -1.0
                best_error = ""
                best_chain: List[Dict[str, Any]] = []
                best_body = ""
                best_local_code = ""
                responses: List[str] = []
                for _ in range(args.max_refine + 1):
                    pipeline_task = (
                        f"User question: {item.get('question', '')}\n\n"
                        f"This single input is {table_name} from the jointly selected "
                        "table set. Generate ONLY its table-local preparation; do not "
                        "join or union another table.\n\n"
                        f"Preparation specification: "
                        f"{table_spec['preparation_specification']}\n\n"
                        f"Expected output columns: "
                        f"{json.dumps(table_spec['expected_output_columns'], ensure_ascii=False)}\n\n"
                        "There is exactly one input table, so every transform_chain "
                        "step must use table_indices [0]. The final output must be the "
                        "prepared version of this table, not the cross-table answer. "
                        "Preserve rows for later integration. Avoid narrow filters on "
                        "question-specific text values unless the value/coding scheme is "
                        "visible in the sample; if a filter would produce an empty table, "
                        "relax it or keep the evidence columns unfiltered so answer_code "
                        "can decide after integration. If the specification is no-op or "
                        "asks to preserve the table unchanged, generate a chain that copies "
                        "the input table or selects the expected columns; never emit a "
                        "zero-column output for no-op preparation.\n\n"
                        "Column-label rules: use the exact label VALUE and TYPE shown "
                        "in the schema. For example, label=1976 with label_type=int "
                        "must be emitted as JSON number 1976, not string \"1976\". "
                        "Text such as position/label_type/duplicate occurrence is "
                        "display metadata and is never part of a column name. When "
                        "duplicate labels must be distinguished, rely on the available "
                        "structured operations and explicit output column names; do not "
                        "pass display metadata to SelectCol. "
                        "Never use `columns.get_loc(label)` for a duplicated label, "
                        "because it returns multiple positions; iterate physical "
                        "column positions and read them directly with `.iloc[:, pos]` "
                        "or `.iloc[row_pos, col_pos]`."
                    )
                    response = llm.generate(
                        adapter.make_generation_prompt(
                            pipeline_task, one_context, previous_error, previous_chain
                        )
                    )
                    response_text = response.get("content", "") if isinstance(response, dict) else str(response or "")
                    responses.append(response_text)
                    try:
                        chain = adapter.normalize_chain(adapter.extract_json(response))
                        if any(step.get("table_indices") != [0] for step in chain):
                            raise ValueError("a one-table pipeline must use table_indices [0]")
                        bad_ops = sorted({
                            str(step.get("op"))
                            for step in chain
                            if str(step.get("op")) not in ALLOWED_PREP_OPS
                        })
                        if bad_ops:
                            raise ValueError(
                                "operation(s) outside benchmark dc_ops space: "
                                + ", ".join(bad_ops)
                            )
                        body = adapter.chain_to_body(chain, 1)
                        local_code = adapter.wrap_code(body, 1, chain)
                        reward, error = adapter.execute_code(local_code, one_table)
                    except Exception as exc:
                        previous_error = (
                            "Your previous one-table transform_chain was invalid: "
                            f"{type(exc).__name__}: {exc}. Use only table_indices [0], "
                            "correct the chain, and return JSON only."
                        )
                        previous_chain = response_text[:4000]
                        continue
                    if reward >= best_reward:
                        best_reward, best_error = reward, error
                        best_chain, best_body = chain, body
                        best_local_code = local_code
                    if reward >= 1.0:
                        break
                    previous_error = error
                    previous_chain = json.dumps(chain, ensure_ascii=False, indent=2)
                if (not best_body or best_reward < 1.0) and table_df.empty:
                    fallback_columns = [
                        col for col in table_spec.get("expected_output_columns", [])
                        if col in table_df.columns
                    ] or list(table_df.columns)
                    fallback_chain = [{
                        "op": "SelectCol",
                        "params": {"columns": fallback_columns},
                        "table_indices": [0],
                    }]
                    fallback_body = adapter.chain_to_body(fallback_chain, 1)
                    fallback_code = adapter.wrap_code(fallback_body, 1, fallback_chain)
                    fallback_output = execute_pipeline_output(fallback_code, one_table)
                    if isinstance(fallback_output, pd.DataFrame) and fallback_output.shape[1] > 0:
                        best_reward = 1.0
                        best_error = (
                            "accepted schema-preserving fallback for an empty input table"
                        )
                        best_chain = fallback_chain
                        best_body = fallback_body
                        best_local_code = fallback_code
                used_fallback = False
                if not best_body or best_reward < 1.0:
                    used_fallback = True
                    best_reward = 0.0
                    best_error = (
                        "fallback_passthrough_after_pipeline_generation_failure: "
                        f"{best_error or previous_error}"
                    )
                    best_chain = [{
                        "op": "PassThroughFallback",
                        "params": {
                            "reason": best_error,
                            "source_table": table_name,
                        },
                        "table_indices": [0],
                    }]
                    best_body = passthrough_body()
                    best_local_code = adapter.wrap_code(best_body, 1, best_chain)
                per_table_chains.append(best_chain)
                per_table_bodies.append(best_body)
                per_table_rewards.append(best_reward)
                per_table_errors.append(best_error)
                per_table_fallbacks.append(used_fallback)
                per_table_outputs.append(execute_pipeline_output(best_local_code, one_table))
                pipeline_responses[table_name] = responses
            usage_by_stage["pipeline_generation"] = usage_delta(
                usage_snapshot(llm), stage_before
            )
            usage_by_stage["pipeline_generation"]["time_cost"] = time.time() - pipeline_started

            # Validate with local selected-table names, then emit the same program
            # against the original retrieved-candidate names for eval_all_oom.py.
            local_code = assemble_code(
                per_table_bodies, per_table_chains, answer_code,
                local_table_names,
            )
            final_reward, final_error = adapter.execute_code(local_code, selected_tables)
            if final_reward < 1.0:
                prepared_context = bounded_table_context(
                    {f"prepared_table_{i}": output for i, output in enumerate(per_table_outputs, 1)},
                    args.sample_rows, args.max_schema_cols, args.max_cell_chars,
                )
                stage_before = usage_snapshot(llm)
                refinement_started = time.time()
                for _ in range(args.max_refine):
                    revised = extract_json(adapter, llm.generate(answer_refinement_prompt(
                        item.get("question", ""), prepared_context,
                        answer_code, final_error,
                    )))
                    candidate_code = str(revised.get("answer_code") or "").strip()
                    if not candidate_code or "target" not in candidate_code:
                        final_error = "Revised answer_code must assign target."
                        continue
                    if re.search(r"(^|\n)\s*(import|from)\s+", candidate_code):
                        final_error = "Revised answer_code must not import modules."
                        continue
                    answer_code = candidate_code
                    local_code = assemble_code(
                        per_table_bodies, per_table_chains, answer_code,
                        local_table_names,
                    )
                    final_reward, final_error = adapter.execute_code(local_code, selected_tables)
                    if final_reward >= 1.0:
                        break
                usage_by_stage["answer_code_refinement"] = usage_delta(
                    usage_snapshot(llm), stage_before
                )
                usage_by_stage["answer_code_refinement"]["time_cost"] = (
                    time.time() - refinement_started
                )
            used_answer_fallback = False
            if final_reward < 1.0:
                used_answer_fallback = True
                final_error = f"fallback_answer_after_assembly_failure: {final_error}"
                answer_code = fallback_answer_code(len(per_table_bodies))
                local_code = assemble_code(
                    per_table_bodies, per_table_chains, answer_code,
                    local_table_names,
                )
                final_reward, fallback_error = adapter.execute_code(local_code, selected_tables)
                if final_reward < 1.0:
                    # The fallback should be robust. If it still fails, keep a
                    # clear exception so the record exposes a true infrastructure
                    # problem rather than silently writing broken code.
                    raise ValueError(
                        "fallback assembled pipeline failed: "
                        f"{fallback_error}; original error: {final_error}"
                    )
            best_code = assemble_code(
                per_table_bodies, per_table_chains, answer_code,
                selected_original,
            )

            artifact = {
                "task_id": task_id,
                "question": item.get("question", ""),
                "candidate_table_files": item.get("input_table", []),
                "selection_decision": selection_obj,
                "selection_cache_status": selection_cache_status,
                "selection_cache_path": str(selection_cache_path),
                "selection_source": "gold" if args.use_gold_tables else "stage1",
                "specification_source": "gold" if args.use_gold_specification else "stage2",
                "selected_table_indices": selected_indices,
                "selected_table_names": selected_original,
                "selected_table_files": [item["input_table"][i] for i in selected_indices],
                **metrics,
                "table_specifications": table_specs,
                "answer_code": answer_code,
                "per_table_transform_chains": {
                    name: chain for name, chain in zip(local_table_names, per_table_chains)
                },
                "generated_operator_names": [
                    step.get("op") for chain in per_table_chains for step in chain
                ],
                "per_table_execution_rewards": per_table_rewards,
                "per_table_execution_errors": per_table_errors,
                "per_table_fallbacks": {
                    name: used for name, used in zip(local_table_names, per_table_fallbacks)
                },
                "answer_code_fallback": used_answer_fallback,
                "pipeline_execution_reward": final_reward,
                "pipeline_execution_error": final_error,
                "pipeline_raw_responses": pipeline_responses,
                "usage_by_stage": usage_by_stage,
            }
            code_path.write_text(best_code, encoding="utf-8")
            artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
            totals = total_usage(usage_by_stage)
            record.update({
                **metrics,
                "selected_table_indices": selected_indices,
                "selection_cache_status": selection_cache_status,
                "selection_source": "gold" if args.use_gold_tables else "stage1",
                "specification_source": "gold" if args.use_gold_specification else "stage2",
                "input_tokens": totals["input_tokens"],
                "output_tokens": totals["output_tokens"],
                "total_tokens": totals["total_tokens"],
                "llm_calls": totals["llm_calls"],
                "usage_by_stage": usage_by_stage,
                "time_cost": totals["time_cost"],
                "status": (
                    "weak_passed"
                    if used_answer_fallback or any(per_table_fallbacks)
                    else "passed"
                ),
                "code_path": str(code_path),
                "artifact_path": str(artifact_path),
            })
            logger.info("[%d/%d] %s selected=%s reward=%.1f", position, len(rows), task_id, selected_indices, final_reward)
        except Exception as exc:
            totals = total_usage(usage_by_stage)
            live_usage = usage_snapshot(llm)
            # If failure happened inside a stage before its delta was recorded,
            # retain the live counters rather than under-reporting the failed run.
            if live_usage["total_tokens"] > totals["total_tokens"]:
                totals.update(live_usage)
                totals["time_cost"] = time.time() - started
            try:
                artifact_path.write_text(json.dumps({
                    "task_id": task_id,
                    "question": item.get("question", ""),
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                    "selection_decision": locals().get("selection_obj"),
                    "selected_table_indices": locals().get("selected_indices"),
                    "table_specifications": locals().get("table_specs"),
                    "answer_code": locals().get("answer_code"),
                    "per_table_transform_chains": {
                        name: chain for name, chain in zip(
                            locals().get("local_table_names", []),
                            locals().get("per_table_chains", []),
                        )
                    },
                    "pipeline_raw_responses": locals().get("pipeline_responses"),
                    "usage_by_stage": usage_by_stage,
                }, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:
                pass
            record.update({
                "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
                "input_tokens": totals["input_tokens"],
                "output_tokens": totals["output_tokens"],
                "total_tokens": totals["total_tokens"],
                "llm_calls": totals["llm_calls"],
                "usage_by_stage": usage_by_stage,
                "time_cost": totals["time_cost"],
            })
            logger.exception("[%d/%d] %s failed", position, len(rows), task_id)
        append_jsonl(record_path, record)
        gc.collect()


if __name__ == "__main__":
    main()
