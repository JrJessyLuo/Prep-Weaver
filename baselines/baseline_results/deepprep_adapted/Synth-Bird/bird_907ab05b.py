import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['APTT'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['APTT'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
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
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="APTT", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['APTT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['APTT']
    if _dtype == "datetime64":
        table_1['APTT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['APTT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['APTT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['APTT'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ID']
    if _dtype == "datetime64":
        table_1['ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'APTT'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'APTT'] if c in table_1.columns]
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     val = row.get('Thrombosis', None)
    #     if val is None:
    #         return False
    #     s = str(val).strip().replace('\"\"','\"')
    #     if len(s) >= 2 and ((s[0] == '\"' and s[-1] == '\"') or (s[0] == \"'\" and s[-1] == \"'\")):
    #         s = s[1:-1].strip()
    #     return s in {'0','1'}
    # """)
    # Filter
    def filter_func(row):
        val = row.get('Thrombosis', None)
        if val is None:
            return False
        s = str(val).strip().replace('\"\"','\"')
        if len(s) >= 2 and ((s[0] == '\"' and s[-1] == '\"') or (s[0] == \"'\" and s[-1] == \"'\")):
            s = s[1:-1].strip()
        return s in {'0','1'}
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Thrombosis", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     # collapse doubled quotes seen in data like ""1""
    #     t = t.replace('""', '"')
    #     # remove wrapping quotes if present
    #     if len(t) >= 2 and ((t[0] == '"' and t[-1] == '"') or (t[0] == "'" and t[-1] == "'")):
    #         t = t[1:-1].strip()
    #     # keep only 0/1 if any stray chars exist
    #     m = re.search(r'[01]', t)
    #     return m.group(0) if m else t
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        t = str(s).strip()
        # collapse doubled quotes seen in data like ""1""
        t = t.replace('""', '"')
        # remove wrapping quotes if present
        if len(t) >= 2 and ((t[0] == '"' and t[-1] == '"') or (t[0] == "'" and t[-1] == "'")):
            t = t[1:-1].strip()
        # keep only 0/1 if any stray chars exist
        m = re.search(r'[01]', t)
        return m.group(0) if m else t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Thrombosis"] = table_1["Thrombosis"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Examination Date", date_format="%Y-%m-%d")
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
    table_1['Examination Date'] = table_1['Examination Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Examination Date'] = table_1['Examination Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ID", dtype="int64")
    # CastType
    _dtype = 'int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ID']
    if _dtype == "datetime64":
        table_1['ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Examination Date', 'Thrombosis'])
    # SelectCol
    _cols = [c for c in ['ID', 'Examination Date', 'Thrombosis'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_labs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_clinical = prepared_table_2

# prepared_labs and prepared_clinical are the synthesized per-table targets
labs = prepared_labs.copy()
clin = prepared_clinical.copy()

# Ensure ID types align
labs['ID'] = pd.to_numeric(labs['ID'], errors='coerce')
clin['ID'] = pd.to_numeric(clin['ID'], errors='coerce')

# Normalize APTT to numeric
labs['APTT'] = pd.to_numeric(labs['APTT'], errors='coerce')

# Define abnormal APTT (example threshold: > 40 seconds). Adjust if domain-specific threshold provided elsewhere.
abnormal_labs = labs[labs['APTT'].notna() & (labs['APTT'] > 40)]

# If multiple lab dates per patient, keep at least one abnormal occurrence per patient
abnormal_patients = abnormal_labs[['ID']].dropna().drop_duplicates()

# Merge with clinical thrombosis info
merged = abnormal_patients.merge(clin[['ID','Thrombosis']], on='ID', how='left')

# Normalize thrombosis flag to boolean (1 => has thrombosis, 0 => no thrombosis)
# Values appear like '"1"' or '"0"', possibly with quotes/spaces
def to_bool_no_throm(v):
    if pd.isna(v):
        return None
    s = str(v).strip().strip('"\'').strip()
    if s == '1':
        return False  # has thrombosis
    if s == '0':
        return True   # no thrombosis
    return None

no_throm_mask = merged['Thrombosis'].apply(to_bool_no_throm)

# Count patients with abnormal APTT and no thrombosis
answer = int(pd.Series(no_throm_mask).fillna(False).sum())

result = pd.DataFrame({'count_patients_abnormal_aptt_no_thrombosis': [answer]})

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
