import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'major_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'major_name', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'department', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'college', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['major_id', 'major_name', 'department', 'college']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'shuxing', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'zhi', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'member_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'shuxing', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'zhi', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'member_id', 'columns': 'shuxing', 'values': 'zhi', 'aggfunc': 'last'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_major', 'new_name': 'member_major_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'member_major_id', 'first_name', 'last_name', 't_shirt_size', 'phone']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['major_id'] = tmp_0['major_id'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['major_name'] = tmp_1['major_name'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['department'] = tmp_2['department'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['college'] = tmp_3['college'].astype(str)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['major_id', 'major_name', 'department', 'college']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['shuxing'] = tmp_0['shuxing'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['zhi'] = tmp_1['zhi'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['member_id'] = tmp_2['member_id'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['shuxing'] = tmp_3['shuxing'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['zhi'] = tmp_4['zhi'].astype(str)
    # Step 6: Pivot
    tmp_5 = pd.pivot_table(tmp_4, index='member_id', columns='shuxing', values='zhi', aggfunc='last').reset_index()
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'link_to_major': 'member_major_id'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['member_id', 'member_major_id', 'first_name', 'last_name', 't_shirt_size', 'phone']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
wide = prepared_table_2
# Join members to majors using the prepared join keys
integrated = wide.merge(prepared_table_1, how='left', left_on='member_major_id', right_on='major_id')
# Filter for Environmental Engineering majors using case-insensitive match on major_name
mask = integrated['major_name'].astype(str).str.strip().str.lower() == 'environmental engineering'
result = integrated[mask]
# Count members
count_df = result.agg({'member_id':'nunique'}).rename({'member_id':'count'}).to_frame().T
count_df['question'] = 'How many members of the Student_Club have majored Environmental Engineering?'
count_df['answer'] = count_df['count']
# Final projection
target = count_df[['question','answer']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
