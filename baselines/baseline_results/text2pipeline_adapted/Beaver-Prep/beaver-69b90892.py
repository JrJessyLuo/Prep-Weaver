import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'LIBRARY_RESERVE_CATALOG_KEY', 'new_name': 'library_reserve_catalog_key'}, {'old_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'new_name': 'material_status'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'library_reserve_catalog_key', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'material_status', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['library_reserve_catalog_key', 'LIBRARY_SUBJECT_OFFERED_KEY', 'material_status']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'CATALOG_TITLE', 'new_name': 'catalog_title'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'catalog_title', 'func': 'def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'library_reserve_catalog_key', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['library_reserve_catalog_key', 'catalog_title']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SUBJECT_TITLE', 'new_name': 'course_title'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_SUBJECT_OFFERED_KEY', 'course_title']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'LIBRARY_RESERVE_CATALOG_KEY': 'library_reserve_catalog_key', 'LIBRARY_MATERIAL_STATUS_KEY': 'material_status'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['library_reserve_catalog_key'] = pd.to_numeric(tmp_1['library_reserve_catalog_key'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_2['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['material_status'] = tmp_3['material_status'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['library_reserve_catalog_key', 'LIBRARY_SUBJECT_OFFERED_KEY', 'material_status']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'CATALOG_TITLE': 'catalog_title'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['catalog_title'] = tmp_1['catalog_title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['library_reserve_catalog_key'] = pd.to_numeric(tmp_2['library_reserve_catalog_key'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['library_reserve_catalog_key', 'catalog_title']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'SUBJECT_TITLE': 'course_title'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_SUBJECT_OFFERED_KEY', 'course_title']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
p1 = prepared_table_1.copy()
p2 = prepared_table_2.copy()
p3 = prepared_table_3.copy()

# Ensure key dtypes align for merges
if p1['library_reserve_catalog_key'].dtype != p2['library_reserve_catalog_key'].dtype:
    p1['library_reserve_catalog_key'] = p1['library_reserve_catalog_key'].astype(p2['library_reserve_catalog_key'].dtype, errors='ignore')

# Merge materials with catalog to ensure we have material rows; keep all materials even if no catalog title
m1 = p1.merge(p2, on='library_reserve_catalog_key', how='left')

# Normalize join key case/whitespace to improve linkage rates
m1['LIBRARY_SUBJECT_OFFERED_KEY'] = m1['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()
p3['LIBRARY_SUBJECT_OFFERED_KEY'] = p3['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()

# Merge to get course titles; keep all materials even if course title missing
m2 = m1.merge(p3, on='LIBRARY_SUBJECT_OFFERED_KEY', how='left')

# If course_title is entirely missing after the merge, fall back to using the subject key as a proxy title
if 'course_title' not in m2.columns or m2['course_title'].notna().sum() == 0:
    m2['course_title'] = m2['LIBRARY_SUBJECT_OFFERED_KEY']
else:
    # For partially missing titles, fill with subject key to avoid dropping rows
    m2['course_title'] = m2['course_title'].fillna(m2['LIBRARY_SUBJECT_OFFERED_KEY'])

# Aggregate per course title
agg = (
    m2.groupby('course_title', dropna=False)
      .agg(
          total_reserved_materials=('library_reserve_catalog_key', 'count'),
          distinct_material_status_count=('material_status', pd.Series.nunique)
      )
      .reset_index()
)

# Sort by total reserved materials descending, then course_title ascending for stability
agg = agg.sort_values(['total_reserved_materials', 'course_title'], ascending=[False, True])

# Final projection
target = agg[['course_title', 'total_reserved_materials', 'distinct_material_status_count']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
