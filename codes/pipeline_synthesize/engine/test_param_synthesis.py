#!/usr/bin/env python3
"""
test_param_synthesis.py
-----------------------
Experiment: given that the operation TYPE is already correct, hand the LLM (nearest-
neighbour examples + the current table preview + the target schema) the job of writing

Flow, per single-op instance:
  1. op type = gold_op (assume the type is right);
  2. retrieve, from training_data, the nearest cases with the same op, using the current
  3. render them as usage examples (the operation as executable JSON), together with the
  4. the LLM emits an operation JSON -> execute it with table_executor.execute_step
  5. parse and execute the gold dc_op string -> gold_result;
  6. compare: are the normalised subtables (column names + values) equal — i.e. were the

Usage:
  export OPENAI_API_KEY=...            # your key
  python3 test_param_synthesis.py --limit 32
  python3 test_param_synthesis.py --dry-run-gold   # no LLM; compare gold against itself
"""
from __future__ import annotations
import os
import argparse, ast, json, re, sys
from pathlib import Path
from collections import Counter

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("NOVELPREP_ROOT") or Path(__file__).resolve().parents[3] / "codes" / "pipeline_synthesize" / "engine")
AUTOPREP = Path(os.environ.get("AUTOPREP_ROOT") or Path(__file__).resolve().parents[3] / "datasets")
for p in (str(HERE), str(ROOT), str(ROOT / "dependency_modeling_react_joint")):
    if p not in sys.path:
        sys.path.insert(0, p)

import test_single_ops_type as T
from infer import SingleOpInfer
from features import featurize, sanitize
from schema_spec import expand_view_to_full, parse_create_table, schema_to_sql
from table_executor import execute_step, func_name_from_code

# Ops whose gold parameters are always empty (the executor default suffices) - no LLM
PARAM_FREE_OPS = {"Transpose"}

import re as _re, math as _math, datetime as _datetime


def _compile_func_rich(code, default):
    """A fuller namespace than table_executor._compile_func (adds re/math/datetime), so a gold func does not fail on a missing module."""
    ns = {}
    exec(code, {"pd": pd, "np": np, "re": _re, "math": _math, "datetime": _datetime}, ns)
    fname = func_name_from_code(code, default=default)
    return ns.get(fname) or ns.get(default) or ns.get("transform") or next(iter(v for v in ns.values() if callable(v)))


def _cell_safe(f):
    """Cell-wise tolerance: LLM and gold funcs assume str input and crash on float/int/NaN; wrap them so a bad cell returns None."""
    def g(x):
        try:
            return f(x)
        except Exception:
            return None
    return g


def robust_execute(df, step):
    """Robust execution of a func-based op: fuller namespace, and SplitColumn accepts a
    func returning either a dict or a list. Every other op is delegated to execute_step."""
    op = step.get("op"); params = step.get("params") or {}
    if op == "SplitColumn":
        out = df.copy()
        func = _cell_safe(_compile_func_rich(params.get("func") or "def transform(s):\n    return s", "transform"))
        tcols = params.get("target_columns") or []
        scol = {str(c).casefold(): c for c in out.columns}.get(str(params.get("source_column")).casefold(), params.get("source_column"))
        if scol not in out.columns:
            return out
        vals = out[scol].apply(func)
        def pick(x, pos, name):
            if isinstance(x, dict):
                return x.get(name)
            if isinstance(x, (list, tuple, pd.Series)):
                return x[pos] if len(x) > pos else pd.NA
            return x if pos == 0 else pd.NA
        for pos, col in enumerate(tcols):
            out[col] = vals.apply(lambda x, p=pos, n=col: pick(x, p, n))
        return out
    if op == "Transpose":
        # Keep the original first-column name as the index name (benchmark semantics);
        p = dict(params)
        if not p.get("new_index_column") and len(df.columns):
            p["new_index_column"] = str(df.columns[0])
        return execute_step(df, {"op": "Transpose", "params": p})
    if op == "Explode":
        out = df.copy()
        m = {str(c).casefold(): c for c in out.columns}
        requested = params.get("column")
        requested_cols = requested if isinstance(requested, (list, tuple)) else [requested]
        cols = [m.get(str(c).casefold(), c) for c in requested_cols]
        if not cols or any(c not in out.columns for c in cols):
            return out
        def _list_value(x):
            if isinstance(x, (list, tuple)):
                return list(x)
            if isinstance(x, str) and x.strip().startswith(("[", "(")):
                try:
                    parsed = ast.literal_eval(x)
                    if isinstance(parsed, (list, tuple)):
                        return list(parsed)
                except Exception:
                    pass
            if params.get("regex_extract") and pd.notna(x):
                return re.findall(str(params.get("regex_extract")), str(x))
            if params.get("split_comma") and pd.notna(x):
                return str(x).split(",")
            return x
        for col in cols:
            out[col] = out[col].apply(_list_value)
        return out.explode(cols if len(cols) > 1 else cols[0])
    if op in ("StandardizeString", "Concatenate", "AddNewColumn", "CalculateStatistic", "CodeGeneration") and params.get("func"):
        # Recompile in the fuller namespace, then follow the same path
        if op == "StandardizeString":
            out = df.copy(); f = _cell_safe(_compile_func_rich(params["func"], "transform"))
            cm = {str(c).casefold(): c for c in out.columns}; c = cm.get(str(params.get("column_name")).casefold(), params.get("column_name"))
            if c in out.columns:
                out[c] = out[c].apply(lambda s: f(s) if pd.notna(s) else s)
            return out
        if op == "Concatenate":
            out = df.copy(); f = _cell_safe(_compile_func_rich(params["func"], "transform"))
            cols = [c for c in (params.get("concatenate_columns") or []) if c in out.columns]
            if cols:
                out[params.get("target_column")] = out[cols].apply(f, axis=1)
            return out
    return execute_step(df, step)


# ---------------- gold op string -> executable step dict ----------------
def op_str_to_step(op_str: str) -> dict:
    tree = ast.parse(op_str.strip(), mode="eval").body
    params = {}
    for kw in tree.keywords:
        try:
            params[kw.arg] = ast.literal_eval(kw.value)
        except Exception:
            params[kw.arg] = ast.get_source_segment(op_str, kw.value)
    params.pop("table_name", None)
    return {"op": tree.func.id, "params": params}


def gold_op_str_for_table(task: dict, logical_table: str) -> str | None:
    """The raw dc_op whose table_name equals this logical table, for this task."""
    for op_text in task.get("dc_ops") or []:
        m = T.OP_WITH_TABLE_RE.search(str(op_text))
        if m and m.group(2) == logical_table:
            return str(op_text)
    return None


# ---------------- result comparison (subtable values + column names, order-free) ----
def _nval(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else format(round(f, 6), "g")
    except Exception:
        return str(v).strip().lower()


def _normalize_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"[^a-z0-9]", "", str(c).lower()) for c in df.columns]
    df = df.loc[:, ~pd.Index(df.columns).duplicated()]
    for c in df.columns:
        df[c] = df[c].map(_nval)
    df = df.reindex(sorted(df.columns), axis=1)
    if len(df.columns):
        df = df.sort_values(list(df.columns)).reset_index(drop=True)
    return df


def tables_equiv(a: pd.DataFrame, b: pd.DataFrame) -> bool:
    try:
        return _normalize_table(a).equals(_normalize_table(b))
    except Exception:
        return False


# ---------------- LLM prompt ----------------
PROMPT = """You are a data-preparation operation-parameter generator.
The operation TYPE is already decided: **{op}**. Only fill in its parameters.

A similar solved example (retrieved by table-feature similarity):
{example}

Now the CURRENT table:
Columns: {columns}
Preview:
{preview}

Target schema (the table should conform to this):
{schema_sql}

Output ONLY one JSON object of the form:
{{"op": "{op}", "params": {{ ... }}}}
Use source column names visible in the CURRENT table; use TARGET column names from the target schema above
(e.g. rename to the schema's names, name the split/concatenated output columns as in the schema).
{func_rules}Do NOT invent value->number mappings or coerce text to integers just to satisfy a column's declared type;
preserve the underlying values and only split/normalize/restructure them.
Only reference column names that appear in the CURRENT table's column list.
No prose, JSON only."""

# Only four operations take a Python function string; the other ~62% of synthesis calls (Rename,
# Pivot, Transpose, Stack, Explode, WideToLong) were reading 83 tokens of `func` guidance that can
# never apply to them. Emit it only for the operations that can use it.
FUNC_OPS = {"SplitColumn", "Concatenate", "StandardizeString", "StandardizeDatetime"}
FUNC_RULES = (
    "Put a Python function string in `func` exactly like the example. SplitColumn `func` must "
    "return a LIST aligned positionally with `target_columns` (not a dict).\n"
    "Funcs MUST be robust: a cell may be NaN/None/int/float, not just str — guard with pd.isna "
    "and wrap with str() before .split()/.strip().\n"
)


def render_example_json(infer, op, nn_id):
    """Render the nearest-neighbour cases as usage examples, the operation as executable JSON, so the LLM can copy the parameter style."""
    rec = infer.details.get(nn_id)
    definition = infer.defs.get(op, "")
    if not rec:
        return f"## {op}\nDefinition: {definition}\n(no retrieved case)"
    try:
        op_json = json.dumps(op_str_to_step(rec["operation"]), ensure_ascii=False)
    except Exception:
        op_json = rec["operation"]
    return (f"## {op}\nDefinition: {definition}\n\n"
            f"Raw table preview:\n```text\n{rec['raw_table_preview']}\n```\n"
            f"Target schema:\n```sql\n{rec['target_schema_sql']}\n```\n"
            f"Correct operation:\n```json\n{op_json}\n```\n")


# How many values the dtype guess looks at. The profile only tells the model
# "int / float / date / str", so a sample decides it as well as the whole column
# does — and the whole column is ruinous. This ran `to_numeric` TWICE and
# `to_datetime` once over every column of every frame, and `build_prompt` is
# called for every candidate operation at every depth of the beam search. On an
# object column `to_datetime` falls back to per-element dateutil parsing, which
# is where a beaver run was found spending its time: py-spy caught the process in
# `to_numeric` inside `_col_profile`, 28 GB resident, 34 minutes per task against
# 1-2 minutes on spider. Sampling makes the cost independent of table height.
_PROFILE_SAMPLE = 500


def _col_profile(df):
    """Per column: inferred dtype + null fraction, so the LLM writes a type-safe func rather than assuming everything is str."""
    prof = []
    for c in list(df.columns)[:40]:
        s = df[c]
        # Null fraction stays on the FULL column: it is a cheap vectorised check
        # and it is the part the model actually needs to be right about, since it
        # decides whether the generated func must guard with pd.isna.
        nullp = float(s.isna().mean())
        sample = s.dropna()
        if len(sample) > _PROFILE_SAMPLE:
            sample = sample.iloc[:_PROFILE_SAMPLE]
        if len(sample) == 0:
            dt = "str"
        else:
            num = pd.to_numeric(sample, errors="coerce")
            if num.notna().mean() > 0.9:
                dt = "int" if num.dropna().mod(1).eq(0).all() else "float"
            elif pd.to_datetime(sample, errors="coerce").notna().mean() > 0.9:
                dt = "date"
            else:
                dt = "str"
        prof.append(f"{c}:{dt}" + (f"(nulls {nullp:.0%})" if nullp > 0.05 else ""))
    return ", ".join(prof)


def build_prompt(op, example_md, df, schema_sql):
    from build_training_data import table_preview
    from schema_spec import parse_create_table
    import param_hints as _PH
    # Structural ops: derive parameter candidates from the table structure and pass them
    hint = None
    try:
        schema = parse_create_table(schema_sql)[0]
        if op == "Pivot":
            hint = _PH.pivot_hint(df, schema)
        elif op == "SplitColumn":
            hint = _PH.split_column_hint(df, schema)
    except Exception:
        hint = None
    extra = ""
    if hint:
        extra = (f"\nStructural analysis suggests these params (strongly prefer unless the preview clearly "
                 f"contradicts): {json.dumps(hint, ensure_ascii=False)}")
    return PROMPT.format(op=op, example=example_md,
                         func_rules=FUNC_RULES if op in FUNC_OPS else "",
                         columns=json.dumps([str(c) for c in df.columns][:40], ensure_ascii=False) +
                                 "\nColumn dtypes/nulls: " + _col_profile(df) + extra,
                         preview=table_preview(df), schema_sql=schema_sql)


def call_llm(prompt, model):
    from prep_utils import llm_generate_setup, timed_llm_generate
    resp, _ = timed_llm_generate(llm_generate_setup, prompt, model=model, json_format=True)
    txt = resp.get("text", "") if isinstance(resp, dict) else str(resp)
    if "```" in txt:
        b = re.findall(r"```(?:json)?\s*(.*?)```", txt, re.S | re.I)
        if b:
            txt = b[0]
    try:
        return json.loads(txt.strip())
    except Exception:
        pass
    dec = json.JSONDecoder()
    m = re.search(r"\{", txt)
    if m:
        obj, _ = dec.raw_decode(txt[m.start():])   # parse only the first JSON object, tolerating trailing text
        return obj
    raise ValueError("no JSON object in LLM output")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="nl2sql-bird")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--table-specs", type=Path,
                    default=ROOT / "dependency_modeling_react_joint" / "results" / "oracle_v1_group_a_specs.jsonl")
    ap.add_argument("--case-file", type=Path,
                    default=ROOT / "pipeline_eval" / "cases_group_a_high_ops_union_structural.jsonl")
    ap.add_argument("--model", default="gpt-4o-2024-08-06")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run-gold", action="store_true", help="no LLM; validate the pipeline by comparing gold with itself")
    ap.add_argument("--output", type=Path, default=HERE / "results" / "param_synth_details.jsonl")
    args = ap.parse_args()

    infer = SingleOpInfer()
    cls = set(map(str, infer.clf.classes_)) | {"StandardizeDatetime"}
    bdir = AUTOPREP / args.benchmark / args.split
    btask = T.load_benchmark(args.benchmark, args.split, AUTOPREP)
    specs = T.load_jsonl(args.table_specs)
    case_ids = set(T.load_case_ids(args.case_file, args.benchmark)) if args.case_file.exists() else None
    inst, _ = T.iter_single_op_instances(specs, btask, bdir, {}, case_ids, cls)
    if args.limit:
        inst = inst[: args.limit]

    rows, ok, total = [], Counter(), Counter()
    per_op_ok, per_op_n = Counter(), Counter()
    for it in inst:
        gold_op = it["gold_op"]; tid = it["task_id"]
        src = it["source"]; db = it["db_id"]
        df = sanitize(infer._load_table(it["table_path"]))
        # Features (aligned with training: expanded to the full schema)
        full_schema, full_pk = expand_view_to_full(it["schema_spec"], db, src)
        x = featurize(df, full_schema, full_pk)
        nn_id = infer._nearest(x, gold_op)
        example_md = render_example_json(infer, gold_op, nn_id)

        gold_op_str = gold_op_str_for_table(btask[tid], it["logical_table"])
        gold_step = op_str_to_step(gold_op_str) if gold_op_str else None
        try:
            gold_df = robust_execute(df.copy(), gold_step)
        except Exception as e:
            rows.append({"task_id": tid, "op": gold_op, "error": f"gold_exec:{e}"}); continue

        total[gold_op] += 1; per_op_n[gold_op] += 1
        if args.dry_run_gold:
            pred_step = gold_step
        elif gold_op in PARAM_FREE_OPS:
            pred_step = {"op": gold_op, "params": {}}      # no LLM needed
        else:
            try:
                # Give the LLM the full expanded schema (all target column names), not the
                full_sql = schema_to_sql(full_schema, full_pk)
                prompt = build_prompt(gold_op, example_md, df, full_sql)
                pred_step = call_llm(prompt, args.model)
            except Exception as e:
                rows.append({"task_id": tid, "op": gold_op, "error": f"llm:{e}"}); continue
        try:
            pred_df = robust_execute(df.copy(), pred_step)
            match = tables_equiv(pred_df, gold_df)
        except Exception as e:
            rows.append({"task_id": tid, "op": gold_op, "pred": pred_step, "error": f"pred_exec:{e}", "match": False}); continue
        ok[gold_op] += int(match); per_op_ok[gold_op] += int(match)
        rows.append({"task_id": tid, "op": gold_op, "nn_example": nn_id,
                     "pred_step": pred_step, "match": bool(match)})

    N = sum(total.values()); OKN = sum(ok.values())
    print(f"instances (op-type correct assumed): {N}")
    print(f"param-correct (result-table match): {OKN}/{N} = {OKN/N:.3f}" if N else "no instances")
    print("\nper-op:")
    for op in sorted(per_op_n):
        print(f"  {op:20s} {per_op_ok[op]}/{per_op_n[op]}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("\ndetails ->", args.output)


if __name__ == "__main__":
    main()
