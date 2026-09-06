"""Run the repair tree over a dataset.

Input  : results/table_discovery/selection/<Dataset>/table_selection.jsonl
         results/pipeline_synthesize/schema/<Dataset>/relational_schema.jsonl
         results/pipeline_synthesize/pipeline/<Dataset>/pipeline.jsonl
Output : results/self_correction/<Dataset>/repair.jsonl
         one record per task: the whole tree, the chosen node, and its path

Run:
    python -m self_correction.loop --dataset Synth-Bird --limit 1
    python -m self_correction.loop --dataset Synth-Bird --breadth 2 --max-depth 3
"""

from __future__ import annotations

import argparse
import json
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import paths as SCP
from .actions import ACTIONS, load_state, meter_reset, meter_total
from .localizer import load_localizer, p_ok_fn, rank_fn
from .tree import RepairTree

from common import dataset as DS
from common import paths as P
from common.io_utils import append_jsonl, load_jsonl_by_key


def default_out_path(dataset: str) -> Path:
    return P.resolve(dataset, module="self_correction",
                     group="").out("repair.jsonl")


def load_pipelines(dataset: str) -> Dict[str, Any]:
    """{task_id: pipeline record} — the terminal candidate pool per table.

    `revise_pipeline` offers the model the candidates the search already found
    and lets it ACCEPT one instead of writing pandas from scratch. Without this
    the candidate list is empty, the accept branch is unreachable, and the action
    is silently reduced to free-form rewriting only.
    """
    path = P.resolve(dataset, module="pipeline_synthesize",
                     group="pipeline").out("pipeline.jsonl")
    return load_jsonl_by_key(path, "task_id")


def repair_task(task_id: str, dataset: str, loc, cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Grow the repair tree for one task and return its record."""
    import diagnose as D

    meter_reset()
    t0 = time.perf_counter()
    st = load_state(task_id, dataset)
    chains = cfg.get("chains") or {}

    def rediagnose(s):
        return D.diagnose(s.task.get("question", ""), s.raw, s.plan, s.produced,
                          edges=s.edges,
                          run={"chains": {lt: chains.get(f"{task_id}::{lt}") or {}
                                          for lt in s.produced}})

    tree = RepairTree(
        actions=ACTIONS,
        rank_fn=rank_fn(loc),
        p_ok_fn=p_ok_fn(loc),
        diagnose_fn=rediagnose,
        max_depth=cfg["max_depth"],
        breadth=cfg["breadth"],
        max_nodes=cfg["max_nodes"],
        expand_threshold=cfg["expand_threshold"],
        trigger_threshold=cfg.get("trigger_threshold"),
        action_order=cfg.get("action_order"),
        stop_when_fixed=cfg.get("stop_when_fixed", False),
        chains=chains,
        cfg=cfg,
        verbose=cfg.get("verbose", True),
    )
    best = tree.run(st)

    rec = {"task_id": task_id, "dataset": dataset, **tree.to_dict()}
    rec["tables"] = {lt: [str(c) for c in df.columns]
                     for lt, df in (best.state.produced if best.state else {}).items()}
    rec["selected_tables"] = list(
        ((best.state.link if best.state else None) or {}).get("selected_tables") or [])
    rec["join_keys"] = list(best.state.edges) if best.state else []
    rec["usage"] = {**meter_total(),
                    "elapsed_seconds": round(time.perf_counter() - t0, 2)}
    return rec


def run_dataset(dataset: str, out_path: Path, cfg: Dict[str, Any],
                task_ids: Optional[List[str]] = None, limit: int = 0,
                overwrite: bool = False) -> Path:
    ds = DS.resolve(dataset)
    pipe_path = P.resolve(dataset, module="pipeline_synthesize",
                          group="pipeline").out("pipeline.jsonl")
    done_upstream = load_jsonl_by_key(pipe_path, "task_id")
    if not done_upstream:
        raise FileNotFoundError(
            f"no synthesized pipelines at {pipe_path}. Run "
            f"pipeline_synthesize.synthesize --dataset {dataset} first.")

    ids = [t for t in done_upstream]
    if task_ids:
        ids = [t for t in ids if t in set(task_ids)]

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and out_path.exists():
        out_path.unlink()
    done = load_jsonl_by_key(out_path, "task_id")
    pending = [t for t in ids if t not in done]
    if limit and limit > 0:
        pending = pending[:limit]

    cfg["pipe"] = load_pipelines(dataset)
    print(f"[repair] candidate pools loaded for {len(cfg['pipe'])} tasks")

    print(SCP.describe())
    loc = load_localizer(cfg["localizer_kind"], cfg.get("checkpoint"),
                         cfg.get("meta"), anonymize=not cfg.get("no_anonymize"),
                         url=cfg.get("localizer_url"))
    print(f"[repair] dataset={dataset} localizer={cfg['localizer_kind']}")
    print(f"[repair] depth<={cfg['max_depth']} breadth={cfg['breadth']} "
          f"nodes<={cfg['max_nodes']} expand>{cfg['expand_threshold']}")
    print(f"[repair] tasks={len(ids)} cached={len(done)} to_process={len(pending)}")
    print(f"[repair] output: {out_path}")

    written = 0
    for tid in pending:
        print(f"\n[repair] {tid}")
        try:
            rec = repair_task(tid, dataset, loc, cfg)
        except Exception as exc:  # noqa: BLE001
            print(f"[repair] {tid} failed: {type(exc).__name__}: {exc}")
            traceback.print_exc()
            continue
        append_jsonl(out_path, rec)
        written += 1
        print(f"[repair] {tid}: {rec['n_nodes']} nodes, best={rec['best_path']}, "
              f"p_ok {rec['best_p_ok']}, {rec['usage'].get('elapsed_seconds')}s")

    print(f"\n[repair] wrote {written} records")
    return out_path


def parse_args():
    ap = argparse.ArgumentParser(description="Run the repair tree over a dataset.")
    ap.add_argument("--dataset", default="Synth-Bird")
    ap.add_argument("--out", type=Path, default=None)

    # tree shape
    ap.add_argument("--max-depth", type=int, default=3,
                    help="Longest chain of revisions. Depth expansion.")
    ap.add_argument("--breadth", type=int, default=1,
                    help="Actions tried from each node. 1 reproduces the "
                         "original loop; 2 exploits hit@2 = 0.80.")
    ap.add_argument("--max-nodes", type=int, default=8,
                    help="Total node budget per task, the real cost cap.")
    ap.add_argument("--expand-threshold", type=float, default=0.05,
                    help="A child is expanded only if its p_ok delta exceeds "
                         "this. Selection ignores it — see tree.py.")
    ap.add_argument("--trigger-threshold", type=float, default=None,
                    help="Act whenever p_ok is below this, instead of stopping "
                         "when the localizer ranks no_revision_needed first.")
    ap.add_argument("--stop-when-fixed", action="store_true")
    ap.add_argument("--action-order", nargs="+", default=None,
                    help="Fallback order for actions the localizer did not rank. "
                         "Cheapest first is a good default: revise_pipeline is "
                         "two calls and no re-synthesis, revise_table re-runs "
                         "selection, schema AND every table's synthesis.")

    # localizer
    ap.add_argument("--localizer-kind", choices=["staged", "llm"], default="staged",
                    help="'staged' is the trained ModernBERT localizer that ships "
                         "with the repository; 'llm' is the comparison baseline.")
    ap.add_argument("--checkpoint", type=Path, default=None)
    ap.add_argument("--meta", type=Path, default=None)
    ap.add_argument("--no-anonymize", action="store_true",
                    help="Keep the real table names. Off by default: the "
                         "benchmark names gold input tables <task>_input_N, "
                         "which leaks the revise_table label outright.")

    # revise models
    ap.add_argument("--model", default="gpt-5-2025-08-07",
                    help="LLM that performs the revisions.")
    ap.add_argument("--model-syn", default=None,
                    help="LLM for the re-synthesis an action triggers.")
    ap.add_argument("--syn-workers", type=int, default=None,
                    help="Threads INSIDE one task's synthesis. The default of 8 "
                         "times several tasks is what got a full run OOM-killed.")

    # Every other stage spells this --task-ids; both are accepted so the
    # flag does not change name half way through the pipeline.
    ap.add_argument("--task-ids", "--tasks", dest="tasks", nargs="+", default=None,
                    help="Only these task ids.")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    cfg = {
        "max_depth": a.max_depth,
        "breadth": a.breadth,
        "max_nodes": a.max_nodes,
        "expand_threshold": a.expand_threshold,
        "trigger_threshold": a.trigger_threshold,
        "stop_when_fixed": a.stop_when_fixed,
        "action_order": a.action_order,
        "localizer_kind": a.localizer_kind,
        "checkpoint": a.checkpoint,
        "meta": a.meta,
        "no_anonymize": a.no_anonymize,
        "model": a.model,
        "model_syn": a.model_syn,
        "syn_workers": a.syn_workers,
        "dataset": a.dataset,
        "benchmark": DS.SOURCE_NAME.get(a.dataset, a.dataset),
        "split": "dev",
        "chains": {},
        "pipe": {},          # filled by run_dataset from pipeline.jsonl
        "verbose": not a.quiet,
    }
    run_dataset(a.dataset, a.out or default_out_path(a.dataset), cfg,
                task_ids=a.tasks, limit=a.limit, overwrite=a.overwrite)
