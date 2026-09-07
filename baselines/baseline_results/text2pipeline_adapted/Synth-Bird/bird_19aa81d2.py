import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'member_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'attribute', 'value']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['zip_code', 1060, 24614, 60408, 15555, 82717, 10019, 6504, 31816, 48205, 29471, 53702, 20525, 37161, 35576, 76544, 76883, 94940, 78657, 46614, 44090, 17611, 66842, 30072, 94133, 19086, 78961, 31516, 40504, 52765, 57533, 33637, 43350, 57719, 33982, 75449, 99143, 40403, 65111, 48208]}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['member_id'] = tmp_0['member_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['attribute'] = tmp_1['attribute'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['value'] = tmp_2['value'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['member_id', 'attribute', 'value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['zip_code', 1060, 24614, 60408, 15555, 82717, 10019, 6504, 31816, 48205, 29471, 53702, 20525, 37161, 35576, 76544, 76883, 94940, 78657, 46614, 44090, 17611, 66842, 30072, 94133, 19086, 78961, 31516, 40504, 52765, 57533, 33637, 43350, 57719, 33982, 75449, 99143, 40403, 65111, 48208]].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
members = prepared_table_1.copy()
# Isolate hometown entries (attribute names may vary in casing/format); keep robust matching
attr_col = members['attribute'].astype(str).str.strip().str.lower()
hometown_mask = attr_col.isin(['hometown', 'home_town', 'home town', 'city', 'homecity', 'home city'])
hometowns = members.loc[hometown_mask, ['member_id', 'value']].rename(columns={'value':'hometown_raw'})

# Robust Maryland detection from free-text hometowns
val = hometowns['hometown_raw'].astype(str).str.strip()
val_lower = val.str.lower()
# Look for full state name or common abbreviations
is_md = (
    val_lower.str.contains(r'\bmaryland\b', regex=True) |
    val_lower.str.contains(r'\bmd\b', regex=True) |
    val_lower.str.contains(r',\s*md\b', regex=True) |
    val_lower.str.endswith(' md') |
    val_lower.str.endswith(' maryland')
)

hometowns_md = hometowns.loc[is_md]

# Count distinct members with Maryland hometowns
count_df = hometowns_md[['member_id']].drop_duplicates()
count_df['maryland_hometown_count'] = 1
result = count_df.agg({'maryland_hometown_count':'sum'}).to_frame().T
result = result.rename(columns={'maryland_hometown_count':'count'})

# If no rows matched due to naming variance, fall back to zero-count but keep structure
if result.empty:
    result = count_df.head(0)
    result = result.assign(count=0).iloc[:1][['count']]
else:
    result = result[['count']]

target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
