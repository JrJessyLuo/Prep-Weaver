#!/usr/bin/env python3
"""
localize.py
===========
Which stage to revise, and whether a revision helped — both from the same
gold-free model over `diagnose.py`'s signals.

    from prep_utils.localize import Localizer
    loc = Localizer.load(path)
    for action, p in loc.rank(diag):        # try in this order
        new_diag = reinvoke(action)
        if loc.delta(diag, new_diag) > loc.delta_threshold:
            diag = new_diag; break          # accept
        # else roll back and fall through to the next action

    python3 localize.py --inter <intermedidate_results/<bm>> --save loc.joblib
    python3 localize.py --inter ... --calibrate-delta <paired diagnose.jsonl>

WHY A RANKING AND NOT A LABEL
-----------------------------
Measured on 141 nl2sql-bird dev tasks, 5-fold CV x 5 seeds:

    top-1   0.599        top-2   0.774        top-3   0.911
    majority class 0.464, hand-written rule cascade 0.362, LLM judge 0.414

Top-1 is weak, and a single hard label spends that weakness badly: a wrong guess
ends the round with nothing to fall back on. The repair loop can afford to be
wrong once — it keeps a best-so-far and rolls back on a non-positive delta — so
what it needs is the correct stage ranked EARLY, not ranked first. 0.599 -> 0.774
is the whole argument for emitting probabilities.

The accuracy also hides two very different sub-problems, and reporting only the
flat number misrepresents both:

    "does this need repair at all"   AUC 0.838   (65 clean vs 76 broken)
    "given it does, which stage"     0.547       (majority 0.421, n=76)

The trigger is usable today. The attribution is not, on its own.

WHY delta IS P(no_revision_needed)
----------------------------------
`no_revision_needed` is defined as subtable_full AND join_key_full both perfect,
so the model's probability for that class IS a gold-free estimate of "is this
output correct". Using it as the progress signal means one model serves both
roles, and it beats a hand-weighted score over (satisfied_columns,
satisfied_edges): the column term there is NAME-based, and this codebase has
already been burnt by that — a grounded view that echoed raw headers scored as
fulfilled while every value was wrong. P also reads C2 containment, C4 viable
pairs and B density, which a rename cannot move.

Validated on 128 paired observations (our plan -> gold plan, i.e. one real
`revise_relational_plan` repair), scoring each pair with a model that never saw
that task:

    truth improved (n=26)     dP > 0 in 18      mean dP  +0.191
    truth unchanged (n=95)    dP > 0 in 44      mean dP  -0.020
    truth REGRESSED (n=7)     dP > 0 in  0      mean dP  -0.592

Sign agreement on the 33 tasks that actually moved: 0.758. The property that
matters for a rollback gate is the third row: it never once called a regression
an improvement. The gate's errors fall on the safe side — a real improvement
rolled back costs a round, an accepted regression costs the result.

Three limits, all live:
  * only ONE action type is represented in that pairing (plan revision). The
    delta behaviour under revise_table / revise_pipeline is untested.
  * 0.758 is 33 samples; the binomial standard error is about 7 points.
  * 44 of 95 no-op repairs still show dP > 0, which is why the threshold is not
    0. It is calibrated to trade those against the 26 real improvements.
"""
from __future__ import annotations

import os
import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
for _p in (str(ROOT), str(ROOT / "construct_training_data")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from audit_vs_labels import flatten                                # noqa: E402

ACTIONS = ("revise_table", "revise_relational_plan",
           "revise_pipeline", "no_revision_needed")
OK = "no_revision_needed"

# Schema linking's prompt says the selection "may range from 2 to {max_tables}",
# for every benchmark. Fewer than two therefore breaks the stage's own contract.
MIN_SELECTED_TABLES = 2


class Localizer:
    """Ranks repair actions, and scores whether a repair helped."""

    def __init__(self, model: Any, columns: Sequence[str],
                 classes: Sequence[str], delta_threshold: float = 0.05,
                 metadata: Optional[Dict[str, Any]] = None) -> None:
        self.model = model
        self.columns = list(columns)
        self.classes = list(classes)
        self.delta_threshold = float(delta_threshold)
        self.metadata = metadata or {}

    # -- features ----------------------------------------------------------
    def _row(self, diag: Dict[str, Any]) -> np.ndarray:
        """One diagnosis -> the training feature vector, in the training order.

        Reindexed rather than taken as-is: a task with no declared edges emits
        no C_* keys at all, so the flattened dicts are ragged. Aligning by
        position would silently feed containment values into a fanout column.
        """
        s = pd.Series(flatten(diag), dtype="float64").reindex(self.columns)
        return s.fillna(0.0).to_numpy(dtype=float).reshape(1, -1)

    def _proba(self, diag: Dict[str, Any]) -> Dict[str, float]:
        p = self.model.predict_proba(self._row(diag))[0]
        return {c: float(v) for c, v in zip(self.classes, p)}

    # -- the two things the loop needs --------------------------------------
    def rank(self, diag: Dict[str, Any],
             exclude: Sequence[str] = (),
             link: Optional[Dict[str, Any]] = None,
             min_tables: int = MIN_SELECTED_TABLES) -> List[Tuple[str, float]]:
        """Actions, most probable first. `exclude` drops directions already tried.

        When `link` is given, an under-filled selection short-circuits the model.
        Schema linking's own prompt states the selection "may range from 2 to
        {max_tables}", so fewer than two tables violates the stage's contract and
        is wrong without reference to gold. On nl2sql-bird dev it fires on 8 of
        141 tasks and all 8 carry the `revise_table` label — no exceptions, and
        no task in that split needs fewer than two tables. Leaving it to the
        classifier turns a certainty into a probability for no benefit.
        """
        ex = set(exclude)
        if link is not None:
            n = len(link.get("selected_tables") or [])
            if n < min_tables and "revise_table" not in ex:
                rest = [(a, v) for a, v in sorted(self._proba(diag).items(),
                                                  key=lambda kv: -kv[1])
                        if a not in ex | {"revise_table"}]
                return [("revise_table", 1.0)] + rest
        p = self._proba(diag)
        return [(a, v) for a, v in sorted(p.items(), key=lambda kv: -kv[1])
                if a not in ex]

    def p_ok(self, diag: Dict[str, Any]) -> float:
        """Gold-free estimate that this output is already correct."""
        return self._proba(diag).get(OK, 0.0)

    def delta(self, before: Dict[str, Any], after: Dict[str, Any]) -> float:
        return self.p_ok(after) - self.p_ok(before)

    def accept(self, before: Dict[str, Any], after: Dict[str, Any]) -> bool:
        return self.delta(before, after) > self.delta_threshold

    # -- persistence --------------------------------------------------------
    def save(self, path: Path) -> None:
        import joblib
        joblib.dump({"model": self.model, "columns": self.columns,
                     "classes": self.classes,
                     "delta_threshold": self.delta_threshold,
                     "metadata": self.metadata}, path)

    @classmethod
    def load(cls, path: Path) -> "Localizer":
        import joblib
        d = joblib.load(path)
        return cls(d["model"], d["columns"], d["classes"],
                   d.get("delta_threshold", 0.05), d.get("metadata"))

    @classmethod
    def fit(cls, diags: Dict[str, dict], labels: Dict[str, str],
            seed: int = 0, delta_threshold: float = 0.05) -> "Localizer":
        from sklearn.ensemble import HistGradientBoostingClassifier
        ids = [t for t in labels if t in diags]
        X = pd.DataFrame([flatten(diags[t]) for t in ids]).fillna(0.0)
        y = np.array([labels[t] for t in ids])
        m = HistGradientBoostingClassifier(max_depth=3, max_iter=200,
                                           random_state=seed).fit(X.to_numpy(), y)
        return cls(m, list(X.columns), list(m.classes_), delta_threshold,
                   {"n_train": len(ids), "labels": dict(Counter(y))})


# --------------------------------------------------------------------------- #
# evaluation
# --------------------------------------------------------------------------- #

def cv_report(diags: Dict[str, dict], labels: Dict[str, str],
              seeds: int = 5) -> Dict[str, Any]:
    """Out-of-fold hit@k, the trigger AUC, and attribution among broken tasks."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    ids = [t for t in labels if t in diags]
    X = pd.DataFrame([flatten(diags[t]) for t in ids]).fillna(0.0).to_numpy()
    y = np.array([labels[t] for t in ids])
    mk = lambda s: HistGradientBoostingClassifier(                        # noqa: E731
        max_depth=3, max_iter=200, random_state=s)

    hits = {k: [] for k in (1, 2, 3)}
    auc, ranks_all = [], []
    for s in range(seeds):
        cv = StratifiedKFold(5, shuffle=True, random_state=s)
        P = cross_val_predict(mk(s), X, y, cv=cv, method="predict_proba")
        cls = np.array(sorted(set(y)))
        order = np.argsort(-P, axis=1)
        # 1-based position of the true class in the ranking = rounds a loop that
        # detects failure and moves on would need.
        rank = np.array([1 + int(np.where(cls[order[i]] == y[i])[0][0])
                         for i in range(len(y))])
        ranks_all.append(rank)
        for k in hits:
            hits[k].append(float((rank <= k).mean()))
        yb = (y != OK).astype(int)
        pb = cross_val_predict(mk(s), X, yb, cv=cv, method="predict_proba")[:, 1]
        auc.append(roc_auc_score(yb, pb))

    broken = y != OK
    cond = []
    for s in range(seeds):
        cv = StratifiedKFold(3, shuffle=True, random_state=s)
        p = cross_val_predict(mk(s), X[broken], y[broken], cv=cv)
        cond.append(float((p == y[broken]).mean()))

    rank = np.concatenate(ranks_all)
    return {
        "n": len(ids),
        "hit@1": float(np.mean(hits[1])), "hit@2": float(np.mean(hits[2])),
        "hit@3": float(np.mean(hits[3])),
        "expected_rounds": float(rank.mean()),
        "trigger_auc": float(np.mean(auc)),
        "conditional_acc": float(np.mean(cond)),
        "conditional_majority": float(Counter(y[broken]).most_common(1)[0][1] / broken.sum()),
        "majority": float(Counter(y).most_common(1)[0][1] / len(y)),
    }


def calibrate_delta(diags_before: Dict[str, dict], diags_after: Dict[str, dict],
                    labels: Dict[str, str], truth: Dict[str, int],
                    seeds: int = 1) -> Dict[str, Any]:
    """Sweep the delta threshold on paired before/after observations.

    `truth[task]` is +1 / 0 / -1: did the repair actually improve, leave alone,
    or damage the result. Each pair is scored by a model that did not train on
    that task, so the probabilities are honest.
    """
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import StratifiedKFold

    ids = [t for t in labels
           if t in diags_before and t in diags_after and t in truth]
    cols = sorted(set(flatten(diags_before[ids[0]])))
    row = lambda d, t: pd.Series(flatten(d[t]), dtype="float64").reindex(cols).fillna(0.0)  # noqa: E731
    Xb = pd.DataFrame([row(diags_before, t) for t in ids])
    Xa = pd.DataFrame([row(diags_after, t) for t in ids])
    yb = np.array([1 if labels[t] == OK else 0 for t in ids])

    Pb, Pa = np.zeros(len(ids)), np.zeros(len(ids))
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(Xb, yb):
        m = HistGradientBoostingClassifier(max_depth=3, max_iter=200,
                                           random_state=0).fit(Xb.iloc[tr], yb[tr])
        Pb[te] = m.predict_proba(Xb.iloc[te])[:, 1]
        Pa[te] = m.predict_proba(Xa.iloc[te])[:, 1]

    d = Pa - Pb
    t = np.array([truth[i] for i in ids])
    rows = []
    for thr in np.arange(-0.05, 0.51, 0.025):
        acc = d > thr
        rows.append({
            "threshold": round(float(thr), 3),
            "kept_improvements": int((acc & (t > 0)).sum()),
            "kept_noops": int((acc & (t == 0)).sum()),
            # The number that must stay at zero: a regression the gate waved through.
            "kept_regressions": int((acc & (t < 0)).sum()),
        })
    return {"n_pairs": len(ids), "delta": d, "truth": t, "sweep": rows,
            "n_improved": int((t > 0).sum()), "n_noop": int((t == 0).sum()),
            "n_regressed": int((t < 0).sum())}


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _load(path: Path, key: str = "task_id") -> Dict[str, dict]:
    return {json.loads(l)[key]: json.loads(l) for l in path.open() if l.strip()}


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Fit and evaluate the stage localizer.")
    ap.add_argument("--inter", type=Path, required=True,
                    help="intermedidate_results/<benchmark> with diagnose.jsonl and labels.jsonl")
    ap.add_argument("--save", type=Path, default=None, help="write the fitted model here")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--delta-threshold", type=float, default=0.05)
    ap.add_argument("--calibrate-delta", type=Path, default=None, metavar="AFTER_DIAGNOSE",
                    help="diagnose.jsonl of a REPAIRED run of the same tasks")
    ap.add_argument("--scores-before", type=Path, default=None)
    ap.add_argument("--scores-after", type=Path, default=None,
                    help="score_subtables jsonl for each side, to derive the truth")
    args = ap.parse_args(argv)

    diags = _load(args.inter / "diagnose.jsonl")
    labels = {t: r["label"] for t, r in _load(args.inter / "labels.jsonl").items()}

    r = cv_report(diags, labels, seeds=args.seeds)
    print(f"{r['n']} task(s), {args.seeds} seeds\n")
    print(f"  majority class            {r['majority']:.3f}")
    print(f"  hit@1                     {r['hit@1']:.3f}")
    print(f"  hit@2                     {r['hit@2']:.3f}   <- 2 rounds")
    print(f"  hit@3                     {r['hit@3']:.3f}")
    print(f"  expected rounds to hit    {r['expected_rounds']:.2f}")
    print()
    print(f"  trigger AUC (repair?)     {r['trigger_auc']:.3f}")
    print(f"  attribution among broken  {r['conditional_acc']:.3f} "
          f"(majority {r['conditional_majority']:.3f})")

    if args.calibrate_delta:
        after = _load(args.calibrate_delta)
        sb = _load(args.scores_before or (args.inter / "scores.jsonl"))
        sa = _load(args.scores_after) if args.scores_after else {}
        if not sa:
            ap.error("--calibrate-delta needs --scores-after")
        ok = lambda s: (s["subtable_full"] >= 0.999) and (s["join_key_full"] >= 0.999)  # noqa: E731
        truth = {t: (1 if ok(sa[t]) else 0) - (1 if ok(sb[t]) else 0)
                 for t in sa if t in sb}
        c = calibrate_delta(diags, after, labels, truth)
        print(f"\ndelta calibration on {c['n_pairs']} paired observation(s): "
              f"{c['n_improved']} improved / {c['n_noop']} unchanged / "
              f"{c['n_regressed']} regressed")
        print(f"  {'thr':>6}{'kept improvements':>20}{'kept no-ops':>14}{'kept REGRESSIONS':>19}")
        for row in c["sweep"]:
            if row["threshold"] % 0.05 > 1e-9:
                continue
            print(f"  {row['threshold']:>6.2f}"
                  f"{row['kept_improvements']:>12}/{c['n_improved']:<7}"
                  f"{row['kept_noops']:>8}/{c['n_noop']:<5}"
                  f"{row['kept_regressions']:>12}/{c['n_regressed']}")

    if args.save:
        loc = Localizer.fit(diags, labels, delta_threshold=args.delta_threshold)
        loc.metadata.update({"cv": r})
        loc.save(args.save)
        print(f"\nmodel -> {args.save}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# --------------------------------------------------------------------------- #
# out-of-fold localizer
# --------------------------------------------------------------------------- #

class CVLocalizer:
    """K fold models plus a task -> fold map, so every task is scored by a model
    that never saw its label.

    `Localizer.fit` on a run's own labels and then evaluating on that same run is
    in-sample: the ranking it reports is optimistic and cannot be quoted. This
    wrapper is the honest version for reporting on the SAME split the labels came
    from. It is a reporting device, not a deployment artefact — a deployed loop
    carries one model fitted on a different split entirely.

        cv = CVLocalizer.fit(diags, labels)
        loc = cv.for_task(tid)      # a plain Localizer, held out for this task
    """

    def __init__(self, models: Dict[int, "Localizer"], fold_of: Dict[str, int],
                 fallback: "Localizer", delta_threshold: float = 0.05):
        self.models, self.fold_of = models, fold_of
        self.fallback, self.delta_threshold = fallback, delta_threshold

    def for_task(self, task_id: str) -> "Localizer":
        """A task the folds never saw (an unlabelled one) falls back to the model
        fitted on everything — correct for deployment, and flagged by `is_held_out`
        so a report can exclude it rather than quietly counting it as honest."""
        f = self.fold_of.get(task_id)
        return self.models[f] if f is not None else self.fallback

    def is_held_out(self, task_id: str) -> bool:
        return task_id in self.fold_of

    @classmethod
    def fit(cls, diags: Dict[str, dict], labels: Dict[str, str],
            n_splits: int = 5, seed: int = 0,
            delta_threshold: float = 0.05) -> "CVLocalizer":
        from sklearn.model_selection import StratifiedKFold
        ids = [t for t in labels if t in diags]
        y = np.array([labels[t] for t in ids])
        # Bounded by the smallest class, and reported rather than silently reduced:
        # `revise_relational_plan` has 12 members on nl2sql-bird dev.
        k = max(2, min(n_splits, min(Counter(y).values())))
        cv = StratifiedKFold(n_splits=k, shuffle=True, random_state=seed)
        models, fold_of = {}, {}
        for f, (tr, te) in enumerate(cv.split(np.zeros(len(ids)), y)):
            sub = {ids[i]: diags[ids[i]] for i in tr}
            models[f] = Localizer.fit(sub, {ids[i]: y[i] for i in tr},
                                      seed=seed, delta_threshold=delta_threshold)
            for i in te:
                fold_of[ids[i]] = f
        full = Localizer.fit(diags, labels, seed=seed,
                             delta_threshold=delta_threshold)
        return cls(models, fold_of, full, delta_threshold)

    def save(self, path: Path) -> None:
        import joblib
        joblib.dump({"models": {f: {"model": m.model, "columns": m.columns,
                                    "classes": m.classes,
                                    "delta_threshold": m.delta_threshold,
                                    "metadata": m.metadata}
                                for f, m in self.models.items()},
                     "fold_of": self.fold_of,
                     "fallback": {"model": self.fallback.model,
                                  "columns": self.fallback.columns,
                                  "classes": self.fallback.classes,
                                  "delta_threshold": self.fallback.delta_threshold,
                                  "metadata": self.fallback.metadata},
                     "delta_threshold": self.delta_threshold}, path)

    @classmethod
    def load(cls, path: Path) -> "CVLocalizer":
        import joblib
        d = joblib.load(path)
        mk = lambda b: Localizer(b["model"], b["columns"], b["classes"],   # noqa: E731
                                 b["delta_threshold"], b["metadata"])
        return cls({int(f): mk(b) for f, b in d["models"].items()},
                   d["fold_of"], mk(d["fallback"]), d["delta_threshold"])


class TwoHeadLocalizer:
    """A trigger head and a router head, trained on DIFFERENT data.

    One multiclass model has to serve two decisions that want opposite training
    sets, and measurably cannot serve both:

        head      question                     best data              measured
        trigger   is this output broken?       round-0 states only    AUC 0.711
                                               (ops >= 2)             vs 0.583 merged
        router    which stage, given broken?   round-0 + round-N      acc 0.676
                                               (no ops filter)        vs 0.486 round-0

    The reason is distributional, not incidental. Inference always starts from a
    round-0 state, so the trigger must be calibrated there; adding post-repair
    states moves its decision surface off the distribution it will see. The
    router has the opposite problem — upstream-first attribution hides pipeline
    faults behind schema-linking faults, so round-0 alone carries 15
    `revise_pipeline` examples against dev's 42, and a router trained on it falls
    BELOW the majority-class baseline (0.486 against 0.568) and collapses onto
    `revise_table` 64 times out of 74. The round-N states are where those hidden
    faults become observable.

    `p_ok` and `rank` keep the `Localizer` interface, so the loop is unchanged.
    """

    def __init__(self, trigger, router, trig_cols, route_cols, route_classes,
                 delta_threshold: float = 0.05, metadata: Optional[dict] = None):
        self.trigger, self.router = trigger, router
        self.trig_cols, self.route_cols = list(trig_cols), list(route_cols)
        self.route_classes = list(route_classes)
        self.delta_threshold = delta_threshold
        self.metadata = metadata or {}

    @staticmethod
    def _vec(diag: Dict[str, Any], cols: Sequence[str]) -> np.ndarray:
        s = pd.Series(flatten(diag), dtype="float64").reindex(list(cols))
        return s.fillna(0.0).to_numpy(dtype=float).reshape(1, -1)

    def p_ok(self, diag: Dict[str, Any]) -> float:
        return float(self.trigger.predict_proba(self._vec(diag, self.trig_cols))[0][0])

    def rank(self, diag: Dict[str, Any], exclude: Sequence[str] = (),
             link: Optional[Dict[str, Any]] = None,
             min_tables: int = MIN_SELECTED_TABLES) -> List[Tuple[str, float]]:
        ex = set(exclude)
        p_broken = 1.0 - self.p_ok(diag)
        r = self.router.predict_proba(self._vec(diag, self.route_cols))[0]
        acts = {c: float(v) * p_broken for c, v in zip(self.route_classes, r)}
        # Same certainty short-circuit as Localizer: schema linking's own prompt
        # states the selection may range from 2 upwards, so fewer than two tables
        # violates the stage's contract without reference to gold.
        if link is not None and "revise_table" not in ex:
            if len(link.get("selected_tables") or []) < min_tables:
                rest = [(a, v) for a, v in sorted(acts.items(), key=lambda kv: -kv[1])
                        if a not in ex | {"revise_table"}]
                return [("revise_table", 1.0)] + rest
        out = {OK: 1.0 - p_broken, **acts}
        return [(a, v) for a, v in sorted(out.items(), key=lambda kv: -kv[1])
                if a not in ex]

    def delta(self, before, after) -> float:
        return self.p_ok(after) - self.p_ok(before)

    def accept(self, before, after) -> bool:
        return self.delta(before, after) > self.delta_threshold

    def save(self, path: Path) -> None:
        import joblib
        joblib.dump({"__twohead__": True, "trigger": self.trigger,
                     "router": self.router, "trig_cols": self.trig_cols,
                     "route_cols": self.route_cols,
                     "route_classes": self.route_classes,
                     "delta_threshold": self.delta_threshold,
                     "metadata": self.metadata}, path)

    @classmethod
    def load(cls, path: Path) -> "TwoHeadLocalizer":
        import joblib
        d = joblib.load(path)
        if not d.get("__twohead__"):
            raise ValueError("not a TwoHeadLocalizer")
        return cls(d["trigger"], d["router"], d["trig_cols"], d["route_cols"],
                   d["route_classes"], d["delta_threshold"], d.get("metadata"))

    @classmethod
    def fit(cls, trig_diags: Dict[str, dict], trig_labels: Dict[str, str],
            route_diags: Dict[str, dict], route_labels: Dict[str, str],
            seed: int = 0, delta_threshold: float = 0.05) -> "TwoHeadLocalizer":
        from sklearn.ensemble import HistGradientBoostingClassifier
        mk = lambda: HistGradientBoostingClassifier(          # noqa: E731
            max_depth=3, max_iter=200, random_state=seed)

        ti = [t for t in trig_labels if t in trig_diags]
        TX = pd.DataFrame([flatten(trig_diags[t]) for t in ti]).fillna(0.0)
        # class 0 == OK, so predict_proba[:, 0] is p_ok
        ty = np.array([0 if trig_labels[t] == OK else 1 for t in ti])
        trig = mk().fit(TX.to_numpy(), ty)

        ri = [t for t in route_labels if t in route_diags and route_labels[t] != OK]
        RX = pd.DataFrame([flatten(route_diags[t]) for t in ri]).fillna(0.0)
        ry = np.array([route_labels[t] for t in ri])
        route = mk().fit(RX.to_numpy(), ry)
        return cls(trig, route, list(TX.columns), list(RX.columns),
                   list(route.classes_), delta_threshold,
                   {"n_trigger": len(ti), "n_router": len(ri),
                    "trigger_labels": dict(Counter(ty.tolist())),
                    "router_labels": dict(Counter(ry.tolist()))})
