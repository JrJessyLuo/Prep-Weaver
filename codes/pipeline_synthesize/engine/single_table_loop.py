#!/usr/bin/env python3
"""
single_table_loop.py
--------------------
Single-table "verify - repair - continue" loop (joinability ignored here), driven by

Strategy:
  each step:
    1. apply the deterministic repairs (auto_rename: transpose row_id->key, casing) —
    2. plan_next decides: complete/deferred_only -> stop, succeeded; needs_generation ->
    3. generate candidates (predictor top-3) and try them in order:
         - synthesize parameters (LLM, costs 1 call), or gold/param-free (free);
         - execute -> if verify passes, done; if coverage rose, accept the op and go
    Budget: at most 3 LLM calls, chain depth at most 3.

op_source:
  "gold"     : use the table's gold op (no LLM) — tests the mechanism and gives the
  "pipeline" : the predictor picks the op type, an LLM synthesizes the parameters

Metrics:
  subtable_accuracy = fraction of tables whose final structure satisfies the schema
  joinkey_accuracy  = every required PK / join-key column is present in the final
"""
from __future__ import annotations
import os
import argparse, json, sys
import weakref
from pathlib import Path
from collections import Counter

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
for p in (str(HERE), str(ROOT), str(ROOT / "dependency_modeling_react_joint")):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_param_synthesis as M
import test_single_ops_type as T
import test_schema_verify as V
from features import featurize
from coverage_policy import plan_next, apply_auto_rename
from table_specs import schema_coverage_check
from table_executor import observation_from_df
from infer import SingleOpInfer


def _cf(x): return str(x).strip().casefold()


_OBS_ARGS = (5, -1, 4000)
_OBS_CACHE: dict = {}


def _observation(df):
    """`observation_from_df` memoised per frame OBJECT.

    The observation depends on the frame alone, not the spec, and the same frame
    is profiled several times: once for the acceptance check's `coverage_score`,
    again inside `strong_score` when the terminals are sorted, and again for
    every spec it is scored against. Each call runs `value_counts` and `nunique`
    over every column — free on bird and spider, ruinous on beaver, where one
    call on a 500k x 30 frame costs 5.1s and py-spy caught a task spending 19
    minutes inside it. Caching removes repeated identical work and changes no
    result.

    NOT `df.attrs`. That was the first attempt and it is wrong: pandas propagates
    `attrs` to derived frames, so `df.rename(...)`, `df.drop(...)`, a slice, a
    merge and a melt ALL inherit the parent's entry — every score after the first
    operator would have been computed from the pre-operator profile. Verified on
    all eight of those operations before this code ever ran.

    The weakref both bounds the cache to live frames and makes the identity check
    exact: an id() alone is reused after collection and would hand one frame's
    profile to another.
    """
    key = id(df)
    hit = _OBS_CACHE.get(key)
    if hit is not None and hit[0]() is df:
        return hit[1]
    obs = observation_from_df(df, *_OBS_ARGS)
    try:
        _OBS_CACHE[key] = (weakref.ref(df, lambda _r, k=key: _OBS_CACHE.pop(k, None)), obs)
    except TypeError:      # not weak-referenceable; skip the cache rather than leak
        pass
    return obs


def coverage_score(df, spec):
    """How many required columns are already materialised (case-insensitive).

    Names only — this cannot tell "rename a fragment" from "actually concatenate the
    fragments": both produce the same target column name and score identically

    FALSIFIED (2026-08-13). Adding a "consumption" tie-break here
    (`n + 0.5 * fraction of the frame's columns that belong to the target schema`, so
    a rename that leaves an unconsumed LastName scores lower) treated the wrong cause:
    replayed under the gold plan, empty chains went 61/274 -> 62/274 — **the symptom it
    was meant to fix did not move** — while subtable_full fell 0.683 -> 0.658. Empty
    chains are not candidates losing a tie; the loop never enters the candidate loop at
    """
    cov = schema_coverage_check(_observation(df), spec, {})
    req = cov.get("target_columns", [])
    have = {_cf(c) for c in df.columns}
    return sum(1 for c in req if _cf(c) in have), len(req), cov


def joinkeys_present(df, spec):
    """Whether every required PK column is present (case-insensitive).

    Returns (all_present, keys, missing).
    """
    keys = [str(c) for c in (spec.get("primary_key") or [])]
    if not keys:
        return None, [], []          # no declared PK
    have = {_cf(c) for c in df.columns}
    missing = [k for k in keys if _cf(k) not in have]
    return (len(missing) == 0), keys, missing


class Loop:
    def __init__(self, op_source="gold", budget=3, max_depth=4, model="gpt-4o-2024-08-06"):
        self.op_source = op_source
        self.budget = budget
        self.max_depth = max_depth
        self.model = model
        self.infer = SingleOpInfer()

    def _candidates(self, df, spec, ctx):
        if self.op_source == "gold":
            g = M.gold_op_str_for_table(ctx["task"], ctx["logical_table"])
            return [M.op_str_to_step(g)["op"]] if g else []
        # pipeline: predictor top-3 (aligned against the full schema)
        out = self.infer.predict(df, ctx["schema_spec"], top_k=3,
                                 db_id=ctx["db_id"], source=ctx["source"])
        return out["candidates"][:3]

    def _synth(self, op, df, spec, missing, ctx, budget_left=2):
        """Returns (step dict, number of LLM calls consumed)."""
        if self.op_source == "gold":
            g = M.gold_op_str_for_table(ctx["task"], ctx["logical_table"])
            return (M.op_str_to_step(g) if g else {"op": op, "params": {}}), 0
        if op in M.PARAM_FREE_OPS:
            return {"op": op, "params": {}}, 0
        # Synthesize parameters with the LLM, using `missing` as focusing context; on an
        from schema_spec import expand_view_to_full, schema_to_sql
        fs, fp = expand_view_to_full(ctx["schema_spec"], ctx["db_id"], ctx["source"])
        x = featurize(df, fs, fp)
        nn = self.infer._nearest(x, op)
        ex = M.render_example_json(self.infer, op, nn)
        sql = schema_to_sql(fs, fp)
        base = M.build_prompt(op, ex, df, sql)
        if missing:
            base += f"\nThe result MUST materialize these still-missing target columns: {missing}."
        prompt = base
        tries = max(1, min(budget_left, 2))     # at most 2 per op (1 retry included)
        calls = 0
        last = {"op": op, "params": {}}
        for _ in range(tries):
            step = M.call_llm(prompt, self.model); calls += 1; last = step
            try:
                M.robust_execute(df.copy(), step)     # trial execution
                return step, calls
            except Exception as e:
                prompt = base + (f"\nYour previous params were {json.dumps(step.get('params', {}), ensure_ascii=False)[:300]} "
                                 f"and FAILED to execute: {type(e).__name__}: {e}. "
                                 f"Return corrected params (robust to NaN/non-str, only existing columns).")
        return last, calls

    def run_table(self, df0, spec, ctx):
        df = apply_auto_rename(df0, plan_next(df0, spec)["auto_rename"])
        chain, calls = [], 0
        for _ in range(self.max_depth):
            plan = plan_next(df, spec)
            df = apply_auto_rename(df, plan["auto_rename"])
            if plan["auto_rename"]:
                plan = plan_next(df, spec)
            if plan["status"] in ("complete", "deferred_only"):
                return {"df": df, "chain": chain, "calls": calls, "ok": True, "plan": plan}
            if calls >= self.budget:
                break
            score, _, _ = coverage_score(df, spec)
            cands = self._candidates(df, spec, ctx)
            advanced = False
            for op in cands:
                if calls >= self.budget:
                    break
                try:
                    step, nc = self._synth(op, df, spec, plan["blocking_missing"], ctx,
                                           budget_left=self.budget - calls)
                    calls += nc
                    executed = M.sanitize(M.robust_execute(df.copy(), step))
                    df2 = apply_auto_rename(executed, plan_next(executed, spec)["auto_rename"])
                except Exception as e:
                    import sys as _sys
                    print(f"[synth/exec fail] op={op}: {type(e).__name__}: {e}", file=_sys.stderr)
                    continue
                p2 = plan_next(df2, spec)
                if p2["status"] in ("complete", "deferred_only"):
                    return {"df": df2, "chain": chain + [op], "calls": calls, "ok": True, "plan": p2}
                ns, _, _ = coverage_score(df2, spec)
                # Enabling reshape op (Transpose/Stack/WideToLong): produces no column by
                # itself, but sets up the next Pivot. Accept it and go deeper whenever the
                ENABLERS = {"Transpose", "Stack", "WideToLong"}
                enabling = (op in ENABLERS and op not in chain
                            and df2.shape != df.shape and ns >= score)
                if ns > score or enabling:          # progress, or an enabling step -> go deeper
                    df, chain, advanced = df2, chain + [op], True
                    break
            if not advanced:
                break
        return {"df": df, "chain": chain, "calls": calls, "ok": False, "plan": plan_next(df, spec)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--op-source", choices=["gold", "pipeline"], default="gold")
    ap.add_argument("--budget", type=int, default=3)
    ap.add_argument("--max-depth", type=int, default=3)
    ap.add_argument("--model", default="gpt-4o-2024-08-06")
    args = ap.parse_args()

    cls = set(map(str, SingleOpInfer().clf.classes_)) | {"StandardizeDatetime"}
    AP = M.AUTOPREP
    btask = T.load_benchmark("nl2sql-bird", "dev", AP)
    specs = T.load_jsonl(ROOT / "dependency_modeling_react_joint/results/oracle_v1_group_a_specs.jsonl")
    cids = set(T.load_case_ids(ROOT / "pipeline_eval/cases_group_a_high_ops_union_structural.jsonl", "nl2sql-bird"))
    inst = V.load_full_spec_instances(specs, btask, AP / "nl2sql-bird/dev", {}, cids, cls)

    loop = Loop(op_source=args.op_source, budget=args.budget, max_depth=args.max_depth, model=args.model)
    sub_ok = jk_ok = jk_total = 0
    calls_hist = Counter(); depth_hist = Counter(); n = 0
    for it in inst:
        ctx = {"task": btask[it["task_id"]], "logical_table": it["logical_table"],
               "schema_spec": it["table_spec"].get("create_table_sql"),
               "db_id": it.get("db_id") or btask[it["task_id"]].get("db_id"),
               "source": "bird"}
        try:
            df0 = M.sanitize(pd.read_pickle(it["table_path"]))
        except Exception:
            continue
        r = loop.run_table(df0, it["table_spec"], ctx)
        n += 1
        sub_ok += int(r["ok"])
        calls_hist[r["calls"]] += 1; depth_hist[len(r["chain"])] += 1
        # join key = the full DB table PK (spec.primary_key is often empty), parsed from
        from schema_spec import expand_view_to_full
        _, full_pk = expand_view_to_full(ctx["schema_spec"], ctx["db_id"], ctx["source"])
        if full_pk:
            have = {_cf(c) for c in r["df"].columns}
            jk_total += 1; jk_ok += int(all(_cf(k) in have for k in full_pk))

    print(f"op-source={args.op_source}  instances={n}")
    print(f"subtable accuracy (structure satisfies schema): {sub_ok}/{n} = {sub_ok/n:.3f}")
    print(f"join-key accuracy (all PK columns present)    : {jk_ok}/{jk_total} = {jk_ok/jk_total:.3f}" if jk_total else "no PK specs")
    print(f"LLM call distribution: {dict(sorted(calls_hist.items()))}")
    print(f"chain depth distribution: {dict(sorted(depth_hist.items()))}")


if __name__ == "__main__":
    main()
