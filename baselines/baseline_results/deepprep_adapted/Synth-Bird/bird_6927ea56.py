import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'id', 'new_name': 'card_id'}])
    # Rename
    table_1 = table_1.rename(columns={'id': 'card_id'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['setCode', 'convertedManaCost', 'card_id'])
    # SelectCol
    _cols = [c for c in ['setCode', 'convertedManaCost', 'card_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="setCode", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     # If multiple codes appear (e.g., "ABC,DEF"), keep the first for a single set identifier
    #     if "," in s:
    #         s = s.split(",")[0].strip()
    #     # Keep only the leading alphanumeric set code token
    #     m = re.match(r"^([A-Za-z0-9]+)", s)
    #     return m.group(1).upper() if m else s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        # If multiple codes appear (e.g., "ABC,DEF"), keep the first for a single set identifier
        if "," in s:
            s = s.split(",")[0].strip()
        # Keep only the leading alphanumeric set code token
        m = re.match(r"^([A-Za-z0-9]+)", s)
        return m.group(1).upper() if m else s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["setCode"] = table_1["setCode"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="convertedManaCost", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['convertedManaCost'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['convertedManaCost']
    if _dtype == "datetime64":
        table_1['convertedManaCost'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['convertedManaCost'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['convertedManaCost'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['convertedManaCost'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['setCode', 'convertedManaCost', 'card_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['setCode', 'convertedManaCost', 'card_id'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
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
    # DropNulls(table_name="table_1", subset=['code', 'name', 'totalSetSize'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['code', 'name', 'totalSetSize'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="code", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["code"] = table_1["code"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name"] = table_1["name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="totalSetSize", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['totalSetSize'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['totalSetSize']
    if _dtype == "datetime64":
        table_1['totalSetSize'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['totalSetSize'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['totalSetSize'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['totalSetSize'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['code', 'name', 'totalSetSize'])
    # SelectCol
    _cols = [c for c in ['code', 'name', 'totalSetSize'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sets = prepared_table_2

# Assume prepared_cards and prepared_sets are available DataFrames
# 1) Join cards to sets by set code
cards_sets = prepared_cards.merge(prepared_sets, left_on='setCode', right_on='code', how='inner')

# 2) Filter to the Coldsnap set (name == 'Coldsnap' or code == its code 'CSP')
cs = cards_sets[(cards_sets['name'] == 'Coldsnap') | (cards_sets['code'] == 'CSP')]

# 3) Compute counts
total_cards = len(cs)
num_cmc7 = (cs['convertedManaCost'] == 7).sum()

# 4) Percentage of cards with CMC 7 within the set
percentage = (num_cmc7 / total_cards * 100.0) if total_cards > 0 else 0.0

result = pd.DataFrame({
    'set': ['Coldsnap'],
    'total_cards': [total_cards],
    'cmc7_cards': [int(num_cmc7)],
    'percentage_cmc7': [percentage]
})

target = result

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
