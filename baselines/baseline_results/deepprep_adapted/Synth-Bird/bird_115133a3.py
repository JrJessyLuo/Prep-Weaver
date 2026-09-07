import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['cds'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['cds'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="cds", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['cds'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['cds']
    if _dtype == "datetime64":
        table_1['cds'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['cds'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['cds'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['cds'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="AvgScrWrite", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['AvgScrWrite'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['AvgScrWrite']
    if _dtype == "datetime64":
        table_1['AvgScrWrite'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['AvgScrWrite'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['AvgScrWrite'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['AvgScrWrite'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['cds', 'school_part1', 'school_part2', 'AvgScrWrite'])
    # SelectCol
    _cols = [c for c in ['cds', 'school_part1', 'school_part2', 'AvgScrWrite'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # DropNulls(table_name="table_1", subset=['Phone'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Phone'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CDSCode", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CDSCode'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CDSCode']
    if _dtype == "datetime64":
        table_1['CDSCode'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CDSCode'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CDSCode'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CDSCode'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="OpenDate", date_format="%Y-%m-%d")
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
    table_1['OpenDate'] = table_1['OpenDate'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['OpenDate'] = table_1['OpenDate'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="ClosedDate", date_format="%Y-%m-%d")
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
    table_1['ClosedDate'] = table_1['ClosedDate'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['ClosedDate'] = table_1['ClosedDate'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CDSCode', 'School', 'OpenDate', 'ClosedDate', 'Phone'])
    # SelectCol
    _cols = [c for c in ['CDSCode', 'School', 'OpenDate', 'ClosedDate', 'Phone'] if c in table_1.columns]
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
prepared_scores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_directory = prepared_table_2

# Merge scores with directory on CDS code (as strings to ensure match)
t = prepared_scores.copy()
d = prepared_directory.copy()

t['cds'] = t['cds'].astype(str)
d['CDSCode'] = d['CDSCode'].astype(str)
merged = t.merge(d, left_on='cds', right_on='CDSCode', how='inner')

# Parse dates
merged['OpenDate_parsed'] = pd.to_datetime(merged['OpenDate'], errors='coerce')
merged['ClosedDate_parsed'] = pd.to_datetime(merged['ClosedDate'], errors='coerce')

# Filter: opened after 1991 OR closed before 2000
cond_open = merged['OpenDate_parsed'] > pd.Timestamp('1991-12-31')
cond_closed = (merged['ClosedDate_parsed'].notna()) & (merged['ClosedDate_parsed'] < pd.Timestamp('2000-01-01'))
filtered = merged[cond_open | cond_closed].copy()

# Compose school name preference: use directory School if available; otherwise join parts
name_from_parts = (filtered['school_part1'].fillna('') + ' ' + filtered['school_part2'].fillna('')).str.strip()
filtered['SchoolName'] = filtered['School'].where(filtered['School'].notna() & (filtered['School'].str.strip() != ''), name_from_parts)

# Communication number (phone)
filtered['CommunicationNumber'] = filtered['Phone']

# Ensure writing score numeric
filtered['AvgScrWrite'] = pd.to_numeric(filtered['AvgScrWrite'], errors='coerce')

# Prepare final columns
result = filtered[['SchoolName', 'AvgScrWrite', 'CommunicationNumber']].dropna(subset=['SchoolName', 'AvgScrWrite'])

# The question asks for the average score in writing for those schools, listing each school's name and its score, plus communication number if any.
# If a single overall average is also desired, compute as:
overall_avg = result['AvgScrWrite'].mean()

# Return both the per-school list and the overall average in a dict-like structure
answer = { 'overall_average_writing_score': overall_avg, 'schools': result }

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
