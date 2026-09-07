import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Receipt', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 1, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 2, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 3, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 4, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 5, 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['Receipt'], 'value_vars': [1, 2, 3, 4, 5], 'var_name': 'ItemPos', 'value_name': 'ItemCode'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['ItemPos']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Receipt', 'ItemCode']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': "fallback_passthrough_after_pipeline_generation_failure: KeyError: 'Receipt'", 'source_table': 'table_2'}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['Id', 'LastName', 'FirstName']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Receipt'] = pd.to_numeric(tmp_0['Receipt'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1[1] = tmp_1[1].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2[2] = tmp_2[2].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3[3] = tmp_3[3].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4[4] = tmp_4[4].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5[5] = tmp_5[5].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: Stack
    tmp_6 = tmp_5.melt(id_vars=['Receipt'], value_vars=[1, 2, 3, 4, 5], var_name='ItemPos', value_name='ItemCode')
    # Step 8: DropColumn
    tmp_7 = tmp_6.drop(columns=['ItemPos'], errors='ignore').copy()
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['Receipt', 'ItemCode']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['Id', 'LastName', 'FirstName']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
items = prepared_table_1.copy()
receipts_wide = prepared_table_2.copy()
customers = prepared_table_3.copy()

# Reshape receipts_wide from wide (columns are receipt numbers) to long with rows per receipt
# The first column indicates the attribute name for the two rows: 'Date' and 'CustomerId'.
attr_col = receipts_wide.columns[0]
attr_names = receipts_wide[attr_col].astype(str).tolist()

# Melt all receipt-number columns
value_cols = [c for c in receipts_wide.columns if c != attr_col]
long = receipts_wide.melt(id_vars=[attr_col], value_vars=value_cols, var_name='Receipt', value_name='Value')

# Pivot to get columns Date and CustomerId per receipt
long['Attribute'] = long[attr_col].astype(str)
long = long.drop(columns=[attr_col])
receipts_long = long.pivot_table(index='Receipt', columns='Attribute', values='Value', aggfunc='first').reset_index()

# Ensure proper dtypes for joining
# Items.Receipt is int; convert receipts_long['Receipt'] to int where possible
receipts_long['Receipt'] = receipts_long['Receipt'].astype(str)
receipts_long['Receipt'] = receipts_long['Receipt'].str.extract(r'(\d+)')[0].astype(float).astype('Int64')
items['Receipt'] = items['Receipt'].astype('int64')

# CustomerId should be numeric
if 'CustomerId' in receipts_long.columns:
    receipts_long['CustomerId'] = pd.to_numeric(receipts_long['CustomerId'], errors='coerce')

# Merge items with receipts to link items to customers and dates
integrated = items.merge(receipts_long, on='Receipt', how='left')

# Condition A: receipts that include an apple flavor pie, broad case-insensitive match on ItemCode
# Include patterns like APPLE PIE, APPLE-PIE, A-PIE, PIE APPLE, etc.
pat = r'(apple\s*-?\s*pie|\bappl?e?\b.*\bpie\b|\bpie\b.*\bapple\b|\bap?ie\b)'
item_mask = integrated['ItemCode'].astype(str).str.contains(pat, case=False, na=False)
receipts_with_apple_pie = integrated.loc[item_mask, ['Receipt']].drop_duplicates()

# Condition B: receipts where the customer id is 12
receipts_cust12 = receipts_long.loc[receipts_long['CustomerId'] == 12, ['Receipt']].drop_duplicates()

# Union and sort
result_receipts = pd.concat([receipts_with_apple_pie, receipts_cust12], ignore_index=True).drop_duplicates()

# Fall back: if empty, relax by matching any code containing 'APPLE' or 'PIE'
if result_receipts.empty:
    loose_mask = integrated['ItemCode'].astype(str).str.contains(r'(apple|pie)', case=False, na=False)
    fallback_receipts = integrated.loc[loose_mask, ['Receipt']].drop_duplicates()
    result_receipts = pd.concat([fallback_receipts, receipts_cust12], ignore_index=True).drop_duplicates()

# Final target: list of qualifying receipt numbers
target = result_receipts.sort_values('Receipt').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
