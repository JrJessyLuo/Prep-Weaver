"""The four reported metrics.

| reported name                | computed as                                    |
|------------------------------|------------------------------------------------|
| table identification accuracy| the selected table set EXACTLY equals the gold set |
| table correctness            | every gold value domain of every table is covered  |
| relationship correctness     | every gold join-key value domain is covered        |
| preparation correctness      | table correctness AND relationship correctness, per task |

WHERE EACH NUMBER COMES FROM
----------------------------
Table correctness and relationship correctness are the external evaluator's
`subtable_cov` and `join_key`, thresholded per task at >= 0.999. They are read
from its per-task CSV rather than recomputed, because there is also an internal
scorer and the two have disagreed on the same run; the reported numbers come
from the external one and nothing else.

Table identification accuracy is NOT produced by that evaluator — it does not
look at table selection at all — so it is computed here, from the selected table
set against the benchmark's gold set.

Preparation correctness is a PER-TASK conjunction, not the product of the two
rates. A dataset where half the tasks get the tables right and a disjoint half
get the relationships right scores 0.5 x 0.5 = 0.25 as a product and 0.0 as a
conjunction, and 0.0 is the truth: no single task was fully prepared.

WHICH SELECTION IS MEASURED
---------------------------
By default the one the self-correction module finally CHOSE, since `revise_table`
can change it. With no repair record it falls back to the first-pass selection.
`--source selection` forces the first-pass one, which is what to use when
reporting the pipeline without self-correction.

Run:
    python -m eval.metrics --dataset Synth-Spider
    python -m eval.metrics --dataset Synth-Spider --source selection
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from common import dataset as DS
from common import paths as P
from common.io_utils import load_jsonl_by_key

FULL = 0.999          # a coverage fraction at or above this counts as complete

METRIC_NAMES = {
    "table_identification_accuracy": "Table identification accuracy",
    "table_correctness": "Table correctness",
    "relationship_correctness": "Relationship correctness",
    "preparation_correctness": "Preparation correctness",
}


def default_csv(dataset: str) -> Path:
    return P.resolve(dataset, module="eval", group="").out("eval_all.csv")


def default_report(dataset: str) -> Path:
    return P.resolve(dataset, module="eval", group="").out("metrics.csv")


def _norm(name: Any) -> str:
    """Table file name -> a comparable key (basename, no .pkl, upper case)."""
    s = str(name).strip().split("/")[-1]
    if "#sep#" in s:
        s = s.split("#sep#")[-1]
    if s.lower().endswith(".pkl"):
        s = s[:-4]
    return s.upper()


def load_selections(dataset: str, source: str = "auto") -> Dict[str, List[str]]:
    """{task_id: selected table files}, from the repair record or the first pass."""
    repair = P.resolve(dataset, module="self_correction",
                       group="").out("repair.jsonl")
    first = P.resolve(dataset, module="table_discovery",
                      group="selection").out("table_selection.jsonl")

    if source in ("auto", "repair"):
        rows = load_jsonl_by_key(repair, "task_id")
        out = {t: list(r.get("selected_tables") or []) for t, r in rows.items()
               if r.get("selected_tables")}
        if out:
            print(f"[metrics] selections from {repair} ({len(out)} tasks)")
            if source == "auto":
                # Fill any task the repair run did not cover from the first pass,
                # so a partial repair run does not silently shrink the denominator.
                base = load_jsonl_by_key(first, "task_id")
                for t, r in base.items():
                    out.setdefault(t, list(r.get("selected_tables") or []))
            return out
        if source == "repair":
            raise FileNotFoundError(f"no selections in {repair}")

    rows = load_jsonl_by_key(first, "task_id")
    print(f"[metrics] selections from {first} ({len(rows)} tasks)")
    return {t: list(r.get("selected_tables") or []) for t, r in rows.items()}


def load_external(csv_path: Path, method: Optional[str] = None) -> Dict[str, dict]:
    """{task_id: {subtable_cov, join_key}} from the external evaluator's CSV."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"no evaluator output at {csv_path}. Run eval.score first.")
    out: Dict[str, dict] = {}
    with csv_path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if method and row.get("method") != method:
                continue
            try:
                out[str(row["task"])] = {
                    "subtable_cov": float(row.get("subtable_cov") or 0.0),
                    "join_key": float(row.get("join_key") or 0.0),
                }
            except (TypeError, ValueError):
                continue
    return out


def compute(dataset: str, csv_path: Optional[Path] = None,
            source: str = "auto", method: Optional[str] = None,
            task_ids: Optional[List[str]] = None) -> dict:
    """The four metrics, plus the per-task rows they were computed from."""
    ds = DS.resolve(dataset)
    gold = {str(t.get("task_id")): {_norm(x) for x in ds.gold_tables(t)}
            for t in ds.tasks()}
    sel = load_selections(dataset, source)
    ext = load_external(csv_path or default_csv(dataset), method)

    ids = sorted(set(ext) | set(sel))
    if task_ids:
        ids = [t for t in ids if t in set(task_ids)]

    rows, n_ident, n_tab, n_rel, n_prep = [], 0, 0, 0, 0
    n_scored = 0
    for tid in ids:
        g = gold.get(tid, set())
        picked = {_norm(x) for x in sel.get(tid, [])}
        # EXACT set equality, not recall: selecting the gold tables plus three
        # distractors is not a correct identification, and a recall-only score
        # would rate "select everything" as perfect.
        ident = bool(g) and picked == g

        e = ext.get(tid)
        tab = rel = prep = None
        if e is not None:
            n_scored += 1
            tab = e["subtable_cov"] >= FULL
            rel = e["join_key"] >= FULL
            prep = tab and rel
            n_tab += int(tab); n_rel += int(rel); n_prep += int(prep)
        n_ident += int(ident)
        rows.append({"task_id": tid, "table_identification": ident,
                     "table_correctness": tab, "relationship_correctness": rel,
                     "preparation_correctness": prep,
                     "subtable_cov": None if e is None else e["subtable_cov"],
                     "join_key": None if e is None else e["join_key"],
                     "n_gold": len(g), "n_selected": len(picked)})

    n = len(ids)
    return {
        "dataset": dataset,
        "n_tasks": n,
        "n_scored": n_scored,
        "table_identification_accuracy": n_ident / n if n else 0.0,
        "table_correctness": n_tab / n_scored if n_scored else 0.0,
        "relationship_correctness": n_rel / n_scored if n_scored else 0.0,
        "preparation_correctness": n_prep / n_scored if n_scored else 0.0,
        "rows": rows,
    }


def report(res: dict, out_path: Optional[Path] = None) -> None:
    print(f"\n===== {res['dataset']}  "
          f"({res['n_tasks']} tasks, {res['n_scored']} scored by the evaluator) =====")
    for key, label in METRIC_NAMES.items():
        print(f"  {label:<32} {res[key]:.4f}")
    if res["n_scored"] < res["n_tasks"]:
        print(f"  NOTE: {res['n_tasks'] - res['n_scored']} task(s) have no "
              f"evaluator row; they count in table identification only.")

    if out_path:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["metric", "value", "n"])
            for key, label in METRIC_NAMES.items():
                n = res["n_tasks"] if key == "table_identification_accuracy" else res["n_scored"]
                w.writerow([label, f"{res[key]:.4f}", n])
            w.writerow([])
            w.writerow(["task_id", "table_identification", "table_correctness",
                        "relationship_correctness", "preparation_correctness",
                        "subtable_cov", "join_key", "n_gold", "n_selected"])
            for r in res["rows"]:
                w.writerow([r["task_id"], r["table_identification"],
                            r["table_correctness"], r["relationship_correctness"],
                            r["preparation_correctness"], r["subtable_cov"],
                            r["join_key"], r["n_gold"], r["n_selected"]])
        print(f"\n  -> {out_path}")


def parse_args():
    ap = argparse.ArgumentParser(description="Report the four evaluation metrics.")
    ap.add_argument("--dataset", default="Synth-Spider")
    ap.add_argument("--csv", type=Path, default=None,
                    help="Per-task CSV from eval.score (eval_all.csv).")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--source", choices=["auto", "repair", "selection"], default="auto",
                    help="Which selection to score. 'auto' prefers the repaired "
                         "one; 'selection' reports the pipeline without "
                         "self-correction.")
    ap.add_argument("--method", default=None,
                    help="Filter the evaluator CSV to one method key.")
    ap.add_argument("--task-ids", nargs="+", default=None)
    return ap.parse_args()


if __name__ == "__main__":
    a = parse_args()
    report(compute(a.dataset, a.csv, a.source, a.method, a.task_ids),
           a.out or default_report(a.dataset))
