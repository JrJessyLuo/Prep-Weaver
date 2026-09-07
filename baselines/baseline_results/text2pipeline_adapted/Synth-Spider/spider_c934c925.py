import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ISBN', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Title', 'func': 'def transform(s):\n    return str(s).strip().casefold()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ISBN', 'Title']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ISBN', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amt', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ISBN', 'oid', 'amt']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ISBN'] = tmp_0['ISBN'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().casefold()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Title'] = tmp_1['Title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ISBN', 'Title']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ISBN'] = tmp_0['ISBN'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['amt'] = pd.to_numeric(tmp_1['amt'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ISBN', 'oid', 'amt']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
merged = prepared_table_2.merge(prepared_table_1, on='ISBN', how='inner')
filtered = merged[merged['Title'].str.strip().str.casefold() == 'pride and prejudice']
# Count number of orders (distinct order IDs) for the title
result = filtered[['oid']].drop_duplicates()
target = result.assign(order_count=1).groupby(lambda x: True).agg({'order_count':'sum'}).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
