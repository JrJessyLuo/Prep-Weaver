import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MAJOR_USE_DESC", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        s = " ".join(s.split())
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MAJOR_USE_DESC"] = table_1["MAJOR_USE_DESC"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ROOM_KEY', 'FCLT_MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_ROOM_KEY', 'FCLT_MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="ASSIGNABLE", func="""
    # def is_valid(val):
    #     try:
    #         if val is None:
    #             return False
    #         v = int(val)
    #         return v in (0, 1)
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        try:
            if val is None:
                return False
            v = int(val)
            return v in (0, 1)
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['ASSIGNABLE'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DESCRIPTION", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DESCRIPTION"] = table_1["DESCRIPTION"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_MAJOR_USE_KEY", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FCLT_MAJOR_USE_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FCLT_MAJOR_USE_KEY']
    if _dtype == "datetime64":
        table_1['FCLT_MAJOR_USE_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FCLT_MAJOR_USE_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FCLT_MAJOR_USE_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FCLT_MAJOR_USE_KEY'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ASSIGNABLE", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ASSIGNABLE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ASSIGNABLE']
    if _dtype == "datetime64":
        table_1['ASSIGNABLE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ASSIGNABLE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ASSIGNABLE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ASSIGNABLE'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_MAJOR_USE_KEY', 'ASSIGNABLE', 'DESCRIPTION'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_MAJOR_USE_KEY', 'ASSIGNABLE', 'DESCRIPTION'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_MAJOR_USE_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_MAJOR_USE_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_MAJOR_USE_KEY', 'ASSIGNABLE', 'DESCRIPTION'])
    # SelectCol
    _cols = [c for c in ['FCLT_MAJOR_USE_KEY', 'ASSIGNABLE', 'DESCRIPTION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_major_use = prepared_table_2

# Assume prepared_rooms and prepared_major_use are provided as DataFrames
# 1) Integrate on major use key
merged = prepared_rooms.merge(prepared_major_use[["FCLT_MAJOR_USE_KEY","ASSIGNABLE","DESCRIPTION"]], on="FCLT_MAJOR_USE_KEY", how="left")

# 2) Filter out rooms where major use or its description starts with 'ZUSE.'
mask = ~(
    merged["MAJOR_USE_DESC"].fillna("").str.startswith("ZUSE.") |
    merged["DESCRIPTION"].fillna("").str.startswith("ZUSE.")
)
merged = merged[mask].copy()

# 3) Normalize ASSIGNABLE label
merged["ASSIGNABLE_LABEL"] = merged["ASSIGNABLE"].apply(lambda x: "ASSIGNABLE" if pd.notna(x) and int(x)==1 else "NON-ASSIGNABLE")

# 4) Compute group aggregates by (ASSIGNABLE_LABEL, MAJOR_USE_DESC)
grp = merged.groupby(["ASSIGNABLE_LABEL","MAJOR_USE_DESC"], dropna=False).agg(
    TOTAL_ROOMS=("FCLT_ROOM_KEY","count"),
    TOTAL_AREA=("AREA","sum"),
    AVG_AREA=("AREA","mean")
).reset_index()

# 5) Sort by assignable status then major use description
grp = grp.sort_values(["ASSIGNABLE_LABEL","MAJOR_USE_DESC"], kind="mergesort").reset_index(drop=True)

# 6) Build subtotal rows per ASSIGNABLE_LABEL
subtotals = grp.groupby(["ASSIGNABLE_LABEL"]).agg(
    TOTAL_ROOMS=("TOTAL_ROOMS","sum"),
    TOTAL_AREA=("TOTAL_AREA","sum")
).reset_index()
subtotals["AVG_AREA"] = subtotals["TOTAL_AREA"] / subtotals["TOTAL_ROOMS"].where(subtotals["TOTAL_ROOMS"]!=0, pd.NA)
subtotals["MAJOR_USE_DESC"] = ""

# 7) Grand total
grand = pd.DataFrame({
    "ASSIGNABLE_LABEL": [""],
    "MAJOR_USE_DESC": [""],
    "TOTAL_ROOMS": [grp["TOTAL_ROOMS"].sum()],
    "TOTAL_AREA": [grp["TOTAL_AREA"].sum()],
    "AVG_AREA": [grp["TOTAL_AREA"].sum() / grp["TOTAL_ROOMS"].sum() if grp["TOTAL_ROOMS"].sum()!=0 else pd.NA]
})

# 8) Interleave subtotals after each assignable block
out_rows = []
for assignable_value, block in grp.groupby("ASSIGNABLE_LABEL", sort=False):
    out_rows.append(block)
    st = subtotals[subtotals["ASSIGNABLE_LABEL"]==assignable_value].copy()
    # Clear label columns for subtotal row
    st["ASSIGNABLE_LABEL"] = ""
    out_rows.append(st)
result = pd.concat(out_rows + [grand], ignore_index=True)

# 9) Display formatting: show ASSIGNABLE_LABEL and MAJOR_USE_DESC only when they differ from previous row
display_df = result.copy()
for col in ["ASSIGNABLE_LABEL","MAJOR_USE_DESC"]:
    vals = display_df[col].fillna("")
    shown = []
    prev = None
    for v in vals:
        if v == "" or v != prev:
            shown.append(v)
            prev = v if v!="" else prev
        else:
            shown.append("")
    display_df[col] = shown

# 10) Optionally round areas
display_df["TOTAL_AREA"] = display_df["TOTAL_AREA"].round(2)
display_df["AVG_AREA"] = display_df["AVG_AREA"].round(2)

target = display_df[["ASSIGNABLE_LABEL","MAJOR_USE_DESC","TOTAL_ROOMS","TOTAL_AREA","AVG_AREA"]]

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
