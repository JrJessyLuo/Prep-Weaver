from __future__ import annotations

import json
import re
from typing import Any


OPERATION_CATEGORIES: dict[str, dict[str, Any]] = {
    "structural_oriented": {
        "purpose": (
            "Recover column-oriented relational structure from non-relational layouts, "
            "including schemas hidden in rows, values encoded as headers, wide/cross-tab "
            "layouts, and list-like cells."
        ),
        "operations": {
            "Transpose": {
                "params": {
                    "use_first_column_as_header": True,
                    "index_column": "optional_col",
                    "new_index_column": "row_id",
                },
                "description": "Transpose rows and columns when attributes/values are in the wrong orientation. By default, the first column values become output headers.",
            },
            "Stack": {
                "params": {
                    "id_vars": ["col"],
                    "value_vars": ["col"],
                    "var_name": "variable",
                    "value_name": "value",
                    "use_first_row_as_variable_labels": False,
                },
                "description": "Melt sibling columns into variable/value rows. For very wide tables, set value_vars to \"__all_except_id_vars__\" instead of enumerating hundreds of columns. If the first data row stores the real variable labels, set use_first_row_as_variable_labels to true.",
            },
            "Pivot": {
                "params": {
                    "index": "col_or_list",
                    "columns": "col",
                    "values": "col",
                    "aggfunc": "sum|mean|max|min|count|first",
                },
                "description": "Turn key/value or long-form rows into normal columns.",
            },
            "WideToLong": {
                "params": {
                    "subnames": ["stub"],
                    "i": ["id_col"],
                    "j": "new_col",
                    "sep": "_",
                    "suffix": "\\w+",
                },
                "description": "Convert repeated wide column groups into a long table.",
            },
            "Explode": {
                "params": {"column": "col", "split_comma": False},
                "description": "Explode list-like or comma-separated cell values into rows.",
            },
        },
    },
    "non_structural_oriented": {
        "purpose": (
            "Align representations after the table has usable structure: fix names, "
            "split/combine composite values, standardize types and values, and remove "
            "columns that are no longer useful."
        ),
        "operations": {
            "Rename": {
                "params": {"rename_map": [{"old_name": "old_col", "new_name": "new_col"}]},
                "description": "Refine or align column names.",
            },
            "SplitColumn": {
                "params": {
                    "source_column": "col",
                    "target_columns": ["new_col_1", "new_col_2"],
                    "func": "def transform(s):\n    return [...]",
                },
                "description": "Split a packed/composite column into multiple semantic columns.",
            },
            "Concatenate": {
                "params": {
                    "concatenate_columns": ["col1", "col2"],
                    "target_column": "new_col",
                    "func": "def transform(row):\n    return ...",
                },
                "description": "Combine several columns into one semantic field.",
            },
            "StandardizeString": {
                "params": {
                    "column_name": "col",
                    "func": "def transform(s):\n    return str(s).strip().lower()",
                },
                "description": "Normalize string values.",
            },
            "StandardizeDatetime": {
                "params": {"column_name": "col", "date_format": "%Y-%m-%d"},
                "description": "Parse and standardize date/time values.",
            },
            "CastType": {
                "params": {"column": "col", "dtype": "str|int|float|datetime64|bool"},
                "description": "Convert a column to another type.",
            },
            # Not used in benchmark dc_ops; keep out of the schema-repair action space.
            # "AddNewColumn": {
            #     "params": {
            #         "new_column_name": "new_col",
            #         "func": "def transform(row):\n    return ...",
            #     },
            #     "description": "Create a query-needed derived column.",
            # },
            "DropColumn": {
                "params": {"drop_columns": ["col"]},
                "description": "Drop irrelevant columns after they are no longer needed.",
            },
            # SQL-answering operations, not benchmark dc_ops.
            # "DropNulls": {
            #     "params": {"subset": ["col"], "how": "any"},
            #     "description": "Drop rows with missing values.",
            # },
            # "Deduplicate": {
            #     "params": {"subset": ["col"], "keep": "first"},
            #     "description": "Remove duplicate rows.",
            # },
            # "Filter": {
            #     "params": {"condition": "pandas query string"},
            #     "description": "Filter rows based on query conditions.",
            # },
            # "GroupBy": {
            #     "params": {"by": ["col"], "agg": {"value_col": "sum|mean|max|min|count|nunique"}},
            #     "description": "Group rows and aggregate query-needed values.",
            # },
            # "Sort": {
            #     "params": {"by": ["col"], "ascending": [True]},
            #     "description": "Sort rows.",
            # },
            # "TopK": {
            #     "params": {"k": 5},
            #     "description": "Keep top-k rows in the current order.",
            # },
            # "CalculateStatistic": {
            #     "params": {
            #         "statistic_name": "name",
            #         "func": "def calculate_stat(df: pd.DataFrame):\n    return ...",
            #     },
            #     "description": "Calculate a scalar statistic as a one-row table.",
            # },
            # "Count": {
            #     "params": {"count_column": "count"},
            #     "description": "Count rows and return a one-row count table.",
            # },
        },
    },
    # SelectCol is intentionally excluded from the ReAct action space. Final
    # projection is deterministic from table-level specs after dc/prep ops.
    # Not used in benchmark dc_ops; disabled to keep the action space attributable.
    # "escape_hatch": {
    #     "purpose": (
    #         "Use only when the structured operations cannot express a local repair. "
    #         "The function must consume the current DataFrame and return one DataFrame."
    #     ),
    #     "operations": {
    #         "CodeGeneration": {
    #             "params": {
    #                 "func": (
    #                     "def transform(tables):\n"
    #                     "    df = tables[0]\n"
    #                     "    return df"
    #                 )
    #             },
    #             "description": "Arbitrary pandas transform over the current single table.",
    #         }
    #     },
    # },
}

ALLOWED_OPS: dict[str, dict[str, Any]] = {
    op: {**meta, "category": category}
    for category, category_meta in OPERATION_CATEGORIES.items()
    for op, meta in category_meta["operations"].items()
}

EXECUTOR_ONLY_OPS: dict[str, dict[str, Any]] = {
    "SelectCol": {
        "params": {"columns": ["col"]},
        "description": "Deterministic final projection from table-level specs.",
        "category": "projection",
    }
}

OP_ALIASES = {
    "pivot": "Pivot",
    "rename": "Rename",
    "stack": "Stack",
    "unpivot": "Stack",
    "explode": "Explode",
    "wide_to_long": "WideToLong",
    "widetolong": "WideToLong",
    "transpose": "Transpose",
    "cast": "CastType",
    "casttype": "CastType",
    "dropcolumn": "DropColumn",
    "drop_column": "DropColumn",
    "splitcolumn": "SplitColumn",
    "split_column": "SplitColumn",
    "concatenate": "Concatenate",
    "standardizestring": "StandardizeString",
    "standardize_string": "StandardizeString",
    "standardizedatetime": "StandardizeDatetime",
    "standardize_datetime": "StandardizeDatetime",
    # Aliases for operations outside benchmark dc_ops are intentionally disabled.
    # "select": "SelectCol",
    # "selectcol": "SelectCol",
    # "filter": "Filter",
    # "sort": "Sort",
    # "groupby": "GroupBy",
    # "group_by": "GroupBy",
    # "dropna": "DropNulls",
    # "dropnulls": "DropNulls",
    # "deduplicate": "Deduplicate",
    # "topk": "TopK",
    # "addnewcolumn": "AddNewColumn",
    # "add_new_column": "AddNewColumn",
    # "calculatestatistic": "CalculateStatistic",
    # "calculate_statistic": "CalculateStatistic",
    # "count": "Count",
    # "codegeneration": "CodeGeneration",
    # "code_generation": "CodeGeneration",
}


def canonical_op_name(op: Any) -> str:
    raw = str(op or "").strip()
    if raw in ALLOWED_OPS or raw in EXECUTOR_ONLY_OPS:
        return raw
    key = re.sub(r"[^A-Za-z0-9_]+", "", raw).lower()
    if key in OP_ALIASES:
        return OP_ALIASES[key]
    raise ValueError(f"Unsupported op: {op}")


def operation_space_text() -> str:
    return """structural_oriented:
- Transpose: {"op":"Transpose","params":{"use_first_column_as_header":true,"new_index_column":"row_id"},"table_indices":[0]}
  Use for one-row/one-col mapping or when attributes are in rows. First column values become headers; old column names become row_id. Do not use for ordinary many-column unpivot.
- Stack: {"op":"Stack","params":{"id_vars":["id_col"],"value_vars":["wide_col1","wide_col2"],"var_name":"attribute","value_name":"value"},"table_indices":[0]}
  Use for many sibling wide columns. id_vars/value_vars must be current columns. For very wide tables use value_vars="__all_except_id_vars__"; do not enumerate hundreds of columns.
- Stack with first-row labels: {"op":"Stack","params":{"id_vars":["id_col"],"value_vars":"__all_except_id_vars__","var_name":"attribute","value_name":"value","use_first_row_as_variable_labels":true},"table_indices":[0]}
  Use only when first data row stores real labels AND later rows store values. Do not use if the table has only one data row.
- Pivot: {"op":"Pivot","params":{"index":["id_col"],"columns":"attribute_col","values":"value_col","aggfunc":"first"},"table_indices":[0]}
  Use for long key/value rows. index/columns/values must be current columns.
- WideToLong: {"op":"WideToLong","params":{"subnames":["score"],"i":["id_col"],"j":"suffix","sep":"_","suffix":"\\w+"},"table_indices":[0]}
  Use for repeated column groups like score_1, score_2.
- Explode: {"op":"Explode","params":{"column":"list_like_col","split_comma":true},"table_indices":[0]}
  Use for list-like or comma-separated cells.

non_structural_oriented:
- Rename: {"op":"Rename","params":{"rename_map":[{"old_name":"old_col","new_name":"new_col"}]},"table_indices":[0]}
  Rename existing columns only; it does not copy/create columns.
- SplitColumn: {"op":"SplitColumn","params":{"source_column":"packed_col","target_columns":["a","b"],"func":"def transform(s):\\n    parts = str(s).split('|', 1)\\n    return [parts[0], parts[1] if len(parts)>1 else None]"},"table_indices":[0]}
  source_column must exist. func must be def transform(s), not lambda, and return values aligned to target_columns.
- Concatenate: {"op":"Concatenate","params":{"concatenate_columns":["col1","col2"],"target_column":"new_col","func":"def transform(row):\\n    return str(row['col1']) + '-' + str(row['col2'])"},"table_indices":[0]}
  concatenate_columns must exist. func must be def transform(row).
- StandardizeString: {"op":"StandardizeString","params":{"column_name":"col","func":"def transform(s):\\n    return str(s).strip().lower()"},"table_indices":[0]}
  column_name must exist. Use to strip quotes/spaces/case.
- StandardizeDatetime: {"op":"StandardizeDatetime","params":{"column_name":"date_col","date_format":"%Y-%m-%d"},"table_indices":[0]}
  column_name must exist.
- CastType: {"op":"CastType","params":{"column":"col","dtype":"str|int|float|datetime64|bool"},"table_indices":[0]}
  column must exist; cast does not create columns.
- DropColumn: {"op":"DropColumn","params":{"drop_columns":["unused_col"]},"table_indices":[0]}
  Drop existing irrelevant columns only after required columns are safe."""


def operation_names() -> list[str]:
    return list(ALLOWED_OPS.keys())
