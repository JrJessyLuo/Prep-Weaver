"""Stage 2: relational schema + raw tables -> the pipeline that materialises it.

Input  : results/pipeline_synthesize/schema/<Dataset>/relational_schema.jsonl
         datasets/<Dataset>/input_tables/*.pkl
Output : results/pipeline_synthesize/pipeline/<Dataset>/pipeline.jsonl
         one record per task: the operator chain, parameters, resulting columns
         and join keys for every logical table.

THE THREE PHASES
----------------
1. per-table synthesis   `BoundedExploreLoop` beam-searches an operator chain
                         for each logical table, synthesizing parameters with an
                         LLM and keeping up to `max_terminal_candidates`
                         finished candidates per table.
2. joint selection       the per-table candidate pools are combined and scored
                         JOINTLY, because a table that looks best alone is often
                         the one that breaks the join. Posed as maximum-weight
                         clique on a complete multipartite graph — see
                         `candidate_graph.py`.
3. join repair           deterministic value-level fixes on the declared edges.

Schema alignment is hard-OFF. The original command passed `--no-align-schema`
on every run, overriding a default of ON; alignment rewrites a predicted schema
into the database's real schema via tables.json, which is exactly the kind of
ground-truth reach-back a deploy-time action must not do.

Run:
    python -m pipeline_synthesize.synthesize --dataset Synth-Bird --limit 1
"""
from __future__ import annotations

import argparse
import contextvars
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# Importing the engine puts its flat modules on sys.path and pins the policy
# model, so it must come before anything that imports them.
from . import engine  # noqa: F401
from .engine import engine_paths

import pandas as pd                                              # noqa: E402
import bounded_explore_loop                                      # noqa: E402
import full_pipeline as FP                                       # noqa: E402
import test_param_synthesis as M                                 # noqa: E402
import prep_utils as PU                                          # noqa: E402
from bounded_explore_loop import BoundedExploreLoop              # noqa: E402
from phase2_joinkey import repair_joins, col_values              # noqa: E402
from schema_spec import schema_to_sql                            # noqa: E402
from schema_conform import conform_to_schema                     # noqa: E402

from common import dataset as DS                                 # noqa: E402
from common import paths as P                                    # noqa: E402
from common.io_utils import append_jsonl, load_jsonl, load_jsonl_by_key  # noqa: E402
from .candidate_graph import ValueCache, select_candidates       # noqa: E402

# ENABLERS: `BoundedExploreLoop` only keeps a candidate op if it raises the
# literal-name coverage score, or is a shape-changing but score-neutral op in
# ENABLERS. Pivot is not in the shipped set — yet many chains start with a Pivot
# that produces ZERO name matches on its own (the names appear only after later
# steps), so the correct first step was silently discarded and the search
# returned an empty chain. Adding these back is worth +2 tasks (0.674 -> 0.721).
bounded_explore_loop.ENABLERS = bounded_explore_loop.ENABLERS | {
    "Pivot", "Explode", "SplitColumn", "Concatenate", "Rename"
}

FIXED = {
    # Search shape. budget 12 / 6 terminals was chosen for cost: it produced
    # 583 LLM calls (~$2.32) against 1065 (~$4.30) for budget 20 / 8 terminals,
    # for the same join_key_full and 2 fewer subtable_full tasks.
    "budget": 12,
    "max_terminal_candidates": 6,
    "join_rerank_candidates": 6,
    "beam_width": 3,
    "uncertain_prob": 0.5,
    "uncertain_gap": 0.15,
    "model": "gpt-4o-2024-08-06",
    "workers": 8,
}


USAGE = {"calls": 0, "input": 0, "cached": 0, "output": 0}

# Per-task meter. Snapshotting the global counter before/after a task is only
# correct while tasks run one at a time; once an orchestrator runs several
# concurrently their calls interleave and each task is billed for the others'
# tokens. A ContextVar keeps the attribution right, and `_run_ctx` below carries
# it into the table-level worker threads, which do not inherit it on their own.
_TASK_USAGE: contextvars.ContextVar = contextvars.ContextVar("task_usage", default=None)
_METER_LOCK = threading.Lock()

_orig_llm = PU.llm_generate_setup


def _metered(prompt, **kw):
    resp = _orig_llm(prompt, **kw)
    delta = {"calls": 1,
             "input": int(resp.get("input_tokens") or 0),
             "output": int(resp.get("output_tokens") or 0)}
    raw = resp.get("usage") or {}
    det = raw.get("prompt_tokens_details") or {} if isinstance(raw, dict) else {}
    delta["cached"] = int((det.get("cached_tokens") if isinstance(det, dict) else 0) or 0)
    task = _TASK_USAGE.get()
    with _METER_LOCK:
        for k, v in delta.items():
            USAGE[k] += v
            if task is not None:
                task[k] = task.get(k, 0) + v
    return resp


def _submit_ctx(ex, fn, *a):
    """Submit `fn` so it runs under a COPY OF THE SUBMITTER'S context.

    `copy_context()` must be called here, on the submitting thread — calling it
    inside the worker copies that worker's own (empty) context instead, and the
    per-task meter silently records nothing.  A Context cannot be entered twice
    concurrently, so each submission gets its own copy.
    """
    return ex.submit(contextvars.copy_context().run, fn, *a)


PU.llm_generate_setup = _metered


def _cost(u: Dict[str, int]) -> float:
    fresh = max(int(u.get("input", 0)) - int(u.get("cached", 0)), 0)
    return fresh / 1e6 * 2.50 + int(u.get("cached", 0)) / 1e6 * 1.25 \
        + int(u.get("output", 0)) / 1e6 * 10.0



def usage_summary() -> Dict[str, Any]:
    """PROCESS-WIDE running totals, at the gpt-4o-2024-08-06 list price.

    Cumulative by design — use `usage_since` for one task's share. Writing this
    value into a per-task record made the per-task figures monotonically
    increasing, so summing them over 43 tasks once reported 13,588 calls for a
    run that made a few hundred.
    """
    return {**USAGE, "cost_usd": round(_cost(USAGE), 4)}


def usage_since(before: Dict[str, int]) -> Dict[str, Any]:
    """What was spent since the `before` snapshot: one task's actual usage."""
    d = {k: int(USAGE[k]) - int(before.get(k, 0)) for k in USAGE}
    return {**d, "cost_usd": round(_cost(d), 4)}


# --------------------------------------------------------------------------- #
# the search loop, with the production fixes applied
# --------------------------------------------------------------------------- #

def _info_need_columns(sql: str) -> set:
    """Casefolded column names a query references."""
    import sqlglot
    from sqlglot import exp
    cols = set()
    try:
        for c in sqlglot.parse_one(sql or "", read="sqlite").find_all(exp.Column):
            nv = re.sub(r"[^a-z0-9]", "", str(c.name).lower())
            if nv:
                cols.add(nv)
    except Exception:
        pass
    return cols


class _Loop(BoundedExploreLoop):
    """Completion target = declared columns the PLAN'S OWN query needs, plus keys.

    `plan_next`'s stop condition is otherwise the entire declared schema, and a
    single declared column that can never be produced then blocks completion
    forever and burns the whole budget. Narrowing to the queried columns is what
    made the gold-spec runs work, so it is kept.

    What changes is WHERE the query comes from. `full_pipeline_bounded` reads
    `ctx["task"]["sql"]`, which on both the gold and the `--pred` path is the
    BENCHMARK's gold SQL — ground truth a deployed system does not have. Here the
    filter is `plan["sql"]`, the query the relational plan itself synthesized.

    The two coincide exactly on `gold_table_specs.jsonl`, whose `sql` field is
    the gold SQL verbatim in all 43 rows, so a gold-plan run reproduces the old
    numbers. They diverge on synthesized plans (0 of 43 plans_v4 rows match gold
    SQL), which is the point: the filter's quality is then a property of the
    plan, and is scored as such.

    `column_types` stays full either way — only the completion/stop target
    shrinks, so classifier features and parameter synthesis are untouched.
    """

    def run_table(self, df0, spec, ctx):
        need = _info_need_columns(ctx.get("plan_sql") or "")
        if need:
            pk = set(spec.get("primary_key") or [])
            joins = set(spec.get("join_cols") or [])
            keep = {c for c in (spec.get("column_types") or {})
                    if re.sub(r"[^a-z0-9]", "", str(c).lower()) in need} | pk | joins
            if keep:
                spec = {**spec, "output_columns": sorted(keep)}
        return super().run_table(df0, spec, ctx)



def _make_loop(model: str):
    return _Loop(
        op_source="pipeline",
        model=model,
        budget=FIXED["budget"],
        beam_width=FIXED["beam_width"],
        uncertain_prob=FIXED["uncertain_prob"],
        uncertain_gap=FIXED["uncertain_gap"],
        max_terminal_candidates=FIXED["max_terminal_candidates"],
    )


# --------------------------------------------------------------------------- #
# phase 2: joint candidate selection
# --------------------------------------------------------------------------- #

def _payload(obj: Any) -> dict:
    if isinstance(obj, dict) and "df" in obj:
        return obj
    return {"df": obj, "chain": [], "steps": [], "ok": False, "terminal_candidates": []}


def _candidate_key(c: dict) -> tuple:
    """Identity of a terminal candidate: its produced columns and its chain."""
    df = c.get("df")
    cols = tuple(map(str, df.columns)) if df is not None else ()
    return cols, tuple(c.get("chain") or [])


def _candidate_digest(cands: Sequence[dict], chosen: Optional[dict]) -> List[dict]:
    """Terminal pool as JSON, frames reduced to columns and shape.

    The selected chain alone cannot answer "was a correct table ever reachable" —
    the question that separates a synthesis fault from a schema that asked for
    something unbuildable. Frames are NOT kept: columns and shape are what the
    question turns on.
    """
    pick = _candidate_key(chosen) if chosen else None
    out, seen = [], set()
    for c in sorted(cands, key=lambda x: -float(x.get("score") or 0.0)):
        if not isinstance(c, dict) or "df" not in c:
            continue
        key = _candidate_key(c)
        if key in seen:
            continue
        seen.add(key)
        df = c.get("df")
        out.append({
            "chain": list(c.get("chain") or []),
            "steps": list(c.get("steps") or []),
            "columns": [str(x) for x in df.columns] if df is not None else [],
            "shape": list(df.shape) if df is not None else None,
            "score": c.get("score"),
            "ok": bool(c.get("ok")),
            "selected": key == pick,
        })
    return out


def _build_pools(table_results: Dict[str, dict], limit: int) -> Dict[str, List[dict]]:
    """Each table's top-`limit` DISTINCT terminal candidates, best-scoring first.

    Distinct by (produced columns, chain): the search often reaches the same
    frame by different routes, and duplicates would only widen the graph without
    adding a choice.
    """
    pools: Dict[str, List[dict]] = {}
    for lt in table_results:
        payload = _payload(table_results[lt])
        cands = [{**c, "df": M.sanitize(c["df"])}
                 for c in (payload.get("terminal_candidates") or [])
                 if isinstance(c, dict) and "df" in c] or [payload]
        seen, uniq = set(), []
        for c in sorted(cands, key=lambda x: -float(x.get("score") or 0.0)):
            key = (tuple(map(str, c["df"].columns)), tuple(c.get("chain") or []))
            if key in seen:
                continue
            seen.add(key)
            uniq.append(c)
            if len(uniq) >= limit:
                break
        pools[lt] = uniq
    return pools


def _joint_select(table_results: Dict[str, dict],
                  edges: Sequence[dict],
                  plan_tables: Dict[str, dict],
                  limit: int,
                  method: str = "branch_and_bound") -> Dict[str, dict]:
    """Choose one candidate per table, jointly.

    Posed as maximum-weight clique on a complete multipartite graph: parts are
    logical tables, nodes are their candidates, node weights are per-table name
    coverage, edge weights are cross-table join-key value overlap. Because the
    objective decomposes exactly into those terms and every transversal of a
    complete multipartite graph is a clique, this returns exactly what the
    original exhaustive product returned — see `verify_graph_alignment.py`.
    """
    if not table_results:
        return {}
    pools = _build_pools(table_results, limit)
    declared = {lt: (info.get("schema") or {}) for lt, info in plan_tables.items()}
    # The engine's `col_values` is the authority on what a column's value set is;
    # the graph's own fallback exists only so it can be tested standalone.
    cache = ValueCache(values_fn=col_values)
    selected = select_candidates(pools, edges, declared, cache=cache, method=method)
    return selected or {lt: _payload(v) for lt, v in table_results.items()}


# --------------------------------------------------------------------------- #
# public API
# --------------------------------------------------------------------------- #

def _resolve_input_files(schema: Dict[str, Any]) -> Dict[str, str]:
    """Bind each logical table to its raw input file BY NAME, not by position.

    `full_pipeline.synth_one` does `input_table[int(lt[-1]) - 1]`, i.e. it
    assumes logical table N is the Nth input file. That holds for gold specs but
    NOT for synthesized ones: half the tasks number their logical tables in a
    different order than the inputs are listed, so half were handed the WRONG
    raw table. The relational schema records `input_file` per table, so use it.
    """
    out: Dict[str, str] = {}
    for t in schema.get("tables") or []:
        lt = str(t.get("logical_table") or "")
        if lt and t.get("input_file"):
            out[lt] = t["input_file"]
    return out


@dataclass
class TablePipeline:
    """One logical table's synthesized pipeline and its materialised result."""
    logical_table: str
    db_table: str
    ops: List[str] = field(default_factory=list)
    steps: List[dict] = field(default_factory=list)
    primary_key: List[str] = field(default_factory=list)
    join_cols: List[str] = field(default_factory=list)
    df: Optional[pd.DataFrame] = None
    complete: bool = False
    score: Optional[float] = None
    llm_calls: int = 0
    candidates: List[dict] = field(default_factory=list)

    def to_dict(self, with_frame: bool = False) -> dict:
        d = {
            "logical_table": self.logical_table,
            "db_table": self.db_table,
            "ops": self.ops,
            "steps": self.steps,
            "primary_key": self.primary_key,
            "join_cols": self.join_cols,
            "columns": [str(c) for c in self.df.columns] if self.df is not None else [],
            "shape": list(self.df.shape) if self.df is not None else None,
            "complete": self.complete,
            "score": self.score,
            "llm_calls": self.llm_calls,
            "candidates": self.candidates,
        }
        if with_frame:
            d["df"] = self.df
        return d


def synthesize_pipeline(schema: Dict[str, Any],
                        tables_dir: Path,
                        *,
                        question: str = "",
                        db_id: str = "",
                        raw_tables: Optional[Dict[str, pd.DataFrame]] = None,
                        model: str = FIXED["model"],
                        workers: int = FIXED["workers"],
                        repair_hints: Optional[Dict[str, str]] = None,
                        repair_joins_after: bool = True,
                        select_method: str = "branch_and_bound") -> Dict[str, Any]:
    """Synthesize the pipeline for ONE task.

    schema       a relational-schema row from `relational_schema.py`:
                 {task_id, question, join_edges,
                  tables: [{logical_table, input_file, db_table, create_table_sql}]}
    tables_dir   where the raw input tables live
    raw_tables   {logical_table: DataFrame} to bypass reading `input_file`
    repair_hints {logical_table: text} appended to that table's parameter-
                 synthesis prompt. Empty on the first pass; set by the
                 self-correction module so a re-run differs from the first run
                 by the evidence and nothing else.

    Requires OPENAI_API_KEY: without it every parameter-synthesis candidate
    fails and the returned chains are silently empty.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is required: without it every parameter-synthesis "
            "candidate fails and every synthesized chain comes back empty")

    tid = schema.get("task_id")
    question = question or schema.get("question") or ""

    # `map_task_from_spec` parses each CREATE TABLE into {schema, pk} and derives
    # the join edges. It reads the older `gold_tables` key, so present the
    # schema under both names rather than editing the engine.
    spec = {**schema, "gold_tables": schema.get("tables") or [],
            # This stage has no answer SQL, and must not reach for the
            # benchmark's. The engine merges edges parsed out of a `sql` field
            # with the explicit ones; with no SQL it simply uses the explicit set.
            "sql": ""}
    plan_tables, edges = FP.map_task_from_spec(spec)

    loop = _make_loop(model)
    task_usage: Dict[str, int] = {"calls": 0, "input": 0, "output": 0, "cached": 0}
    _TASK_USAGE.set(task_usage)
    t_start = time.perf_counter()

    input_files = _resolve_input_files(schema)
    task_ctx = {"question": question, "db_id": db_id,
                "input_table": list(input_files.values())}

    def _one(lt: str, info: dict):
        if raw_tables and lt in raw_tables:
            df0 = M.sanitize(raw_tables[lt])
        else:
            df0 = M.sanitize(pd.read_pickle(Path(tables_dir) / input_files[lt]))
        schema_sql = schema_to_sql(info["schema"], info["pk"])
        ctx = {"task": task_ctx, "logical_table": lt, "schema_spec": schema_sql,
               "db_id": db_id, "source": "bird",
               # No plan SQL at this stage, so the completion target is the full
               # declared schema. See `_Loop` for what that changes.
               "plan_sql": "",
               "repair_hint": (repair_hints or {}).get(lt, ""),
               "join_targets": info.get("join_targets") or []}
        tspec = {"create_table_sql": schema_sql,
                 "primary_key": sorted(info["pk"]),
                 "column_types": info["schema"],
                 "output_columns": list(info["schema"]),
                 "join_cols": sorted(info.get("join_cols") or []),
                 "join_targets": info.get("join_targets") or []}
        return loop.run_table(df0, tspec, ctx)

    table_results: Dict[str, dict] = {}
    errors: List[str] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {_submit_ctx(ex, _one, lt, info): lt
                for lt, info in plan_tables.items()}
        for fu, lt in futs.items():
            try:
                table_results[lt] = _payload(fu.result())
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{tid}::{lt}: {type(exc).__name__}: {exc}")

    selected = _joint_select(table_results, edges, plan_tables,
                             FIXED["join_rerank_candidates"], method=select_method)

    subs = {lt: (M.sanitize(p["df"]), plan_tables[lt]["db_table"],
                 set(plan_tables[lt]["pk"]))
            for lt, p in selected.items() if lt in plan_tables}

    log: List[str] = []
    if repair_joins_after and subs:
        subs, log = repair_joins(subs, edges, FP.anchors_for(plan_tables, edges),
                                 expose_fn=None)

    # AFTER join repair. `repair_joins` matches the declared edges by VALUE and
    # conformance rewrites values, so running it first hands the repairer
    # different domains than it was tuned against. Replaying one run's chains:
    #     no conform            subtable .517  join_key .658
    #     conform after repair  subtable .542  join_key .733
    #     conform before repair subtable .533  join_key .725
    if os.environ.get("CONFORM_SCHEMA") == "1":
        subs = {lt: (conform_to_schema(df, plan_tables[lt]["schema"]), db, pk)
                for lt, (df, db, pk) in subs.items()}

    tables: Dict[str, TablePipeline] = {}
    for lt, info in plan_tables.items():
        p = selected.get(lt) or {}
        # The table's real spend is the loop's total, not the selected
        # candidate's own branch: reading the candidate's value under-reports by
        # roughly 6x and makes any cost comparison meaningless.
        total_calls = int((table_results.get(lt) or {}).get("calls") or 0)
        tables[lt] = TablePipeline(
            logical_table=lt,
            db_table=info["db_table"],
            ops=list(p.get("chain") or []),
            steps=list(p.get("steps") or []),
            primary_key=sorted(info["pk"]),
            join_cols=sorted(info.get("join_cols") or []),
            df=subs[lt][0] if lt in subs else p.get("df"),
            complete=bool(p.get("ok")),
            score=p.get("score"),
            llm_calls=total_calls,
            candidates=_candidate_digest(
                (table_results.get(lt) or {}).get("terminal_candidates") or [], p),
        )

    return {
        "task_id": tid,
        "question": question,
        "tables": tables,
        "join_keys": list(edges),
        "join_repair_log": log,
        "errors": errors,
        "llm_calls": sum(t.llm_calls for t in tables.values()),
        "usage": {**task_usage,
                  "elapsed_seconds": round(time.perf_counter() - t_start, 3),
                  "cost_usd": round(_cost(task_usage), 4),
                  "model": model},
    }


def result_to_dict(result: Dict[str, Any], with_frames: bool = False) -> dict:
    """JSON-friendly view of `synthesize_pipeline`'s return value."""
    return {**result,
            "tables": {lt: t.to_dict(with_frames) for lt, t in result["tables"].items()}}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def default_schema_path(dataset: str) -> Path:
    return P.resolve(dataset, module="pipeline_synthesize",
                     group="schema").out("relational_schema.jsonl")


def default_pipeline_path(dataset: str) -> Path:
    return P.resolve(dataset, module="pipeline_synthesize",
                     group="pipeline").out("pipeline.jsonl")


def run_dataset(dataset: str, out_path: Path, schema_path: Optional[Path] = None,
                model: str = FIXED["model"], workers: int = FIXED["workers"],
                limit: int = 0, task_ids: Optional[Sequence[str]] = None,
                overwrite: bool = False,
                select_method: str = "branch_and_bound") -> Path:
    """Synthesize a pipeline for every relational schema, one record each."""
    ds = DS.resolve(dataset)
    by_task = {str(t.get("task_id")): t for t in ds.tasks()}

    schema_path = Path(schema_path or default_schema_path(dataset))
    schemas = load_jsonl(schema_path)
    if not schemas:
        raise FileNotFoundError(
            f"no relational schemas at {schema_path}. Run "
            f"pipeline_synthesize.relational_schema --dataset {dataset} first.")
    if task_ids:
        wanted = set(task_ids)
        schemas = [s for s in schemas if str(s.get("task_id")) in wanted]

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and out_path.exists():
        out_path.unlink()

    done = load_jsonl_by_key(out_path, "task_id")
    pending = [s for s in schemas if str(s.get("task_id")) not in done]
    if limit and limit > 0:
        pending = pending[:limit]

    print(f"[synth] dataset={dataset}  model={model}  workers={workers}")
    print(engine_paths.describe())
    print(f"[synth] schemas: {schema_path} ({len(schemas)})")
    print(f"[synth] cached={len(done)} to_process={len(pending)}")
    print(f"[synth] output:  {out_path}")

    written = 0
    for sch in pending:
        tid = str(sch.get("task_id"))
        task = by_task.get(tid) or {}
        t0 = time.perf_counter()
        try:
            res = synthesize_pipeline(
                sch, ds.input_tables,
                question=sch.get("question") or task.get("question", ""),
                db_id=task.get("db_id", ""),
                model=model, workers=workers, select_method=select_method)
        except Exception as exc:  # noqa: BLE001
            print(f"[synth] task {tid} failed: {type(exc).__name__}: {exc}")
            continue
        append_jsonl(out_path, result_to_dict(res))
        written += 1
        print(f"[synth] {tid}: {len(res['tables'])} tables, "
              f"{res['llm_calls']} calls, {time.perf_counter() - t0:.1f}s")

    print(f"[synth] wrote {written} records; usage so far: {usage_summary()}")
    return out_path


def parse_args():
    ap = argparse.ArgumentParser(
        description="Stage 2: synthesize the pipeline that materialises each schema.")
    ap.add_argument("--dataset", type=str, default="Synth-Bird")
    ap.add_argument("--schema", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--model", type=str, default=FIXED["model"])
    ap.add_argument("--workers", type=int, default=FIXED["workers"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--task-ids", type=str, nargs="+", default=None)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--select-method", choices=["branch_and_bound", "exhaustive"],
                    default="branch_and_bound",
                    help="Joint-selection solver. Both are exact and return the "
                         "same choice; 'exhaustive' is the original enumeration, "
                         "kept for cross-checking.")
    ap.add_argument("--policy-model", type=Path, default=None,
                    help="Override the trained operator classifier.")
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    if a.policy_model:
        os.environ["MULTISTEP_MODEL_PATH"] = str(a.policy_model)
    run_dataset(a.dataset, a.out or default_pipeline_path(a.dataset),
                schema_path=a.schema, model=a.model, workers=a.workers,
                limit=a.limit, task_ids=a.task_ids, overwrite=a.overwrite,
                select_method=a.select_method)
