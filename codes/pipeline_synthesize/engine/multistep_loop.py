#!/usr/bin/env python3
"""
multistep_loop.py
-----------------
Standalone multi-step single-table synthesis (full_pipeline and single_table_loop are

- op prediction: model_multistep.joblib (includes a STOP class, trained on intermediate
- stopping = two signals: the prediction is STOP, OR verify(plan_next) says
- each step: predict the next op (top-k) -> stop on STOP or a complete verify; otherwise
        synthesize parameters (reusing test_param_synthesis) -> execute + deterministic

Usage:
    from multistep_loop import MultiStepLoop
    m = MultiStepLoop(op_source="pipeline")     # or "gold"
    out = m.run_table(df0, tspec, ctx)          # -> {"df","chain","calls","ok"}
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path
import numpy as np
import pandas as pd
import os
import joblib

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE,):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_param_synthesis as M
import test_single_ops_type as T
from features import featurize, sanitize, FEATURE_NAMES
from coverage_policy import plan_next, apply_auto_rename
from single_table_loop import coverage_score
from infer import SingleOpInfer

from engine_paths import POLICY_MODEL as _POLICY_MODEL
MODEL = os.environ.get("MULTISTEP_MODEL_PATH", str(_POLICY_MODEL))
STOP = "STOP"
ENABLERS = {"Transpose", "Stack", "WideToLong"}
PARAM_FREE = {"Transpose"}
AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
BENCH_DIR = AUTOP / "nl2sql-bird/dev"


def _cf(x):
    return re.sub(r"[^a-z0-9]", "", str(x).lower())


def _gold_value_hint_text(ctx, columns=None, limit=8):
    """Oracle-only value-domain hints for parameter-synthesis ablations.

    GOLD_VALUE_HINTS can be all, join-only, or missing. The hints are sampled
    from the gold prepared table and are intentionally non-deployable; they
    diagnose whether LLM parameter errors come from underspecified target values.
    """
    mode = (os.environ.get("GOLD_VALUE_HINTS") or "").strip().lower()
    if mode not in {"all", "join-only", "missing"}:
        return ""
    task = (ctx or {}).get("task") or {}
    lt = (ctx or {}).get("logical_table")
    if not task or not lt:
        return ""
    try:
        idx = int(str(lt).split("_")[1]) - 1
        df = sanitize(pd.read_pickle(BENCH_DIR / task["input_table"][idx]))
        for raw in task.get("dc_ops") or []:
            m = T.OP_WITH_TABLE_RE.search(str(raw))
            if m and m.group(2) == lt:
                try:
                    df = sanitize(M.robust_execute(df, M.op_str_to_step(str(raw))))
                except Exception:
                    pass
    except Exception:
        return ""

    table_spec = (ctx or {}).get("table_spec") or {}
    if mode == "all":
        wanted = list(table_spec.get("column_types") or [])
    elif mode == "join-only":
        wanted = list(table_spec.get("join_cols") or [])
        wanted += [
            jt.get("column") for jt in table_spec.get("join_targets", [])
            if isinstance(jt, dict) and jt.get("column")
        ]
    else:
        wanted = list(columns or [])
    if not wanted:
        wanted = list(df.columns)

    cmap = {_cf(c): c for c in df.columns}
    refs = {}
    for col in wanted:
        real = cmap.get(_cf(col))
        if real is None:
            continue
        vals, seen = [], set()
        for v in df[real].dropna().astype(str).tolist():
            s = re.sub(r"\s+", " ", v.strip())
            if not s or s.lower() in {"nan", "none", "<na>"} or s in seen:
                continue
            seen.add(s)
            vals.append(s)
            if len(vals) >= limit:
                break
        if vals:
            refs[str(col)] = vals
    if not refs:
        return ""
    return (
        "\n\nORACLE target value-domain references sampled from the gold prepared table "
        f"(GOLD_VALUE_HINTS={mode}; ablation only):\n"
        f"{json.dumps(refs, ensure_ascii=False, indent=2)}\n"
        "Use these samples to choose parameters whose produced target-column values "
        "resemble the intended domains. Do not merely create correctly named columns "
        "with unrelated values."
    )


class MultiStepLoop:
    def __init__(self, op_source="pipeline", budget=3, max_depth=5, 
                #  model = "gpt-5-2025-08-07",
                 model="gpt-4o-2024-08-06",
                 stop_thresh=0.5):
        self.op_source = op_source
        self.budget = budget
        self.max_depth = max_depth
        self.model = model
        self.stop_thresh = stop_thresh
        b = joblib.load(MODEL)
        self.model_bundle = b
        self.clf = b["clf"]; self.classes = np.array(b["classes"])
        self.base = SingleOpInfer()   # reused: nearest-neighbour example retrieval + parameter synthesis

    # ---- op ranking (including STOP) ----
    def _rank(self, df, schema, pk, history=(), initial_shape=None,
              previous_shape=None, previous_coverage=None):
        if self.model_bundle.get("feature_version") == "v2":
            from features_multistep_v2 import featurize_v2
            x = featurize_v2(df, schema, pk, history, initial_shape,
                             previous_shape, previous_coverage)
        else:
            x = featurize(df, schema, pk)
        proba = self.clf.predict_proba(x.reshape(1, -1))[0]
        order = np.argsort(-proba)
        return [(str(self.classes[o]), float(proba[o])) for o in order]

    # ---- parameter synthesis (reusing the existing mechanism: examples + hint + LLM + retry on error) ----
    def _synth(self, op, df, schema, pk, missing, ctx, budget_left, history=()):
        if self.op_source in {"gold", "policy-gold-params"}:
            matches = []
            for raw in ctx["task"].get("dc_ops") or []:
                text = str(raw)
                if f"table_name='{ctx['logical_table']}'" not in text and \
                   f'table_name="{ctx["logical_table"]}"' not in text:
                    continue
                try:
                    step = M.op_str_to_step(text)
                except Exception:
                    continue
                if step.get("op") == op:
                    matches.append(step)
            occurrence = list(history).count(op)
            if occurrence < len(matches):
                return matches[occurrence], 0
            return {"op": op, "params": {}}, 0
        if op in PARAM_FREE:
            return {"op": op, "params": {}}, 0
        from schema_spec import schema_to_sql
        sql = schema_to_sql(schema, pk)
        # SYNTH_CACHE: the LLM param-synthesis output is fully determined by
        # (op, current table content, still-missing target cols, target schema).
        # The beam re-synthesizes the SAME (op, table-state) many times (last run:
        # 104 of 173 terminal chains were duplicates), so a content-keyed memo skips
        # those repeat LLM calls with IDENTICAL inputs -> same params, result-neutral.
        cache = None
        ckey = None
        if os.environ.get("SYNTH_CACHE"):
            try:
                import pandas as _pd
                dfh = int(_pd.util.hash_pandas_object(df, index=False).sum())
            except Exception:
                dfh = (df.shape, tuple(map(str, df.columns)))
            ckey = (op, tuple(map(str, df.columns)), dfh,
                    tuple(sorted(missing or [])), tuple(sorted(schema)),
                    # A repair hint changes the prompt, so it must change the
                    # key: otherwise the repair run reads the first run's
                    # cached parameters and the two arms are identical.
                    hash(ctx.get("repair_hint") or ""))
            cache = getattr(self, "_synth_cache", None)
            if cache is None:
                cache = self._synth_cache = {}
            if ckey in cache:
                return cache[ckey], 0
        nn = self.base._nearest(featurize(df, schema, pk), op)
        ex = M.render_example_json(self.base, op, nn)
        base = M.build_prompt(op, ex, df, sql)
        if missing:
            base += f"\nThe result MUST materialize these still-missing target columns: {missing}."
        base += _gold_value_hint_text(ctx, missing)
        # Deployable repair evidence (unlike GOLD_VALUE_HINTS above, which is an
        # oracle ablation). Set by `actions/revise_pipeline.py` and empty on the
        # first pass, so the mainline prompt is unchanged.
        if ctx.get("repair_hint"):
            base += "\n\n" + str(ctx["repair_hint"])
        prompt = base; calls = 0; last = {"op": op, "params": {}}
        for attempt in range(max(1, min(budget_left, 2))):
            try:
                step = M.call_llm(prompt, self.model)
            except Exception as exc:
                raise RuntimeError(
                    f"parameter synthesis failed for {op} on attempt {attempt + 1}: "
                    f"{type(exc).__name__}: {exc}"
                ) from exc
            calls += 1; last = step
            try:
                M.robust_execute(df.copy(), step)
                if cache is not None:
                    cache[ckey] = step
                return step, calls
            except Exception as e:
                prompt = base + f"\nPrevious params FAILED: {type(e).__name__}: {e}. Return corrected params."
        if cache is not None:
            cache[ckey] = last
        return last, calls

    def run_table(self, df0, spec, ctx):
        df = apply_auto_rename(sanitize(df0), plan_next(sanitize(df0), spec)["auto_rename"])
        schema = spec.get("column_types") or {}
        pk = set(spec.get("primary_key") or [])
        chain, calls = [], 0
        initial_shape = df.shape
        previous_shape = df.shape
        previous_coverage = float(featurize(df, schema, pk)[FEATURE_NAMES.index("frac_present")])
        for _ in range(self.max_depth):
            plan = plan_next(df, spec)
            df = apply_auto_rename(df, plan["auto_rename"])
            if plan["auto_rename"]:
                plan = plan_next(df, spec)
            # Stop signal one: verify is complete
            if plan["status"] in ("complete", "deferred_only"):
                return {"df": df, "chain": chain, "calls": calls, "ok": True, "stop": "verify"}
            ranked = self._rank(df, schema, pk, chain, initial_shape,
                                previous_shape, previous_coverage)
            # Stop signal two: STOP predicted and no structurally missing column
            top_op, top_p = ranked[0]
            if top_op == STOP and top_p >= self.stop_thresh and not plan.get("blocking_missing"):
                return {"df": df, "chain": chain, "calls": calls, "ok": True, "stop": "predicted"}
            if calls >= self.budget:
                break
            score, _, _ = coverage_score(df, spec)
            cands = [op for op, _ in ranked if op != STOP][:3]
            advanced = False
            for op in cands:
                if calls >= self.budget:
                    break
                try:
                    step, nc = self._synth(op, df, schema, pk, plan["blocking_missing"],
                                           ctx, self.budget - calls, chain)
                    calls += nc
                    ex = sanitize(M.robust_execute(df.copy(), step))
                    df2 = apply_auto_rename(ex, plan_next(ex, spec)["auto_rename"])
                except Exception as e:
                    print(f"[multistep synth/exec fail] op={op}: {type(e).__name__}: {e}", file=sys.stderr)
                    continue
                p2 = plan_next(df2, spec)
                if p2["status"] in ("complete", "deferred_only"):
                    return {"df": df2, "chain": chain + [op], "calls": calls, "ok": True, "stop": "verify"}
                ns, _, _ = coverage_score(df2, spec)
                enabling = (op in ENABLERS and op not in chain and df2.shape != df.shape and ns >= score)
                if ns > score or enabling:
                    previous_shape = df.shape
                    previous_coverage = float(
                        featurize(df, schema, pk)[FEATURE_NAMES.index("frac_present")]
                    )
                    df, chain, advanced = df2, chain + [op], True
                    break
            if not advanced:
                break
        return {"df": df, "chain": chain, "calls": calls, "ok": False, "stop": "budget/stall"}
