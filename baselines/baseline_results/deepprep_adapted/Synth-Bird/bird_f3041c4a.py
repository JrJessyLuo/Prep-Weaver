import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="id", dtype="float")
    # CastType
    _dtype = 'float'
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="asciiName_filled", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     v = row.get('asciiName', None)
    #     # Treat NaN/None/empty as missing
    #     if v is None or (isinstance(v, float) and pd.isna(v)) or (isinstance(v, str) and v.strip().lower() in ['', 'nan', 'none']):
    #         return row.get('name', v)
    #     return v
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        v = row.get('asciiName', None)
        # Treat NaN/None/empty as missing
        if v is None or (isinstance(v, float) and pd.isna(v)) or (isinstance(v, str) and v.strip().lower() in ['', 'nan', 'none']):
            return row.get('name', v)
        return v
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["asciiName_filled"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['asciiName'])
    # DropColumn
    table_1 = table_1.drop(columns=['asciiName'], errors='ignore')

    # ---------------- Step 4 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'asciiName_filled', 'new_name': 'asciiName'}])
    # Rename
    table_1 = table_1.rename(columns={'asciiName_filled': 'asciiName'})

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     val = row.get('asciiName', '')
    #     if val is None or (isinstance(val, float) and pd.isna(val)):
    #         return False
    #     return 'angel of mercy' in str(val).lower()
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        val = row.get('asciiName', '')
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return False
        return 'angel of mercy' in str(val).lower()
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'asciiName'])
    # SelectCol
    _cols = [c for c in ['id', 'asciiName'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('id') is not None and row.get('translation') is not None and row.get('language_setCode') is not None
    # """)
    # Filter
    def filter_func(row):
        return row.get('id') is not None and row.get('translation') is not None and row.get('language_setCode') is not None
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="translation", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["translation"] = table_1["translation"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="language_setCode", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize spacing around the separator
    #     s = s.replace(" | ", "|").replace("| ", "|").replace(" |", "|")
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize spacing around the separator
        s = s.replace(" | ", "|").replace("| ", "|").replace(" |", "|")
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["language_setCode"] = table_1["language_setCode"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id', 'translation', 'language_setCode'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id', 'translation', 'language_setCode'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'translation', 'language_setCode'])
    # SelectCol
    _cols = [c for c in ['id', 'translation', 'language_setCode'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
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
def _prep_3(table_1):
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_translations = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])

angel_cards = prepared_cards[prepared_cards['asciiName'].fillna('').str.contains('Angel of Mercy', case=False, na=False)]
merged = angel_cards.merge(prepared_translations, on='id', how='inner')
# Count distinct translations for those cards (by language and set code entry)
answer = merged['language_setCode'].nunique()

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
