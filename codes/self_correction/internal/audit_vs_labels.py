#!/usr/bin/env python3
"""
audit_vs_labels.py
==================
Which of `diagnose.py`'s gold-free signals actually separate the FOUR-CLASS
stage-attribution label, one class at a time.

    python3 audit_vs_labels.py --diagnose <diagnose.jsonl> --labels <labels.jsonl>

`signal_audit.py` answers a different question — separability of a binary
"did the run succeed" label — and that collapses exactly the distinction the
stage decision needs: `revise_table` and `revise_pipeline` are both failures, so
a signal that tells them apart scores as useless there. This runs one-vs-rest per
class instead.

Read the output as a filter, not a ranking:

    |auc - 0.5| ~ 0   the signal cannot separate this class from the others and
                      is safe to drop for it
    large             worth keeping, but AUC on this sample size is noisy —
                      43 labelled tasks means one flipped task moves AUC by
                      roughly 0.02, so treat anything under ~0.65 as unproven

Nothing here may feed the classifier being audited: `labels.jsonl` is built from
gold, `diagnose.jsonl` is not, and mixing them would score a model on its own
answer key.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

LABELS = ("revise_table", "revise_relational_plan",
          "revise_pipeline", "no_revision_needed")


def _agg(name: str, values: Sequence[Any], out: Dict[str, float]) -> None:
    """Per-table / per-edge signals become min/mean/max over the task.

    Which aggregate matters is not knowable in advance: a single degenerate
    table dooms the task (min/max), while echo is better summarised by its
    worst offender. Emitting all three lets the audit decide.
    """
    nums = [float(v) for v in values if isinstance(v, (int, float, bool)) and v is not None]
    if not nums:
        return
    out[f"{name}__min"] = min(nums)
    out[f"{name}__mean"] = sum(nums) / len(nums)
    out[f"{name}__max"] = max(nums)


def flatten(diag: Dict[str, Any]) -> Dict[str, float]:
    """Every number `diagnose` produces, as one flat row."""
    out: Dict[str, float] = {}
    T, A, C = diag["T_table_selection"], diag["A_plan_fulfilment"], diag["C_join_health"]
    B = diag["B_result_health"]

    # --- T
    out["T1_plan_tables_without_input"] = float(T["T1_count"])
    out["T2_n_literals"] = float(len(T["T2_question_literals"]))
    out["T2_n_absent_literals"] = float(len(T["T2_literals_absent_from_all_values"]))
    out["T2_literal_grounding"] = float(T["T2_literal_grounding"])
    out["T3_n_isolated_tables"] = float(len(T["T3_isolated_tables"]))
    out["info_question_token_coverage"] = float(T["info_question_token_coverage"])

    # --- A
    out["A1_overall_fulfilment"] = float(A["A1_overall_fulfilment"])
    out["A1_unmet_columns"] = float(A["A1_unmet_columns"])
    out["A1_declared_columns"] = float(A["A1_declared_columns"])
    out["A2_execution_errors"] = float(A["A2_execution_errors"])
    pt = list(A["per_table"].values())
    _agg("A1_fulfilment", [p.get("A1_fulfilment") for p in pt], out)
    _agg("A5_verbatim_frac", [p.get("A5_verbatim_frac") for p in pt], out)
    _agg("A3_calls", [p.get("A3_calls") for p in pt], out)
    _agg("A4_terminal_count", [p.get("A4_terminal_count") for p in pt], out)
    _agg("A4_score_spread", [p.get("A4_score_spread") for p in pt], out)
    _agg("A4_distinct_chains", [p.get("A4_distinct_chains") for p in pt], out)
    out["A_n_tables"] = float(len(pt))
    out["A_n_chain_not_ok"] = float(sum(1 for p in pt if p.get("chain_ok") is False))
    out["A_n_saturated"] = float(sum(1 for p in pt if p.get("A3_budget_saturated")))
    out["A_n_all_tied"] = float(sum(1 for p in pt if p.get("A4_all_tied")))
    out["A_n_empty_chain"] = float(sum(1 for p in pt if not (p.get("chain") or [])))

    # --- B
    bl = list(B.values())
    _agg("B1_header_echo", [b["B1_header_echo_frac"] for b in bl], out)
    _agg("B2_density", [b["B2_non_null_density"] for b in bl], out)
    _agg("B_rows", [b["shape"][0] for b in bl], out)
    _agg("B_cols", [b["shape"][1] for b in bl], out)
    out["B_n_degenerate"] = float(sum(1 for b in bl if b["B2_degenerate_shape"]))
    _agg("B3_n_const_cols", [len(b["B3_constant_columns"]) for b in bl], out)
    _agg("B3_n_alluniq_cols", [len(b["B3_all_unique_text_columns"]) for b in bl], out)
    _agg("B4_n_type_mismatch", [len(b["B4_declared_numeric_but_not"]) for b in bl], out)

    # --- C
    edges = [e for e in C["edges"] if e.get("C5_endpoints_materialised")]
    out["C_n_edges"] = float(C["n_edges"])
    out["C5_n_missing_endpoint"] = float(C["n_edges"] - len(edges))
    if edges:
        best = [max(e["C2_containment_l_in_r"], e["C2_containment_r_in_l"]) for e in edges]
        _agg("C2_best_containment", best, out)
        _agg("C2_jaccard", [e["C2_jaccard"] for e in edges], out)
        _agg("C3_join_yield", [e["C3_join_yield"] for e in edges], out)
        _agg("C3_fanout", [e["C3_est_fanout"] for e in edges], out)
        _agg("C4_viable_pairs", [e["C4_ambiguity"]["n_viable_pairs"] for e in edges], out)
        _agg("C1_left_unique", [e["C1_left_key"].get("unique_ratio") for e in edges], out)
        _agg("C1_right_unique", [e["C1_right_key"].get("unique_ratio") for e in edges], out)
        _agg("C1_left_nonnull", [e["C1_left_key"].get("non_null") for e in edges], out)
        _agg("C1_right_nonnull", [e["C1_right_key"].get("non_null") for e in edges], out)
        out["C1_n_invalid_keys"] = float(sum(
            (0 if e["C1_left_key"].get("valid") else 1) +
            (0 if e["C1_right_key"].get("valid") else 1) for e in edges))
        out["C_n_undecidable"] = float(sum(
            1 for e in edges if str(e.get("verdict", "")).startswith("undecidable")))
    return out



def auc(x: np.ndarray, y: np.ndarray) -> float:
    """Rank AUC of feature `x` against binary label `y`, ties handled.

    Preferred over raw correlation for ranking: it is scale-free and unaffected
    by the heavy tails several of these features have (call counts, row counts).
    """
    pos, neg = x[y == 1], x[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = pd.Series(x).rank().to_numpy()
    return (ranks[y == 1].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def point_biserial(x: np.ndarray, y: np.ndarray) -> float:
    if x.std() == 0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def audit(rows: List[Dict[str, float]], labels: List[int]) -> pd.DataFrame:
    df = pd.DataFrame(rows).fillna(0.0)
    y = np.asarray(labels)
    recs = []
    for col in df.columns:
        x = df[col].to_numpy(dtype=float)
        a = auc(x, y)
        recs.append({
            "feature": col,
            "fire_rate": float((x != 0).mean()),
            "r": point_biserial(x, y),
            "auc": a,
            "sep": abs(a - 0.5) if a == a else float("nan"),
            "mean_success": float(x[y == 1].mean()) if (y == 1).any() else float("nan"),
            "mean_fail": float(x[y == 0].mean()) if (y == 0).any() else float("nan"),
        })
    return pd.DataFrame(recs).sort_values("sep", ascending=False).reset_index(drop=True)




def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[3])
    ap.add_argument("--diagnose", required=True, type=Path)
    ap.add_argument("--labels", required=True, type=Path)
    ap.add_argument("--top", type=int, default=8, help="signals shown per class")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)

    diag = {json.loads(l)["task_id"]: json.loads(l)
            for l in args.diagnose.open() if l.strip()}
    lab = {json.loads(l)["task_id"]: json.loads(l)
           for l in args.labels.open() if l.strip()}
    ids = [t for t in lab if t in diag]
    if not ids:
        ap.error("no task overlaps between the diagnostics and the labels")

    rows = [flatten(diag[t]) for t in ids]
    y = [lab[t]["label"] for t in ids]
    df = pd.DataFrame(rows).fillna(0.0)
    print(f"{len(ids)} labelled task(s) with diagnostics\n")
    for k, v in Counter(y).most_common():
        print(f"  {k:<24} {v:>3}")

    out_rows = []
    for cls in LABELS:
        yy = np.array([1 if v == cls else 0 for v in y])
        if yy.sum() == 0 or yy.sum() == len(yy):
            print(f"\n=== {cls} — {yy.sum()} example(s); not auditable ===")
            continue
        recs = []
        for col in df.columns:
            x = df[col].to_numpy(dtype=float)
            a = auc(x, yy)
            if a != a:
                continue
            recs.append({"class": cls, "feature": col, "auc": a,
                         "sep": abs(a - 0.5),
                         "mean_in": float(x[yy == 1].mean()),
                         "mean_out": float(x[yy == 0].mean())})
        tab = pd.DataFrame(recs).sort_values("sep", ascending=False)
        out_rows.append(tab)
        print(f"\n=== {cls}  (n={int(yy.sum())} vs {int(len(yy)-yy.sum())}) ===")
        print(tab.head(args.top).to_string(
            index=False, float_format=lambda v: f"{v:.3f}",
            columns=["feature", "auc", "sep", "mean_in", "mean_out"]))

    if args.out and out_rows:
        pd.concat(out_rows).to_csv(args.out, index=False)
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
