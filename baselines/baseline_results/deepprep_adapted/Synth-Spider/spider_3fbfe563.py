import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="document_id", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['document_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['document_id']
    if _dtype == "datetime64":
        table_1['document_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['document_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['document_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['document_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['document_id', 'category_prefix', 'connector', 'topic', 'document_description'])
    # SelectCol
    _cols = [c for c in ['document_id', 'category_prefix', 'connector', 'topic', 'document_description'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="process_status_code", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_outcome_part1", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["process_outcome_part1"] = table_1["process_outcome_part1"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_outcome_part2", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["process_outcome_part2"] = table_1["process_outcome_part2"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="document_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['document_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['document_id']
    if _dtype == "datetime64":
        table_1['document_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['document_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['document_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['document_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="process_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['process_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['process_id']
    if _dtype == "datetime64":
        table_1['process_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['process_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['process_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['process_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['document_id', 'process_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['document_id', 'process_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['document_id', 'process_id', 'process_status_code', 'process_outcome_part1', 'process_outcome_part2'])
    # SelectCol
    _cols = [c for c in ['document_id', 'process_id', 'process_status_code', 'process_outcome_part1', 'process_outcome_part2'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="process_id", func="""
    # def is_valid_process_id(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     s = s.replace('"','').replace("'",'').strip()
    #     return s.isdigit()
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_process_id(val):
        if val is None:
            return False
        s = str(val).strip()
        s = s.replace('"','').replace("'",'').strip()
        return s.isdigit()
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_process_id(val))
        except Exception:
            return False
    table_1 = table_1[table_1['process_id'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_id", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove any leading/trailing quote characters repeatedly
    #     s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
    #     # if still wrapped multiple times, repeat once more
    #     s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove any leading/trailing quote characters repeatedly
        s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
        # if still wrapped multiple times, repeat once more
        s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_id"] = table_1["process_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_name", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
    #     s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
        s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_name"] = table_1["process_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="process_description", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
    #     s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
        s = re.sub(r'^[\s"']+|[\s"']+$', '', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["process_description"] = table_1["process_description"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="process_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['process_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['process_id']
    if _dtype == "datetime64":
        table_1['process_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['process_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['process_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['process_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['process_id', 'process_name', 'process_description'])
    # SelectCol
    _cols = [c for c in ['process_id', 'process_name', 'process_description'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['process_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['process_id'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_documents = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_document_processes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_process_metadata = prepared_table_3

# Assume prepared_documents, prepared_document_processes, prepared_process_metadata are DataFrames

# Build the document title string to match the question
prepared_documents = prepared_documents.assign(document_title=(prepared_documents['category_prefix'].astype(str).str.strip() + ' ' + prepared_documents['connector'].astype(str).str.strip() + ' ' + prepared_documents['topic'].astype(str).str.strip()))

# Filter to the document titled "Travel to Brazil"
doc_filtered = prepared_documents[prepared_documents['document_title'].str.casefold() == 'travel to brazil']

# Join documents to their processes
joined = doc_filtered.merge(prepared_document_processes, on='document_id', how='inner')

# Normalize process_id types for joining
prepared_process_metadata_norm = prepared_process_metadata.copy()
prepared_process_metadata_norm['process_id'] = prepared_process_metadata_norm['process_id'].astype(str).str.replace('"', '').str.strip()
joined['process_id'] = joined['process_id'].astype(str).str.strip()

# Join to process metadata to get process_name
final = joined.merge(prepared_process_metadata_norm[['process_id','process_name']], on='process_id', how='left')

# Select the process_name (deduplicate if multiple rows)
answer = final['process_name'].dropna().unique().tolist()

# If multiple, choose unique names; result variable should be a string or list as needed
result = answer[0] if len(answer) == 1 else answer

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
