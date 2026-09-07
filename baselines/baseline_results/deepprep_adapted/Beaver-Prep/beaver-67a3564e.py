import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MOIRA_LIST_MEMBER_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID']
    if _dtype == "datetime64":
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     val = row.get('MOIRA_LIST_KEY')
    #     if pd.isna(val):
    #         return False
    #     s = str(val).strip()
    #     return s.lower().startswith('b')
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        val = row.get('MOIRA_LIST_KEY')
        if pd.isna(val):
            return False
        s = str(val).strip()
        return s.lower().startswith('b')
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     if isinstance(s, float) and pd.isna(s):
    #         return None
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        if isinstance(s, float) and pd.isna(s):
            return None
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_MIT_ID", func="""
    # def transform_func(s):
    #     import re
    #     if s is None:
    #         return None
    #     if isinstance(s, float) and pd.isna(s):
    #         return None
    #     txt = str(s).strip().strip('"').strip("'")
    #     if txt == '' or txt.lower() in ('nan', 'none', 'null'):
    #         return None
    #     # remove trailing .0 if present (common when numeric IDs were read as floats)
    #     txt = re.sub(r'\.0$', '', txt)
    #     # keep only digits; if anything unexpected remains, return None
    #     return txt if re.fullmatch(r'\d+', txt) else None
    # """)
    # StandardizeString
    def transform_func(s):
        import re
        if s is None:
            return None
        if isinstance(s, float) and pd.isna(s):
            return None
        txt = str(s).strip().strip('"').strip("'")
        if txt == '' or txt.lower() in ('nan', 'none', 'null'):
            return None
        # remove trailing .0 if present (common when numeric IDs were read as floats)
        txt = re.sub(r'\.0$', '', txt)
        # keep only digits; if anything unexpected remains, return None
        return txt if re.fullmatch(r'\d+', txt) else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_MIT_ID"] = table_1["MOIRA_LIST_MEMBER_MIT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MOIRA_LIST_MEMBER_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID']
    if _dtype == "datetime64":
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'] if c in table_1.columns]
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
    # AddNewColumn(table_name="table_1", new_column_name="KRB_NAME_UPPERCASE", func="""
    # def compute(row):
    #     v = row.get('krb_name')
    #     if v is None:
    #         return None
    #     return str(v).strip().strip('"').upper()
    # """)
    # AddNewColumn
    def compute(row):
        v = row.get('krb_name')
        if v is None:
            return None
        return str(v).strip().strip('"').upper()
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["KRB_NAME_UPPERCASE"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="krb_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     # remove wrapping quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        # remove wrapping quotes if present
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
    table_1["krb_name"] = table_1["krb_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
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
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MIT_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MIT_ID']
    if _dtype == "datetime64":
        table_1['MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MIT_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MIT_ID', 'krb_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MIT_ID', 'krb_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'DEPARTMENT_NAME', 'krb_name', 'KRB_NAME_UPPERCASE'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'DEPARTMENT_NAME', 'krb_name', 'KRB_NAME_UPPERCASE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_mailing_list_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_people_directory = prepared_table_2

# Start from prepared tables
ml = prepared_mailing_list_members.copy()
dir = prepared_people_directory.copy()

# Normalize keys for joining
# MIT IDs in ml are float-like strings (e.g., '984301411.0'); convert to string ints
ml_id = ml['MOIRA_LIST_MEMBER_MIT_ID'].astype(str).str.replace('.0$', '', regex=True).str.strip()
dir_id = dir['MIT_ID'].astype(str).str.strip()

# Normalize kerberos names: strip and uppercase
ml_krb = ml['moira_list_member'].astype(str).str.strip().str.upper()
dir_krb = dir['KRB_NAME_UPPERCASE'].astype(str).str.strip()

ml_norm = ml.assign(_MIT_ID_NORM=ml_id, _KRB_NORM=ml_krb)
dir_norm = dir.assign(_MIT_ID_NORM=dir_id, _KRB_NORM=dir_krb)

# Left join by MIT_ID first
joined_id = ml_norm.merge(
    dir_norm[['MIT_ID','DEPARTMENT_NAME','_MIT_ID_NORM']],
    how='left', left_on='_MIT_ID_NORM', right_on='_MIT_ID_NORM', suffixes=('', '_dir')
)

# Rows not matched on MIT_ID
unmatched = joined_id[joined_id['DEPARTMENT_NAME'].isna()].copy()
matched = joined_id[~joined_id['DEPARTMENT_NAME'].isna()].copy()

# Attempt secondary join on kerberos for the unmatched subset
if not unmatched.empty:
    unmatched2 = unmatched.drop(columns=['DEPARTMENT_NAME'], errors='ignore').merge(
        dir_norm[['KRB_NAME_UPPERCASE','DEPARTMENT_NAME','_KRB_NORM']],
        how='left', left_on='_KRB_NORM', right_on='_KRB_NORM', suffixes=('', '_krb')
    )
    rejoined = pd.concat([matched, unmatched2], ignore_index=True)
else:
    rejoined = matched

# Filter to EECS department members
eecs_mask = rejoined['DEPARTMENT_NAME'].astype(str).str.contains('Electrical Engineering and Computer Science', case=False, na=False)
eecs_members = rejoined[eecs_mask].copy()

# Consider only lists whose names start with 'B' (case-insensitive)
b_mask = eecs_members['MOIRA_LIST_KEY'].astype(str).str.startswith(('B','b'), na=False)
eecs_b = eecs_members[b_mask].copy()

# Compute outputs
# 1) Count of distinct mailing lists with at least one EECS member
count_lists = eecs_b['MOIRA_LIST_KEY'].nunique()

# 2) List starting with B that has the highest number of EECS members and that count
list_counts = eecs_b.groupby('MOIRA_LIST_KEY', dropna=False).size().reset_index(name='eecs_member_count')
if list_counts.empty:
    top_list_name = None
    top_member_count = 0
else:
    top_row = list_counts.sort_values(['eecs_member_count','MOIRA_LIST_KEY'], ascending=[False, True]).iloc[0]
    top_list_name = top_row['MOIRA_LIST_KEY']
    top_member_count = int(top_row['eecs_member_count'])

answer = {
    'count_mailing_lists_starting_B_with_EECS_members': int(count_lists),
    'list_with_max_EECS_members_starting_B': top_list_name,
    'max_EECS_member_count_in_that_list': top_member_count
}

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
