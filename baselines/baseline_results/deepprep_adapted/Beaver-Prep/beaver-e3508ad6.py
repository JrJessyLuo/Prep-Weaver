import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['OWNERSHIP_TYPE', 'PARENT_BUILDING_NUMBER', 'DATE_BUILT', 'DATE_OCCUPIED', 'BUILDING_SORT'], how="all")
    # DropNulls
    table_1 = table_1.dropna(subset=['OWNERSHIP_TYPE', 'PARENT_BUILDING_NUMBER', 'DATE_BUILT', 'DATE_OCCUPIED', 'BUILDING_SORT'], how='all').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DATE_BUILT", date_format="%Y-%m-%d")
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
    table_1['DATE_BUILT'] = table_1['DATE_BUILT'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_BUILT'] = table_1['DATE_BUILT'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DATE_OCCUPIED", date_format="%Y-%m-%d")
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
    table_1['DATE_OCCUPIED'] = table_1['DATE_OCCUPIED'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_OCCUPIED'] = table_1['DATE_OCCUPIED'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # Keep owned buildings only
    #     if str(row.get('OWNERSHIP_TYPE', '')).strip().upper() != 'OWNED':
    #         return False
    # 
    #     # Exclude subdivisions: parent building number must be null/empty
    #     p = row.get('PARENT_BUILDING_NUMBER', None)
    #     if pd.isna(p):
    #         return True
    #     p_str = str(p).strip().lower()
    #     return p_str in ['', 'nan', 'none', '(null)']
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # Keep owned buildings only
        if str(row.get('OWNERSHIP_TYPE', '')).strip().upper() != 'OWNED':
            return False

        # Exclude subdivisions: parent building number must be null/empty
        p = row.get('PARENT_BUILDING_NUMBER', None)
        if pd.isna(p):
            return True
        p_str = str(p).strip().lower()
        return p_str in ['', 'nan', 'none', '(null)']
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['BUILDING_SORT', 'BUILDING_NUMBER'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_SORT', 'BUILDING_NUMBER'], ascending=[True, True])

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'OWNERSHIP_TYPE', 'PARENT_BUILDING_NUMBER', 'DATE_BUILT', 'DATE_OCCUPIED', 'BUILDING_SORT'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'OWNERSHIP_TYPE', 'PARENT_BUILDING_NUMBER', 'DATE_BUILT', 'DATE_OCCUPIED', 'BUILDING_SORT'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_buildings = prepared_table_1

# Start from the prepared single-table result
df = prepared_buildings.copy()

# Filter to owned buildings that are not subdivisions (no parent building)
df = df[(df['OWNERSHIP_TYPE'].str.upper() == 'OWNED') & (df['PARENT_BUILDING_NUMBER'].isna())]

# Order by BUILDING_SORT (fallback to BUILDING_NUMBER if BUILDING_SORT missing)
if 'BUILDING_SORT' in df.columns:
    sort_key = df['BUILDING_SORT'].astype(str).str.zfill(4)
else:
    sort_key = df['BUILDING_NUMBER'].astype(str)

df = df.assign(_sort_key=sort_key).sort_values('_sort_key', kind='mergesort')

# Extract years; handle unknowns

def extract_year(s):
    # s like 'MM/DD/YYYY' or NaN
    if pd.isna(s) or str(s).strip().lower() in {'nan', '', 'none'}:
        return None
    txt = str(s).strip()
    # try to find a 4-digit year at end
    m = re.search(r'(19|20)\d{2}$', txt)
    if m:
        return int(m.group(0))
    # fallback: parse with pandas
    try:
        dt = pd.to_datetime(txt, errors='coerce')
        if pd.isna(dt):
            return None
        return int(dt.year)
    except Exception:
        return None

built_year = df['DATE_BUILT'].apply(extract_year)
occupied_year = df['DATE_OCCUPIED'].apply(extract_year)

out = pd.DataFrame({
    'Construction Start Year': built_year,
    'Building Number': df['BUILDING_NUMBER'].astype(str),
    'Year of Initial Occupancy': occupied_year
})

# Replace unknowns with 'UNKNOWN' for display columns except where we need to suppress repeat year
out['Year of Initial Occupancy'] = out['Year of Initial Occupancy'].apply(lambda x: 'UNKNOWN' if pd.isna(x) else str(int(x)))

# Suppress repeating construction start year values: show only when it differs from previous row
shown_years = []
prev = None
for y in out['Construction Start Year']:
    if pd.isna(y):
        shown_years.append('UNKNOWN')
        prev = prev  # no change
    else:
        if prev is None or y != prev:
            shown_years.append(str(int(y)))
        else:
            shown_years.append(None)
        prev = y

out['Construction Start Year'] = shown_years

# Append total row: (null, '#building Buildings', null)
count_buildings = len(df)
summary_row = pd.DataFrame({
    'Construction Start Year': [None],
    'Building Number': [f"{count_buildings} Buildings"],
    'Year of Initial Occupancy': [None]
})

result = pd.concat([out, summary_row], ignore_index=True)

target = result[['Construction Start Year', 'Building Number', 'Year of Initial Occupancy']]

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
