"""Score the exported scripts with the external evaluator.

    python -m eval.score --dataset Synth-Spider

This shells out to DeepPrep's `eval_all_oom.py`, which re-executes each exported
script under a lineage tracer and reports subtable / join-key accuracy. That
evaluator is the REPORTABLE one and is deliberately not reimplemented here:
there is also an internal scorer (`self_correction/internal/score_subtables.py`)
and the two have disagreed on the same run before, so the numbers in the paper
come from this one and nothing else.

The evaluator is not part of this repository. Point at it with
`--eval-dir` or `DEEPPREP_EVAL_DIR`.

METHOD NAMES ARE A KEY, NOT A LABEL
-----------------------------------
`eval_all_oom` stores results keyed by method, and every name starting with
`ours` shares one code layout pointed at a different `--ours_dir`. Scoring a
repaired export as plain `ours` OVERWRITES the unrepaired baseline row it is
meant to be compared against, so `--repaired` defaults the method to
`ours_repaired`.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from common import dataset as DS
from common import paths as P

DEFAULT_EVAL_DIR = Path(os.environ.get(
    "DEEPPREP_EVAL_DIR", ""))


def default_code_root(dataset: str) -> Path:
    """`--ours_dir` points at the PARENT of the per-benchmark folders."""
    return P.resolve(dataset, module="eval", group="").out_dir / "codes"


def default_csv(dataset: str) -> Path:
    return P.resolve(dataset, module="eval", group="").out("eval_all.csv")


def run(dataset: str, *, eval_dir: Optional[Path] = None,
        ours_dir: Optional[Path] = None, method: str = "ours",
        out_csv: Optional[Path] = None, task_ids: Optional[list] = None,
        limit: int = 0, timeout: int = 120, mem_gb: float = 8.0,
        conform: bool = False, extra: Optional[list] = None) -> int:
    eval_dir = Path(eval_dir or DEFAULT_EVAL_DIR)
    script = eval_dir / "eval_all_oom.py"
    if not script.exists():
        raise FileNotFoundError(
            f"external evaluator not found at {script}. Set DEEPPREP_EVAL_DIR "
            f"or pass --eval-dir; it is not part of this repository.")

    benchmark = DS.SOURCE_NAME.get(dataset, dataset)
    ours_dir = Path(ours_dir or default_code_root(dataset))
    out_csv = Path(out_csv or default_csv(dataset))
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, str(script),
           "--benchmarks", benchmark,
           "--methods", method,
           "--ours_dir", str(ours_dir),
           "--out", str(out_csv),
           "--timeout", str(timeout),
           "--mem-gb", str(mem_gb)]
    if task_ids:
        cmd += ["--task-ids", *task_ids]
    if limit:
        cmd += ["--limit", str(limit)]
    cmd += list(extra or [])

    env = dict(os.environ)
    # CONFORM_SCHEMA gates the type-conformance pass. The evaluator has never
    # set it, so every reported number was produced with it OFF; turning it on
    # here would make this run incomparable to those.
    env["CONFORM_SCHEMA"] = "1" if conform else "0"

    # The evaluator REPLACES every row for this method key in its own results
    # store. Scoring a partial export therefore discards a complete earlier run
    # of the same name, and the loss is silent — the run prints "N new + M kept"
    # with this method simply absent from "kept".
    n_scripts = len(list((ours_dir / benchmark).glob("*.py")))
    n_tasks = len(DS.resolve(dataset).tasks())
    print(f"[score] dataset={dataset} benchmark={benchmark} method={method}")
    print(f"[score] scripts exported: {n_scripts}/{n_tasks} tasks")
    if n_scripts < n_tasks:
        print(f"[score] WARNING partial export. The evaluator will replace ALL "
              f"'{method}' rows in its store with these {n_scripts}. Use a "
              f"distinct --method for a partial run, or export every task first.")
    print(f"[score] scripts: {ours_dir}/{benchmark}")
    print(f"[score] out    : {out_csv}")
    print("[score] $ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=str(eval_dir), env=env)


def parse_args():
    ap = argparse.ArgumentParser(description="Score exported scripts.")
    ap.add_argument("--dataset", default="Synth-Spider")
    ap.add_argument("--eval-dir", type=Path, default=None,
                    help="DeepPrep evaluation directory (has eval_all_oom.py).")
    ap.add_argument("--ours-dir", type=Path, default=None)
    ap.add_argument("--method", default=None,
                    help="Result key. Defaults to 'ours', or 'ours_repaired' "
                         "with --repaired, so the two do not overwrite each other.")
    ap.add_argument("--repaired", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--task-ids", nargs="+", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--mem-gb", type=float, default=8.0)
    ap.add_argument("--conform", action="store_true",
                    help="Enable CONFORM_SCHEMA. OFF by default because every "
                         "previously reported number was produced without it.")
    ap.add_argument("rest", nargs="*", help="extra args passed through")
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    raise SystemExit(run(
        a.dataset, eval_dir=a.eval_dir, ours_dir=a.ours_dir,
        method=a.method or ("ours_repaired" if a.repaired else "ours"),
        out_csv=a.out, task_ids=a.task_ids, limit=a.limit,
        timeout=a.timeout, mem_gb=a.mem_gb, conform=a.conform, extra=a.rest))
