#!/usr/bin/env python3
"""
score_subtables.py
==================
Score a run's materialised subtables with the SAME two metrics the earlier
`full_pipeline.py` runs printed, so a new run can be put next to the old
grounded-spec numbers.

    subtable_full   value-domain bipartite match over every produced column
    join_key_full   value-domain match over the declared edges' key columns

Both definitions are copied from `full_pipeline.main()`'s evaluation block rather
than re-derived, because the numbers only compare if the metric does not move.

    python3 score_subtables.py --run <tables.pkl> [--tasks a,b,c]

The `.pkl` may come from either `example_run/initital_run/run.py` or a
`DUMP_CALIB=1` run of `full_pipeline_bounded.py` — both write the same structure
({task_id: {"subtables": {lt: DataFrame}, "edges": [...]}}).

READ THE COMPARABILITY WARNING
------------------------------
Putting a fresh run next to the old grounded numbers is only meaningful if you
know what else changed. Four things did, and each moves the score on its own:

  1. schema linking is now a real stage. The old runs were handed their tables by
     `--pred <spec>`; the new run picks them, so it can pick wrong.
  2. the completion gate no longer reads the gold SQL. Over-declared plans now
     burn budget and finish incomplete instead of being quietly rescued.
  3. the input-file binding bug is fixed. 22 of the 43 tasks (44 of 91 tables)
     were being handed the WRONG raw table under the old positional rule.
  4. schema linking now runs on gpt-4o rather than gpt-5.

Fix 3 should help, changes 1 and 2 should hurt, and 4 is unknown. A single
end-to-end number cannot separate them — use `--stages` in run.py, or feed a
fixed plan file, to isolate one at a time.
"""
from __future__ import annotations

import os
import argparse
import json
import pickle
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
for _p in (str(ROOT / "pipeline_eval"), str(ROOT / "train_infer_single_ops")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pandas as pd                                              # noqa: E402

# STRICT normalisation, matching the external evaluator.
#
# `eval_react_subtables.fast_norm_series` lowercases values before comparing.
# Nothing else does: DeepPrep-0432/evaluation (`_norm`), DeepPrep's own
# `evaluator.validate`, and BAT's `evaluator.py` all compare case-sensitively.
# Lowercasing here quietly forgave the one operation this benchmark scores for
# exactly that — `StandardizeString`, required by 7 of the 43 group_a tasks. On
# bird_1e4929d5 the raw `source` column holds Dues/DUES/DueS/DUes/dUeS/DuEs/
# duES/dues, the gold SQL filters `WHERE source = 'Dues'`, and the gold op
# canonicalises the casing; lowercasing in the metric scored that column as
# matched even though the pipeline never standardised it.
#
# Cost of switching, measured across five saved runs: a flat -3 tasks (-0.070),
# always the same three (bird_1e4929d5, bird_8a064cd5, bird_c74b2527). Because
# the penalty is constant, every relative comparison between configurations is
# unchanged — only the absolute level moves, and it now matches what
# eval_all_oom.py reports for the same frames.
sys.path.insert(0, os.environ.get(
    "DEEPPREP_EVAL_DIR", ""))
import eval_all_oom as _EXT                                     # noqa: E402

fast_norm_series = _EXT.fast_norm_series
_ARTIFACT_GT: dict = {}


def _as_sets(g: dict) -> dict:
    """Value domains as SETS, matching what `gt_birdspider` returns.

    JSON cannot hold a set, so `eval_gt` arrives as lists while the sqlite-backed
    path yields sets, and the external matcher intersects them with `&` — it
    raises `TypeError: unsupported operand type(s) for &: 'set' and 'list'` on
    the first task. The two producers have to agree in shape here, at the one
    point where the artefact form enters, rather than in the matcher.
    """
    return {"cols": [set(c) for c in (g.get("cols") or [])],
            "edges": [{"left": set(e.get("left") or []),
                       "right": set(e.get("right") or [])}
                      for e in (g.get("edges") or [])]}


def _artifact_gt(root, benchmark: str) -> dict:
    """Ground truth from `intermedidate_artifacts/gold_subtables_join_keys.jsonl`.

    `_EXT.gt_birdspider` reads `<benchmark>/<split>/outputs/<task>.json` and
    rebuilds the value domains by querying the source sqlite. The staged training
    split has no `outputs/` directory — its ground truth ships as an `eval_gt`
    field already in the `{cols, edges}` shape the scorer wants, so it is read
    directly. Measured on the 300 selected tasks: 300/300 carry `eval_gt`, 295
    carry `cols` and 260 carry `edges` (the other 40 are single-table, for which
    `join_key_full` is correctly None).
    """
    from pathlib import Path as _P
    key = str(benchmark)
    if key in _ARTIFACT_GT:
        return _ARTIFACT_GT[key]
    out: dict = {}
    for cand in (_P(root) / benchmark / "intermedidate_artifacts"
                 / "gold_subtables_join_keys.jsonl",
                 _P(root) / "all_training_data" / "intermedidate_artifacts"
                 / "gold_subtables_join_keys.jsonl"):
        if cand.exists():
            for line in cand.open():
                if line.strip():
                    r = json.loads(line)
                    g = r.get("eval_gt")
                    if g:
                        out[r["task_id"]] = _as_sets(g)
            break
    _ARTIFACT_GT[key] = out
    return out


def gt_birdspider(tid, bm, split, root):
    """Gold reference, from `outputs/` when present and from the staged
    artifacts otherwise. Tried in that order so existing benchmarks are
    untouched."""
    g = _EXT.gt_birdspider(tid, bm, split, str(root))
    if g:
        return g
    return _artifact_gt(root, bm).get(tid)
_max_value_domain_matching = _EXT._max_value_domain_matching


def score_predictions(pred, gt):
    """Subtable score under the external evaluator's matcher."""
    matched, total = _max_value_domain_matching(pred.get("cols") or [], gt.get("cols") or [])
    return {"subtable_full": bool(total) and matched == total,
            "subtable_recall": matched / max(total, 1)}


def col_values(df, col):
    """Strict-normalised value set of a column, case-insensitive column LOOKUP.

    Only the column NAME is matched case-insensitively; the values are not
    lowercased, unlike phase2_joinkey.col_values.
    """
    import re
    m = {re.sub(r"[^a-z0-9]", "", str(c).lower()): c for c in df.columns}
    real = m.get(re.sub(r"[^a-z0-9]", "", str(col).lower()))
    if real is None:
        return None
    return fast_norm_series(df[real])


def _value_domain_jk_frac(pred_keys, gold_domains):
    if not gold_domains:
        return None
    matched, total = _max_value_domain_matching(pred_keys, gold_domains)
    return matched / max(total, 1)


def score_task(subtables: Dict[str, pd.DataFrame],
               edges: Sequence[dict],
               gt: dict) -> Dict[str, Any]:
    """One task's two metrics, under `full_pipeline`'s definitions."""
    # subtable: pool every produced column's normalised value set and cover the
    # gold column domains one-to-one.
    pred_cols = []
    for df in subtables.values():
        for c in df.columns:
            v = fast_norm_series(df[c])
            if v:
                pred_cols.append(v)
    sc = score_predictions({"cols": pred_cols, "edges": []}, gt)

    # join key: direction-robust. Each edge contributes all four
    # (table, column) combinations; a column that does not exist yields an empty
    # set and drops out on its own.
    pred_keys = []
    for e in edges or []:
        for tbl, on in ((e.get("left_table"), e.get("left_on")),
                        (e.get("right_table"), e.get("right_on")),
                        (e.get("left_table"), e.get("right_on")),
                        (e.get("right_table"), e.get("left_on"))):
            if tbl in subtables and on:
                v = col_values(subtables[tbl], on)
                if v:
                    pred_keys.append(v)
    gold_domains = []
    for ge in gt.get("edges", []):
        if ge.get("left"):
            gold_domains.append(ge["left"])
        if ge.get("right"):
            gold_domains.append(ge["right"])
    jk = _value_domain_jk_frac(pred_keys, gold_domains)

    return {"subtable_full": bool(sc["subtable_full"]),
            "subtable_recall": float(sc["subtable_recall"]),
            "join_key_full": None if jk is None else int(jk >= 0.999),
            "join_key_recall": None if jk is None else float(jk)}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--run", required=True, type=Path, help="tables.pkl")
    ap.add_argument("--benchmark", default="nl2sql-bird")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--autoprep-root", type=Path, default=AUTOP)
    ap.add_argument("--tasks", default=None, help="comma-separated task_id filter")
    ap.add_argument("--cases", type=Path, default=None,
                    help="a cases jsonl whose task_ids define the scored set "
                         "(e.g. pipeline_eval/cases_group_a_high_ops_union_structural.jsonl)")
    ap.add_argument("--out", type=Path, default=None, help="per-task jsonl")
    args = ap.parse_args(argv)

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from prep_utils import load_run
    run = load_run(args.run)                 # tables.pkl, or the tables/ shard dir

    keep = None
    if args.cases:
        keep = {json.loads(l)["task_id"] for l in args.cases.open() if l.strip()}
    if args.tasks:
        sel = {t.strip() for t in args.tasks.split(",") if t.strip()}
        keep = sel if keep is None else (keep & sel)

    rows = []
    missing = []
    for tid, rec in run.items():
        if keep is not None and tid not in keep:
            continue
        gt = gt_birdspider(tid, args.benchmark, args.split, args.autoprep_root)
        if not gt:
            missing.append(tid)
            continue
        subs = {lt: v for lt, v in (rec.get("subtables") or {}).items()
                if isinstance(v, pd.DataFrame)}
        r = score_task(subs, rec.get("edges") or [], gt)
        r["task_id"] = tid
        rows.append(r)

    if keep is not None:
        absent = sorted(keep - {r["task_id"] for r in rows} - set(missing))
        if absent:
            print(f"WARNING: {len(absent)} requested task(s) are not in the run "
                  f"and are EXCLUDED from the denominator, which inflates the "
                  f"score relative to a full run: {absent[:6]}")

    n = len(rows)
    if not n:
        print("no scorable tasks")
        return 1
    njk = sum(1 for r in rows if r["join_key_full"] is not None)
    sf = sum(r["subtable_full"] for r in rows)
    sr = sum(r["subtable_recall"] for r in rows)
    jf = sum(r["join_key_full"] or 0 for r in rows)
    jr = sum(r["join_key_recall"] or 0.0 for r in rows if r["join_key_recall"] is not None)

    print(f"=== {args.run.name} | tasks={n} ===")
    print(f"subtable_full_accuracy : {sf/n:.3f}   ({sf}/{n})")
    print(f"subtable_recall        : {sr/n:.3f}")
    if njk:
        print(f"join_key_full_accuracy : {jf/njk:.3f}   ({jf}/{njk}, tasks with keys)")
        print(f"join_key_recall        : {jr/njk:.3f}")
    if missing:
        print(f"\n{len(missing)} task(s) had no gold reference and were skipped")

    if args.out:
        with args.out.open("w") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\nper-task -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
