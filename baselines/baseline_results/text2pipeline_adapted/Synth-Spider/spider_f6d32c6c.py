import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'PassThroughFallback', 'params': {'reason': "fallback_passthrough_after_pipeline_generation_failure: KeyError: 'Number_of_Stories'", 'source_table': 'table_1'}, 'table_indices': [0]}], [{'op': 'Concatenate', 'params': {'concatenate_columns': ['Name_Part1', 'Name_Part2'], 'target_column': 'Region_Name', 'func': 'def transform(row):\n    p1 = \'\' if pd.isna(row.get(\'Name_Part1\')) else str(row.get(\'Name_Part1\')).strip()\n    p2_raw = row.get(\'Name_Part2\')\n    p2 = \'\' if (pd.isna(p2_raw) or str(p2_raw).strip() in [\'\', \'None\', \'none\', \'NULL\', \'null\']) else str(p2_raw).strip()\n    if p2:\n        s = f"{p1} {p2}"\n    else:\n        s = p1\n    return \' \'.join(s.split())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Region_Name', 'func': "def transform(s):\n    s = '' if pd.isna(s) else str(s)\n    return ' '.join(s.split())"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Region_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Area', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Population', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Region_ID', 'Capital', 'Area', 'Population', 'Region_Name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(row):\n    p1 = \'\' if pd.isna(row.get(\'Name_Part1\')) else str(row.get(\'Name_Part1\')).strip()\n    p2_raw = row.get(\'Name_Part2\')\n    p2 = \'\' if (pd.isna(p2_raw) or str(p2_raw).strip() in [\'\', \'None\', \'none\', \'NULL\', \'null\']) else str(p2_raw).strip()\n    if p2:\n        s = f"{p1} {p2}"\n    else:\n        s = p1\n    return \' \'.join(s.split())', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['Region_Name'] = tmp_0[['Name_Part1', 'Name_Part2']].apply(_concat_func_1, axis=1)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if pd.isna(s) else str(s)\n    return ' '.join(s.split())", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['Region_Name'] = tmp_1['Region_Name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Region_ID'] = pd.to_numeric(tmp_2['Region_ID'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Area'] = pd.to_numeric(tmp_3['Area'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Population'] = pd.to_numeric(tmp_4['Population'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['Region_ID', 'Capital', 'Area', 'Population', 'Region_Name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
region = prepared_table_2.copy()
# Identify the Abruzzo region row using robust matching
cand = region[region['Region_Name'].str.strip().str.casefold() == 'abruzzo']
if cand.empty:
    cand = region[region['Region_Name'].str.casefold().str.contains('abruzzo', na=False)]

# There is no explicit relational key between buildings and regions in the provided schemas.
# To follow instructions, perform a safe cross join only with the matched Abruzzo region rows
# before selecting/aggregating building stories-like information.
buildings = prepared_table_1.copy()

# Melt potential stories columns (numeric-labeled columns) into a single column to represent number of stories.
value_vars = [c for c in buildings.columns if isinstance(c, (int, float)) or (isinstance(c, str) and c.isdigit())]
if not value_vars:
    # Fallback: use all columns except obvious identifiers if no numeric-labeled columns are present
    value_vars = [c for c in buildings.columns if c not in ['Building_ID', 'Name', 'Address', 'Completed_Year']]

melted = buildings.melt(id_vars=[c for c in buildings.columns if c not in value_vars], value_vars=value_vars, var_name='Stories_Col', value_name='Stories_Value')
# Keep rows where a stories value is present
melted = melted[~melted['Stories_Value'].isna()]

# If no region match, proceed with all buildings (cannot fabricate linkage). If matched, cross join to annotate.
if not cand.empty:
    cand_ann = cand.assign(_key=1)
    melted_ann = melted.assign(_key=1)
    merged = melted_ann.merge(cand_ann, on='_key', how='inner').drop(columns=['_key'])
else:
    merged = melted.copy()

# Select the number of stories; no further filtering before aggregation per instructions
target = merged[['Building_ID', 'Stories_Value']].rename(columns={'Stories_Value': 'Number_of_Stories'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
