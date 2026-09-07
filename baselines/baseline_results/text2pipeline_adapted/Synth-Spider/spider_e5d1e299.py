import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['Institution_ID', 'Institution_Name', 'Location']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['staff_ID'], 'value_vars': ['Canada', 'United Kindom', 'United States'], 'var_name': 'affiliation_country', 'value_name': 'Institution_ID'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Institution_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['affiliation_country']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['staff_ID', 'Institution_ID']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'yuangong_id', 'new_name': 'staff_ID'}, {'old_name': 'huiyi_id', 'new_name': 'Conference_ID'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'staff_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Conference_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['staff_ID', 'Conference_ID', 'role']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'Conference_Info', 'target_columns': ['conf_series', 'year_str'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 2:\n        return parts\n    # Fallback: extract last 4 consecutive digits\n    import re\n    m = re.search(r'(\\d{4})$', s)\n    yr = m.group(1) if m else ''\n    return [s, yr]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year_str', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'year_str', 'new_name': 'Year'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Conference_ID', 'Year']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['Institution_ID', 'Institution_Name', 'Location']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['staff_ID'], value_vars=['Canada', 'United Kindom', 'United States'], var_name='affiliation_country', value_name='Institution_ID')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Institution_ID'] = pd.to_numeric(tmp_1['Institution_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: DropColumn
    tmp_2 = tmp_1.drop(columns=['affiliation_country'], errors='ignore').copy()
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['staff_ID', 'Institution_ID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'yuangong_id': 'staff_ID', 'huiyi_id': 'Conference_ID'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['staff_ID'] = pd.to_numeric(tmp_1['staff_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Conference_ID'] = pd.to_numeric(tmp_2['Conference_ID'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['staff_ID', 'Conference_ID', 'role']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 2:\n        return parts\n    # Fallback: extract last 4 consecutive digits\n    import re\n    m = re.search(r'(\\d{4})$', s)\n    yr = m.group(1) if m else ''\n    return [s, yr]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['Conference_Info'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['conf_series'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['year_str'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['year_str'] = pd.to_numeric(tmp_1['year_str'], errors='coerce').fillna(0).astype(int)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'year_str': 'Year'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['Conference_ID', 'Year']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
staff_affil = prepared_table_2
staff_conf = prepared_table_3
conf_year = prepared_table_4
univ = prepared_table_1
# Link staff to conferences and filter to 2004 participations
sc = staff_conf.merge(conf_year, on='Conference_ID', how='left')
sc2004 = sc[sc['Year'] == 2004]
# Link participations to universities via staff affiliations
sc2004_affil = sc2004.merge(staff_affil, on='staff_ID', how='left')
# Universities with at least one participating staff in 2004
univ_with_participants = sc2004_affil[['Institution_ID']].dropna().drop_duplicates()
# Left-join all universities to marker and keep those without participants
all_univ = univ[['Institution_ID', 'Institution_Name', 'Location']]
marked = all_univ.merge(univ_with_participants.assign(had_participation_2004=True), on='Institution_ID', how='left')
result = marked[marked['had_participation_2004'].isna()][['Institution_Name', 'Location']]
# Final target
target = result.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
