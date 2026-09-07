import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ConfName_Year'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ConfName_Year'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Conference_ID", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes and whitespace
    #     s = str(s).strip().strip('"').strip("'").strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # remove surrounding quotes and whitespace
        s = str(s).strip().strip('"').strip("'").strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Conference_ID"] = table_1["Conference_ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Conference_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Conference_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Conference_ID']
    if _dtype == "datetime64":
        table_1['Conference_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Conference_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Conference_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Conference_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ConfName_Year", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'").strip()
    #     # collapse internal whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     # normalize spaces around '#'
    #     s = re.sub(r'\s*#\s*', '#', s)
    #     # normalize casing for the conference acronym part (before '#')
    #     if '#' in s:
    #         name, year = s.split('#', 1)
    #         return f"{name.strip().upper()}#{year.strip()}"
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'").strip()
        # collapse internal whitespace
        s = re.sub(r'\s+', ' ', s)
        # normalize spaces around '#'
        s = re.sub(r'\s*#\s*', '#', s)
        # normalize casing for the conference acronym part (before '#')
        if '#' in s:
            name, year = s.split('#', 1)
            return f"{name.strip().upper()}#{year.strip()}"
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ConfName_Year"] = table_1["ConfName_Year"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Conference_ID', 'ConfName_Year'])
    # SelectCol
    _cols = [c for c in ['Conference_ID', 'ConfName_Year'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="Conference_ID", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     # remove repeated quotes like ""1"" -> 1
    #     s2 = s2.replace('""', '"')
    #     if len(s2) >= 2 and s2[0] == '"' and s2[-1] == '"':
    #         s2 = s2[1:-1]
    #     return s2.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip()
        # remove repeated quotes like ""1"" -> 1
        s2 = s2.replace('""', '"')
        if len(s2) >= 2 and s2[0] == '"' and s2[-1] == '"':
            s2 = s2[1:-1]
        return s2.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Conference_ID"] = table_1["Conference_ID"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Conference_ID', 'staff_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Conference_ID', 'staff_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Conference_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Conference_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Conference_ID']
    if _dtype == "datetime64":
        table_1['Conference_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Conference_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Conference_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Conference_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="staff_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['staff_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['staff_ID']
    if _dtype == "datetime64":
        table_1['staff_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['staff_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['staff_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['staff_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Conference_ID', 'staff_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Conference_ID', 'staff_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Conference_ID', 'staff_ID'])
    # SelectCol
    _cols = [c for c in ['Conference_ID', 'staff_ID'] if c in table_1.columns]
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
prepared_conferences = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_participation = prepared_table_2

# Assume prepared_conferences and prepared_participation are provided as DataFrames
# 1) Parse ConfName_Year into name and year (robust to variations like 'acl#2003', 'ACL#2004', ' Naccl #2003')
def parse_name_year(s):
    if pd.isna(s):
        return pd.Series({'conference_name': None, 'year': None})
    txt = str(s).strip()
    # Normalize separators and spaces
    txt = txt.replace(' ', '')
    parts = txt.split('#')
    if len(parts) == 2:
        name_part, year_part = parts[0], parts[1]
    else:
        # Fallback: last 4-digit year
        m = re.search(r'(\d{4})', txt)
        year_part = m.group(1) if m else None
        name_part = re.sub(r'(\d{4})', '', txt)
    # Normalize casing of name
    conference_name = name_part.strip()
    year = pd.to_numeric(str(year_part).strip(), errors='coerce')
    return pd.Series({'conference_name': conference_name, 'year': year})

conf = prepared_conferences.copy()
conf[['conference_name', 'year']] = conf['ConfName_Year'].apply(parse_name_year)

# 2) Count participants per conference (distinct staff_ID)
part = prepared_participation.copy()
participants = part.dropna(subset=['staff_ID']).groupby('Conference_ID')['staff_ID'].nunique().reset_index(name='num_participants')

# 3) Integrate on Conference_ID
result = conf.merge(participants, on='Conference_ID', how='left')
result['num_participants'] = result['num_participants'].fillna(0).astype(int)

# 4) Final columns per question
target = result[['Conference_ID', 'conference_name', 'year', 'num_participants']]

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
