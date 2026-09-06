from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from data_loader import append_jsonl, find_table_file, load_jsonl
from joinability import compact_joinability_for_prompt, compute_joinability_signal, load_neighbor_tables
from table_executor import df_to_cotable, load_table


DEFAULT_EXAMPLES_DIR = Path(__file__).resolve().parent / "table_specs_examples"


SPEC_PROMPT_TEMPLATE = """You are reifying a natural-language question into a query-conditioned relational model (T, S).

Definitions:
- T is a set of factual relational views, one view per selected raw table.
- S is a SQL reasoning program over T that answers the question.

Your job is a two-stage planning task:
Stage 1: For each selected raw table, infer a factual relational view T_i that can be locally materialized from that raw table after data preparation.
Stage 2: Write SQLite-compatible SQL S over only these T_i views to answer the question. S is not written over the raw tables directly. The downstream executor registers materialized T_i views in an in-memory SQLite database, so S must use SQLite syntax and functions.

Consequence:
- Every column needed by S must first appear as a factual, materializable column in some T_i created from its corresponding raw table.
- Do not move Stage-2 SQL logic into Stage-1 T columns. Joins, filters, grouping, ordering, aggregation, ranking, and final answer computation belong in S, not in T.
- Stage 1 must perform local schema repair conceptually. If a raw table uses key-value rows, transposed attributes, packed columns, or wide repeated columns, T_i should expose the repaired relational columns directly. Do not leave local repair to S using CASE WHEN, attribute/value filtering, SPLIT_PART, SUBSTRING_INDEX, or pivot-like SQL unless the raw table is genuinely intended to remain a key-value fact table.
- If a raw table has non-relational layout, hidden schema, transposed attributes, key/value rows, packed columns, or abbreviated/noisy headers, T_i should describe the repaired relational view schema that S can query.

Input note about recovered headers:
Recovered headers are inferred schema hints produced from raw table content. They may expose hidden schema caused by non-relational layouts, transposed tables, pivoted key-value layouts, packed columns, or abbreviated headers. They are NOT ground truth. Use them as soft evidence together with the raw table preview and the question.

Hard separation:
- T contains factual columns that can be materialized from raw tables after local data preparation.
- S contains joins, filters, comparisons, grouping, ordering, limits, aggregation, and final answer computation.
- Do NOT put computed condition/result columns in T, such as is_cze, has_korean, has_japanese, is_draw, is_highest, count, total, rank, or top_1. Put those computations in S.

Output rules:
{join_requirement}
- Use one view per selected table, named T1, T2, ... in the same order as the selected tables. Do not drop a selected table unless it is clearly irrelevant noise.
- Do not collapse cross-table semantics into a single T_i. If a value or filter requires another selected table, keep the local operand/join columns in T_i and express the cross-table logic in S.
- Each T_i should describe only the factual relational columns materializable from its own raw table after local repair.
- Keep each T_i compact and semantically named. Prefer the minimum set of columns needed by S plus necessary entity/join keys.
- Do NOT expand cell values, IDs, categories, entity instances, years, names, or repeated records into many separate columns such as name_1, name_2, region_1, power_flag_428, power_flag_700, etc. Those values should usually remain rows under a small number of semantic columns, e.g., entity_id, attribute, value, name, region, population, power_id, power_flag.
- If many similar columns would be needed only because the raw table is wide or repeated, use a compact relational schema and let S filter/group rows. A good T_i usually has clear semantic columns, not dozens of enumerated columns.
- If a one-row wide table maps column headers to values, create a compact two-column mapping view after transpose, e.g., hero_id/power_id. Do not invent a has_power flag when every non-id wide column already represents an existing mapping row.
- Do NOT create semantic shortcut columns that already answer a filter or aggregation condition, such as isBanned, isDraw, isCzech, hasKorean, noJapanese, top, rank, count, total, or percentage. Keep the operand columns instead, such as status, format, language, borderColor, uuid, id, score, date, amount.
- For count/aggregation/order/filter questions, T must retain the entity id and operand columns needed by S. For example, COUNT(cards.id) needs id; banned cards need legalities.status, not an isBanned flag; draw matches need home_team_goal and away_team_goal, not an isDraw flag.
- Each CREATE TABLE must include column names and SQL types.
- Include PRIMARY KEY only when it is reasonably inferable.
- column_comments is optional and sparse. Include comments only for ambiguous, abbreviated, repaired, renamed, or critical columns. Do not comment obvious columns.
- S must be a SQLite-compatible SQL query over T1, T2, ... only. S may use joins, filters, grouping, ordering, aggregation, and subqueries when needed.
- Avoid non-SQLite functions or syntax such as SUBSTRING_INDEX, SPLIT_PART, DATE 'YYYY-MM-DD', QUALIFY, ILIKE, ARRAY, or vendor-specific casts. Prefer SQLite-compatible expressions such as substr/instr, LIKE, CAST(... AS ...), date('YYYY-MM-DD'), and standard CASE WHEN.
- Every column referenced in S must appear in the corresponding CREATE TABLE.
- Return valid JSON only.

Few-shot examples:
{examples_text}

Question:
{question}

Selected tables:
{tables_text}

Joinability hints:
{joinability_text}

Return only valid JSON with this schema:
{{
  "T": [
    {{
      "table_file": "...",
      "view_name": "T1",
      "create_table_sql": "CREATE TABLE T1 (...);",
      "column_comments": {{
        "ambiguous_or_critical_column": "short meaning or why needed"
      }}
    }}
  ],
  "S": "SELECT ..."
}}
"""

def normalize_columns(cols: list[Any]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for col in cols or []:
        text = str(col).strip()
        if text and text not in seen:
            out.append(text)
            seen.add(text)
    return out


def _split_sql_items(body: str) -> list[str]:
    items: list[str] = []
    cur: list[str] = []
    depth = 0
    quote: str | None = None
    for ch in body:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in {"`", "\"", "'"}:
            quote = ch
            cur.append(ch)
        elif ch == "(":
            depth += 1
            cur.append(ch)
        elif ch == ")":
            depth = max(depth - 1, 0)
            cur.append(ch)
        elif ch == "," and depth == 0:
            item = "".join(cur).strip()
            if item:
                items.append(item)
            cur = []
        else:
            cur.append(ch)
    item = "".join(cur).strip()
    if item:
        items.append(item)
    return items


def _clean_sql_identifier(name: str) -> str:
    return str(name).strip().strip("`").strip()


def parse_create_table_sql(create_sql: str) -> dict[str, Any]:
    create_sql = str(create_sql or "")
    match = re.search(r"CREATE\s+TABLE\s+[`\"]?([A-Za-z_][A-Za-z0-9_]*)[`\"]?\s*\((.*)\)\s*;?\s*$", create_sql, flags=re.I | re.S)
    if not match:
        return {"view_name": "", "columns": [], "primary_key": [], "column_types": {}}
    view_name = match.group(1)
    body = match.group(2)
    columns: list[str] = []
    primary_key: list[str] = []
    column_types: dict[str, str] = {}
    for item in _split_sql_items(body):
        lowered = item.lower().strip()
        if lowered.startswith("primary key"):
            pk_match = re.search(r"\((.*)\)", item, flags=re.S)
            if pk_match:
                primary_key.extend(_clean_sql_identifier(x) for x in _split_sql_items(pk_match.group(1)))
            continue
        if lowered.startswith("foreign key") or lowered.startswith("constraint"):
            continue
        col_match = re.match(r"[`\"]?([^`\"\s]+(?: [^`\"\s]+)*)[`\"]?\s+(.+)$", item, flags=re.S)
        if col_match:
            col_name = _clean_sql_identifier(col_match.group(1))
            if col_name and col_name.upper() not in {"PRIMARY", "FOREIGN", "CONSTRAINT"}:
                columns.append(col_name)
                raw_type = col_match.group(2).strip()
                raw_type = re.split(r"\s+(?:PRIMARY|NOT|NULL|UNIQUE|DEFAULT|CHECK|REFERENCES)\b", raw_type, maxsplit=1, flags=re.I)[0].strip()
                column_types[col_name] = raw_type
    return {"view_name": view_name, "columns": normalize_columns(columns), "primary_key": normalize_columns(primary_key), "column_types": column_types}


def normalize_spec(spec: dict[str, Any], table_file: str | None = None) -> dict[str, Any]:
    create_sql = str(spec.get("create_table_sql") or "")
    parsed = parse_create_table_sql(create_sql) if create_sql else {"view_name": "", "columns": [], "primary_key": []}
    parsed_columns = normalize_columns(parsed.get("columns", []))
    parsed_pk = normalize_columns(parsed.get("primary_key", []))
    parsed_types = {str(k): str(v) for k, v in (parsed.get("column_types") or {}).items()}
    semantic = normalize_columns(spec.get("semantic_columns") or spec.get("columns") or parsed_columns)
    bridge = normalize_columns(spec.get("bridge_columns") or spec.get("must_keep_join_keys") or parsed_pk)
    output = normalize_columns(spec.get("output_columns") or parsed_columns or semantic + bridge)
    if not output:
        output = normalize_columns(semantic + bridge)
    column_comments = spec.get("column_comments") or {}
    if not isinstance(column_comments, dict):
        column_comments = {}
    return {
        "table_file": str(spec.get("table_file") or table_file or ""),
        "view_name": str(spec.get("view_name") or parsed.get("view_name") or ""),
        "create_table_sql": create_sql,
        "column_comments": {str(k): str(v) for k, v in column_comments.items()},
        "primary_key": parsed_pk,
        "column_types": parsed_types,
        "is_bridge_table": bool(spec.get("is_bridge_table", False)),
        "semantic_columns": semantic,
        "bridge_columns": bridge,
        "output_columns": output,
        "layout_repair_hints": [str(x) for x in spec.get("layout_repair_hints", []) or []],
        "rationale": str(spec.get("rationale", "")),
    }


def spec_key(benchmark: str, split: str, task_id: str, table_file: str) -> str:
    return "::".join([benchmark, split, task_id, table_file])


def load_table_specs(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    for row in load_jsonl(path):
        benchmark = str(row.get("benchmark", ""))
        split = str(row.get("split", ""))
        task_id = str(row.get("task_id", ""))
        table_specs = row.get("T") or row.get("table_specs") or []
        if not table_specs and row.get("table_file"):
            table_specs = [row]
        for spec in table_specs:
            norm = normalize_spec(spec)
            if row.get("S"):
                norm["reasoning_sql"] = str(row.get("S") or "")
            table_file = norm.get("table_file", "")
            if benchmark and split and task_id and table_file:
                out[spec_key(benchmark, split, task_id, table_file)] = norm
    return out


def get_instance_spec(instance: dict[str, Any], specs: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    key = spec_key(
        str(instance.get("benchmark", "")),
        str(instance.get("split", "")),
        str(instance.get("task_id", "")),
        str(instance.get("table_file", "")),
    )
    return specs.get(key)


def format_spec_for_prompt(spec: dict[str, Any] | None) -> str:
    if not spec:
        return "None."
    norm = normalize_spec(spec or {})
    compact = {
        "table_file": norm.get("table_file"),
        "view_name": norm.get("view_name"),
        "create_table_sql": norm.get("create_table_sql"),
        "column_comments": norm.get("column_comments") or {},
        "output_columns": norm.get("output_columns") or [],
        "primary_key": norm.get("primary_key") or [],
        "column_types": norm.get("column_types") or {},
    }
    if norm.get("layout_repair_hints"):
        compact["layout_repair_hints"] = norm.get("layout_repair_hints")
    return json.dumps(compact, ensure_ascii=False, indent=2)


def columns_present(current_columns: list[str], wanted: list[str]) -> tuple[list[str], list[str]]:
    current = {str(c) for c in current_columns}
    present = [c for c in wanted if c in current]
    missing = [c for c in wanted if c not in current]
    return present, missing


def _sql_view_column_refs(reasoning_sql: str, view_name: str) -> list[str]:
    if not reasoning_sql or not view_name:
        return []
    refs: list[str] = []
    alias_to_view = {view_name: view_name}
    for match in re.finditer(
        r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)(?:\s+(?:AS\s+)?([A-Za-z_][A-Za-z0-9_]*))?",
        reasoning_sql,
        flags=re.I,
    ):
        view = match.group(1)
        alias = match.group(2)
        if view == view_name and alias and alias.upper() not in {"ON", "WHERE", "INNER", "LEFT", "RIGHT", "FULL", "JOIN"}:
            alias_to_view[alias] = view
    aliases = sorted(alias_to_view, key=len, reverse=True)
    ident = r"`([^`]+)`|\"([^\"]+)\"|([A-Za-z_][A-Za-z0-9_]*)"
    for alias in aliases:
        pattern = re.compile(rf"\b{re.escape(alias)}\s*\.\s*(?:{ident})", flags=re.I)
        for match in pattern.finditer(reasoning_sql):
            col = next((part for part in match.groups() if part), "")
            if col:
                refs.append(col)
    return normalize_columns(refs)


def _required_columns_with_reasons(spec: dict[str, Any], joinability_signal: dict[str, Any]) -> dict[str, list[str]]:
    reasons: dict[str, list[str]] = {}

    def add(cols: list[str], reason: str) -> None:
        for col in normalize_columns(cols):
            reasons.setdefault(col, [])
            if reason not in reasons[col]:
                reasons[col].append(reason)

    add(spec.get("output_columns", []), "create_table_sql/output column")
    add(spec.get("semantic_columns", []), "semantic target column")
    add(spec.get("bridge_columns", []), "bridge/entity column")
    add(spec.get("primary_key", []), "primary key")
    add(
        _sql_view_column_refs(str(spec.get("reasoning_sql") or ""), str(spec.get("view_name") or "")),
        "referenced by reasoning SQL S",
    )
    sql_join_cols = [str(h.get("this_table_column")) for h in joinability_signal.get("spec_sql_join_keys", []) or [] if h.get("this_table_column")]
    add(sql_join_cols, "join key required by reasoning SQL S")
    return reasons


def _join_key_status_all_satisfied(joinability_signal: dict[str, Any]) -> bool:
    statuses = joinability_signal.get("spec_sql_join_key_status") or []
    if not statuses:
        return True
    for status in statuses:
        if not status.get("this_column_present"):
            return False
        # The current runner may evaluate one table before its SQL-neighbor table
        # has been materialized. In that case, require this table's key to exist,
        # but only enforce overlap once the neighbor key is from a processed table.
        if (
            status.get("other_table_processed")
            and status.get("overlap_size") == 0
            and status.get("this_distinct", 0)
            and status.get("other_distinct", 0)
        ):
            return False
    return True


def _sql_type_family(sql_type: str) -> str:
    t = str(sql_type or "").upper()
    if any(x in t for x in ["INT", "REAL", "DOUBLE", "FLOAT", "NUMERIC", "DECIMAL"]):
        return "numeric"
    if any(x in t for x in ["DATE", "TIME", "YEAR"]):
        return "datetime"
    if any(x in t for x in ["BOOL"]):
        return "boolean"
    return "text"


def _observed_type_family(dtype_text: str) -> str:
    t = str(dtype_text or "").lower()
    if any(x in t for x in ["int", "float", "double", "decimal"]):
        return "numeric"
    if any(x in t for x in ["date", "time"]):
        return "datetime"
    if "bool" in t:
        return "boolean"
    return "text"


def _parseable_datetime_ratio(values: list[Any]) -> float:
    cleaned = [v for v in values if v is not None and str(v).strip().lower() not in {"", "nan", "none", "null", "<na>"}]
    if not cleaned:
        return 1.0
    parsed = pd.to_datetime(pd.Series(cleaned), errors="coerce")
    return round(float(parsed.notna().mean()), 4)


def _dtype_contract_status(current_obs: dict[str, Any], spec: dict[str, Any]) -> list[dict[str, Any]]:
    expected = spec.get("column_types") or {}
    observed = current_obs.get("dtypes") or {}
    sample_values = current_obs.get("column_sample_values") or {}
    statuses: list[dict[str, Any]] = []
    for col, sql_type in expected.items():
        if col not in observed:
            statuses.append({"column": col, "expected_sql_type": sql_type, "observed_dtype": None, "compatible": False, "reason": "column missing"})
            continue
        exp_family = _sql_type_family(sql_type)
        obs_family = _observed_type_family(observed.get(col))
        parseable_ratio = None
        if exp_family == "datetime" and obs_family == "text":
            parseable_ratio = _parseable_datetime_ratio(sample_values.get(col, []))
            compatible = parseable_ratio >= 0.8
        else:
            compatible = exp_family == obs_family or exp_family == "text"
        status = {
            "column": col,
            "expected_sql_type": sql_type,
            "observed_dtype": observed.get(col),
            "expected_family": exp_family,
            "observed_family": obs_family,
            "compatible": compatible,
        }
        if parseable_ratio is not None:
            status["parseable_datetime_ratio"] = parseable_ratio
            status["compatibility_rule"] = "datetime SQL type accepts datetime64 or parseable datetime string for SQLite execution"
        statuses.append(status)
    return statuses


def _primary_key_contract_status(current_obs: dict[str, Any], spec: dict[str, Any]) -> list[dict[str, Any]]:
    pk_cols = normalize_columns(spec.get("primary_key", []))
    if not pk_cols:
        return []
    current_columns = [str(c) for c in current_obs.get("columns", [])]
    stats = current_obs.get("column_stats") or {}
    statuses: list[dict[str, Any]] = []
    is_composite = len(pk_cols) > 1
    for col in pk_cols:
        present = col in current_columns
        col_stats = stats.get(col) or {}
        non_null_ratio = col_stats.get("non_null_ratio")
        unique_ratio = col_stats.get("unique_ratio")
        non_null_enough = bool(present and non_null_ratio is not None and non_null_ratio >= 0.95)
        unique_enough = bool(present and unique_ratio is not None and unique_ratio >= 0.95)
        if is_composite:
            # Composite primary keys require tuple-level uniqueness. The compact
            # observation does not carry full-row tuples, so do not incorrectly
            # require each component column to be unique by itself.
            unique_enough = non_null_enough
        statuses.append({
            "column": col,
            "present": present,
            "non_null_ratio": non_null_ratio,
            "unique_ratio": unique_ratio,
            "unique_enough": unique_enough,
            "non_null_enough": non_null_enough,
            "composite_primary_key_component": is_composite,
        })
    return statuses


def _contract_status_ok(statuses: list[dict[str, Any]], key: str) -> bool:
    return all(bool(item.get(key)) for item in statuses)


def schema_coverage_check(current_obs: dict[str, Any], spec: dict[str, Any] | None, joinability_signal: dict[str, Any]) -> dict[str, Any]:
    if not spec:
        return {"has_spec": False, "stop": False, "reason": "No table spec provided."}
    spec = normalize_spec(spec)
    current_columns = [str(c) for c in current_obs.get("columns", [])]
    required_reasons = _required_columns_with_reasons(spec, joinability_signal)
    required = normalize_columns(list(required_reasons))
    present_required, missing_required = columns_present(current_columns, required)
    dropped: list[str] = []
    join_keys_ok = _join_key_status_all_satisfied(joinability_signal)
    dtype_status = _dtype_contract_status(current_obs, spec)
    pk_status = _primary_key_contract_status(current_obs, spec)
    dtypes_ok = _contract_status_ok(dtype_status, "compatible")
    primary_keys_ok = _contract_status_ok(pk_status, "unique_enough") and _contract_status_ok(pk_status, "non_null_enough")
    stop = bool(required) and not missing_required and join_keys_ok and dtypes_ok and primary_keys_ok
    missing_with_reasons = [
        {"column": col, "reasons": required_reasons.get(col, [])}
        for col in missing_required
    ]
    present_with_reasons = [
        {"column": col, "reasons": required_reasons.get(col, [])}
        for col in present_required
    ]
    incorrect_column_types = [item for item in dtype_status if not item.get("compatible")]
    incorrect_primary_keys = [
        item for item in pk_status
        if not item.get("present") or not item.get("unique_enough") or not item.get("non_null_enough")
    ]
    incorrect_join_keys = []
    for item in joinability_signal.get("spec_sql_join_key_status", []) or []:
        if not item.get("this_column_present"):
            incorrect_join_keys.append({**item, "reason": "join key column has not been materialized in this subtable"})
        elif (
            item.get("other_table_processed")
            and item.get("overlap_size") == 0
            and item.get("this_distinct", 0)
            and item.get("other_distinct", 0)
        ):
            incorrect_join_keys.append({**item, "reason": "join key exists but has zero overlap with the available materialized neighbor key"})

    if missing_required:
        reason = "missing required columns: " + ", ".join(missing_required)
    elif incorrect_primary_keys:
        reason = "primary key columns are missing, null-heavy, or not sufficiently unique"
    elif incorrect_column_types:
        reason = "column dtypes do not satisfy CREATE TABLE SQL type contract"
    elif incorrect_join_keys:
        reason = "declared join-key constraints are not satisfied"
    else:
        reason = "subtable schema contract pass"
    return {
        "has_spec": True,
        "stop": stop,
        "target_columns": required,
        "target_column_reasons": required_reasons,
        "present_columns": present_required,
        "missing_columns": missing_with_reasons,
        "incorrect_column_types": incorrect_column_types,
        "incorrect_primary_keys": incorrect_primary_keys,
        "incorrect_join_keys": incorrect_join_keys,
        "primary_key_status": pk_status,
        "primary_keys_satisfied": primary_keys_ok,
        "dtype_status": dtype_status,
        "dtypes_satisfied": dtypes_ok,
        "join_key_status": joinability_signal.get("spec_sql_join_key_status", []),
        "join_keys_satisfied": join_keys_ok,
        "layout_repair_hints": spec.get("layout_repair_hints", []),
        "reason": reason,
        # Backward-compatible fields for existing analysis scripts.
        "required_columns": required,
        "required_column_reasons": required_reasons,
        "present_required_columns": present_required,
        "missing_required_columns": missing_required,
        "missing_required_columns_with_reasons": missing_with_reasons,
        "present_required_columns_with_reasons": present_with_reasons,
        "dropped_required_join_keys": dropped,
        "sql_join_key_status": joinability_signal.get("spec_sql_join_key_status", []),
        "sql_join_keys_satisfied": join_keys_ok,
    }



def _looks_like_date(text: str) -> bool:
    text = str(text or "").strip()
    if not text or text.lower() in {"nan", "none", "null", "<na>"}:
        return False
    if re.search(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", text):
        return True
    try:
        parsed = pd.to_datetime(pd.Series([text]), errors="coerce")
        return bool(parsed.notna().iloc[0]) and bool(re.search(r"\d", text))
    except Exception:
        return False


def _clean_sample_values(values: list[Any], limit: int = 20) -> list[str]:
    out: list[str] = []
    for value in values or []:
        text = str(value).strip().strip('"').strip("'")
        if text and text.lower() not in {"nan", "none", "null", "<na>"}:
            out.append(text)
        if len(out) >= limit:
            break
    return out


def value_semantic_check(current_obs: dict[str, Any], spec: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Lightweight checks for columns that exist but contain suspicious values.

    This is intentionally conservative. It only flags obvious contract/value
    mismatches that schema coverage cannot see, such as a sex column filled
    with dates or a date column filled with unparsable strings.
    """
    if not spec:
        return []
    spec = normalize_spec(spec)
    columns = {str(c) for c in current_obs.get("columns", [])}
    stats = current_obs.get("column_stats") or {}
    samples = current_obs.get("column_sample_values") or {}
    comments = {str(k): str(v) for k, v in (spec.get("column_comments") or {}).items()}
    findings: list[dict[str, Any]] = []
    required = normalize_columns(spec.get("output_columns", []) + spec.get("semantic_columns", []) + spec.get("bridge_columns", []))
    for col in required:
        if col not in columns:
            continue
        col_l = col.lower()
        comment_l = comments.get(col, "").lower()
        col_stats = stats.get(col) or {}
        values = _clean_sample_values(list(samples.get(col, [])) + list(col_stats.get("frequent_values", [])), limit=40)
        non_null_ratio = col_stats.get("non_null_ratio")
        if any(key in col_l or key in comment_l for key in ["sex", "gender"]):
            allowed = {"m", "f", "male", "female", "+", "-", "0", "1"}
            suspicious = []
            for value in values:
                v = value.lower()
                if v in allowed:
                    continue
                if _looks_like_date(value) or len(v) > 16 or re.search(r"[a-z]{3,}", v):
                    suspicious.append(value)
            if suspicious and (len(suspicious) >= 2 or any(_looks_like_date(x) for x in suspicious)):
                findings.append({
                    "column": col,
                    "issue": "values do not look like patient sex/gender; the column may have been split or mapped incorrectly",
                    "sample_values": values[:10],
                    "suspicious_values": suspicious[:8],
                })
        if any(key in col_l or key in comment_l for key in ["birthday", "birth_date", "dob", "date"]):
            if values:
                parse_ratio = _parseable_datetime_ratio(values)
                if parse_ratio < 0.6:
                    findings.append({
                        "column": col,
                        "issue": "values do not look parseable as the required date/datetime semantics",
                        "parseable_datetime_ratio": parse_ratio,
                        "sample_values": values[:10],
                    })
    return findings

def final_projection_columns(current_columns: list[str], spec: dict[str, Any] | None, joinability_signal: dict[str, Any]) -> list[str]:
    if not spec:
        return []
    spec = normalize_spec(spec)
    wanted = normalize_columns(
        list(spec.get("output_columns", []))
        + list(spec.get("semantic_columns", []))
        + list(spec.get("bridge_columns", []))
        + list(joinability_signal.get("must_keep_columns", []))
    )
    current = [str(c) for c in current_columns]
    return [c for c in wanted if c in current]


def apply_final_projection(df: pd.DataFrame, spec: dict[str, Any] | None, joinability_signal: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    cols = final_projection_columns([str(c) for c in df.columns], spec, joinability_signal)
    if not cols or cols == [str(c) for c in df.columns]:
        return df, None
    projected = df.loc[:, cols].copy()
    return projected, {"op": "SelectCol", "params": {"columns": cols}, "table_indices": [0], "source": "deterministic_final_projection"}


def table_brief(table_file: str, df: pd.DataFrame, top_k: int, cut_col: int, max_table_len: int) -> str:
    return (
        f"Table file: {table_file}\n"
        "Recovered headers (soft hints; may simply be visible raw headers when no separate recovery is available): "
        f"{json.dumps([str(c) for c in df.columns], ensure_ascii=False)}\n"
        f"Table preview:\n{df_to_cotable(df, cut_line=top_k, cut_col=cut_col, max_len=max_table_len)}"
    )


def load_table_spec_examples(benchmark: str, examples_dir: Path | None = None, max_examples: int | None = None) -> str:
    examples_dir = examples_dir or DEFAULT_EXAMPLES_DIR
    path = examples_dir / f"{benchmark}.txt"
    if not path.exists():
        return "No benchmark-specific examples are provided."
    text = path.read_text(encoding="utf-8").strip()
    if max_examples is None or max_examples <= 0:
        return text
    chunks = re.split(r"(?=^Example\s+)", text, flags=re.M)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return "\n\n".join(chunks[:max_examples]) if chunks else text


def join_requirement_for_benchmark(benchmark: str, table_count: int) -> str:
    benchmark = str(benchmark)
    if benchmark in {"nl2sql-bird", "nl2sql-spider", "beaver"} and table_count >= 2:
        return (
            "- HARD JOIN REQUIREMENT for this benchmark: every task requires joins. "
            "S MUST use every selected T view and MUST contain explicit JOIN clauses or equivalent explicit multi-table composition over all selected T views. "
            "Do NOT answer using only one T view. Do NOT absorb another table's factual/filter semantics into one T_i to avoid a join. "
            "Each T_i must keep the local join operand columns needed by S."
        )
    return (
        "- For this benchmark, S may use one or multiple T views as needed. "
        "When multiple selected T views are needed, express cross-table logic in S rather than absorbing it into one T_i."
    )


def build_spec_prompt(
    question: str,
    tables: dict[str, pd.DataFrame],
    joinability_by_table: dict[str, dict[str, Any]],
    top_k: int,
    cut_col: int,
    max_table_len: int,
    examples_text: str = "No examples are provided.",
    benchmark: str = "",
) -> str:
    tables_text = "\n\n".join(table_brief(name, df, top_k=top_k, cut_col=cut_col, max_table_len=max_table_len) for name, df in tables.items())
    joinability_text = json.dumps(joinability_by_table, ensure_ascii=False, indent=2)
    return SPEC_PROMPT_TEMPLATE.format(
        question=question,
        tables_text=tables_text,
        joinability_text=joinability_text,
        examples_text=examples_text,
        join_requirement=join_requirement_for_benchmark(benchmark, len(tables)),
    )


def build_task_tables(benchmark_dir: Path, input_tables: list[str]) -> dict[str, pd.DataFrame]:
    cache: dict[str, Path | None] = {}
    out: dict[str, pd.DataFrame] = {}
    for table_file in input_tables:
        path = find_table_file(benchmark_dir, str(table_file), cache=cache)
        if path is None:
            continue
        try:
            out[str(table_file)] = load_table(path)
        except Exception:
            continue
    return out


def task_joinability_hints(tables: dict[str, pd.DataFrame], top_neighbors: int) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for table_file, df in tables.items():
        neighbors = {name: other for name, other in tables.items() if name != table_file}
        signal = compute_joinability_signal(df, df, neighbors, top_neighbors=top_neighbors)
        out[table_file] = compact_joinability_for_prompt(signal)
    return out
