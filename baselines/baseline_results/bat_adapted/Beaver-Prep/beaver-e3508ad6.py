import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_NUMBER','OWNERSHIP_TYPE','PARENT_BUILDING_NUMBER','DATE_BUILT','DATE_OCCUPIED','BUILDING_SORT']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
