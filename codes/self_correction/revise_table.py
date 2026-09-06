#!/usr/bin/env python3
"""
revise_table.py
===============
Re-run schema linking for a task whose table selection was judged wrong, with
the evidence of what that selection led to.

    from revise_table import revise_table
    new = revise_table(task, diag=diag, plan=plan, link=link, chains=chains,
                       produced=produced, inter=inter)
    new["selected_tables"]        # the revised selection
    new["revision"]["changed"]    # did it actually move

WHY THIS IS A THIN WRAPPER
--------------------------
It calls `schema_linking.link_schema_for_task` with a `prompt_suffix` and
nothing else. That is deliberate. The first pass and the repair must be
identical up to the appended evidence, otherwise a measured improvement cannot
be attributed to the evidence rather than to the rewrite. Every hypothesis that
tried to help by changing the base prompt instead (question-aware trimming,
sample values in the first pass, filename anonymisation) was measured and did
not survive; the one reproducible win came from putting recovery-dropped raw
column names into the repair context, which is a suffix.

WHAT IT IS FOR, AND WHERE IT STOPS
----------------------------------
Measured on the 32 bird tasks labelled `revise_table` (repair_eval v6):

    arm A  retry, no evidence      6/32  = 0.188
    arm B  retry + this evidence  16/32  = 0.500      McNemar p = 0.0063

but that total hides a split:

    tasks needing 2 tables    A  6/23    B 15/23   = 0.65
    tasks needing 3 tables    A  0/9     B  1/9    = 0.11

The evidence supports "this selection is missing something; find it" and does
not support "work out how three tables must hang together". On the failures the
mean gold-table recall is 0.52 — the typical failure is one table short, not a
wholesale miss. Three-table selection is a joinability-structure problem and
belongs to `revise_relational_plan`, whose evidence lives elsewhere.
"""
from __future__ import annotations

import os
import argparse
import json
import pickle
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT), str(ROOT / "actions"), str(ROOT / "prep_utils")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pandas as pd                                                 # noqa: E402
import schema_linking as SL                                         # noqa: E402
from repair_context import build_context                            # noqa: E402

AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[2] / "datasets")

#: Prepended to the diagnostics. Arm A of the A/B is this line alone, so the
#: measured effect is the evidence and not the fact of being asked twice.
RETRY_NOTE = """

NOTE ON THIS ATTEMPT
A previous selection for this question was judged incorrect. Select again.
"""


def build_suffix(*, diag: Dict[str, Any], plan: Dict[str, Any],
                 link: Dict[str, Any], chains: Dict[str, Any], task_id: str,
                 question: str, raw_tables: Dict[str, "pd.DataFrame"],
                 bench_dir: Path, produced: Dict[str, Any]) -> str:
    """The full text appended to the schema-linking prompt for a repair."""
    ctx = build_context(
        "revise_table", diag=diag, plan=plan, link=link, chains=chains,
        task_id=task_id, question=question, raw_tables=raw_tables,
        bench_dir=bench_dir, produced=produced,
        tried=[{"action": "revise_table",
                "what": f"selected {link.get('selected_tables')}"}])
    return RETRY_NOTE + "\nDIAGNOSTICS\n" + ctx


def load_evidence(inter: Path, task_id: str, *, benchmark: str = "nl2sql-bird",
                  split: str = "dev") -> Dict[str, Any]:
    """Gather everything `build_suffix` needs from a run directory.

    Reads the per-task pickle shard rather than the combined `tables.pkl`: the
    combined file is ~500 MB and a repair only ever needs one task.
    """
    def rows(name: str) -> Dict[str, dict]:
        p = inter / name
        if not p.exists():
            return {}
        return {json.loads(l)["task_id"]: json.loads(l)
                for l in p.open() if l.strip()}

    bench_dir = AUTOP / benchmark / split
    plans = rows("relational_plan.jsonl")
    cp = inter / "chains.json"

    produced: Dict[str, Any] = {}
    shard = inter / "tables" / f"{task_id}.pkl"
    if shard.exists():
        try:
            with shard.open("rb") as fh:
                produced = pickle.load(fh).get("subtables") or {}
        except Exception:
            produced = {}

    raw: Dict[str, pd.DataFrame] = {}
    for tb in (plans.get(task_id, {}).get("gold_tables") or []):
        p = bench_dir / (tb.get("input_file") or "")
        if p.exists():
            try:
                raw[tb["logical_table"]] = pd.read_pickle(p)
            except Exception:
                pass

    return {
        "diag": rows("diagnose.jsonl").get(task_id, {}),
        "plan": plans.get(task_id, {}),
        "link": rows("schema_linking.jsonl").get(task_id, {}),
        "chains": json.loads(cp.read_text()) if cp.exists() else {},
        "produced": produced,
        "raw_tables": raw,
        "bench_dir": bench_dir,
    }


def revise_table(task: Dict[str, Any], *,
                 diag: Dict[str, Any],
                 plan: Dict[str, Any],
                 link: Dict[str, Any],
                 chains: Optional[Dict[str, Any]] = None,
                 produced: Optional[Dict[str, Any]] = None,
                 raw_tables: Optional[Dict[str, "pd.DataFrame"]] = None,
                 bench_dir: Optional[Path] = None,
                 benchmark: str = "nl2sql-bird",
                 split: str = "dev",
                 model: str = SL.DEFAULT_MODEL,
                 with_evidence: bool = True) -> Dict[str, Any]:
    """Select tables again, given what the previous selection produced.

    `with_evidence=False` is the control arm: the model is told only that its
    answer was wrong. Keep it reachable — a model re-asked the same question
    answers differently on its own (measured 6/32 here), and without the control
    every sampling win reads as evidence that the evidence worked.

    Returns the `link_schema` result with an extra `revision` block:
        {previous, changed, added, dropped, with_evidence}
    """
    tid = task.get("task_id") or plan.get("task_id") or ""
    bench_dir = bench_dir or (AUTOP / benchmark / split)

    suffix = RETRY_NOTE
    context_error = None
    if with_evidence:
        try:
            suffix = build_suffix(
                diag=diag, plan=plan, link=link, chains=chains or {},
                task_id=tid, question=task.get("question", ""),
                raw_tables=raw_tables or {}, bench_dir=bench_dir,
                produced=produced or {})
        except Exception as exc:
            # A missing artefact must not silently downgrade the treatment arm
            # into the control arm; report it instead.
            context_error = f"{type(exc).__name__}: {exc}"

    res = SL.link_schema_for_task(task, benchmark=benchmark, split=split,
                                  model=model, on_missing="original",
                                  prompt_suffix=suffix)

    before = list(link.get("selected_tables") or [])
    after = list(res.get("selected_tables") or [])
    res["revision"] = {
        "previous": before,
        "changed": sorted(after) != sorted(before),
        "added": sorted(set(after) - set(before)),
        "dropped": sorted(set(before) - set(after)),
        "with_evidence": with_evidence and context_error is None,
    }
    if context_error:
        res["revision"]["context_error"] = context_error
    return res


def load_task(task_id: str, benchmark: str = "nl2sql-bird",
              split: str = "dev") -> Dict[str, Any]:
    """One benchmark row, read straight from benchmark.jsonl.

    Deliberately not `test_single_ops_type.load_benchmark`: that pulls in the
    whole synthesis stack (and its import-time env contract) for what is a
    single line of JSON.
    """
    p = AUTOP / benchmark / split / "benchmark.jsonl"
    for line in p.open():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("task_id") == task_id:
            return row
    raise KeyError(f"task {task_id!r} not in {benchmark}/{split}")


def revise_table_from_run(task_id: str, inter: Path, *,
                          benchmark: str = "nl2sql-bird", split: str = "dev",
                          **kw) -> Dict[str, Any]:
    """`revise_table` for a task in a run directory, loading its own evidence."""
    task = load_task(task_id, benchmark, split)
    ev = load_evidence(inter, task_id, benchmark=benchmark, split=split)
    return revise_table(task, benchmark=benchmark, split=split, **ev, **kw)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--inter", type=Path, required=True)
    ap.add_argument("--task-id", required=True)
    ap.add_argument("--benchmark", default="nl2sql-bird")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--model", default=SL.DEFAULT_MODEL)
    ap.add_argument("--no-evidence", action="store_true",
                    help="control arm: retry with no diagnostics")
    ap.add_argument("--show-prompt", action="store_true",
                    help="print the appended evidence and call nothing")
    args = ap.parse_args(argv)

    if args.show_prompt:
        ev = load_evidence(args.inter, args.task_id, benchmark=args.benchmark,
                           split=args.split)
        task = load_task(args.task_id, args.benchmark, args.split)
        print(build_suffix(task_id=args.task_id,
                           question=task.get("question", ""), **ev))
        return 0

    res = revise_table_from_run(args.task_id, args.inter,
                                benchmark=args.benchmark, split=args.split,
                                model=args.model,
                                with_evidence=not args.no_evidence)
    print(json.dumps({"task_id": args.task_id,
                      "selected_tables": res.get("selected_tables"),
                      "revision": res.get("revision")},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
