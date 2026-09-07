import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'CATALOG_TITLE', 'func': "def transform(s):\n    if s is None or (isinstance(s, float) and pd.isna(s)):\n        return ''\n    try:\n        return str(s)\n    except Exception:\n        return ''"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'CATALOG_TITLE', 'target_columns': ['TITLE_LENGTH'], 'func': 'def transform(s):\n    try:\n        return [len(s) if isinstance(s, str) else 0]\n    except Exception:\n        return [0]'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'library_reserve_catalog_key', 'new_name': 'LIBRARY_RESERVE_CATALOG_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_RESERVE_CATALOG_KEY', 'CATALOG_YEAR', 'CATALOG_TITLE', 'TITLE_LENGTH']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else None'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'LIBRARY_MATERIAL_STATUS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(tmp_0['LIBRARY_RESERVE_CATALOG_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['LIBRARY_MATERIAL_STATUS_KEY'] = tmp_1['LIBRARY_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    if s is None or (isinstance(s, float) and pd.isna(s)):\n        return ''\n    try:\n        return str(s)\n    except Exception:\n        return ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['CATALOG_TITLE'] = tmp_0['CATALOG_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    try:\n        return [len(s) if isinstance(s, str) else 0]\n    except Exception:\n        return [0]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['CATALOG_TITLE'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['TITLE_LENGTH'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'library_reserve_catalog_key': 'LIBRARY_RESERVE_CATALOG_KEY'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_RESERVE_CATALOG_KEY', 'CATALOG_YEAR', 'CATALOG_TITLE', 'TITLE_LENGTH']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_MATERIAL_STATUS_KEY'] = tmp_0['LIBRARY_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'LIBRARY_MATERIAL_STATUS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='LIBRARY_RESERVE_CATALOG_KEY', how='inner').merge(prepared_table_3, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')
# Exclude non-year or placeholder years like 0 if present for publication year-based aggregation
valid = integrated[integrated['CATALOG_YEAR'].notna()]
# Aggregate by publication year
agg = valid.groupby('CATALOG_YEAR').agg(
    total_reserved_materials=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    avg_title_length=('TITLE_LENGTH', 'mean'),
    distinct_status_count=('LIBRARY_MATERIAL_STATUS_KEY', 'nunique'),
    courses_count=('LIBRARY_RESERVE_CATALOG_KEY', 'nunique')
).reset_index()
# Rename columns per question wording
agg = agg.rename(columns={'CATALOG_YEAR': 'publication_year', 'courses_count': 'number_of_courses'})
# Sort by publication year descending
target = agg.sort_values('publication_year', ascending=False)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
