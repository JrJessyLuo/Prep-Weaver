import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Collection_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Parent_Collection_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Name_Prefix', 'Name_Suffix'], 'target_column': 'Full_Name', 'func': "def transform(row):\n    p = '' if row.get('Name_Prefix') is None else str(row.get('Name_Prefix'))\n    s = '' if row.get('Name_Suffix') is None else str(row.get('Name_Suffix'))\n    return p + s"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Collection_ID', 'Parent_Collection_ID', 'Collection_Description', 'Name_Prefix', 'Name_Suffix', 'Full_Name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Collection_ID'] = pd.to_numeric(tmp_0['Collection_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Parent_Collection_ID'] = pd.to_numeric(tmp_1['Parent_Collection_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(row):\n    p = '' if row.get('Name_Prefix') is None else str(row.get('Name_Prefix'))\n    s = '' if row.get('Name_Suffix') is None else str(row.get('Name_Suffix'))\n    return p + s", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_2['Full_Name'] = tmp_2[['Name_Prefix', 'Name_Suffix']].apply(_concat_func_1, axis=1)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['Collection_ID', 'Parent_Collection_ID', 'Collection_Description', 'Name_Prefix', 'Name_Suffix', 'Full_Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
best_id_df = prepared_table_1.loc[prepared_table_1['Full_Name'].str.strip().str.casefold() == 'best']
if best_id_df.empty:
    # Fallback: try partial robust matching on name parts
    mask = (
        prepared_table_1['Name_Prefix'].fillna('').str.strip().str.casefold().eq('b') &
        prepared_table_1['Name_Suffix'].fillna('').str.strip().str.casefold().eq('est')
    )
    best_id_df = prepared_table_1.loc[mask]

# If still empty, use the most plausible candidate by concatenation equality ignoring case
if best_id_df.empty:
    best_id_df = prepared_table_1.loc[
        (prepared_table_1['Name_Prefix'].fillna('') + prepared_table_1['Name_Suffix'].fillna('')).str.casefold() == 'best'
    ]

# Proceed if we have at least one candidate; use all candidates' IDs
best_ids = best_id_df['Collection_ID'].unique()
related = prepared_table_1[prepared_table_1['Parent_Collection_ID'].isin(best_ids)]
# Exclude the collection itself from the count of related collections
related_distinct = related[~related['Collection_ID'].isin(best_ids)]
count = related_distinct['Collection_ID'].nunique()
target = related_distinct.assign(related_count=count).iloc[:1][['related_count']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
