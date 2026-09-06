from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd


OP_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(")
TABLE_REF_RE = re.compile(r'\b(?:table_name|left_table|right_table)\s*=\s*["\'](table_\d+)["\']')
NON_PREP_OPS = {"Projection"}


def op_name(op: Any) -> str | None:
    if isinstance(op, dict):
        return str(op.get("op") or op.get("name") or "") or None
    m = OP_RE.match(str(op))
    return m.group(1) if m else None


def referenced_tables(op_text: str) -> List[str]:
    seen = set()
    out = []
    for ref in TABLE_REF_RE.findall(op_text):
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out


def dc_ops_by_table(item: Dict[str, Any], table_names: List[str]) -> Dict[str, List[str]]:
    out = {name: [] for name in table_names}
    for op in item.get("dc_ops") or []:
        text = str(op)
        name = op_name(text)
        if name in NON_PREP_OPS:
            continue
        refs = referenced_tables(text)
        for ref in refs:
            if ref in out:
                out[ref].append(text)
    return out


def load_gold_output(item: Dict[str, Any], table_dir: Path) -> Dict[str, Any]:
    output_path = table_dir / "outputs" / f"{item['task_id']}.json"
    if output_path.exists():
        return json.loads(output_path.read_text(encoding="utf-8"))
    return {}


def _literal_arg(op_text: str, arg_name: str):
    m = re.search(rf"\b{re.escape(arg_name)}\s*=\s*(\[[^\n]*?\]|\{{[^\n]*?\}}|\"[^\"]*\"|'[^']*')", op_text, re.DOTALL)
    if not m:
        return None
    try:
        return ast.literal_eval(m.group(1))
    except Exception:
        return None


def _string_arg(op_text: str, arg_name: str) -> str | None:
    v = _literal_arg(op_text, arg_name)
    return str(v) if v is not None else None


def inferred_column_sets(
    table_name: str,
    selected_tables: Dict[str, pd.DataFrame],
    by_table_ops: Dict[str, List[str]],
) -> Tuple[set[str], set[str]]:
    df = selected_tables.get(table_name)
    source_cols = set(map(str, list(df.columns))) if isinstance(df, pd.DataFrame) else set()
    current = set(source_cols)
    evidence = set(source_cols)
    for op in by_table_ops.get(table_name) or []:
        name = op_name(op)
        if name == "Rename":
            rename_map = _literal_arg(op, "rename_map") or []
            if isinstance(rename_map, dict):
                rename_map = [{"old_name": k, "new_name": v} for k, v in rename_map.items()]
            for item in rename_map:
                if not isinstance(item, dict):
                    continue
                old = str(item.get("old_name") or item.get("old") or "")
                new = str(item.get("new_name") or item.get("new") or "")
                if old and old in current:
                    current.discard(old)
                if new:
                    current.add(new)
                    evidence.add(new)
        elif name == "SplitColumn":
            targets = _literal_arg(op, "target_columns") or []
            for col in targets:
                current.add(str(col))
                evidence.add(str(col))
        elif name == "Concatenate":
            col = _string_arg(op, "target_column")
            if col:
                current.add(col)
                evidence.add(col)
        elif name == "AddNewColumn":
            col = _string_arg(op, "new_column_name")
            if col:
                current.add(col)
                evidence.add(col)
        elif name == "DropColumn":
            drops = _literal_arg(op, "drop_columns") or []
            for col in drops:
                current.discard(str(col))
        elif name == "SelectCol":
            cols = _literal_arg(op, "columns")
            if isinstance(cols, list):
                current = set(map(str, cols))
                evidence.update(map(str, cols))
        elif name in {"Pivot", "Stack", "WideToLong", "Explode", "Transpose"}:
            # These operators may create schema values dynamically. Keep source
            # evidence and any explicitly named output fields where available.
            for arg in ("var_name", "value_name", "j"):
                col = _string_arg(op, arg)
                if col:
                    current.add(col)
                    evidence.add(col)
    return current, evidence


def map_gold_tables_to_local(
    gold_output: Dict[str, Any],
    table_names: List[str],
    selected_tables: Dict[str, pd.DataFrame],
    by_table_ops: Dict[str, List[str]],
) -> Tuple[Dict[str, str], Dict[str, str]]:
    table_columns = gold_output.get("table_columns") or {}
    gold_names = list(table_columns)
    if not gold_names:
        return {}, {}
    local_sets = {
        name: inferred_column_sets(name, selected_tables, by_table_ops)
        for name in table_names
    }
    pairs = []
    for gold_name in gold_names:
        gold_cols = set(map(str, table_columns.get(gold_name) or []))
        for local_name in table_names:
            current, evidence = local_sets[local_name]
            score = 3 * len(gold_cols & current) + len(gold_cols & evidence)
            # Join-key columns are especially diagnostic for table identity.
            for edge in (gold_output.get("join_keys") or []) + (gold_output.get("set_relations") or []):
                if edge.get("left_table") == gold_name and str(edge.get("left_column")) in evidence:
                    score += 5
                if edge.get("right_table") == gold_name and str(edge.get("right_column")) in evidence:
                    score += 5
            pairs.append((score, gold_name, local_name))
    pairs.sort(reverse=True)
    gold_to_local: Dict[str, str] = {}
    local_to_gold: Dict[str, str] = {}
    used_local = set()
    for score, gold_name, local_name in pairs:
        if score <= 0 or gold_name in gold_to_local or local_name in used_local:
            continue
        gold_to_local[gold_name] = local_name
        local_to_gold[local_name] = gold_name
        used_local.add(local_name)
    # Fallback only for unresolved tables.
    for i, gold_name in enumerate(gold_names):
        if gold_name in gold_to_local:
            continue
        if i < len(table_names) and table_names[i] not in used_local:
            local_name = table_names[i]
            gold_to_local[gold_name] = local_name
            local_to_gold[local_name] = gold_name
            used_local.add(local_name)
    return gold_to_local, local_to_gold


def output_columns_for_local_tables(
    gold_output: Dict[str, Any],
    table_names: List[str],
    selected_tables: Dict[str, pd.DataFrame],
    by_table_ops: Dict[str, List[str]],
) -> Tuple[Dict[str, List[str]], Dict[str, str], Dict[str, str]]:
    table_columns = gold_output.get("table_columns") or {}
    gold_to_local, local_to_gold = map_gold_tables_to_local(
        gold_output, table_names, selected_tables, by_table_ops
    )
    out: Dict[str, List[str]] = {}
    for i, name in enumerate(table_names):
        gold_name = local_to_gold.get(name)
        if gold_name and table_columns.get(gold_name):
            out[name] = [str(c) for c in table_columns[gold_name]]
        else:
            df = selected_tables.get(name)
            out[name] = [str(c) for c in list(df.columns)] if isinstance(df, pd.DataFrame) else []
    return out, gold_to_local, local_to_gold


def join_summary(gold_output: Dict[str, Any]) -> str:
    pieces = []
    for e in (gold_output.get("join_keys") or []) + (gold_output.get("set_relations") or []):
        lt, lc = e.get("left_table"), e.get("left_column")
        rt, rc = e.get("right_table"), e.get("right_column")
        if lt and lc and rt and rc:
            pieces.append(f"{lt}.{lc} = {rt}.{rc}")
    return "; ".join(pieces) if pieces else "No explicit gold join edge is annotated."


def simple_gold_answer_code(
    table_names: List[str],
    gold_output: Dict[str, Any],
    gold_to_local: Dict[str, str],
) -> str:
    """Integration code for gold-spec runs.

    It performs the annotated gold joins when the prepared tables expose the
    corresponding key columns. This lets eval_all_oom trace join-key value
    domains. If no annotated edge can be materialized, it falls back to a
    concatenation that still preserves prepared-table value evidence.
    """
    lines = []
    for i, _ in enumerate(table_names, 1):
        lines.append(f"_pt_{i} = prepared_table_{i}.copy() if isinstance(prepared_table_{i}, pd.DataFrame) else pd.DataFrame()")
    lines.append("_joined_frames = []")
    seen = set()
    for edge in (gold_output.get("join_keys") or []) + (gold_output.get("set_relations") or []):
        key = (edge.get("left_table"), edge.get("left_column"), edge.get("right_table"), edge.get("right_column"))
        if key in seen:
            continue
        seen.add(key)
        left_local = gold_to_local.get(str(edge.get("left_table")))
        right_local = gold_to_local.get(str(edge.get("right_table")))
        if not left_local or not right_local:
            continue
        try:
            li = table_names.index(left_local) + 1
            ri = table_names.index(right_local) + 1
        except ValueError:
            continue
        lc = str(edge.get("left_column"))
        rc = str(edge.get("right_column"))
        lines.extend([
            f"if not _pt_{li}.empty and not _pt_{ri}.empty and {lc!r} in _pt_{li}.columns and {rc!r} in _pt_{ri}.columns:",
            f"    _joined_frames.append(_pt_{li}.merge(_pt_{ri}, left_on={lc!r}, right_on={rc!r}, how='inner', suffixes=('_t{li}', '_t{ri}')))",
        ])
    lines.append("if _joined_frames:")
    lines.append("    target = pd.concat(_joined_frames, ignore_index=True, sort=False)")
    lines.append("else:")
    lines.append("    _frames = []")
    for i, _ in enumerate(table_names, 1):
        lines.extend([
            f"    if isinstance(prepared_table_{i}, pd.DataFrame):",
            f"        _tmp = prepared_table_{i}.copy()",
            f"        _tmp['__prepared_table__'] = 'prepared_table_{i}'",
            "        _frames.append(_tmp)",
        ])
    lines.append("    target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()")
    return "\n".join(lines)


def text2pipeline_gold_stage2(
    item: Dict[str, Any],
    selected_tables: Dict[str, pd.DataFrame],
    table_dir: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
    table_names = list(selected_tables)
    gold_output = load_gold_output(item, table_dir)
    by_table_ops = dc_ops_by_table(item, table_names)
    expected_cols, gold_to_local, local_to_gold = output_columns_for_local_tables(
        gold_output, table_names, selected_tables, by_table_ops
    )
    joins = join_summary(gold_output)
    specs = []
    for name in table_names:
        ops = by_table_ops.get(name) or []
        if ops:
            spec_text = (
                "Apply the following gold data-preparation operations to this table, "
                "preserving rows and join keys needed for downstream integration:\n"
                + "\n".join(f"- {op}" for op in ops)
                + f"\nGold integration relationships: {joins}"
            )
        else:
            spec_text = (
                "Gold specification is identity/no-op for this relevant table: preserve "
                "the source rows and columns, especially any keys needed for downstream "
                f"integration. Gold integration relationships: {joins}"
            )
        specs.append({
            "table": name,
            "preparation_specification": spec_text,
            "expected_output_columns": expected_cols.get(name) or [],
            "gold_dc_ops": ops,
        })
    plan = {
        "source": "gold_specification",
        "gold_join_summary": joins,
        "table_specifications": specs,
        "gold_table_mapping": local_to_gold,
        "answer_code": simple_gold_answer_code(table_names, gold_output, gold_to_local),
    }
    return plan, specs, plan["answer_code"]


def target_metadata_gold_stage2(
    item: Dict[str, Any],
    selected_tables: Dict[str, pd.DataFrame],
    table_dir: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
    table_names = list(selected_tables)
    gold_output = load_gold_output(item, table_dir)
    by_table_ops = dc_ops_by_table(item, table_names)
    expected_cols, gold_to_local, local_to_gold = output_columns_for_local_tables(
        gold_output, table_names, selected_tables, by_table_ops
    )
    joins = join_summary(gold_output)
    targets = []
    for i, name in enumerate(table_names, 1):
        ops = by_table_ops.get(name) or []
        cols = expected_cols.get(name) or [str(c) for c in list(selected_tables[name].columns)]
        if ops:
            desc = (
                "Gold target metadata derived from benchmark dc_ops. The prepared "
                "table should realize these operations:\n"
                + "\n".join(f"- {op}" for op in ops)
                + f"\nPreserve columns needed for integration. Gold joins: {joins}"
            )
        else:
            desc = (
                "Gold target metadata is identity/no-op for this relevant table. "
                f"Preserve source evidence and integration keys. Gold joins: {joins}"
            )
        targets.append({
            "table": name,
            "target_table_name": f"prepared_table_{i}",
            "target_columns": cols,
            "target_description": desc,
            "gold_dc_ops": ops,
            "identity_fallback": not bool(ops),
        })
    plan = {
        "source": "gold_specification",
        "table_targets": targets,
        "integration_plan": joins,
        "gold_table_mapping": local_to_gold,
        "answer_code": simple_gold_answer_code(table_names, gold_output, gold_to_local),
    }
    return plan, targets, plan["answer_code"]
