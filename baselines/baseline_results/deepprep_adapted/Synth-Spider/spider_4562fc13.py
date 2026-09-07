import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_outcome_code", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_outcome_code"] = table_1["process_outcome_code"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_status_code", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_status_code"] = table_1["process_status_code"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_outcome_code", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().lower()
    #     # keep only letters/numbers/underscore (drop punctuation like ! and stray quotes)
    #     s = re.sub(r"[^a-z0-9_]+", "", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().lower()
        # keep only letters/numbers/underscore (drop punctuation like ! and stray quotes)
        s = re.sub(r"[^a-z0-9_]+", "", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_outcome_code"] = table_1["process_outcome_code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_status_code", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().lower()
    #     s = re.sub(r"[^a-z0-9_]+", "", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().lower()
        s = re.sub(r"[^a-z0-9_]+", "", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_status_code"] = table_1["process_status_code"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['document_id', 'process_id', 'process_outcome_code', 'process_status_code'])
    # SelectCol
    _cols = [c for c in ['document_id', 'process_id', 'process_outcome_code', 'process_status_code'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['document_id', 'process_id', 'process_outcome_code', 'process_status_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['document_id', 'process_id', 'process_outcome_code', 'process_status_code'], keep='last').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['process_status_code', 'attribute', 'value'])
    # SelectCol
    _cols = [c for c in ['process_status_code', 'attribute', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['attribute']) == 'process_status_description'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['attribute']) == 'process_status_description'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

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

prepared_table_1 = _prep_1(tables['table_3'])
docs_process = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
outcome_lut = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
status_lut = prepared_table_3

# Assume prepared tables already loaded as dataframes: docs_process, outcome_lut, status_lut
# 1) Filter to the target document
doc = docs_process[docs_process['document_id'] == 0]

# 2) Resolve process outcome description using the header-mapped outcome_lut row
#    The outcome code in docs_process (e.g., 'finish!' or 'start!') may contain punctuation; normalize to match outcome_lut column names
normalize = lambda s: str(s).strip().lower().replace('!', '')

doc = doc.assign(_outcome_col=doc['process_outcome_code'].map(normalize))

# outcome_lut is single-row; extract the matching column's value
outcome_row = outcome_lut.iloc[0]
# Map each row in doc to its outcome description by indexing the outcome_lut row with the normalized column name
outcome_desc = doc['_outcome_col'].map(lambda c: outcome_row.get(c, None))

doc = doc.assign(process_outcome_description=outcome_desc).drop(columns=['_outcome_col'])

# 3) Join status description from status_lut where attribute == 'process_status_description'
status_desc = status_lut[status_lut['attribute'] == 'process_status_description'][['process_status_code', 'value']].rename(columns={'value': 'process_status_description'})

doc = doc.merge(status_desc, on='process_status_code', how='left')

# 4) Select the requested columns for the final answer
answer = doc[['process_outcome_description', 'process_status_description']]

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
