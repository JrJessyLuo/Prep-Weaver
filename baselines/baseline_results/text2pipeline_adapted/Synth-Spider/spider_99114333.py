import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'agency_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'agency_details', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['agency_id', 'agency_details']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'sic_client_combined', 'target_columns': ['sic_part_1', 'sic_part_2'], 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    parts = s.split(\'|\', 1)\n    if len(parts) == 1:\n        return [parts[0], ""]\n    return [parts[0], parts[1]]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'agency_id', 'sic_client_combined', 'sic_part_1', 'sic_part_2']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['agency_id'] = pd.to_numeric(tmp_0['agency_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['agency_details'] = tmp_1['agency_details'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['agency_id', 'agency_details']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    parts = s.split(\'|\', 1)\n    if len(parts) == 1:\n        return [parts[0], ""]\n    return [parts[0], parts[1]]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['sic_client_combined'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['sic_part_1'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['sic_part_2'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['client_id', 'agency_id', 'sic_client_combined', 'sic_part_1', 'sic_part_2']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='agency_id')
mask_exact = (integrated['sic_part_1'].astype(str).str.casefold() == 'mac'.casefold()) | (integrated['sic_part_2'].astype(str).str.casefold() == 'mac'.casefold())
subset = integrated[mask_exact]
if subset.empty:
    # Fallback: broad contains match over original combined field and split parts
    cf = integrated['sic_client_combined'].astype(str).str.casefold()
    m2 = cf.str.contains('mac'.casefold(), na=False) | integrated['sic_part_1'].astype(str).str.casefold().str.contains('mac', na=False) | integrated['sic_part_2'].astype(str).str.casefold().str.contains('mac', na=False)
    subset = integrated[m2]
# Show agency details for the matching client(s)
target = subset[['client_id', 'agency_id', 'agency_details']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
