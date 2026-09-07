import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ORGANIZATION_LEVEL', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ASSIGNABLE', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'ORGANIZATION_NUMBER', 'target_columns': ['ORGANIZATION_NUMBER_int', 'tmp_drop'], 'func': "def transform(s):\n    import pandas as pd\n    import numpy as np\n    x = pd.to_numeric(pd.Series(s), errors='coerce')\n    xi = np.rint(x).astype('float')\n    xi = pd.Series(xi).where(pd.isna(x), xi).astype('Int64')\n    return [xi, pd.Series([None]*len(x))]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['tmp_drop', 'ORGANIZATION_NUMBER']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return pd.Series(s).astype(str).str.strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ORGANIZATION_ID', 'new_name': 'org_id'}, {'old_name': 'ORGANIZATION_LEVEL', 'new_name': 'level'}, {'old_name': 'ORGANIZATION_NUMBER_int', 'new_name': 'org_number'}, {'old_name': 'ORGANIZATION_NAME', 'new_name': 'org_name'}, {'old_name': 'ASSIGNABLE', 'new_name': 'assignable_flag'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['org_id', 'org_number', 'level', 'org_name', 'assignable_flag']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ORGANIZATION_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ORGANIZATION_KEY', 'new_name': 'organization_key'}, {'old_name': 'AREA', 'new_name': 'area'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['organization_key', 'area', 'fac_room_key']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ORGANIZATION_LEVEL'] = pd.to_numeric(tmp_0['ORGANIZATION_LEVEL'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ASSIGNABLE'] = pd.to_numeric(tmp_1['ASSIGNABLE'], errors='coerce').fillna(0).astype(int)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import pandas as pd\n    import numpy as np\n    x = pd.to_numeric(pd.Series(s), errors='coerce')\n    xi = np.rint(x).astype('float')\n    xi = pd.Series(xi).where(pd.isna(x), xi).astype('Int64')\n    return [xi, pd.Series([None]*len(x))]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['ORGANIZATION_NUMBER'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['ORGANIZATION_NUMBER_int'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['tmp_drop'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['tmp_drop', 'ORGANIZATION_NUMBER'], errors='ignore').copy()
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return pd.Series(s).astype(str).str.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['ORGANIZATION_NAME'] = tmp_4['ORGANIZATION_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'ORGANIZATION_ID': 'org_id', 'ORGANIZATION_LEVEL': 'level', 'ORGANIZATION_NUMBER_int': 'org_number', 'ORGANIZATION_NAME': 'org_name', 'ASSIGNABLE': 'assignable_flag'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['org_id', 'org_number', 'level', 'org_name', 'assignable_flag']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ORGANIZATION_KEY'] = pd.to_numeric(tmp_0['ORGANIZATION_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['AREA'] = pd.to_numeric(tmp_1['AREA'], errors='coerce').astype(float)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'ORGANIZATION_KEY': 'organization_key', 'AREA': 'area'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['organization_key', 'area', 'fac_room_key']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, left_on='organization_key', right_on='org_id', how='inner')
# Exclude Cambridge-MIT Institute by robust case-insensitive matching on org_name; if no match found, keep all
mask_cmi = integrated['org_name'].str.contains('Cambridge-MIT Institute', case=False, na=False)
if mask_cmi.any():
    integrated = integrated[~mask_cmi]
# Aggregate by organization
agg = integrated.groupby(['org_id','org_number','level','org_name','assignable_flag'], as_index=False).agg(total_area=('area','sum'), rooms=('fac_room_key','nunique'), avg_area=('area','mean'))
# Prepare formatted fields
agg['assignable'] = agg['assignable_flag'].apply(lambda x: 'ASSIGNABLE' if int(x)==1 else 'NON-ASSIGNABLE')
# Round totals and counts to integers
agg['total_area_int'] = agg['total_area'].round(0).astype('Int64')
agg['rooms_int'] = agg['rooms'].round(0).astype('Int64')
# Average room area rounded to integer as well per instructions ("Area and number of rooms" -> avg treated as area metric too)
agg['avg_area_int'] = agg['avg_area'].round(0).astype('Int64')
# Thousands separators
agg['total_area_fmt'] = agg['total_area_int'].apply(lambda v: f"{int(v):,}" if v is not None and v==v else '')
agg['rooms_fmt'] = agg['rooms_int'].apply(lambda v: f"{int(v):,}" if v is not None and v==v else '')
agg['avg_area_fmt'] = agg['avg_area_int'].apply(lambda v: f"{int(v):,}" if v is not None and v==v else '')
# Indented name per level (level 2 -> 1 space, level 3 -> 2 spaces, ... up to level 6)
agg['indent_spaces'] = agg['level'].apply(lambda L: ' ' * max(0, min(6, int(L)) - 1) if pd.notnull(L) else '')
agg['formatted_name'] = agg['indent_spaces'] + agg['org_name']
# Final projection and reasonable ordering (by org_number then org_id)
target = agg[['org_id','org_number','level','formatted_name','assignable','total_area_fmt','rooms_fmt','avg_area_fmt']].sort_values(by=['org_number','org_id'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
