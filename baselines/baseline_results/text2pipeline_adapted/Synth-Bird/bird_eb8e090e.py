import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['id', 'team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['id'], 'value_vars': [1321, 837, 414, 523, 1036, 615, 219, 1032, 1289, 887, 577, 1251, 1191, 568, 1108, 853, 169, 1102, 1119, 68, 1042, 454, 670, 1173, 193, 124, 416, 278, 434, 1170, 185, 555, 1188, 77, 906, 1024, 1285, 375, 1447], 'var_name': 'team_api_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'team_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'id', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'attribute'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['attribute', 'team_api_id', 'value']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['id', 'team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['id'], value_vars=[1321, 837, 414, 523, 1036, 615, 219, 1032, 1289, 887, 577, 1251, 1191, 568, 1108, 853, 169, 1102, 1119, 68, 1042, 454, 670, 1173, 193, 124, 416, 278, 434, 1170, 185, 555, 1188, 77, 906, 1024, 1285, 375, 1447], var_name='team_api_id', value_name='value')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['team_api_id'] = pd.to_numeric(tmp_1['team_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['id'] = tmp_2['id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'id': 'attribute'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['attribute', 'team_api_id', 'value']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
_frames = []
if isinstance(prepared_table_1, pd.DataFrame) and not prepared_table_1.empty:
    _tmp = prepared_table_1.copy()
    _tmp['__prepared_table__'] = 'prepared_table_1'
    _frames.append(_tmp)
if isinstance(prepared_table_2, pd.DataFrame) and not prepared_table_2.empty:
    _tmp = prepared_table_2.copy()
    _tmp['__prepared_table__'] = 'prepared_table_2'
    _frames.append(_tmp)
target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
