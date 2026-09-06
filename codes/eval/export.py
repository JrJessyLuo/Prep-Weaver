"""Turn a synthesized (or repaired) pipeline into an executable script per task.

Input  : results/pipeline_synthesize/pipeline/<Dataset>/pipeline.jsonl
         results/pipeline_synthesize/schema/<Dataset>/relational_schema.jsonl
         optionally results/self_correction/<Dataset>/repair.jsonl
Output : results/eval/<Dataset>/codes/<benchmark>/<task_id>.py

WHY EXPORT AT ALL
-----------------
`eval_all_oom.py` scores a method by RE-EXECUTING its source under a lineage
tracer, not by reading frames. Two consequences:

  * a task with no script is unscoreable, not merely unscored;
  * a script that does not reproduce the frame the run produced silently scores
    something else. `verify` replays each script and diffs its columns against
    the recorded run for exactly this reason.

Run:
    python -m eval.export --dataset Synth-Spider
    python -m eval.export --dataset Synth-Spider --repaired
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Optional

from common import dataset as DS
from common import paths as P
from common.io_utils import load_jsonl, load_jsonl_by_key

from . import __init__ as _  # noqa: F401  (path setup)


def default_code_dir(dataset: str) -> Path:
    """Where the scripts go. Laid out as <root>/<benchmark>/<task>.py because
    that is the shape `eval_all_oom --ours_dir` expects."""
    root = P.resolve(dataset, module="eval", group="").out_dir / "codes"
    return root / DS.SOURCE_NAME.get(dataset, dataset)


def export_dataset(dataset: str, out_dir: Optional[Path] = None,
                   repaired: bool = False, task_ids: Optional[list] = None,
                   limit: int = 0) -> list:
    """Write one script per task."""
    import export_for_eval as EX

    ds = DS.resolve(dataset)
    schema_path = P.resolve(dataset, module="pipeline_synthesize",
                            group="schema").out("relational_schema.jsonl")
    pipe_path = P.resolve(dataset, module="pipeline_synthesize",
                          group="pipeline").out("pipeline.jsonl")
    schemas = load_jsonl_by_key(schema_path, "task_id")
    pipes = load_jsonl(pipe_path)
    if not pipes:
        raise FileNotFoundError(f"no pipelines at {pipe_path}")

    repairs = {}
    if repaired:
        rp = P.resolve(dataset, module="self_correction", group="").out("repair.jsonl")
        repairs = load_jsonl_by_key(rp, "task_id")
        if not repairs:
            raise FileNotFoundError(f"--repaired asked for, but no records at {rp}")

    out_dir = Path(out_dir or default_code_dir(dataset))
    out_dir.mkdir(parents=True, exist_ok=True)

    by_task = {str(t.get("task_id")): t for t in ds.tasks()}
    written, skipped = [], []
    for pipe in pipes:
        tid = str(pipe.get("task_id"))
        if task_ids and tid not in set(task_ids):
            continue
        plan, task = schemas.get(tid), by_task.get(tid)
        if not plan or not task:
            skipped.append((tid, "missing schema or benchmark record"))
            continue
        # The exporter reads `gold_tables`; the schema uses `tables`.
        plan = dict(plan)
        plan["gold_tables"] = plan.get("tables") or plan.get("gold_tables") or []
        try:
            p = EX.export_one(pipe, plan, task, out_dir, bench_dir=ds.input_tables)
            written.append(p)
        except Exception as exc:  # noqa: BLE001
            skipped.append((tid, f"{type(exc).__name__}: {exc}"))
        if limit and len(written) >= limit:
            break

    print(f"[export] wrote {len(written)} scripts -> {out_dir}")
    if skipped:
        print(f"[export] skipped {len(skipped)}: {skipped[:5]}")

    write_usage(dataset, out_dir, repaired=repaired,
                task_ids=[p.stem for p in written])
    return written


def write_usage(dataset: str, out_dir: Path, repaired: bool = False,
                task_ids: Optional[list] = None) -> Path:
    """Write `_metrics.csv` beside the scripts: per task, tokens / calls / time.

    The evaluator reads exactly this file for any method named `ours*`, in
    exactly these columns, and reports cost as n/a when it is missing — which is
    indistinguishable from a method that made no calls.

    The figure is SUMMED OVER THE STAGES, because that is what a per-query cost
    means for this system: the relational schema, the pipeline synthesis, and
    (when scoring a repaired run) the repair. Reporting only the last stage
    would undercount by roughly the synthesis, which is where most of the tokens
    actually go.
    """
    stages = [
        ("pipeline_synthesize", "schema", "relational_schema.jsonl"),
        ("pipeline_synthesize", "pipeline", "pipeline.jsonl"),
    ]
    if repaired:
        stages.append(("self_correction", "", "repair.jsonl"))

    totals: dict = {}
    for module, group, name in stages:
        path = P.resolve(dataset, module=module, group=group).out(name)
        for tid, rec in load_jsonl_by_key(path, "task_id").items():
            u = rec.get("usage") or {}
            t = totals.setdefault(tid, {"in": 0, "out": 0, "calls": 0, "time": 0.0})
            # The two stages name these differently: the schema stage uses the
            # LLM-client keys, the synthesis and repair stages use the meter's.
            t["in"] += int(u.get("input") or u.get("in") or 0)
            t["out"] += int(u.get("output") or u.get("out") or 0)
            t["calls"] += int(u.get("calls") or 0)
            t["time"] += float(u.get("elapsed_seconds") or 0.0)

    if task_ids:
        keep = set(task_ids)
        totals = {k: v for k, v in totals.items() if k in keep}

    p = Path(out_dir) / "_metrics.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["task_id", "in", "out", "calls", "time"])
        for tid, t in sorted(totals.items()):
            w.writerow([tid, t["in"], t["out"], t["calls"], round(t["time"], 3)])
    n = len(totals)
    tot_in = sum(t["in"] for t in totals.values())
    tot_out = sum(t["out"] for t in totals.values())
    print(f"[export] usage for {n} tasks -> {p}  "
          f"({tot_in:,} in / {tot_out:,} out tokens)")
    return p


def parse_args():
    ap = argparse.ArgumentParser(description="Export executable scripts for scoring.")
    ap.add_argument("--dataset", default="Synth-Spider")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--repaired", action="store_true",
                    help="Export the self-correction module's chosen state "
                         "instead of the unrepaired synthesis.")
    ap.add_argument("--task-ids", nargs="+", default=None)
    ap.add_argument("--limit", type=int, default=0)
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    export_dataset(a.dataset, a.out, repaired=a.repaired,
                   task_ids=a.task_ids, limit=a.limit)
