#!/usr/bin/env python3
"""
bounded_explore_loop.py
-----------------------
Bounded LLM-exploration single-table synthesis loop (standalone; multistep_loop and

Idea, from components validated offline:
  - on most steps the predictor is confident at top-1 -> take it greedily (1 LLM call),
  - on the few "uncertain" steps (low top-1 probability, or a small top1-top2 gap) -> fork
  - at the end, a strong selector (coverage + value-semantic + PK) picks the best table
  - budget caps the total LLM calls (estimated ~1.76x greedy).

Spending LLM exploration only on uncertain steps sidesteps the dead end of "cheap rule
MultiStepLoop.run_table interface: run_table(df0, spec, ctx) -> {"df","chain","calls","ok"}
"""
from __future__ import annotations
import json
import os
import re
from pathlib import Path
import numpy as np
import pandas as pd

import test_param_synthesis as M
import test_single_ops_type as T
from features import FEATURE_NAMES, featurize, sanitize
from coverage_policy import plan_next, apply_auto_rename
from single_table_loop import coverage_score
from multistep_loop import MultiStepLoop, STOP, ENABLERS


def _cf(x): return re.sub(r"[^a-z0-9]", "", str(x).lower())


def _step_fingerprint(step, df_after):
    """Short, stable id for 'which params ran, and what frame came out'.

    Two parts because they answer different questions:
      params : did the LLM actually write different params?
      frame  : did those params land on a different table? (this is what
               layer-2's value-overlap join score can discriminate on)
    Frame hash falls back to (shape, columns) on unhashable content, matching
    the fallback in `_synth`'s cache key.
    """
    import hashlib
    try:
        praw = json.dumps(step.get("params") or {}, sort_keys=True, default=str)
    except Exception:
        praw = repr(step.get("params"))
    p = hashlib.md5(praw.encode("utf-8", "replace")).hexdigest()[:8]
    try:
        h = int(pd.util.hash_pandas_object(df_after, index=False).sum())
    except Exception:
        h = hash((df_after.shape, tuple(map(str, df_after.columns))))
    f = hashlib.md5(str(h).encode()).hexdigest()[:8]
    # The params themselves ride along: a fingerprint answers "is this the same
    # step?", but a consumer that wants to REPLAY or EXPORT the pipeline needs the
    # actual argument values. `fp` stays a plain string so existing readers of
    # `param_fp` are unaffected.
    return {"op": step.get("op"), "params": step.get("params") or {}, "fp": f"{p}/{f}"}


def _jsonish_value(v):
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except Exception:
        pass
    if isinstance(v, (str, int, float, bool)):
        return v
    return str(v)


def _table_sample_preview(df, max_rows=5, max_cols=12):
    """Small JSON-safe table preview for chain diagnostics."""
    if not os.environ.get("CHAIN_CAPTURE_PREVIEW"):
        return None
    try:
        small = df.iloc[:max_rows, :max_cols]
        return {
            "shape": [int(df.shape[0]), int(df.shape[1])],
            "columns": [str(c) for c in df.columns[:max_cols]],
            "truncated_columns": max(0, int(df.shape[1]) - max_cols),
            "rows": [
                {str(c): _jsonish_value(v) for c, v in row.items()}
                for row in small.to_dict(orient="records")
            ],
        }
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


JOIN_STRUCTURAL_OPS = {"Pivot", "SplitColumn", "Stack", "Explode", "Transpose", "WideToLong"}
AUTOP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
BENCH_DIR = AUTOP / "nl2sql-bird/dev"


def strong_score(df, spec):
    """Several signals: coverage + a valid PK + value-semantics (consistent, non-degenerate types)."""
    schema = spec.get("column_types") or {}; pk = set(spec.get("primary_key") or [])
    cov, tot, _ = coverage_score(df, spec); cover = cov / max(tot, 1)
    have = {_cf(c): c for c in df.columns}
    pkok = 0
    for k in pk:
        c = have.get(_cf(k))
        if c is not None:
            s = df[c]
            if s.notna().mean() > 0.95 and s.dropna().astype(str).nunique() / max(s.notna().sum(), 1) > 0.9:
                pkok += 1
    pk_valid = pkok / max(len(pk), 1) if pk else 1.0
    sem = n = 0
    for k, t in schema.items():
        c = have.get(_cf(k))
        if c is None:
            continue
        n += 1; s = df[c].dropna().astype(str)
        if len(s) == 0 or s.nunique() <= 1:
            continue
        num = pd.to_numeric(df[c], errors="coerce").notna().mean()
        want_num = any(x in str(t).lower() for x in ("int", "float", "num", "real", "double"))
        if (want_num and num > 0.8) or not want_num:
            sem += 1
    semantic = sem / max(n, 1)
    # CONSUMPTION — did the transformation USE UP the source columns, or just relabel one?
    #
    # Every term above is blind to the difference. On spider_4bd7fb66::table_2 the gold
    # step is Concatenate(['first_char','name_rest'] -> 'teacher_details'); what the loop
    # produced was a Rename of `first_char` to `teacher_details`, leaving `name_rest`
    # untouched beside it. The target column NAME is then present, so `cover` is
    # identical, `pk_valid` is identical, and `semantic` — which only asks whether a
    # numeric-typed column parses as numeric — is identical too. The two terminals tie
    # exactly, the sort at the end of `run_table` falls through to `len(chain)`, and a
    # one-step Rename is never longer than a one-step Concatenate. The table is reported
    # complete holding one character of each teacher's name (subtable_recall .667).
    #
    # `name_rest` surviving is the signal: it is not in the target schema, so its content
    # has not been used. This is the same 19-task pattern of "every column name right,
    # values wrong" that dominates the gold-plan failures.
    #
    # Weight 0.25, deliberately below the 1/n_cols that one covered column is worth on a
    # 4-column target — it must break ties, never outrank a genuine coverage gain. Note
    # leftover columns are NOT penalised by the metric itself (dropping undeclared columns
    # measured WORSE: .650 -> .642); this is evidence that the transform is unfinished,
    # not a judgement about the output.
    #
    # An earlier attempt put this in `coverage_score` instead. That function feeds
    # candidate ACCEPTANCE, not the terminal sort, and the change moved nothing
    # (empty chains 61 -> 62, .683 -> .658). Placement is the whole point.
    return cover + 0.5 * pk_valid + 0.5 * semantic


# REFUTED — "did the transform CONSUME its source columns" does not separate a real
# Concatenate from a Rename that merely relabels one fragment to the target name,
# because OUR Concatenate does not consume anything: it appends the merged column and
# leaves both sources in place. Measured on the gold-plan run:
#
#   spider_4b4dff2c::table_2, target [paper_id, author_id, affiliation_id]
#     Concatenate -> [author_id, affiliation_id, paper_prefix, paper_suffix, paper_id]  3/5 = .60
#     Rename      -> [author_id, affiliation_id, paper_id, paper_suffix]                3/4 = .75
#
# The tie-break would therefore have favoured Rename systematically — the opposite of
# its purpose. Replaying the stored terminals under the proposed key flipped 26 tables,
# 4 of them from a passing Concatenate to a Rename.
#
# WHAT THE INVESTIGATION DID ESTABLISH, and it is worse than a biased judge: these two
# terminals tie on EVERY key — coverage identical (both produce the target column NAME),
# pk_valid identical, `semantic` identical (it only checks that numeric-typed columns
# parse as numbers), chain length both 1. The winner is therefore decided by the order
# terminals happened to be appended. spider_4b4dff2c kept Concatenate and
# spider_53a941fc kept Rename on the same structure. The choice is a coin flip, and no
# name-level signal can make it otherwise — separating them requires reading the VALUES.


def _norm_values(values):
    out = set()
    for v in values or []:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            continue
        s = re.sub(r"\s+", " ", str(v).strip().lower())
        if s:
            out.add(s)
    return out


def _series_casefold(df, col):
    m = {_cf(c): c for c in df.columns}
    c = m.get(_cf(col))
    if c is None:
        return None
    s = df[c]
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    return s


def _gold_value_hint_text(ctx, columns=None, limit=8):
    """Oracle ablation only: expose sampled values from the gold prepared table.

    Enabled by GOLD_VALUE_HINTS={all,join-only,missing}. This is intentionally
    non-deployable; it diagnoses whether parameter synthesis fails because the
    LLM lacks target value-domain grounding.
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
        for op in task.get("dc_ops") or []:
            m = T.OP_WITH_TABLE_RE.search(str(op))
            if m and m.group(2) == lt:
                try:
                    df = sanitize(M.robust_execute(df, M.op_str_to_step(str(op))))
                except Exception:
                    pass
    except Exception:
        return ""

    wanted = list(columns or [])
    if mode == "join-only":
        wanted = [
            c for c in (ctx.get("table_spec") or {}).get("join_cols", [])
            if str(c).strip()
        ] or [
            jt.get("column") for jt in (ctx.get("table_spec") or {}).get("join_targets", [])
            if jt.get("column")
        ]
    elif mode == "all":
        wanted = list((ctx.get("table_spec") or {}).get("column_types") or [])
    if not wanted:
        wanted = list(df.columns)

    cmap = {_cf(c): c for c in df.columns}
    refs = {}
    for col in wanted:
        real = cmap.get(_cf(col))
        if real is None:
            continue
        vals = []
        seen = set()
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
        f"(GOLD_VALUE_HINTS={mode}; for ablation only):\n"
        f"{json.dumps(refs, ensure_ascii=False, indent=2)}\n"
        "Use these samples to choose operation parameters whose produced target-column "
        "values resemble the intended domains. Do not merely create a correctly named "
        "column with unrelated values."
    )


def _kind_counts(values):
    vals = [str(v).strip() for v in (values or []) if str(v).strip()]
    if not vals:
        return {"empty": 1.0}
    n = len(vals)
    def frac(pred):
        return sum(1 for v in vals if pred(v)) / max(n, 1)
    return {
        "uuid": frac(lambda v: bool(re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", v))),
        "record_id": frac(lambda v: bool(re.fullmatch(r"rec[a-zA-Z0-9]{8,}", v))),
        "numeric": frac(lambda v: bool(re.fullmatch(r"-?\d+(?:\.\d+)?", v))),
        "list_like": frac(lambda v: ("," in v or ";" in v or "|" in v) and len(v) < 300),
        "header_like": frac(lambda v: bool(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_ ]{0,40}", v)) and ("_" in v or v.lower() in {
            "id", "name", "date", "status", "cost", "amount", "description", "category", "type", "value"
        })),
    }


def _domain_compat(this_vals, other_vals):
    this = _norm_values(this_vals)
    other = _norm_values(other_vals)
    if not other:
        return None
    if not this:
        return 0.0
    inter = len(this & other)
    exact = max(
        inter / max(len(this), 1),
        inter / max(len(other), 1),
        inter / max(min(len(this), len(other)), 1),
    )
    if exact >= 0.5:
        return 1.0
    tp = _kind_counts(this)
    op = _kind_counts(other)
    kind_match = max(
        min(tp.get("uuid", 0.0), op.get("uuid", 0.0)),
        min(tp.get("record_id", 0.0), op.get("record_id", 0.0)),
        min(tp.get("numeric", 0.0), op.get("numeric", 0.0)),
    )
    penalty = 0.0
    if tp.get("list_like", 0.0) > 0.2 and op.get("list_like", 0.0) < 0.05:
        penalty += 0.35
    if tp.get("header_like", 0.0) > 0.25 and op.get("header_like", 0.0) < 0.10:
        penalty += 0.30
    return max(0.0, exact * 0.75 + kind_match * 0.35 - penalty)


def join_value_plausibility_score(df, spec):
    scores = []
    for jt in spec.get("join_targets") or []:
        other = jt.get("other_values") or []
        if not other:
            continue
        s = _series_casefold(df, jt.get("column"))
        if s is None:
            scores.append(0.0)
            continue
        vals = s.dropna().astype(str).drop_duplicates().head(1000).tolist()
        score = _domain_compat(vals, other)
        if score is not None:
            scores.append(score)
    return max(scores) if scores else None


def _join_columns(spec):
    return {_cf(jt.get("column")) for jt in (spec.get("join_targets") or []) if jt.get("column")}


def _step_columns(step):
    params = step.get("params") or {}
    cols = []
    for k in ("column", "column_name", "source_column", "id_var", "j", "index", "columns"):
        v = params.get(k)
        if isinstance(v, str):
            cols.append(v)
        elif isinstance(v, list):
            cols.extend(str(x) for x in v)
        elif isinstance(v, dict):
            cols.extend(str(x) for x in v.keys())
            cols.extend(str(x) for x in v.values())
    for k in ("target_columns", "value_vars", "id_vars"):
        v = params.get(k)
        if isinstance(v, list):
            cols.extend(str(x) for x in v)
    return {_cf(c) for c in cols if c is not None}


def is_join_critical_step(step, before_df, after_df, spec):
    join_cols = _join_columns(spec)
    if not join_cols:
        return False
    if step.get("op") in JOIN_STRUCTURAL_OPS:
        before_cols = {_cf(c) for c in before_df.columns}
        after_cols = {_cf(c) for c in after_df.columns}
        if join_cols & (before_cols | after_cols | _step_columns(step)):
            return True
        if before_df.shape != after_df.shape:
            return True
    return bool(join_cols & _step_columns(step))


def join_materialization_score(df, spec):
    scores = []
    for jt in spec.get("join_targets") or []:
        other = _norm_values(jt.get("other_values") or [])
        if not other:
            continue
        s = _series_casefold(df, jt.get("column"))
        if s is None:
            scores.append(0.0)
            continue
        vals = _norm_values(s.dropna().astype(str).drop_duplicates().head(1000).tolist())
        if not vals:
            scores.append(0.0)
            continue
        inter = len(vals & other)
        scores.append(max(
            inter / max(len(vals), 1),
            inter / max(len(other), 1),
            inter / max(min(len(vals), len(other)), 1),
        ))
    return max(scores) if scores else None


def join_target_materialization_score(df, jt):
    other = _norm_values(jt.get("other_values") or [])
    if not other:
        return None
    s = _series_casefold(df, jt.get("column"))
    if s is None:
        return 0.0
    vals = _norm_values(s.dropna().astype(str).drop_duplicates().head(1000).tolist())
    if not vals:
        return 0.0
    inter = len(vals & other)
    return max(
        inter / max(len(vals), 1),
        inter / max(len(other), 1),
        inter / max(min(len(vals), len(other)), 1),
    )


def join_target_plausibility_score(df, jt):
    s = _series_casefold(df, jt.get("column"))
    if s is None:
        return 0.0
    return _domain_compat(
        s.dropna().astype(str).drop_duplicates().head(1000).tolist(),
        jt.get("other_values") or [],
    )


def _column_domain_compat(df, col, other_values):
    s = _series_casefold(df, col)
    if s is None:
        return 0.0
    score = _domain_compat(
        s.dropna().astype(str).drop_duplicates().head(1000).tolist(),
        other_values or [],
    )
    return 0.0 if score is None else float(score)


def join_evidence_recoverability_score(df, jt):
    """Gold-free-ish proxy: can this table still expose the join value domain?

    This intentionally scans all current columns, not only the final join column.
    The goal is evidence preservation: before the key is materialized, the future
    key may still be hidden in value cells, metric columns, packed fields, etc.
    """
    other = jt.get("other_values") or []
    if not other:
        return None
    best = _column_domain_compat(df, jt.get("column"), other)
    for c in df.columns:
        best = max(best, _column_domain_compat(df, c, other))
    return best


def _join_col_exists(df, col):
    return _series_casefold(df, col) is not None


def join_evidence_preservation_check(before_df, after_df, step, spec):
    """Reject only clear evidence-destroying moves.

    This is deliberately not a join reward. It does not require every intermediate
    table to be joinable; it only blocks candidates that make previously
    recoverable join evidence disappear.
    """
    if not os.environ.get("JOIN_EVIDENCE_PRESERVATION"):
        return True, None
    targets = spec.get("join_targets") or []
    if not targets:
        return True, None
    op = step.get("op")
    touched = _step_columns(step)
    dangerous = op in JOIN_STRUCTURAL_OPS or op in {"FilterRows", "SelectColumns", "DropColumns", "Aggregate"}
    if not dangerous and not (_join_columns(spec) & touched):
        return True, None
    for jt in targets:
        col = jt.get("column")
        before_has_key = _join_col_exists(before_df, col)
        after_has_key = _join_col_exists(after_df, col)
        if before_has_key and not after_has_key:
            return False, f"join_col_removed:{col}"
        before_rec = join_evidence_recoverability_score(before_df, jt)
        after_rec = join_evidence_recoverability_score(after_df, jt)
        if before_rec is None or after_rec is None:
            continue
        # Only block obvious destruction.  A small dip can be a valid structural
        # intermediate; a large drop from recoverable to unrecoverable is the bug.
        if before_rec >= 0.35 and after_rec < max(0.10, before_rec - 0.30):
            return False, (
                f"join_evidence_dropped:{col}:"
                f"{before_rec:.3f}->{after_rec:.3f}"
            )
    return True, None


def active_join_target(df, spec):
    worst = None
    for jt in spec.get("join_targets") or []:
        if not jt.get("column") or not jt.get("other_values"):
            continue
        overlap = join_target_materialization_score(df, jt)
        plaus = join_target_plausibility_score(df, jt)
        overlap = 0.0 if overlap is None else float(overlap)
        plaus = 0.0 if plaus is None else float(plaus)
        key = (overlap, plaus)
        if worst is None or key < worst[0]:
            worst = (key, jt, overlap, plaus)
    if worst is None:
        return None, None, None
    _, jt, overlap, plaus = worst
    return jt, overlap, plaus


def spec_for_active_join(spec, active):
    if not active:
        return spec
    return {**spec, "join_targets": [active]}


def _sample_norm_values(values, limit=24):
    vals = sorted(_norm_values(values or []))
    return vals[:limit]


def compact_join_target_for_prompt(jt, df=None, value_limit=24):
    if not jt:
        return None
    out = {
        "column": jt.get("column"),
        "other_table": jt.get("other_table"),
        "other_column": jt.get("other_column"),
        "counterpart_value_count": len(_norm_values(jt.get("other_values") or [])),
        "counterpart_sample_values": _sample_norm_values(jt.get("other_values") or [], value_limit),
    }
    if df is not None:
        s = _series_casefold(df, jt.get("column"))
        out["current_key_sample_values"] = (
            _sample_norm_values(s.dropna().astype(str).drop_duplicates().head(200).tolist(), value_limit)
            if s is not None else []
        )
    return out


def join_aware_score(df, spec, enabled):
    base = strong_score(df, spec)
    js = join_materialization_score(df, spec) if enabled else None
    ps = join_value_plausibility_score(df, spec) if enabled and os.environ.get("JOIN_CRITICAL_VALUE_GATE") else None
    score = base if js is None else base + 1.5 * js
    return score if ps is None else score + 0.5 * ps


def _join_context_lines(df, spec):
    lines = []
    for jt in spec.get("join_targets") or []:
        lines.append(compact_join_target_for_prompt(jt, df))
    return lines


def _extract_json_objects(text):
    if not isinstance(text, str):
        return []
    blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, re.S | re.I)
    search_space = blocks if blocks else [text]
    out = []
    dec = json.JSONDecoder()
    for chunk in search_space:
        i = 0
        while i < len(chunk):
            m = re.search(r"[\[{]", chunk[i:])
            if not m:
                break
            start = i + m.start()
            try:
                obj, end = dec.raw_decode(chunk[start:])
                out.append(obj)
                i = start + end
            except Exception:
                i = start + 1
    return out


def _normalize_candidate_steps(raw, fixed_op):
    objs = _extract_json_objects(raw) if isinstance(raw, str) else [raw]
    steps = []
    for obj in objs:
        candidates = obj
        if isinstance(obj, dict):
            if isinstance(obj.get("candidates"), list):
                candidates = obj["candidates"]
            elif isinstance(obj.get("steps"), list):
                candidates = obj["steps"]
            else:
                candidates = [obj]
        if not isinstance(candidates, list):
            continue
        for cand in candidates:
            if not isinstance(cand, dict):
                continue
            step = cand.get("step") if isinstance(cand.get("step"), dict) else cand
            params = step.get("params") if isinstance(step.get("params"), dict) else {}
            steps.append({"op": fixed_op, "params": params})
    seen = set(); uniq = []
    for step in steps:
        key = json.dumps(step, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key); uniq.append(step)
    return uniq


class BoundedExploreLoop(MultiStepLoop):
    def __init__(self, *a, uncertain_prob=0.5, uncertain_gap=0.15, beam_width=3,
                 cand_per_branch=3, max_terminal_candidates=None, budget=8, **kw):
        kw.setdefault("budget", budget)
        super().__init__(*a, **kw)
        self.uncertain_prob = uncertain_prob
        self.uncertain_gap = uncertain_gap
        self.beam_width = beam_width
        self.cand_per_branch = cand_per_branch
        self.max_terminal_candidates = max_terminal_candidates

    def _join_aware_param_candidates(self, op, df, schema, pk, missing, ctx, budget_left, history=()):
        if budget_left <= 0:
            return [], 0
        if op in M.PARAM_FREE_OPS:
            return [{"op": op, "params": {}}], 0
        from schema_spec import schema_to_sql
        from build_training_data import table_preview
        sql = schema_to_sql(schema, pk)
        nn = self.base._nearest(featurize(df, schema, pk), op)
        ex = M.render_example_json(self.base, op, nn)
        join_ctx = _join_context_lines(df, ctx.get("table_spec") or {})
        active = compact_join_target_for_prompt(
            ctx.get("active_join_target"), df
        ) or (join_ctx[0] if len(join_ctx) == 1 else None)
        prompt = f"""You are generating parameter candidates for exactly one data-preparation operation.
The operation TYPE is fixed: {op}. Do not choose another operation.

Goal:
Materialize the target relation while making the active join edge equi-joinable.
The generated parameters must serve both the target schema and the active join-key value domain.

Retrieved solved example:
{ex}

Current table columns:
{json.dumps([str(c) for c in df.columns][:60], ensure_ascii=False)}

Current table preview:
```text
{table_preview(df)}
```

Target relation schema:
```sql
{sql}
```

Still-missing target columns:
{json.dumps(list(missing or []), ensure_ascii=False)}
{_gold_value_hint_text(ctx, missing)}

Joinability targets:
{json.dumps(join_ctx, ensure_ascii=False, indent=2)}

Active join target to optimize in this step:
{json.dumps(active, ensure_ascii=False, indent=2)}

Return JSON only in this format:
{{"candidates":[{{"op":"{op}","params":{{...}}}}, {{"op":"{op}","params":{{...}}}}]}}

Rules:
- Return 3 different candidate parameterizations when possible.
- The op field in every candidate must be exactly "{op}".
- Use only source columns visible in the current table.
- Use target-schema names for newly created or renamed required columns.
- Prefer candidates that expose or repair the active join key and make its values overlap counterpart samples.
- Do not optimize unrelated columns when the active join key is missing or has low overlap.
- For SplitColumn/Concatenate/StandardizeString/StandardizeDatetime, include a robust Python func string.
- Do not add prose outside JSON.
"""
        try:
            from prep_utils import llm_generate_setup, timed_llm_generate
            resp, _ = timed_llm_generate(llm_generate_setup, prompt, model=self.model, json_format=True)
            txt = resp.get("text", "") if isinstance(resp, dict) else str(resp)
            return _normalize_candidate_steps(txt, op), 1
        except Exception as exc:
            raise RuntimeError(f"join-aware parameter candidates failed for {op}: {type(exc).__name__}: {exc}") from exc

    def _synth_candidates(self, op, df, schema, pk, missing, ctx, budget_left, history=()):
        join_aware = bool(os.environ.get("JOIN_AWARE_MATERIALIZATION")) and bool((ctx.get("table_spec") or {}).get("join_targets"))
        candidate_mode = bool(os.environ.get("JOIN_AWARE_PARAM_CANDIDATES"))
        if join_aware and candidate_mode and op in JOIN_STRUCTURAL_OPS | {"Rename", "StandardizeString", "CastType", "Concatenate"}:
            return self._join_aware_param_candidates(op, df, schema, pk, missing, ctx, budget_left, history)
        step, calls = self._synth(op, df, schema, pk, missing, ctx, budget_left, history)
        return [step], calls

    def run_table(self, df0, spec, ctx):
        ctx = {**(ctx or {}), "table_spec": spec}
        trace_enabled = bool(os.environ.get("POLICY_TRACE"))
        trace_id = f"{(ctx.get('task') or {}).get('task_id')}::{ctx.get('logical_table')}"
        join_aware = bool(os.environ.get("JOIN_AWARE_MATERIALIZATION")) and bool(spec.get("join_targets"))
        edge_conditioned = join_aware and bool(os.environ.get("EDGE_CONDITIONED_MATERIALIZATION"))
        inject_structural = (
            bool(os.environ.get("JOIN_AWARE_STRUCTURAL_INJECTION")) or
            self.op_source == "policy-gold-params" or
            edge_conditioned
        )
        def trace(event, **payload):
            if trace_enabled:
                print("[policy-trace] " + json.dumps({"id": trace_id, "event": event, **payload},
                                                       ensure_ascii=False), flush=True)
        schema = spec.get("column_types") or {}; pk = set(spec.get("primary_key") or [])
        df0 = apply_auto_rename(sanitize(df0), plan_next(sanitize(df0), spec)["auto_rename"])
        # beam item: (df, chain, calls, prev_shape, prev_cov, pfp, previews)
        # `pfp` mirrors `chain` one-for-one: chain[i] is the op NAME, pfp[i] is a
        # fingerprint of the params that op ran with plus the frame it produced.
        # Needed because chains.json only ever stored op names, so two terminals
        # reading `["Rename","SplitColumn"]` were indistinguishable offline — we
        # could not tell a genuine param variant (useful: layer-2 breaks layer-1
        # ties by value overlap, so different params = different join score) from
        # a true duplicate (wasted budget).
        cov0 = float(featurize(df0, schema, pk)[FEATURE_NAMES.index("frac_present")])
        beams = [(df0, [], 0, df0.shape, cov0, [], [])]
        terminals = []      # (df, chain, calls, pfp, previews)
        total_calls = 0
        candidate_errors = []
        for depth in range(self.max_depth):
            nxt = []
            for (df, chain, calls, previous_shape, previous_coverage, pfp, previews) in beams:
                plan = plan_next(df, spec); df = apply_auto_rename(df, plan["auto_rename"])
                if plan["auto_rename"]:
                    plan = plan_next(df, spec)
                ranked = self._rank(df, schema, pk, chain, df0.shape,
                                    previous_shape, previous_coverage)
                top_op, top_p = ranked[0]
                active_jt = active_score = active_plaus = None
                active_spec = spec
                if edge_conditioned:
                    active_jt, active_score, active_plaus = active_join_target(df, spec)
                    active_spec = spec_for_active_join(spec, active_jt)
                join_score = (
                    active_score if edge_conditioned and active_score is not None
                    else join_materialization_score(df, spec) if join_aware else None
                )
                join_plaus = (
                    active_plaus if edge_conditioned and active_plaus is not None
                    else join_value_plausibility_score(df, spec)
                    if join_aware and os.environ.get("JOIN_CRITICAL_VALUE_GATE") else None
                )
                trace("rank", depth=depth, chain=chain, shape=list(df.shape),
                      blocking=plan.get("blocking_missing"), status=plan.get("status"),
                      join_score=join_score, join_plausibility=join_plaus,
                      active_join_target=compact_join_target_for_prompt(active_jt, df),
                      ranked=[[op, round(prob, 6)] for op, prob in ranked[:5]])
                # Stop: verify says complete, or the prediction is STOP
                join_blocked = join_aware and join_score is not None and join_score < 0.5
                if join_aware and os.environ.get("JOIN_CRITICAL_VALUE_GATE") and join_plaus is not None:
                    join_blocked = join_blocked or join_plaus < 0.35
                if (plan["status"] in ("complete", "deferred_only") and not join_blocked) or \
                   (top_op == STOP and top_p >= self.stop_thresh and not plan.get("blocking_missing") and not join_blocked):
                    terminals.append((df, chain, calls, pfp, previews)); continue
                if total_calls >= self.budget:
                    terminals.append((df, chain, calls, pfp, previews)); continue
                # Confidence check: confident -> top-1 only; uncertain -> fork top-K
                nonstop = [(o, p) for o, p in ranked if o != STOP]
                gap = nonstop[0][1] - nonstop[1][1] if len(nonstop) > 1 else 1.0
                confident = (nonstop[0][1] >= self.uncertain_prob and gap >= self.uncertain_gap)
                structural_gate = bool(os.environ.get("STRUCTURAL_ENABLING_GATE"))
                candidate_limit = max(self.cand_per_branch, 5) if (join_blocked or structural_gate) else self.cand_per_branch
                candidate_limit = max(candidate_limit, 4) if self.op_source == "policy-gold-params" else candidate_limit
                # WIDEN_JOINKEY_CANDS: on tables that carry a join key, the policy model
                # systematically ranks the gold structural/Rename finishing op at 4th, and
                # a confident (but wrong) top-1 collapses cands to a single op — so the gold
                # sequence leaves the candidate set and never reaches a terminal. On these
                # tables widen to top-5 and DO NOT collapse to top-1, so gold survives to the
                # terminal set for the reranker to pick. (Verified offline: this puts the gold
                # next-op in cands at every step for all 9 subtable-OK/join-key-wrong cases.)
                # `join_cols` is non-empty for every table that participates in any edge, which
                # on this benchmark is ALL of them (measured: 91/91), so the original condition
                # was constant-true and the `confident -> top-1` branch below never ran — every
                # table branched 5-wide at every depth. Widen only while a declared join key is
                # still MISSING from the frame: once it is materialized, the reason for widening
                # (keeping the gold finishing op alive) no longer applies, and top-1 can resume.
                _jk_cols = {_cf(c) for c in (spec.get("join_cols") or [])}
                _jk_cols |= {_cf(jt.get("column")) for jt in (spec.get("join_targets") or [])
                             if jt.get("column")}
                jk_table = bool(_jk_cols - {_cf(c) for c in df.columns})
                if os.environ.get("WIDEN_JOINKEY_CANDS") and jk_table:
                    candidate_limit = max(candidate_limit, 5)
                    cands = [o for o, _ in nonstop[:candidate_limit]]
                else:
                    cands = [nonstop[0][0]] if confident else [o for o, _ in nonstop[:candidate_limit]]
                if structural_gate:
                    structural_ops = [o for o, _ in nonstop[:5] if o in JOIN_STRUCTURAL_OPS]
                    cands = list(dict.fromkeys(cands + structural_ops))
                if os.environ.get("JOIN_RISK_TOP5") and spec.get("join_targets"):
                    # Lightweight exploration: if a join-relevant table's correct
                    # operation is a structural reshape at rank 4/5, the default
                    # top-3 branch never executes it. Add only structural ops from
                    # top-5; do not add join reward or alter stopping.
                    risk_ops = [o for o, _ in nonstop[:5] if o in JOIN_STRUCTURAL_OPS]
                    cands = list(dict.fromkeys(cands + risk_ops))
                if join_blocked and inject_structural:
                    cands = list(dict.fromkeys(cands + [op for op in JOIN_STRUCTURAL_OPS if op not in cands]))
                sc, _, _ = coverage_score(df, spec)
                jsc = (
                    join_target_materialization_score(df, active_jt)
                    if edge_conditioned and active_jt else
                    join_materialization_score(df, spec) if join_aware else None
                )
                for op in cands:
                    if total_calls >= self.budget:
                        break
                    try:
                        step_ctx = ctx
                        if edge_conditioned and active_jt:
                            step_ctx = {
                                **ctx,
                                "table_spec": active_spec,
                                "active_join_target": compact_join_target_for_prompt(active_jt, df),
                            }
                        steps, nc = self._synth_candidates(op, df, schema, pk, plan["blocking_missing"],
                                                           step_ctx, self.budget - total_calls, chain)
                        total_calls += nc; calls_i = calls + nc
                    except Exception as exc:
                        error = f"synth {op}: {type(exc).__name__}: {exc}"
                        candidate_errors.append(error)
                        trace("candidate_error", depth=depth, chain=chain, op=op,
                              stage="synth", error=error)
                        continue
                    op_results = []
                    for step_idx, step in enumerate(steps or [{"op": op, "params": {}}]):
                        try:
                            ex = sanitize(M.robust_execute(df.copy(), step))
                            df2 = apply_auto_rename(ex, plan_next(ex, spec)["auto_rename"])
                        except Exception as exc:
                            error = f"execute {op}: {type(exc).__name__}: {exc}"
                            candidate_errors.append(error)
                            trace("candidate_error", depth=depth, chain=chain, op=op,
                                  stage="execute", step_idx=step_idx, error=error)
                            continue
                        ns, _, _ = coverage_score(df2, spec)
                        njsc = (
                            join_target_materialization_score(df2, active_jt)
                            if edge_conditioned and active_jt else
                            join_materialization_score(df2, spec) if join_aware else None
                        )
                        nplaus = (
                            join_target_plausibility_score(df2, active_jt)
                            if edge_conditioned and active_jt else
                            join_value_plausibility_score(df2, spec)
                            if join_aware and os.environ.get("JOIN_CRITICAL_VALUE_GATE") else None
                        )
                        state_changed = (
                            df2.shape != df.shape or
                            [str(c) for c in df2.columns] != [str(c) for c in df.columns]
                        )
                        join_critical = (
                            join_aware and os.environ.get("JOIN_CRITICAL_VALUE_GATE") and
                            is_join_critical_step(step, df, df2, active_spec)
                        )
                        evidence_ok, evidence_reason = join_evidence_preservation_check(
                            df, df2, step, spec
                        )
                        post_plan = plan_next(df2, spec)
                        incomplete_after = post_plan.get("status") not in ("complete", "deferred_only")
                        structural_enabling = (
                            structural_gate and op in JOIN_STRUCTURAL_OPS and
                            state_changed and ns >= sc and incomplete_after
                        )
                        enabling = (
                            (op in ENABLERS and op not in chain and state_changed and ns >= sc) or
                            structural_enabling
                        )
                        join_improves = (
                            join_aware and jsc is not None and njsc is not None and
                            njsc > jsc + 1e-9 and ns >= sc
                        )
                        join_plausible = True
                        if join_critical and nplaus is not None:
                            before_plaus = (
                                join_target_plausibility_score(df, active_jt)
                                if edge_conditioned and active_jt else
                                join_value_plausibility_score(df, spec)
                            )
                            before_plaus = 0.0 if before_plaus is None else before_plaus
                            join_plausible = nplaus >= 0.20 or nplaus >= before_plaus - 1e-9
                        accepted = bool(ns > sc or enabling or join_improves)
                        accepted = accepted and join_plausible and evidence_ok
                        trace("candidate", depth=depth, chain=chain, op=op, step_idx=step_idx,
                              before_shape=list(df.shape), after_shape=list(df2.shape),
                              score_before=sc, score_after=ns, join_before=jsc,
                              join_after=njsc, join_plausibility=nplaus,
                              join_critical=join_critical,
                              join_plausible=join_plausible,
                              join_evidence_ok=evidence_ok,
                              join_evidence_reason=evidence_reason,
                              enabling=enabling, structural_enabling=structural_enabling,
                              incomplete_after=incomplete_after,
                              join_improves=join_improves,
                              accepted=accepted)
                        if accepted:
                            preview = None
                            if os.environ.get("CHAIN_CAPTURE_PREVIEW"):
                                preview = {
                                    "op": op,
                                    "step_idx": step_idx,
                                    "step": step,
                                    "score_before": sc,
                                    "score_after": ns,
                                    "join_before": jsc,
                                    "join_after": njsc,
                                    "before": _table_sample_preview(df),
                                    "after": _table_sample_preview(df2),
                                }
                            op_results.append((df2, step_idx, ns, njsc, enabling, join_improves, step, preview))
                    if op_results:
                        def _param_key(item):
                            cand_df, step_idx, ns, njsc, enabling, join_improves, _step, _preview = item
                            js = -1.0 if njsc is None else float(njsc)
                            return (-join_aware_score(cand_df, spec, join_aware), -ns, -js, step_idx)
                        op_results.sort(key=_param_key)
                        best_df, best_step_idx, best_ns, best_jsc, _, _, best_step, best_preview = op_results[0]
                        prev_cov = float(
                            featurize(df, schema, pk)[FEATURE_NAMES.index("frac_present")]
                        )
                        trace("candidate_selected_param", depth=depth, chain=chain, op=op,
                              step_idx=best_step_idx, score_after=best_ns, join_after=best_jsc,
                              tried=len(op_results))
                        nxt.append((best_df, chain + [op], calls_i, df.shape, prev_cov,
                                    pfp + [_step_fingerprint(best_step, best_df)],
                                    previews + ([best_preview] if best_preview else [])))
            if not nxt:
                break
            # Prune to beam_width by the strong selector score (coverage + semantics + PK)
            nxt.sort(key=lambda t: -join_aware_score(t[0], spec, join_aware))
            beams = nxt[:self.beam_width]
            # BEAM-PRUNE TRACE: which chains survived to next depth vs which were dropped,
            # with their ranking score — so an offline diff can see if the GOLD-prefix chain
            # was generated but pruned here (beam too narrow / mis-scored) vs never generated.
            trace("beam_prune", depth=depth, beam_width=self.beam_width,
                  kept=[{"chain": t[1], "score": round(join_aware_score(t[0], spec, join_aware), 4)}
                        for t in beams],
                  dropped=[{"chain": t[1], "score": round(join_aware_score(t[0], spec, join_aware), 4)}
                           for t in nxt[self.beam_width:]])
            for (df, chain, calls, previous_shape, previous_coverage, pfp, previews) in beams:
                if plan_next(df, spec)["status"] in ("complete", "deferred_only"):
                    terminals.append((df, chain, calls, pfp, previews))
        for b in beams:
            terminals.append((b[0], b[1], b[2], b[5], b[6]))
        if not terminals:
            if candidate_errors:
                print(f"[pipeline-error] {trace_id}: {candidate_errors[0]}", flush=True)
            return {"df": df0, "chain": [], "calls": total_calls, "ok": False,
                    "candidate_errors": candidate_errors}
        # Final strong selection: verify-complete first, then the strong selector score
        def key(t):
            comp = plan_next(t[0], spec)["status"] in ("complete", "deferred_only")
            join_blocked = False
            if join_aware:
                active_jt, active_score, active_plaus = active_join_target(t[0], spec) if edge_conditioned else (None, None, None)
                js = active_score if edge_conditioned and active_score is not None else join_materialization_score(t[0], spec)
                join_blocked = js is not None and js < 0.5
                if os.environ.get("JOIN_CRITICAL_VALUE_GATE"):
                    ps = active_plaus if edge_conditioned and active_plaus is not None else join_value_plausibility_score(t[0], spec)
                    join_blocked = join_blocked or (ps is not None and ps < 0.35)
            return (not comp, join_blocked, -join_aware_score(t[0], spec, join_aware), len(t[1]))
        terminals.sort(key=key)
        if self.max_terminal_candidates is not None and self.max_terminal_candidates > 0:
            terminals = terminals[:self.max_terminal_candidates]
        df, chain, calls, _pfp, _previews = terminals[0]
        ok = plan_next(df, spec)["status"] in ("complete", "deferred_only")
        trace("selected", chain=chain, shape=list(df.shape), ok=ok,
              terminal_count=len(terminals), score=strong_score(df, spec))
        if not chain and candidate_errors:
            print(f"[pipeline-error] {trace_id}: {candidate_errors[0]}", flush=True)
        terminal_payload = []
        for cand_df, cand_chain, cand_calls, cand_pfp, cand_previews in terminals:
            payload = {
                "df": cand_df,
                "chain": cand_chain,
                "calls": cand_calls,
                "ok": plan_next(cand_df, spec)["status"] in ("complete", "deferred_only"),
                "score": join_aware_score(cand_df, spec, join_aware),
                "join_materialization_score": join_materialization_score(cand_df, spec) if join_aware else None,
                # "<params_md5>/<frame_md5>" per chain step; lets an offline pass tell
                # param variants apart from true duplicates of the same op-name chain.
                "param_fp": [d["fp"] for d in cand_pfp],
                # The executable pipeline: one {op, params} per element of `chain`,
                # in order. This is what an exporter replays; `chain` alone is only
                # the operator names.
                "steps": [{"op": d["op"], "params": d["params"]} for d in cand_pfp],
            }
            if os.environ.get("CHAIN_CAPTURE_PREVIEW"):
                payload["step_previews"] = cand_previews
            terminal_payload.append(payload)
        return {"df": df, "chain": chain, "calls": total_calls, "ok": ok,
                "steps": [{"op": d["op"], "params": d["params"]} for d in _pfp],
                "candidate_errors": candidate_errors,
                "terminal_candidates": terminal_payload}
