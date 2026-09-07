import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['Driver_ID', 'Citizenship', 'Racing_Series', 'First_Name', 'Last_Name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Driver_ID', 'new_name': 'Header'}]}, 'table_indices': [0]}, {'op': 'Transpose', 'params': {}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 0, 'target_columns': ['Driver_ID', 'Vehicle_ID'], 'func': 'def transform(s):\n    import pandas as pd\n    # s is the transposed index column after reset; we need to reset index and pair with value column.\n    # This function will be applied element-wise; we will reconstruct using available ops, so here just passthrough.\n    return [s, None]'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['Driver_ID', 'Citizenship', 'Racing_Series', 'First_Name', 'Last_Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Driver_ID': 'Header'})
    # Step 2: Transpose
    tmp_1 = tmp_0.T.reset_index()
    # Step 3: SplitColumn
    result = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import pandas as pd\n    # s is the transposed index column after reset; we need to reset index and pair with value column.\n    # This function will be applied element-wise; we will reconstruct using available ops, so here just passthrough.\n    return [s, None]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = result[0].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    result['Driver_ID'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    result['Vehicle_ID'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
drv = prepared_table_1
links = prepared_table_2

# Clean links: remove header-like rows and normalize types
links_clean = links.copy()
# Drop rows where Driver_ID is not a digit (e.g., header artifacts) or is null
links_clean = links_clean[links_clean['Driver_ID'].astype(str).str.fullmatch(r"\d+")]
# Convert Driver_ID to numeric to match dtype in drv
links_clean['Driver_ID'] = links_clean['Driver_ID'].astype(int)

# Merge drivers with links
integrated = drv.merge(links_clean[['Driver_ID', 'Vehicle_ID']], how='left', on='Driver_ID')

# Drivers with no vehicles: Vehicle_ID is null or explicitly 'None' (case-insensitive)
no_vehicle_mask = integrated['Vehicle_ID'].isna() | integrated['Vehicle_ID'].astype(str).str.strip().str.lower().eq('none')
no_vehicle = integrated.loc[no_vehicle_mask, ['Driver_ID']].drop_duplicates()

# Produce a one-row DataFrame with the count
target = no_vehicle.agg(count=('Driver_ID', 'size')).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
