"""
build_training_data.py
----------------------
Build two training sets from the autoprep benchmark's single-table single-op samples

  training_data/feature_op_mapping.jsonl
      Compact: {feature vector -> operation type}. One row per sample:

  training_data/operation_details.jsonl
      Full: each row carries the feature vector, the operation type, the complete
      raw table preview, target-conditioned schema (SQL + dict + primary key)。
      -- used at inference for nearest-neighbour retrieval, rendered as a usage example

Usage: python3 build_training_data.py
"""
from __future__ import annotations
import json, os, re
import pandas as pd
from features import featurize, sanitize, FEATURE_NAMES
from schema_spec import SchemaResolver, schema_to_sql, sql_view_schema

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.environ.get("SINGLE_OP_TRAINING_BENCHMARK", "")
AUTOPREP = os.environ.get("AUTOPREP_ROOT", "")
OUT_DIR = os.path.join(HERE, "training_data")
ROW_OPS = {"DropNulls", "MissingValueImputation", "Deduplicate", "ErrorDetection", "OutlierDetection"}


def table_preview(df: pd.DataFrame, max_rows=5, max_cols=12) -> str:
    """Markdown-style preview, matching the Raw table preview of operation_usage_examples."""
    cols = list(df.columns)[:max_cols]
    omitted = len(df.columns) - len(cols)
    header = " | ".join(str(c) for c in cols) + (f" | ...(+{omitted} cols)" if omitted > 0 else "")
    sep = "|".join(["---"] * len(cols))
    lines = [header, sep]
    for i in range(min(len(df), max_rows)):
        vals = df.iloc[i][cols]
        lines.append(" | ".join(_cell(v) for v in vals))
    if len(df) > max_rows:
        lines.append("......")
    return "\n".join(lines)


def _cell(v):
    if isinstance(v, str):
        return '"' + v.replace("\n", "\\n")[:40] + '"'
    return str(v)[:40]


def parse_op(op_str: str):
    """dc_op string -> (op_name, raw_params_str)."""
    m = re.match(r"\s*([A-Za-z_]\w*)\s*\((.*)\)\s*$", op_str, re.S)
    if not m:
        return op_str.strip(), ""
    return m.group(1), m.group(2).strip()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    R = SchemaResolver()
    recs = [json.loads(l) for l in open(BENCH)]
    focus = [r for r in recs if r["dc_ops_count"] == 1 and r["dc_op_types"][0] not in ROW_OPS]

    map_path = os.path.join(OUT_DIR, "feature_op_mapping.jsonl")
    det_path = os.path.join(OUT_DIR, "operation_details.jsonl")
    n = 0
    with open(map_path, "w") as fmap, open(det_path, "w") as fdet:
        for r in focus:
            op = r["dc_op_types"][0]
            src = "bird" if "bird" in r["source_file"] else "spider"
            schema, pk, tname = R.resolve(r["db_id"], r["sql"], src)
            if schema is None:
                continue
            p = os.path.join(AUTOPREP, os.path.dirname(r["source_file"]), r["input_table"][0])
            try:
                df = sanitize(pd.read_pickle(p))
            except Exception:
                continue
            fv = featurize(df, schema, pk)
            feat_dict = {k: round(float(v), 6) if v == v else None for k, v in zip(FEATURE_NAMES, fv)}
            op_name, op_params = parse_op(r["dc_ops"][0])

            # Version 1: the compact mapping
            fmap.write(json.dumps({"task_id": r["task_id"], "op_type": op,
                                   "features": feat_dict}, ensure_ascii=False) + "\n")

            # Version 2: the full detail
            fdet.write(json.dumps({
                "task_id": r["task_id"],
                "db_id": r["db_id"], "source": src, "source_table": tname,
                "op_type": op,
                "operation": r["dc_ops"][0],          # the complete operation text
                "op_params_raw": op_params,           # the raw parameter text inside the parentheses
                "sql": r["sql"],
                "features": feat_dict,
                "raw_table_preview": table_preview(df),
                "target_schema_sql": schema_to_sql(schema, pk),
                "target_schema": schema,
                "primary_key": sorted(pk),
            }, ensure_ascii=False) + "\n")
            n += 1
    print(f"wrote {n} records")
    print(" ->", map_path)
    print(" ->", det_path)
    from collections import Counter
    print("op distribution:", dict(Counter(json.loads(l)["op_type"]
          for l in open(det_path)).most_common()))


if __name__ == "__main__":
    main()
