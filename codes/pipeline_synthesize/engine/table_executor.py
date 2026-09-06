from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from operation_space import canonical_op_name


def _format_preview_cell(value: Any, max_cell_len: int = 160) -> str:
    if isinstance(value, str):
        text = value.replace("\n", "\\n")
        if len(text) > max_cell_len:
            return f'"<long_text len={len(text)}>"'
        return f'"{text}"'
    return str(value)


def df_to_cotable(tbl: pd.DataFrame, cut_line: int = 10, cut_col: int = 30, max_len: int = 6000) -> str:
    if tbl is None:
        return "None"
    # Only the first cut_line rows are printed (the loop below), so slice rows BEFORE
    # copying. This used to copy the whole table: on beaver every observation deep-copied
    # several million rows, and observation is called twice per step of the bounded loop
    # One extra row: the loop below decides whether to append "......" by checking that
    # row cut_line still exists, so slicing exactly at cut_line would drop the ellipsis
    df = tbl.iloc[:cut_line + 1].copy() if cut_line != -1 else tbl.copy()
    columns = list(df.columns)
    omitted_cols = 0
    if cut_col != -1 and len(columns) > cut_col:
        head = cut_col // 2
        tail = cut_col - head
        keep_columns = columns[:head] + columns[-tail:]
        omitted_cols = len(columns) - len(keep_columns)
        df = df.loc[:, keep_columns]
        columns = keep_columns

    ret = ""
    header = " | ".join(str(col).replace("\n", "\\n") for col in columns)
    if omitted_cols:
        header += f" | ... {omitted_cols} columns omitted ..."
    ret += header + "\n"
    ret += "|".join(["---" for _ in columns])
    if omitted_cols:
        ret += " | ---"
    ret += "\n"

    for i in range(len(df)):
        if cut_line != -1 and i > cut_line - 1:
            ret += "......\n"
            break
        row_str = " | ".join(_format_preview_cell(x) for x in df.iloc[i].values)
        if omitted_cols:
            row_str += " | ..."
        ret += row_str + "\n"

    ret = ret.strip()
    if len(ret) > max_len:
        return ret[:max_len] + "\n......\n[Truncated due to length]"
    if len(tbl) == 0:
        ret += "\n(The table is empty!!!)"
    return ret


def load_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".pkl":
        obj = pd.read_pickle(path)
    elif suffix == ".csv":
        obj = pd.read_csv(path)
    elif suffix in {".json", ".jsonl"}:
        obj = pd.read_json(path, lines=suffix == ".jsonl")
    elif suffix in {".xls", ".xlsx"}:
        obj = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported table format: {path}")
    return obj if isinstance(obj, pd.DataFrame) else pd.DataFrame(obj)


def read_table_preview(path: Path, top_k: int, cut_col: int, max_table_len: int) -> tuple[list[str], str, tuple[int, int]]:
    df = load_table(path)
    return [str(c) for c in df.columns], df_to_cotable(df, cut_line=top_k, cut_col=cut_col, max_len=max_table_len), tuple(df.shape)


def extract_json(text: Any) -> Any:
    if isinstance(text, dict):
        return text
    text = str(text or "").strip()
    if "```" in text:
        blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.S | re.I)
        if blocks:
            text = blocks[0].strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"(\{.*\}|\[.*\])", text, flags=re.S)
    if match:
        candidate = match.group(1)
        try:
            return json.loads(candidate)
        except Exception:
            return ast.literal_eval(candidate)
    return ast.literal_eval(text)


def normalize_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_bool_list(value: Any, size: int) -> list[bool] | bool:
    if isinstance(value, list):
        return [bool(x) for x in value]
    if value is None:
        return True
    return bool(value)


def _is_all_except_id_vars(value: Any) -> bool:
    if isinstance(value, str):
        return value == "__all_except_id_vars__"
    if isinstance(value, list):
        return any(str(item) == "__all_except_id_vars__" for item in value)
    return False


def rename_map_to_dict(rename_map: Any) -> dict[str, str]:
    if isinstance(rename_map, dict):
        return {str(k): str(v) for k, v in rename_map.items()}
    out: dict[str, str] = {}
    if isinstance(rename_map, list):
        for item in rename_map:
            if isinstance(item, dict):
                old = item.get("old_name") or item.get("old") or item.get("from")
                new = item.get("new_name") or item.get("new") or item.get("to")
                if old is not None and new is not None:
                    out[str(old)] = str(new)
    return out


def func_name_from_code(func_code: str, default: str = "transform") -> str:
    match = re.search(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", func_code or "")
    return match.group(1) if match else default


def canonical_step(step: dict[str, Any]) -> dict[str, Any]:
    op = canonical_op_name(step.get("op") or step.get("operation"))
    return {
        "op": op,
        "params": step.get("params") or {},
        "table_indices": [0],
    }


def validate_function_param(params: dict[str, Any], field: str, signature_hint: str) -> None:
    func = str(params.get(field) or "")
    stripped = func.strip()
    if not stripped:
        raise ValueError(f"{field} is required and must be a complete Python function: {signature_hint}")
    if re.search(r"(^|\b)lambda\b", stripped):
        raise ValueError(f"{field} must be a complete Python function named transform, not a lambda. Use: {signature_hint}")
    if not re.search(r"def\s+transform\s*\(", stripped):
        raise ValueError(f"{field} must define a function named transform. Use: {signature_hint}")


def validate_step_for_executor(step: dict[str, Any]) -> None:
    op = step["op"]
    params = step.get("params") or {}
    if op == "Rename":
        rename_map = params.get("rename_map")
        if not rename_map_to_dict(rename_map):
            raise ValueError(
                "Rename.params.rename_map must be non-empty, e.g. "
                "[{'old_name':'old_col','new_name':'new_col'}] or {'old_col':'new_col'}."
            )
    elif op == "Pivot":
        if params.get("index") in (None, [], ""):
            raise ValueError("Pivot.params.index is required; use a column name or a list of column names.")
        if params.get("columns") in (None, ""):
            raise ValueError("Pivot.params.columns is required; use the column whose values become new headers.")
        if params.get("values") in (None, [], ""):
            raise ValueError("Pivot.params.values is required; use the column whose values fill the pivoted cells.")
    elif op == "Stack":
        if not normalize_list(params.get("id_vars")):
            raise ValueError("Stack.params.id_vars must be a non-empty list of columns to keep.")
        if not _is_all_except_id_vars(params.get("value_vars")) and not normalize_list(params.get("value_vars")):
            raise ValueError("Stack.params.value_vars must be a non-empty list of columns to melt.")
    elif op == "WideToLong":
        if not normalize_list(params.get("subnames")):
            raise ValueError("WideToLong.params.subnames must be a non-empty list of stub names.")
        if not normalize_list(params.get("i")):
            raise ValueError("WideToLong.params.i must be a non-empty list of id columns.")
        if not params.get("j"):
            raise ValueError("WideToLong.params.j is required; it names the suffix/variable column.")
    elif op == "Explode":
        if not params.get("column"):
            raise ValueError("Explode.params.column is required.")
    elif op == "SplitColumn":
        validate_function_param(params, "func", "def transform(s):\\n    return [value_for_col_1, value_for_col_2]")
        source = params.get("source_column")
        targets = normalize_list(params.get("target_columns"))
        if not source:
            raise ValueError("SplitColumn.params.source_column is required.")
        if not targets:
            raise ValueError("SplitColumn.params.target_columns must be a non-empty list.")
    elif op == "Concatenate":
        validate_function_param(params, "func", "def transform(row):\\n    return ...")
        if not normalize_list(params.get("concatenate_columns")):
            raise ValueError("Concatenate.params.concatenate_columns must be a non-empty list.")
        if not params.get("target_column"):
            raise ValueError("Concatenate.params.target_column is required.")
    elif op == "StandardizeString":
        validate_function_param(params, "func", "def transform(s):\\n    return str(s).strip().lower()")
        if not params.get("column_name"):
            raise ValueError("StandardizeString.params.column_name is required.")
    elif op == "StandardizeDatetime":
        if not params.get("column_name"):
            raise ValueError("StandardizeDatetime.params.column_name is required.")
    elif op == "CastType":
        if not params.get("column"):
            raise ValueError("CastType.params.column is required.")
        dtype = str(params.get("dtype", ""))
        allowed = {"str", "int", "integer", "float", "double", "datetime64", "datetime", "date", "bool", "boolean"}
        if dtype not in allowed:
            raise ValueError(f"CastType.params.dtype must be one of {sorted(allowed)}.")
    elif op == "DropColumn":
        if not normalize_list(params.get("drop_columns")):
            raise ValueError("DropColumn.params.drop_columns must be a non-empty list.")


def normalize_action_block(obj: Any, max_ops: int) -> list[dict[str, Any]]:
    if isinstance(obj, str):
        obj = extract_json(obj)
    if isinstance(obj, dict):
        obj = obj.get("operations") or obj.get("transform_chain") or obj.get("action_block") or obj.get("steps") or []
    if not isinstance(obj, list):
        raise ValueError("Action block must be a JSON list or object with operations/transform_chain.")
    if len(obj) == 0:
        raise ValueError("Action block is empty.")
    if len(obj) > max_ops:
        raise ValueError(f"Action block has {len(obj)} operations, exceeding max_ops_per_turn={max_ops}.")
    steps = [canonical_step(step) for step in obj]
    blocked = [step["op"] for step in steps if step["op"] == "SelectCol"]
    if blocked:
        raise ValueError("SelectCol is deterministic final projection and cannot be generated as a ReAct action.")
    for step in steps:
        validate_step_for_executor(step)
    return steps


def execute_chain(initial_df: pd.DataFrame, chain: list[dict[str, Any]]) -> tuple[pd.DataFrame | None, str | None]:
    current = initial_df.copy()
    try:
        for step in chain:
            current = execute_step(current, step)
        return current, None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def execute_stack(df: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    id_vars = [str(col) for col in normalize_list(params.get("id_vars"))]
    original_cols = [str(col) for col in df.columns]
    id_positions: list[int] = []
    for col in id_vars:
        if col not in original_cols:
            raise KeyError(f"Stack id_var is not present in the DataFrame: {col}")
        id_positions.append(original_cols.index(col))

    if _is_all_except_id_vars(params.get("value_vars")):
        value_positions = [idx for idx in range(len(original_cols)) if idx not in set(id_positions)]
    else:
        requested = {str(col) for col in normalize_list(params.get("value_vars"))}
        value_positions = [idx for idx, col in enumerate(original_cols) if col in requested and idx not in set(id_positions)]
        missing = sorted(requested - set(original_cols))
        if missing:
            raise KeyError(f"Stack value_vars are not present in the DataFrame: {missing[:20]}")
    if not value_positions:
        raise ValueError("Stack has no value columns to melt.")

    internal_cols = [f"__col_{idx}" for idx in range(len(original_cols))]
    tmp = df.copy()
    tmp.columns = internal_cols
    id_internal = [internal_cols[idx] for idx in id_positions]
    value_internal = [internal_cols[idx] for idx in value_positions]

    variable_labels = {internal_cols[idx]: original_cols[idx] for idx in value_positions}
    if params.get("use_first_row_as_variable_labels"):
        if len(tmp) == 0:
            raise ValueError("Stack.use_first_row_as_variable_labels cannot be used on an empty table.")
        first = tmp.iloc[0]
        variable_labels = {
            internal_cols[idx]: str(first[internal_cols[idx]]).strip().strip('"').strip("'")
            for idx in value_positions
        }
        tmp = tmp.iloc[1:].reset_index(drop=True)

    var_name = params.get("var_name", "variable")
    value_name = params.get("value_name", "value")
    out = tmp.melt(
        id_vars=id_internal,
        value_vars=value_internal,
        var_name=var_name,
        value_name=value_name,
    )
    out[var_name] = out[var_name].map(variable_labels)
    rename_ids = {internal_cols[idx]: original_cols[idx] for idx in id_positions}
    return out.rename(columns=rename_ids)


# A Pivot's result is (distinct index tuples) x (distinct column values), and
# pandas materialises it DENSELY inside unstack. The explore loop proposes Pivot
# as a candidate and executes it to see what comes out, so a badly-chosen
# columns= on a warehouse table is not a wrong answer that scores 0 — it is an
# allocation that takes the whole machine down. Measured on beaver stage 3: two
# worker threads sat in `pivot_table -> unstack -> _make_selectors` while the
# process reached 237 GB RSS and completed one task per hour.
#
# The cap is a plausibility bound, not a performance knob. A prepared subtable
# that answers a question does not have 50 million cells; a candidate that would
# produce one is wrong whatever else is true of it, so refusing it costs no
# reachable answer. Raising (rather than truncating) lets the loop score this
# candidate as failed and move on, which is what it already does for any
# operator that throws.
_PIVOT_CELL_CAP = 50_000_000


def _guard_pivot(df: pd.DataFrame, params: dict[str, Any]) -> None:
    idx = normalize_list(params.get("index"))
    cols = normalize_list(params.get("columns"))
    if not cols:
        return
    try:
        n_cols = 1
        for c in cols:
            if c in df.columns:
                n_cols *= max(int(df[c].nunique(dropna=True)), 1)
        if idx and all(c in df.columns for c in idx):
            n_rows = int(df.groupby(idx, dropna=False, observed=True).ngroups)
        else:
            n_rows = len(df)
        est = n_rows * n_cols
    except Exception:
        return                      # cannot estimate: let pandas try
    if est > _PIVOT_CELL_CAP:
        raise ValueError(
            f"Pivot refused: index={idx} x columns={cols} would materialise about "
            f"{est:,} cells (cap {_PIVOT_CELL_CAP:,}); choose a lower-cardinality "
            "columns= or a coarser index=")


def execute_step(df: pd.DataFrame, step: dict[str, Any]) -> pd.DataFrame:
    op = canonical_op_name(step.get("op"))
    params = step.get("params") or {}

    if op == "Filter":
        return df.query(str(params.get("condition", ""))).copy()
    if op == "Sort":
        by = normalize_list(params.get("by"))
        return df.sort_values(by=by, ascending=normalize_bool_list(params.get("ascending"), len(by))).copy()
    if op == "Pivot":
        _guard_pivot(df, params)
        return pd.pivot_table(
            df,
            index=params.get("index"),
            columns=params.get("columns"),
            values=params.get("values"),
            aggfunc=params.get("aggfunc", "mean"),
        ).reset_index()
    if op == "GroupBy":
        return df.groupby(normalize_list(params.get("by")), as_index=False).agg(params.get("agg", {}))
    if op == "Rename":
        return df.rename(columns=rename_map_to_dict(params.get("rename_map", {}))).copy()
    if op == "Stack":
        return execute_stack(df, params)
    if op == "Explode":
        out = df.copy()
        col = params.get("column")
        if params.get("split_comma"):
            out[col] = out[col].apply(lambda x: str(x).split(",") if pd.notna(x) else x)
        return out.explode(col)
    if op == "WideToLong":
        return pd.wide_to_long(
            df,
            stubnames=params.get("subnames", []),
            i=params.get("i"),
            j=params.get("j", "variable"),
            sep=params.get("sep", "_"),
            suffix=params.get("suffix", "\\w+"),
        ).reset_index()
    if op == "Transpose":
        index_column = params.get("index_column")
        use_first_column_as_header = params.get("use_first_column_as_header", True)
        new_index_column = params.get("new_index_column", "row_id")
        if use_first_column_as_header and len(df.columns) > 0:
            source_col = index_column if index_column in df.columns else df.columns[0]
            out = df.set_index(source_col).T.reset_index()
            return out.rename(columns={"index": new_index_column})
        return df.T.reset_index().rename(columns={"index": new_index_column})
    if op == "DropNulls":
        subset = params.get("subset")
        return df.dropna(subset=normalize_list(subset) if subset else None, how=params.get("how", "any")).copy()
    if op == "Deduplicate":
        subset = params.get("subset")
        return df.drop_duplicates(subset=normalize_list(subset) if subset else None, keep=params.get("keep", "first")).copy()
    if op == "TopK":
        return df.head(int(params.get("k", 5))).copy()
    if op == "SelectCol":
        return df.loc[:, normalize_list(params.get("columns"))].copy()
    if op == "CastType":
        out = df.copy()
        col = params.get("column")
        dtype = str(params.get("dtype", "str"))
        if dtype in {"datetime64", "datetime", "date"}:
            out[col] = pd.to_datetime(out[col], errors="coerce")
        elif dtype in {"int", "integer"}:
            out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")
        elif dtype in {"float", "double"}:
            out[col] = pd.to_numeric(out[col], errors="coerce").astype(float)
        elif dtype in {"bool", "boolean"}:
            out[col] = out[col].astype(bool)
        else:
            out[col] = out[col].astype(str)
        return out
    if op == "DropColumn":
        return df.drop(columns=normalize_list(params.get("drop_columns")), errors="ignore").copy()
    if op == "SplitColumn":
        out = df.copy()
        func = _compile_func(params.get("func") or "def transform(s):\n    return s", default="transform")
        values = out[params.get("source_column")].apply(func)
        values = values.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
        for pos, col in enumerate(normalize_list(params.get("target_columns"))):
            out[col] = values.apply(lambda x: x[pos] if len(x) > pos else pd.NA)
        return out
    if op == "Concatenate":
        out = df.copy()
        func = _compile_func(
            params.get("func") or "def transform(row):\n    return ''.join(row.astype(str).tolist())",
            default="transform",
        )
        cols = normalize_list(params.get("concatenate_columns"))
        out[params.get("target_column")] = out[cols].apply(func, axis=1)
        return out
    if op == "StandardizeString":
        out = df.copy()
        func = _compile_func(params.get("func") or "def transform(s):\n    return str(s).strip().lower()", default="transform")
        col = params.get("column_name")
        out[col] = out[col].apply(lambda s: func(s) if pd.notna(s) else s)
        return out
    if op == "StandardizeDatetime":
        out = df.copy()
        col = params.get("column_name")
        fmt = params.get("date_format", "%Y-%m-%d")
        out[col] = pd.to_datetime(out[col], errors="coerce").dt.strftime(fmt)
        return out
    if op == "AddNewColumn":
        out = df.copy()
        func = _compile_func(params.get("func") or "def transform(row):\n    return None", default="transform")
        out[params.get("new_column_name")] = out.apply(func, axis=1)
        return out
    if op == "CalculateStatistic":
        func = _compile_func(
            params.get("func") or "def calculate_stat(df: pd.DataFrame):\n    return len(df)",
            default="calculate_stat",
        )
        return pd.DataFrame(
            {
                "statistic_name": [params.get("statistic_name", "statistic")],
                "value": [func(df)],
            }
        )
    if op == "Count":
        return pd.DataFrame({params.get("count_column", "count"): [len(df)]})
    if op == "CodeGeneration":
        func = _compile_func(params.get("func") or "def transform(tables):\n    return tables[0]", default="transform")
        result = func([df])
        return result if isinstance(result, pd.DataFrame) else pd.DataFrame(result)
    raise ValueError(f"Unsupported op: {op}")


def _compile_func(func_code: str, default: str):
    ns: dict[str, Any] = {}
    exec(func_code, {"pd": pd, "np": np}, ns)
    fname = func_name_from_code(func_code, default=default)
    func = ns.get(fname) or ns.get(default) or ns.get("transform")
    if func is None:
        raise ValueError(f"Could not find function in code: {func_code}")
    return func


# Above this many rows, string-derived statistics are sampled. Below the threshold this is
# byte-for-byte the pre-sampling implementation, so existing bird/spider results (whose
# tables are far smaller) are unaffected; only large tables such as beaver sample. Before
# sampling, dropna().map(str) per column is O(rows) Python calls, which took minutes per
# single_table_loop._observation)。
_OBS_ROW_CAP = 20000


def observation_from_df(df: pd.DataFrame, top_k: int, cut_col: int, max_table_len: int) -> dict[str, Any]:
    columns = [str(c) for c in df.columns]
    dtypes: dict[str, str] = {}
    column_stats: dict[str, dict[str, Any]] = {}
    column_sample_values: dict[str, list[str]] = {}
    for pos, col in enumerate(columns):
        series = df.iloc[:, pos]
        dtypes[col] = str(series.dtype)
        non_null = series.dropna()
        if len(non_null) > _OBS_ROW_CAP:
            non_null = non_null.iloc[:_OBS_ROW_CAP]
        # It must be map(str), not astype(str): the latter yields '2020-01-01' on a datetime
        # column while the former yields '2020-01-01 00:00:00'. Switching would silently
        normalized = non_null.map(lambda x: str(x))
        n_uniq = int(normalized.nunique())
        column_stats[col] = {
            # notna().mean() is a vectorised whole-column operation, cheap and exact, so it is not sampled
            "non_null_ratio": round(float(series.notna().mean()), 4) if len(series) else 0.0,
            "unique_ratio": round(float(n_uniq / max(len(normalized), 1)), 4),
            "distinct_count": n_uniq,
        }
        frequent = normalized.value_counts(dropna=True).head(20).index.tolist()
        column_sample_values[col] = normalized.head(20).tolist()
        column_stats[col]["frequent_values"] = frequent
    return {
        "shape": list(df.shape),
        "columns": columns,
        "dtypes": dtypes,
        "column_stats": column_stats,
        "column_sample_values": column_sample_values,
        "table_preview": df_to_cotable(df, cut_line=top_k, cut_col=cut_col, max_len=max_table_len),
    }
