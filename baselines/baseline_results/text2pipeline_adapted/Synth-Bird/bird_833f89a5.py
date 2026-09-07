import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'weizhi', 'new_name': 'location'}, {'old_name': 'guojia', 'new_name': 'country'}, {'old_name': 'wangzhi', 'new_name': 'url'}, {'old_name': 'name', 'new_name': 'circuit_name'}, {'old_name': 'circuitRef', 'new_name': 'circuit_ref'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['circuitId', 'circuit_ref', 'circuit_name', 'country', 'location']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'raceId', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'raceId', 'new_name': 'raceId'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'year', 'circuitId']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['year', 'url']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['circuitId'] = pd.to_numeric(tmp_0['circuitId'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'weizhi': 'location', 'guojia': 'country', 'wangzhi': 'url', 'name': 'circuit_name', 'circuitRef': 'circuit_ref'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['circuitId', 'circuit_ref', 'circuit_name', 'country', 'location']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['raceId'] = pd.to_numeric(tmp_0['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 2: Pivot
    tmp_1 = pd.pivot_table(tmp_0, index='raceId', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['year'] = pd.to_numeric(tmp_2['year'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['circuitId'] = pd.to_numeric(tmp_3['circuitId'], errors='coerce').fillna(0).astype(int)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'raceId': 'raceId'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['raceId', 'year', 'circuitId']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['year'] = pd.to_numeric(tmp_0['year'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['year', 'url']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_12', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', on='circuitId')
# Identify Brands Hatch rows via circuit name or ref, case-insensitive contains
bh_mask_name = integrated['circuit_name'].fillna('').str.contains('brands hatch', case=False, na=False)
bh_mask_ref = integrated['circuit_ref'].fillna('').str.contains('brands', case=False, na=False)
bh_rows = integrated[bh_mask_name | bh_mask_ref]
# Among those, identify British Grands Prix by country/location context; prefer country == 'UK'/'United Kingdom' or location contains 'Brit' if available
country = integrated['country'].fillna('')
loc = integrated['location'].fillna('')
brit_mask = country.str.contains('UK|United Kingdom|Great Britain|Britain|England', case=False, na=False) | loc.str.contains('UK|United Kingdom|Great Britain|Britain|England', case=False, na=False)
bh_brit = bh_rows[bh_rows.index.isin(integrated[brit_mask].index)]
# Fallback: if no rows after brit_mask, use all Brands Hatch rows
bh_final = bh_brit if len(bh_brit) > 0 else bh_rows
# Get the last season year where Brands Hatch hosted the British GP (i.e., max year)
if len(bh_final) == 0:
    # Fallback to any Brands Hatch year if filters removed all
    bh_final = bh_rows
last_year = bh_final['year'].max() if 'year' in bh_final.columns and len(bh_final) > 0 else None
# Optionally attach season URL
result = pd.DataFrame({'last_season_year': [last_year]})
result = result.merge(prepared_table_3, how='left', left_on='last_season_year', right_on='year')
target = result[['last_season_year', 'url']].rename(columns={'url': 'season_url'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
