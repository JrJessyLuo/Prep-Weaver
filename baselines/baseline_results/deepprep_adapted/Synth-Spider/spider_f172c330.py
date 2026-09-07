import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="First_part", mode="mode")
    # MissingValueImputation
    table_1["First_part"] = table_1["First_part"].fillna(table_1["First_part"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Last_part", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip().strip('"').strip("'")
    #     # Treat common placeholder(s) as missing
    #     if s2 in {"*", "N/A", "NA", "NULL", "null", ""}:
    #         return ""
    #     # Collapse internal whitespace
    #     s2 = re.sub(r"\s+", " ", s2)
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip().strip('"').strip("'")
        # Treat common placeholder(s) as missing
        if s2 in {"*", "N/A", "NA", "NULL", "null", ""}:
            return ""
        # Collapse internal whitespace
        s2 = re.sub(r"\s+", " ", s2)
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Last_part"] = table_1["Last_part"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Player_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Player_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Player_ID']
    if _dtype == "datetime64":
        table_1['Player_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Player_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Player_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Player_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Player_ID', 'First_part', 'Last_part'])
    # SelectCol
    _cols = [c for c in ['Player_ID', 'First_part', 'Last_part'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="If_active_1", mode="constant:F")
    # MissingValueImputation
    # Unsupported or unknown imputation mode: constant:F
    # Please check server-side implementation for this operator.

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="If_active_2", mode="constant:F")
    # MissingValueImputation
    # Unsupported or unknown imputation mode: constant:F
    # Please check server-side implementation for this operator.

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="If_active_3", mode="constant:F")
    # MissingValueImputation
    # Unsupported or unknown imputation mode: constant:F
    # Please check server-side implementation for this operator.

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="If_active_4", mode="constant:F")
    # MissingValueImputation
    # Unsupported or unknown imputation mode: constant:F
    # Please check server-side implementation for this operator.

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="If_active_1", func="""
    # def transform_func(s):
    #     if s is None:
    #         return "F"
    #     v = str(s).strip().strip('"').strip("'").upper()
    #     if v in ["T", "TRUE", "1", "Y", "YES"]:
    #         return "T"
    #     return "F"
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return "F"
        v = str(s).strip().strip('"').strip("'").upper()
        if v in ["T", "TRUE", "1", "Y", "YES"]:
            return "T"
        return "F"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["If_active_1"] = table_1["If_active_1"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="If_active_2", func="""
    # def transform_func(s):
    #     if s is None:
    #         return "F"
    #     v = str(s).strip().strip('"').strip("'").upper()
    #     if v in ["T", "TRUE", "1", "Y", "YES"]:
    #         return "T"
    #     return "F"
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return "F"
        v = str(s).strip().strip('"').strip("'").upper()
        if v in ["T", "TRUE", "1", "Y", "YES"]:
            return "T"
        return "F"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["If_active_2"] = table_1["If_active_2"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="If_active_3", func="""
    # def transform_func(s):
    #     if s is None:
    #         return "F"
    #     v = str(s).strip().strip('"').strip("'").upper()
    #     if v in ["T", "TRUE", "1", "Y", "YES"]:
    #         return "T"
    #     return "F"
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return "F"
        v = str(s).strip().strip('"').strip("'").upper()
        if v in ["T", "TRUE", "1", "Y", "YES"]:
            return "T"
        return "F"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["If_active_3"] = table_1["If_active_3"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="If_active_4", func="""
    # def transform_func(s):
    #     if s is None:
    #         return "F"
    #     v = str(s).strip().strip('"').strip("'").upper()
    #     if v in ["T", "TRUE", "1", "Y", "YES"]:
    #         return "T"
    #     return "F"
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return "F"
        v = str(s).strip().strip('"').strip("'").upper()
        if v in ["T", "TRUE", "1", "Y", "YES"]:
            return "T"
        return "F"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["If_active_4"] = table_1["If_active_4"].apply(_std_apply)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Player_ID', 'If_active_1', 'If_active_2', 'If_active_3', 'If_active_4'])
    # SelectCol
    _cols = [c for c in ['Player_ID', 'If_active_1', 'If_active_2', 'If_active_3', 'If_active_4'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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

prepared_table_1 = _prep_1(tables['table_1'])
players = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
player_activity_flags = prepared_table_2

prepared = players.merge(player_activity_flags, on='Player_ID', how='left')
active_cols = ['If_active_1','If_active_2','If_active_3','If_active_4']
# Treat 'T' as active; anything else (F or NaN) as not active
is_active = prepared[active_cols].eq('T').any(axis=1)
no_game = prepared.loc[~is_active]
# Build full name from parts, keeping names even if last part is missing or placeholder
no_game['Player_Name'] = no_game[['First_part','Last_part']].fillna('').agg(' '.join, axis=1).str.strip()
answer = no_game[['Player_Name']].drop_duplicates()

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
