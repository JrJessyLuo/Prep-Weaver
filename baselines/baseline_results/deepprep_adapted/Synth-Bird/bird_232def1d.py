import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # Exclude multi-face cards by layout and by presence of otherFaceIds.
    #     multi_face_layouts = {
    #         'split','flip','transform','meld',
    #         'modal_dfc','double_faced_token',
    #         'adventure'  # often treated as special multi-part behavior
    #     }
    #     layout = row.get('layout')
    #     other_face_ids = row.get('otherFaceIds')
    #     # Keep only if layout is present, not in multi-face list, and has no otherFaceIds
    #     return (layout is not None) and (str(layout).lower() not in multi_face_layouts) and (other_face_ids is None)
    # """)
    # Filter
    def filter_func(row):
        # Exclude multi-face cards by layout and by presence of otherFaceIds.
        multi_face_layouts = {
            'split','flip','transform','meld',
            'modal_dfc','double_faced_token',
            'adventure'  # often treated as special multi-part behavior
        }
        layout = row.get('layout')
        other_face_ids = row.get('otherFaceIds')
        # Keep only if layout is present, not in multi-face list, and has no otherFaceIds
        return (layout is not None) and (str(layout).lower() not in multi_face_layouts) and (other_face_ids is None)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'layout'])
    # SelectCol
    _cols = [c for c in ['id', 'layout'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'layout'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'layout'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id', 'layout'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id', 'layout'], keep='first').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="sts_premodern", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     low = t.lower()
    #     mapping = {
    #         'legal': 'Legal',
    #         'restricted': 'Restricted',
    #         'banned': 'Banned',
    #         'not legal': 'Not Legal',
    #         'not_legal': 'Not Legal',
    #         'notlegal': 'Not Legal'
    #     }
    #     return mapping.get(low, t)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        t = str(s).strip()
        low = t.lower()
        mapping = {
            'legal': 'Legal',
            'restricted': 'Restricted',
            'banned': 'Banned',
            'not legal': 'Not Legal',
            'not_legal': 'Not Legal',
            'notlegal': 'Not Legal'
        }
        return mapping.get(low, t)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["sts_premodern"] = table_1["sts_premodern"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     v = row.get('sts_premodern')
    #     if pd.isna(v):
    #         return False
    #     s = str(v).strip()
    #     return s != \"\" and s.lower() != \"nan\"
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        v = row.get('sts_premodern')
        if pd.isna(v):
            return False
        s = str(v).strip()
        return s != \"\" and s.lower() != \"nan\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'sts_premodern'])
    # SelectCol
    _cols = [c for c in ['id', 'sts_premodern'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # optional: restrict to English for downstream use
    #     return str(row.get('language','')).strip().lower() in ['english','en']
    # """)
    # Filter
    def filter_func(row):
        # optional: restrict to English for downstream use
        return str(row.get('language','')).strip().lower() in ['english','en']
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'text', 'language'])
    # SelectCol
    _cols = [c for c in ['id', 'text', 'language'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
cards_core = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
cards_formats = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
cards_text = prepared_table_3

# Assume prepared tables are provided as DataFrames: cards_core, cards_formats, cards_text
# Join core with formats to get Premodern status
cf = cards_core.merge(cards_formats[['id','sts_premodern']], on='id', how='left')

# Join with text (restrict to English to match exact sentence in the question)
cf_text = cf.merge(cards_text[cards_text['language'] == 'English'][['id','text']], on='id', how='left')

# Define multi-face layouts to exclude (cards that "do not have multiple faces")
multi_face_layouts = {
    'transform', 'modal_dfc', 'double_faced_token', 'split', 'flip', 'adventure', 'aftermath', 'meld'
}

# Filter conditions:
# - In Premodern format: sts_premodern not null and not equal to 'Banned' (keep 'Legal' et al.)
# - Text contains the exact ruling string
# - Layout not in multi-face set (and not null)
mask_premodern = cf_text['sts_premodern'].notna() & (cf_text['sts_premodern'].str.lower() != 'banned')
mask_text = cf_text['text'].fillna('').str.contains(r'^This is a triggered mana ability\.$', regex=True) | cf_text['text'].fillna('').str.contains(r'\bThis is a triggered mana ability\.\b')
mask_single_face = cf_text['layout'].notna() & (~cf_text['layout'].isin(multi_face_layouts))

result = cf_text[mask_premodern & mask_text & mask_single_face]

# Count unique cards by id
answer = int(result['id'].nunique())
answer_df = pd.DataFrame({'count': [answer]})

target = answer_df

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
