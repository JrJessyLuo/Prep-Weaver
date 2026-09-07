import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="rarity", func="""
    # def is_valid_rarity(val):
    #     if val is None:
    #         return False
    #     v = str(val).strip().lower()
    #     return v in {"common", "uncommon", "rare", "mythic", "mythic rare", "special", "bonus"}
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_rarity(val):
        if val is None:
            return False
        v = str(val).strip().lower()
        return v in {"common", "uncommon", "rare", "mythic", "mythic rare", "special", "bonus"}
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_rarity(val))
        except Exception:
            return False
    table_1 = table_1[table_1['rarity'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="rarity", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip().lower()
    #     # normalize common variants
    #     if v == "mythic rare":
    #         return "mythic"
    #     return v
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip().lower()
        # normalize common variants
        if v == "mythic rare":
            return "mythic"
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["rarity"] = table_1["rarity"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['id']
    if _dtype == "datetime64":
        table_1['id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'rarity'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'rarity'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'rarity'])
    # SelectCol
    _cols = [c for c in ['id', 'rarity'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'rq', 'nr'])
    # SelectCol
    _cols = [c for c in ['id', 'rq', 'nr'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="rq", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['rq'] = table_1['rq'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['rq'] = table_1['rq'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # keep rulings on/after 2007-01-02
    #     return pd.to_datetime(row['rq'], errors='coerce') >= pd.to_datetime(\"2007-01-02\")
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # keep rulings on/after 2007-01-02
        return pd.to_datetime(row['rq'], errors='coerce') >= pd.to_datetime(\"2007-01-02\")
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
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
prepared_rulings = prepared_table_2

# Assume prepared_cards and prepared_rulings are dataframes produced per targets above.
# Normalize date strings to a common format and match 01/02/2007 in either MM/DD/YYYY or DD/MM/YYYY inputs.

def parse_date_mdy_dmy(s):
    # try ISO first
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return pd.to_datetime(s, format=fmt, errors='raise')
        except Exception:
            continue
    return pd.NaT

rul = prepared_rulings.copy()
rul['rq_dt'] = rul['rq'].apply(parse_date_mdy_dmy)

cards = prepared_cards.copy()
# Filter to print rarity exactly 'print' (case-insensitive, trims spaces)
cards['rarity_norm'] = cards['rarity'].astype(str).str.strip().str.lower()
cards_print = cards[cards['rarity_norm'] == 'print'][['id']]

merged = cards_print.merge(rul[['id','rq_dt','nr']], on='id', how='inner')

# Target date is 01/02/2007; interpret as exact calendar day regardless of locale after parsing
target_day = pd.Timestamp(year=2007, month=2, day=1)
result_count = merged[merged['rq_dt'] == target_day].shape[0]

answer = result_count

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
