import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['University_ID', 'yxmc', 'City', 'State', 'dm', 'ssfl', 'Enrollment', 'Home_Conference'])
    # SelectCol
    _cols = [c for c in ['University_ID', 'yxmc', 'City', 'State', 'dm', 'ssfl', 'Enrollment', 'Home_Conference'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['University_ID', 'yxmc'])
    # SelectCol
    _cols = [c for c in ['University_ID', 'yxmc'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="yxmc", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes, trim whitespace, normalize internal whitespace
    #     s2 = str(s).strip().strip('"').strip("'").strip()
    #     s2 = re.sub(r'\s+', ' ', s2)
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove surrounding quotes, trim whitespace, normalize internal whitespace
        s2 = str(s).strip().strip('"').strip("'").strip()
        s2 = re.sub(r'\s+', ' ', s2)
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["yxmc"] = table_1["yxmc"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['University_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['University_ID'], keep='first').reset_index(drop=True)

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
    # DropColumn(table_name="table_1", drop_columns=['Major_Code'])
    # DropColumn
    table_1 = table_1.drop(columns=['Major_Code'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Major_ID", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding double quotes repeatedly (handles '""1""' cases)
    #     while len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding double quotes repeatedly (handles '""1""' cases)
        while len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Major_ID"] = table_1["Major_ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Major_Name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     while len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        while len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Major_Name"] = table_1["Major_Name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Major_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Major_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Major_ID']
    if _dtype == "datetime64":
        table_1['Major_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Major_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Major_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Major_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Major_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Major_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Major_ID', 'Major_Name'])
    # SelectCol
    _cols = [c for c in ['Major_ID', 'Major_Name'] if c in table_1.columns]
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
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="m_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['m_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['m_id']
    if _dtype == "datetime64":
        table_1['m_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['m_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['m_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['m_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['u_id', 'm_id'])
    # SelectCol
    _cols = [c for c in ['u_id', 'm_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['u_id', 'm_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['u_id', 'm_id'], keep='first').reset_index(drop=True)

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
universities = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
majors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
university_major_offerings = prepared_table_3

majors_filtered = majors[majors['Major_Name'].isin(['Accounting', 'Urban Education'])]
offerings_joined = university_major_offerings.merge(majors_filtered, left_on='m_id', right_on='Major_ID', how='inner')
# Count distinct matched majors per university and keep those with both
major_counts = offerings_joined.groupby('u_id')['Major_Name'].nunique().reset_index(name='num_majors')
unis_with_both = major_counts[major_counts['num_majors'] == 2]
result = unis_with_both.merge(universities, left_on='u_id', right_on='University_ID', how='inner')
answer = result['yxmc'].drop_duplicates().sort_values().tolist()

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
