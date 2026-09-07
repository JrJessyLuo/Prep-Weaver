import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'IdClient', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': 'def transform(s):\n    # Trim outer whitespace and collapse internal whitespace, but keep original casing of letters\n    if s is None:\n        return s\n    text = str(s)\n    # split on whitespace and join with single spaces preserves original case of tokens\n    parts = text.strip().split()\n    return " ".join(parts)'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdClient', 'Name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'IdClient', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'IdClient']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['IdClient'] = pd.to_numeric(tmp_0['IdClient'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim outer whitespace and collapse internal whitespace, but keep original casing of letters\n    if s is None:\n        return s\n    text = str(s)\n    # split on whitespace and join with single spaces preserves original case of tokens\n    parts = text.strip().split()\n    return " ".join(parts)', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Name'] = tmp_1['Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IdClient', 'Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['IdClient'] = pd.to_numeric(tmp_0['IdClient'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['IdOrder', 'IdClient']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='IdClient')
counts = integrated.groupby(['IdClient', 'Name'], as_index=False).agg(num_orders=('IdOrder', 'count'))
target = counts[['Name', 'num_orders']].sort_values(['Name']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
