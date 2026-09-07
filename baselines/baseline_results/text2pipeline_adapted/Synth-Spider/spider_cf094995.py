import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Customer_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': 'def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == s[-1]) and s[0] in "\'\\""):\n        s = s[1:-1].strip()\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Customer_ID', 'Name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Customer_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Branch_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Chow Mein', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Kung Pao Chicken', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Ma Po Tofu', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Peking Roasted Duck', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Spring Rolls', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['Customer_ID', 'Branch_ID'], 'value_vars': ['Chow Mein', 'Kung Pao Chicken', 'Ma Po Tofu', 'Peking Roasted Duck', 'Spring Rolls'], 'var_name': 'Dish', 'value_name': 'Quantity'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Customer_ID', 'Branch_ID', 'Dish', 'Quantity']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Customer_ID'] = pd.to_numeric(tmp_0['Customer_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == s[-1]) and s[0] in "\'\\""):\n        s = s[1:-1].strip()\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Name'] = tmp_1['Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Customer_ID', 'Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Customer_ID'] = pd.to_numeric(tmp_0['Customer_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Branch_ID'] = pd.to_numeric(tmp_1['Branch_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Chow Mein'] = pd.to_numeric(tmp_2['Chow Mein'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Kung Pao Chicken'] = pd.to_numeric(tmp_3['Kung Pao Chicken'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Ma Po Tofu'] = pd.to_numeric(tmp_4['Ma Po Tofu'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Peking Roasted Duck'] = pd.to_numeric(tmp_5['Peking Roasted Duck'], errors='coerce').astype(float)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['Spring Rolls'] = pd.to_numeric(tmp_6['Spring Rolls'], errors='coerce').astype(float)
    # Step 8: Stack
    tmp_7 = tmp_6.melt(id_vars=['Customer_ID', 'Branch_ID'], value_vars=['Chow Mein', 'Kung Pao Chicken', 'Ma Po Tofu', 'Peking Roasted Duck', 'Spring Rolls'], var_name='Dish', value_name='Quantity')
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['Customer_ID', 'Branch_ID', 'Dish', 'Quantity']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
long_orders = prepared_table_2.copy()
# Keep only actual ordered lines (positive quantities); preserve 0s if present but drop NaNs
long_orders = long_orders[long_orders['Quantity'].notna()]
# Join with customers to get names
integrated = long_orders.merge(prepared_table_1, on='Customer_ID', how='inner')
# Project required columns and sort by quantity desc
result = integrated[['Customer_ID', 'Name', 'Dish', 'Quantity']]
result = result.sort_values(by='Quantity', ascending=False)
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
