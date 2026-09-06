"""Offline: infer linking-oriented metadata for every table in a collection.

Input  : datasets/<Dataset>/input_tables/*.pkl   (the whole table collection)
Output : results/table_discovery/metadata/<Dataset>/table_metadata.jsonl
         one record per table:
           {table_file, original_headers, recovered_schema,
            potential_issue, rationale, shape, llm_usage}

Why this stage exists
---------------------
A raw header row is frequently not a header at all. Transposed tables put field
names in the first column, pivoted tables hide attribute names in cells, and
warehouse tables carry abbreviated or cryptic names. Selecting tables by those
strings judges a table by a name that does not describe its contents. Here an
LLM sees the header row plus the first few rows of each table and returns the
schema that best describes the attributes the table actually provides.

This is collection-level, not task-level: each table is profiled exactly once,
independently of which question might use it, so the cost is |tables|, not
|tasks| x |tables per task|. The output is a static artefact that the online
stage (table_selection.py) reads for every question.

Run:
    python -m table_discovery.meta_inferrence --dataset Beaver-Prep
    python -m table_discovery.meta_inferrence --dataset Synth-Bird --limit 5
"""

from __future__ import annotations

import argparse
import copy
import json
import time
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from common import dataset as DS
from common import paths as P
from common.io_utils import append_jsonl, load_jsonl_by_key
from common.llm_client import llm_generate_setup


PROMPT_TEMPLATE = """You are recovering a linking-oriented schema for a raw table from a data-preparation benchmark.

Background:
Some raw tables may have schema issues that make semantic linking difficult. For example, the real schema may be hidden in cell values due to non-relational layouts such as pivoted, stacked, unpivoted, or transposed tables. Or the visible headers may be abbreviated, cryptic, incomplete, or even not real attributes. 

Goal:
Given only the table headers and top rows, recover the schema that best describes the semantic attributes provided by this table, if schema issues detected. The recovered schema should make it easier to link a natural-language question to this table during retrieval or data preparation.

The recovered schema should:
- preserve the original schema when the headers are already meaningful;
- rename abbreviated or cryptic headers when their meanings are clear from cell values;
- expose hidden attributes when real column names appear inside cells;
- reshape non-relational layouts conceptually when this is necessary to reveal the semantic schema;
- avoid inventing attributes that are not supported by the headers or cell values.

Common issue types:
- no obvious issue: headers already describe meaningful semantic attributes.
- rename/refine issue: current headers do not accurately express the true column semantics. This includes abbreviated, cryptic, generic, misleading, encoded, or semantically incomplete headers.
- pivot-related issue: one column stores attribute names and another column stores their values.
- stack/unpivot-related issue: many sibling columns represent values of the same variable, e.g. countries, years, months, or statuses.
- transpose-related issue: rows and columns appear swapped, and row values look like headers.
- concatenate-related issue: multiple columns jointly express one higher-level attribute, e.g. first_name + last_name -> full_name.
- split/decompose-related issue: one column contains multiple semantic parts.
- normalize/explode-related issue: one cell contains a list or set of values.
- mixed or other issue: multiple issues appear together, or the issue does not fit the above categories.

Rules:
- Be conservative. Do not invent schema attributes without evidence.
- Prefer schema names that are semantically meaningful for natural-language linking.
- If the original headers are already meaningful, keep them.
- For rename/refine, replace a header only when the column values provide enough evidence for a clearer semantic name; otherwise keep the original header and mention uncertainty.
- If real attributes appear in cell values, recover them as schema attributes.
- If sibling columns are values of the same variable, replace them with a variable column and a value column.
- If rows behave like headers, recover schema attributes from those row values.
- Preserve row granularity unless pivot, stack/unpivot, or transpose is clearly needed.
- If unsure, keep the original column names.

Few-shot examples:

Example 1: Pivot-related schema issue
Table:
raceId | attribute | value
---|---|---
1 | "year" | 2009
1 | "round" | 1

Output:
{{
  "potential issue": "pivot-related issue",
  "rationale": "The attribute column contains hidden schema attributes such as year and round, while the value column stores their values.",
  "recovered schema": ["raceId", "year", "round"]
}}

Example 2: Stack/unpivot-related schema issue
Table:
circuitId | name | Austria | Bahrain | Canada
---|---|---|---|---
1 | "Albert Park" | nan | nan | nan
2 | "Red Bull Ring" | 47.2197 | nan | nan

Output:
{{
  "potential issue": "stack/unpivot-related issue",
  "rationale": "Austria, Bahrain, and Canada are sibling country columns. They are better represented as a country variable and a value attribute for semantic linking.",
  "recovered schema": ["circuitId", "name", "country", "value"]
}}

Example 3: Rename/refine issue
Table:
col_a | col_b | date | amount
---|---|---|---
"Pizza" | "Food" | "2019-09-10" | 51.81
"Posters" | "Advertisement" | "2019-10-10" | 67.81

Output:
{{
  "potential issue": "rename/refine issue",
  "rationale": "The headers col_a and col_b are generic and do not accurately describe the column semantics. The cell values indicate that col_a is an expense item or description and col_b is an expense category.",
  "recovered schema": ["expense_description", "expense_category", "date", "amount"]
}}

Example 4: Concatenate-related schema issue
Table:
event_id | item1 | item2 | item3 | amount
---|---|---|---|---
"e1" | "pizza" | "drinks" | "plates" | 72

Output:
{{
  "potential issue": "concatenate-related issue",
  "rationale": "item1, item2, and item3 jointly describe the purchased items for the same event, so they correspond to one higher-level item description attribute.",
  "recovered schema": ["event_id", "item_description", "amount"]
}}

Example 5: No obvious issue
Table:
account_id | district_id | frequency | date
---|---|---|---
1 | 18 | "monthly" | "1995-03-24"

Output:
{{
  "potential issue": "no obvious issue",
  "rationale": "The headers are already meaningful relational attributes and can be directly used for semantic linking.",
  "recovered schema": ["account_id", "district_id", "frequency", "date"]
}}

Now analyze this table.

Table:
{table_preview}

Return only valid JSON:
{{
  "potential issue": "...",
  "rationale": "...",
  "recovered schema": ["..."]
}}
"""


BEAVER_PROMPT_TEMPLATE = """You are recovering a linking-oriented schema for a raw table from the Beaver enterprise data warehouse benchmark.

Background:
Beaver tables often use warehouse-style column names. These names may look abbreviated or coded, but many of them carry important table identity, domain, key, and join semantics. Prefixes and suffixes such as FAC_, FCLT_, SIS_, TIP_, LIBRARY_, COURSE_CATALOG_, SUBJECT_, _KEY, _CODE, and _ID are often meaningful and should usually be preserved.

Goal:
Given only the table headers and top rows, produce a schema useful for schema linking while preserving Beaver-specific identity signals. The recovered schema should not make different Beaver table families look interchangeable.

Beaver-specific rules:
- Be conservative. Prefer keeping original headers when they are meaningful warehouse attributes.
- Do not remove or generalize table-family prefixes such as FAC_, FCLT_, SIS_, TIP_, LIBRARY_, COURSE_CATALOG_, and SUBJECT_ when they help distinguish related tables.
- Do not remove KEY/CODE/ID suffixes unless the original header is clearly generic or misleading. These suffixes often identify bridge, dimension, and join columns.
- Do not rewrite FAC_* columns into generic names that could also describe FCLT_* tables, or TIP_* columns into generic names that could also describe LIBRARY_* tables.
- Preserve original headers for join keys and identifiers unless there is strong evidence from cell values that the header is wrong.
- You may add clearer semantic names only for truly generic, misleading, or non-real headers, or when a non-relational layout hides real attributes in cell values.
- Avoid inventing attributes that are not supported by the headers or cell values.

Common issue types:
- no obvious issue: headers already describe meaningful warehouse attributes.
- conservative rename/refine issue: only a small number of generic or misleading headers need refinement while identity-bearing headers are preserved.
- pivot-related issue: one column stores attribute names and another column stores their values.
- stack/unpivot-related issue: many sibling columns represent values of the same variable.
- transpose-related issue: rows and columns appear swapped, and row values look like headers.
- split/decompose-related issue: one column contains multiple semantic parts.
- mixed or other issue: multiple issues appear together.

Examples:

Example 1: Preserve table-family and key signals
Table:
FCLT_ROOM_KEY | BUILDING_ROOM | FCLT_BUILDING_KEY | FLOOR | FCLT_FLOOR_KEY | ROOM | ORGANIZATION_NAME
---|---|---|---|---|---|---
1 | "10-250" | "10" | "2" | "10-2" | "250" | "Physics"

Output:
{{
  "potential issue": "no obvious issue",
  "rationale": "The FCLT_ prefixes and _KEY suffixes distinguish this facilities table and its join keys. Generic aliases like room_key or building_key would make it easier to confuse with FAC_* tables.",
  "recovered schema": ["FCLT_ROOM_KEY", "BUILDING_ROOM", "FCLT_BUILDING_KEY", "FLOOR", "FCLT_FLOOR_KEY", "ROOM", "ORGANIZATION_NAME"]
}}

Example 2: Preserve status dimension identity
Table:
LIBRARY_MATERIAL_STATUS_KEY | LIBRARY_MATERIAL_STATUS_CODE | LIBRARY_MATERIAL_STATUS | WAREHOUSE_LOAD_DATE
---|---|---|---
1 | "A" | "Available" | "2024-12-19"

Output:
{{
  "potential issue": "no obvious issue",
  "rationale": "The headers clearly identify a LIBRARY material-status dimension table. The KEY and CODE columns are important for linking and should not be collapsed into generic status names.",
  "recovered schema": ["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS_CODE", "LIBRARY_MATERIAL_STATUS", "WAREHOUSE_LOAD_DATE"]
}}

Example 3: Refine only truly generic headers
Table:
COL_A | COL_B | TERM_CODE | SUBJECT_ID
---|---|---|---
"Biology" | "Lecture" | "2023FA" | "7.01"

Output:
{{
  "potential issue": "conservative rename/refine issue",
  "rationale": "COL_A and COL_B are generic and their values suggest department/topic and session/type. TERM_CODE and SUBJECT_ID are meaningful identifiers and should be preserved.",
  "recovered schema": ["department_or_topic", "course_format", "TERM_CODE", "SUBJECT_ID"]
}}

Now analyze this table.

Table:
{table_preview}

Return only valid JSON:
{{
  "potential issue": "...",
  "rationale": "...",
  "recovered schema": ["..."]
}}
"""


def parse_llm_json_response(resp: dict[str, Any]) -> dict[str, Any]:
    text = resp.get("text", "")

    if isinstance(text, dict):
        return text

    if not isinstance(text, str):
        return {
            "potential issue": "parse error",
            "rationale": "LLM response text is not a string or dict.",
            "recovered schema": [],
            "raw_response": str(text),
        }

    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        parsed = json.loads(text)
    except Exception:
        return {
            "potential issue": "parse error",
            "rationale": "Failed to parse LLM response as valid JSON.",
            "recovered schema": [],
            "raw_response": text,
        }

    if not isinstance(parsed, dict):
        return {
            "potential issue": "parse error",
            "rationale": "Parsed LLM response is not a JSON object.",
            "recovered schema": [],
            "raw_response": parsed,
        }

    return parsed


def normalize_schema_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    schema = []
    for x in value:
        if isinstance(x, (str, int, float)):
            col = str(x).strip()
            if col:
                schema.append(col)

    return schema


def contains_truncation_marker(schema: list[str]) -> bool:
    for col in schema:
        text = str(col).lower()
        if "omitted" in text or "truncated" in text or text.strip(". ") == "":
            return True
    return False


def merge_info(
    original_headers: list[str],
    llm_info: dict[str, Any],
    benchmark: str = "",
) -> list[str]:
    """
    The prompt asks the LLM to output:
      {
        "potential issue": "...",
        "rationale": "...",
        "recovered schema": [...]
      }

    Therefore this function should read "recovered schema".
    If the LLM output is missing or invalid, fall back to original headers.
    """
    recovered_schema = normalize_schema_list(llm_info.get("recovered schema"))

    if benchmark == "beaver":
        # Beaver table-family prefixes and KEY/CODE/ID fields are often the
        # useful linking signal. If the LLM returns a truncated/incomplete
        # schema, keep the complete original warehouse schema.
        if (
            not recovered_schema
            or contains_truncation_marker(recovered_schema)
            or len(recovered_schema) != len(original_headers)
        ):
            return original_headers

    if recovered_schema and all("<" not in x and ">" not in x for x in recovered_schema):
        return recovered_schema

    return original_headers



TWO_STEP_PROMPT_TEMPLATE = '''You are recovering a linking-oriented schema for a raw table from a data-preparation benchmark.

Background:
Some raw tables may have schema issues that make semantic linking difficult. For example, the real schema may be hidden in cell values due to non-relational layouts such as pivoted, stacked, unpivoted, or transposed tables. Or the visible headers may be abbreviated, cryptic, incomplete, or even not real attributes.

Goal:
Given only the table headers and top rows, recover the schema that best describes the semantic attributes provided by this table. Work in TWO EXPLICIT STEPS.

STEP 1 - Collect layout evidence.
Examine the headers and cell values and list the concrete observations that indicate a data-preparation operation would be needed before this table is relationally usable. Each observation must cite the specific headers or cell values it comes from, and name the operation it implies. Only report what you can actually see; if the table is already relational, return an empty list.

Operations to look for, and the evidence that signals each:
- rename/refine: a header is abbreviated, cryptic, generic (col_a, value, field1), encoded, or misleading, while its cell values reveal a clearer meaning.
- pivot: one column holds attribute NAMES and another holds their values, so a single entity spans several rows.
- stack/unpivot: many sibling columns are values of one variable (countries, years, months, statuses) rather than distinct attributes.
- transpose: the first column holds strings that read like field names and the rows behave like columns.
- concatenate: several columns jointly express one higher-level attribute (first_name + last_name, item1/item2/item3).
- split/decompose: one column packs several semantic parts into each cell.
- normalize/explode: one cell holds a list or set of values.

STEP 2 - Derive the attributes.
Using ONLY the evidence from step 1 plus the visible headers, write the attribute list that describes what this table semantically provides, as it would be used to link a natural-language question to this table.

Rules for step 2:
- Every change to the original headers must be traceable to a step-1 observation. If step 1 found no evidence, return the original headers unchanged.
- Be conservative. Do not invent attributes without evidence.
- For rename/refine, replace a header only when the cell values give enough evidence for a clearer name; otherwise keep the original header.
- If real attributes appear in cell values, recover them as attributes.
- If sibling columns are values of one variable, replace them with a variable column and a value column.
- If rows behave like headers, recover attributes from those row values.
- Preserve row granularity unless pivot, stack/unpivot, or transpose is clearly needed.
- Prefer names that are semantically meaningful for natural-language linking.

Few-shot examples:

Example 1: Pivot-related schema issue
Table:
raceId | attribute | value
---|---|---
1 | "year" | 2009
1 | "round" | 1

Output:
{{
  "evidence": [
    {{"observation": "the attribute column holds the strings 'year' and 'round', which are field names rather than data values", "columns": ["attribute", "value"], "implied_operation": "pivot"}},
    {{"observation": "raceId 1 repeats across rows, so one race is split over several rows", "columns": ["raceId"], "implied_operation": "pivot"}}
  ],
  "potential issue": "pivot-related issue",
  "rationale": "The attribute column contains hidden schema attributes such as year and round, while the value column stores their values.",
  "recovered schema": ["raceId", "year", "round"]
}}

Example 2: Stack/unpivot-related schema issue
Table:
circuitId | name | Austria | Bahrain | Canada
---|---|---|---|---
1 | "Albert Park" | nan | nan | nan
2 | "Red Bull Ring" | 47.2197 | nan | nan

Output:
{{
  "evidence": [
    {{"observation": "Austria, Bahrain and Canada are sibling headers that are all country names, i.e. values of one variable rather than distinct attributes", "columns": ["Austria", "Bahrain", "Canada"], "implied_operation": "stack/unpivot"}},
    {{"observation": "their cells hold a single measure of the same kind (numbers or nan)", "columns": ["Austria", "Bahrain", "Canada"], "implied_operation": "stack/unpivot"}}
  ],
  "potential issue": "stack/unpivot-related issue",
  "rationale": "Austria, Bahrain, and Canada are sibling country columns. They are better represented as a country variable and a value attribute for semantic linking.",
  "recovered schema": ["circuitId", "name", "country", "value"]
}}

Example 3: Rename/refine issue
Table:
col_a | col_b | date | amount
---|---|---|---
"Pizza" | "Food" | "2019-09-10" | 51.81
"Posters" | "Advertisement" | "2019-10-10" | 67.81

Output:
{{
  "evidence": [
    {{"observation": "col_a is a generic header whose values 'Pizza' and 'Posters' are purchased items", "columns": ["col_a"], "implied_operation": "rename/refine"}},
    {{"observation": "col_b is a generic header whose values 'Food' and 'Advertisement' are expense categories", "columns": ["col_b"], "implied_operation": "rename/refine"}},
    {{"observation": "date and amount are already meaningful and their values agree with the names", "columns": ["date", "amount"], "implied_operation": "none"}}
  ],
  "potential issue": "rename/refine issue",
  "rationale": "The headers col_a and col_b are generic and do not accurately describe the column semantics. The cell values indicate that col_a is an expense item or description and col_b is an expense category.",
  "recovered schema": ["expense_description", "expense_category", "date", "amount"]
}}

Example 4: Concatenate-related schema issue
Table:
event_id | item1 | item2 | item3 | amount
---|---|---|---|---
"e1" | "pizza" | "drinks" | "plates" | 72

Output:
{{
  "evidence": [
    {{"observation": "item1, item2 and item3 are numbered siblings whose values are all purchased items for the same event", "columns": ["item1", "item2", "item3"], "implied_operation": "concatenate"}}
  ],
  "potential issue": "concatenate-related issue",
  "rationale": "item1, item2, and item3 jointly describe the purchased items for the same event, so they correspond to one higher-level item description attribute.",
  "recovered schema": ["event_id", "item_description", "amount"]
}}

Example 5: No obvious issue
Table:
account_id | district_id | frequency | date
---|---|---
1 | 18 | "monthly" | "1995-03-24"

Output:
{{
  "evidence": [],
  "potential issue": "no obvious issue",
  "rationale": "The headers are already meaningful relational attributes and can be directly used for semantic linking.",
  "recovered schema": ["account_id", "district_id", "frequency", "date"]
}}

Now analyze this table.

Table:
{table_preview}

Return only valid JSON:
{{
  "evidence": [
    {{"observation": "...", "columns": ["..."], "implied_operation": "..."}}
  ],
  "potential issue": "...",
  "rationale": "...",
  "recovered schema": ["..."]
}}
'''


TWO_STEP_BEAVER_PROMPT_TEMPLATE = '''You are recovering a linking-oriented schema for a raw table from the Beaver enterprise data warehouse benchmark.

Background:
Beaver tables use warehouse-style column names. These names may look abbreviated or coded, but many carry important table identity, domain, key, and join semantics. Prefixes and suffixes such as FAC_, FCLT_, SIS_, TIP_, LIBRARY_, COURSE_CATALOG_, SUBJECT_, _KEY, _CODE, and _ID are usually meaningful and should be preserved.

Goal:
Given only the table headers and top rows, produce a schema useful for schema linking while preserving Beaver-specific identity signals. Work in TWO EXPLICIT STEPS.

STEP 1 - Collect layout evidence.
List the concrete observations that indicate a data-preparation operation would be needed before this table is relationally usable. Each observation must cite the specific headers or cell values it comes from, and name the operation it implies. Report only what you can see; if the table is already a clean warehouse relation, return an empty list.

Operations to look for, and the evidence that signals each:
- rename/refine: a header is TRULY generic (COL_A, FIELD1, VALUE), misleading, or not a real attribute, while its cell values reveal a clearer meaning. A warehouse abbreviation with a consistent family prefix or a KEY/CODE/ID suffix is NOT evidence of this.
- pivot: one column holds attribute NAMES and another holds their values.
- stack/unpivot: many sibling columns are values of one variable.
- transpose: the first column holds strings that read like field names.
- split/decompose: one column packs several semantic parts into each cell.

Explicitly NOT evidence, and must not be reported:
- a family prefix such as FAC_, FCLT_, SIS_, TIP_, LIBRARY_, COURSE_CATALOG_, SUBJECT_
- a _KEY, _CODE or _ID suffix on an identifier or join column
- an abbreviation whose meaning is already clear from the values

STEP 2 - Derive the attributes.
Using ONLY the evidence from step 1 plus the visible headers, write the attribute list.

Rules for step 2:
- Every change to the original headers must be traceable to a step-1 observation. If step 1 found no evidence, return the original headers unchanged.
- Preserve table-family prefixes and KEY/CODE/ID suffixes; they distinguish related tables and identify bridge, dimension and join columns.
- Do not rewrite FAC_* columns into generic names that could also describe FCLT_* tables, or TIP_* columns into names that could also describe LIBRARY_* tables.
- Preserve original headers for join keys and identifiers unless cell values give strong evidence that the header is wrong.
- Do not invent attributes that the headers or cell values do not support.

Examples:

Example 1: Preserve table-family and key signals
Table:
FCLT_ROOM_KEY | BUILDING_ROOM | FCLT_BUILDING_KEY | FLOOR | FCLT_FLOOR_KEY | ROOM | ORGANIZATION_NAME
---|---|---|---|---|---|---
1 | "10-250" | "10" | "2" | "10-2" | "250" | "Physics"

Output:
{{
  "evidence": [],
  "potential issue": "no obvious issue",
  "rationale": "The FCLT_ prefixes and _KEY suffixes distinguish this facilities table and its join keys. Generic aliases like room_key or building_key would make it easier to confuse with FAC_* tables.",
  "recovered schema": ["FCLT_ROOM_KEY", "BUILDING_ROOM", "FCLT_BUILDING_KEY", "FLOOR", "FCLT_FLOOR_KEY", "ROOM", "ORGANIZATION_NAME"]
}}

Example 2: Preserve status dimension identity
Table:
LIBRARY_MATERIAL_STATUS_KEY | LIBRARY_MATERIAL_STATUS_CODE | LIBRARY_MATERIAL_STATUS | WAREHOUSE_LOAD_DATE
---|---|---|---
1 | "A" | "Available" | "2024-12-19"

Output:
{{
  "evidence": [],
  "potential issue": "no obvious issue",
  "rationale": "The headers clearly identify a LIBRARY material-status dimension table. The KEY and CODE columns are important for linking and should not be collapsed into generic status names.",
  "recovered schema": ["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS_CODE", "LIBRARY_MATERIAL_STATUS", "WAREHOUSE_LOAD_DATE"]
}}

Example 3: Refine only truly generic headers
Table:
COL_A | COL_B | TERM_CODE | SUBJECT_ID
---|---|---|---
"Biology" | "Lecture" | "2023FA" | "7.01"

Output:
{{
  "evidence": [
    {{"observation": "COL_A is a truly generic header and its values 'Biology' name a department or topic", "columns": ["COL_A"], "implied_operation": "rename/refine"}},
    {{"observation": "COL_B is a truly generic header and its values 'Lecture' name a course format", "columns": ["COL_B"], "implied_operation": "rename/refine"}},
    {{"observation": "TERM_CODE and SUBJECT_ID carry warehouse identifier semantics and must be preserved", "columns": ["TERM_CODE", "SUBJECT_ID"], "implied_operation": "none"}}
  ],
  "potential issue": "conservative rename/refine issue",
  "rationale": "COL_A and COL_B are generic and their values suggest department/topic and session/type. TERM_CODE and SUBJECT_ID are meaningful identifiers and should be preserved.",
  "recovered schema": ["department_or_topic", "course_format", "TERM_CODE", "SUBJECT_ID"]
}}

Now analyze this table.

Table:
{table_preview}

Return only valid JSON:
{{
  "evidence": [
    {{"observation": "...", "columns": ["..."], "implied_operation": "..."}}
  ],
  "potential issue": "...",
  "rationale": "...",
  "recovered schema": ["..."]
}}
'''


# ============================================================
# Table preview
# ============================================================

def _format_cell(value: Any, omitted_marker: str | None = None) -> str:
    if omitted_marker is not None and value == omitted_marker:
        return omitted_marker
    return f'"{value}"' if isinstance(value, str) else str(value)


def df_to_text(df: pd.DataFrame, cut_line: int = 10, cut_col: int = 20,
               max_len: int = 6000) -> str:
    """Render the head of a table as a markdown-ish block for the prompt.

    Wide tables are shown head-and-tail rather than as a prefix, because a
    prefix hides every measure column of a wide table.
    """
    if df is None:
        return "None"

    frame = copy.deepcopy(df)
    all_columns = list(df.columns)
    columns = all_columns
    omitted_columns = 0
    head_columns: list[Any] = []
    tail_columns: list[Any] = []
    if cut_col != -1 and len(all_columns) > cut_col:
        head_count = cut_col // 2
        tail_count = cut_col - head_count
        head_columns = all_columns[:head_count]
        tail_columns = all_columns[-tail_count:]
        columns = head_columns + tail_columns
        omitted_columns = len(all_columns) - len(columns)
        frame = frame[columns]

    if omitted_columns:
        display_columns = (
            [str(c).replace("\n", "\\n") for c in head_columns]
            + [f"... {omitted_columns} columns omitted ..."]
            + [str(c).replace("\n", "\\n") for c in tail_columns]
        )
    else:
        display_columns = [str(c).replace("\n", "\\n") for c in columns]

    ret = " | ".join(display_columns) + "\n"
    ret += "|".join("---" for _ in display_columns) + "\n"

    for i in range(len(frame)):
        if cut_line != -1 and i > cut_line - 1:
            ret += "......\n"
            break
        row = [x.replace("\n", "\\n") if isinstance(x, str) else x
               for x in frame.iloc[i].values]
        if omitted_columns:
            marker = f"... {omitted_columns} columns omitted ..."
            row = row[:len(head_columns)] + [marker] + row[len(head_columns):]
            ret += " | ".join(_format_cell(x, omitted_marker=marker) for x in row) + "\n"
        else:
            ret += " | ".join(_format_cell(x) for x in row) + "\n"

    ret = ret.strip()
    if len(ret) > max_len:
        return ret[:max_len] + "\n......\n[Truncated due to length]"
    if len(df) == 0:
        ret += "\n(The table is empty!!!)"
    return ret


def read_table_preview(path: Path, top_k: int = 10, cut_col: int = 20,
                       max_table_len: int = 6000):
    """(column names, prompt preview, shape) for one table file."""
    suffix = path.suffix.lower()
    if suffix == ".pkl":
        df = pd.read_pickle(path)
    elif suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".json", ".jsonl"}:
        df = pd.read_json(path, lines=suffix == ".jsonl")
    elif suffix in {".xls", ".xlsx"}:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported table format: {path}")
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    columns = [str(c) for c in df.columns]
    preview = df_to_text(df, cut_line=top_k, cut_col=cut_col, max_len=max_table_len)
    return columns, preview, tuple(df.shape)


# ============================================================
# Per-table inference
# ============================================================

PROMPT_STYLES = ("single", "two_step")

_TEMPLATES = {
    ("single", False): PROMPT_TEMPLATE,
    ("single", True): BEAVER_PROMPT_TEMPLATE,
    ("two_step", False): TWO_STEP_PROMPT_TEMPLATE,
    ("two_step", True): TWO_STEP_BEAVER_PROMPT_TEMPLATE,
}


def build_prompt(is_warehouse: bool, table_preview: str,
                 style: str = "single") -> str:
    """Pick the prompt variant.

    is_warehouse  Beaver uses the variant that preserves table-family prefixes
                  and KEY/CODE/ID suffixes, because those are exactly what
                  distinguishes near-duplicate table families.
    style         "single"   ask for the schema directly (default; this is what
                             every recorded run used)
                  "two_step" make the reasoning explicit: first list the layout
                             evidence with the operation each observation
                             implies, then derive the attributes from that
                             evidence alone

    Both styles return the same JSON keys, plus "evidence" for two_step, so
    parsing and everything downstream is unaffected by the choice.
    """
    if style not in PROMPT_STYLES:
        raise ValueError(f"unknown prompt style {style!r}; choose from {PROMPT_STYLES}")
    return _TEMPLATES[(style, bool(is_warehouse))].format(table_preview=table_preview)


def infer_table_metadata(table_file: str, table_path: Path, is_warehouse: bool,
                         model: str, top_k: int, cut_col: int,
                         max_table_len: int,
                         style: str = "single") -> dict[str, Any]:
    """Profile one table: preview it, ask the LLM, merge the answer with the
    original headers."""
    columns, preview, shape = read_table_preview(
        table_path, top_k=top_k, cut_col=cut_col, max_table_len=max_table_len)

    prompt = build_prompt(is_warehouse, preview, style=style)

    llm_error = None
    usage = {"input_tokens": None, "output_tokens": None, "elapsed_seconds": None}
    try:
        t0 = time.perf_counter()
        resp = llm_generate_setup(prompt, model=model, json_format=True)
        usage = {
            "input_tokens": resp.get("input_tokens"),
            "output_tokens": resp.get("output_tokens"),
            "elapsed_seconds": round(time.perf_counter() - t0, 3),
        }
        llm_info = parse_llm_json_response(resp)
    except Exception as exc:  # noqa: BLE001 - record and continue to the next table
        llm_error = str(exc)
        llm_info = {"potential issue": "llm error", "rationale": str(exc),
                    "recovered schema": []}

    recovered = merge_info(
        original_headers=columns,
        llm_info=llm_info,
        benchmark="beaver" if is_warehouse else "",
    )

    return {
        "table_file": table_file,
        "original_headers": columns,
        "recovered_schema": recovered,
        "potential_issue": str(llm_info.get("potential issue", "")),
        "rationale": str(llm_info.get("rationale", "")),
        # Present only for style="two_step": the step-1 observations the
        # step-2 attribute list was derived from.
        "evidence": llm_info.get("evidence") or [],
        "prompt_style": style,
        "shape": list(shape),
        "llm_error": llm_error,
        "llm_usage": usage,
    }


# ============================================================
# Entry point
# ============================================================

def build_table_metadata(dataset: str, out_path: Path, model: str,
                         table_files: list[str] | None = None,
                         input_tables: Path | None = None,
                         top_k: int = 10, cut_col: int = 20,
                         max_table_len: int = 6000, limit: int = 0,
                         overwrite: bool = False, sleep: float = 0.0,
                         style: str = "single") -> Path:
    """Profile every table of one collection, writing one JSONL record each.

    The output file is also the cache: a table already present is skipped, so an
    interrupted run resumes and a re-run costs nothing.
    """
    ds = DS.resolve(dataset) if input_tables is None else None
    tables_dir = Path(input_tables) if input_tables is not None else ds.input_tables
    if not tables_dir.exists():
        raise FileNotFoundError(f"input table directory not found: {tables_dir}")

    if table_files is None:
        table_files = sorted(p.name for p in tables_dir.iterdir()
                             if p.suffix.lower() in {".pkl", ".csv", ".json", ".jsonl",
                                                     ".xls", ".xlsx"})

    # Beaver is an enterprise warehouse: its column names carry table identity
    # and join semantics that the generic prompt would generalize away.
    is_warehouse = DS.SOURCE_NAME.get(dataset, dataset) == "beaver"

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and out_path.exists():
        out_path.unlink()

    done = load_jsonl_by_key(out_path, "table_file")
    pending = [t for t in table_files if t not in done]
    if limit and limit > 0:
        pending = pending[:limit]

    print(f"[meta] dataset={dataset} warehouse_prompt={is_warehouse} style={style}")
    print(f"[meta] tables={len(table_files)} cached={len(done)} to_process={len(pending)}")
    print(f"[meta] input tables: {tables_dir}")
    print(f"[meta] output:       {out_path}")

    written = 0
    for table_file in tqdm(pending, desc="Profiling tables"):
        table_path = tables_dir / table_file
        if not table_path.exists():
            print(f"[meta] WARNING table file not found, skipped: {table_file}")
            continue
        record = infer_table_metadata(
            table_file=table_file, table_path=table_path,
            is_warehouse=is_warehouse, model=model,
            top_k=top_k, cut_col=cut_col, max_table_len=max_table_len,
            style=style)
        append_jsonl(out_path, record)
        written += 1
        if sleep > 0:
            time.sleep(sleep)

    print(f"[meta] wrote {written} new records; {len(done) + written} tables profiled in total")
    return out_path


def load_table_metadata(path: Path) -> dict[str, dict[str, Any]]:
    """{table_file: record} from a metadata JSONL written by this module."""
    return load_jsonl_by_key(Path(path), "table_file")


def default_metadata_path(dataset: str, out_dir: str | None = None) -> Path:
    paths = P.resolve(dataset, out_dir=out_dir, group="metadata")
    return paths.out("table_metadata.jsonl")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Offline: infer linking-oriented metadata for a table collection.")
    parser.add_argument("--dataset", type=str, default="Beaver-Prep",
                        help="Dataset name, e.g. Beaver-Prep, Synth-Bird, Synth-Spider.")
    parser.add_argument("--input-tables", type=Path, default=None,
                        help="Override the table collection directory.")
    parser.add_argument("--out", type=Path, default=None,
                        help="Override the output JSONL path. Default: "
                             "results/table_discovery/metadata/<Dataset>/table_metadata.jsonl")
    parser.add_argument("--model", type=str, default="gpt-5-2025-08-07",
                        help="LLM used for schema recovery.")
    parser.add_argument("--top-k", type=int, default=10,
                        help="Rows of each table shown to the LLM.")
    parser.add_argument("--cut-col", type=int, default=20,
                        help="Columns shown (head and tail); -1 shows all.")
    parser.add_argument("--max-table-len", type=int, default=6000,
                        help="Character cap on the table preview.")
    parser.add_argument("--limit", type=int, default=0,
                        help="Profile at most N not-yet-cached tables (0 = all). "
                             "Use it for a smoke test.")
    parser.add_argument("--tables", type=str, nargs="+", default=None,
                        help="Profile only these table file names.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Discard the existing metadata file and start over.")
    parser.add_argument("--sleep", type=float, default=0.0,
                        help="Seconds to wait between calls.")
    parser.add_argument("--style", choices=list(PROMPT_STYLES), default="single",
                        help="Prompt formulation. 'single' (default) asks for the "
                             "schema directly and reproduces every recorded run. "
                             "'two_step' first extracts operation-related evidence, "
                             "then derives the attributes from it.")
    return parser.parse_args()


if __name__ == "__main__":
    a = parse_args()
    build_table_metadata(
        dataset=a.dataset,
        out_path=a.out or default_metadata_path(a.dataset),
        model=a.model,
        table_files=a.tables,
        input_tables=a.input_tables,
        top_k=a.top_k,
        cut_col=a.cut_col,
        max_table_len=a.max_table_len,
        limit=a.limit,
        overwrite=a.overwrite,
        sleep=a.sleep,
        style=a.style,
    )
