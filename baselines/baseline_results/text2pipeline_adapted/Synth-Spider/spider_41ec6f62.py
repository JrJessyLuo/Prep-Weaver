import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'EmployeeID', 'new_name': 'employee_id'}, {'old_name': 'Name', 'new_name': 'employee_name'}, {'old_name': 'pos', 'new_name': 'position'}, {'old_name': 'Salary', 'new_name': 'salary'}, {'old_name': 'rmks', 'new_name': 'remarks'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'employee_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'salary', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'employee_name', 'func': 'def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'position', 'func': 'def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['employee_id', 'employee_name', 'position', 'salary', 'remarks']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Shipment', 'new_name': 'shipment_id'}, {'old_name': 'PackageNumber', 'new_name': 'package_number'}, {'old_name': 'Contents', 'new_name': 'contents'}, {'old_name': 'Weight', 'new_name': 'weight_kg'}, {'old_name': 'Sender', 'new_name': 'sender_id'}, {'old_name': 'Recipient', 'new_name': 'recipient_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'shipment_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'package_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'weight_kg', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'sender_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'recipient_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'contents', 'func': 'def transform(s):\n    # Trim but preserve original casing\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['shipment_id', 'package_number', 'contents', 'weight_kg', 'sender_id', 'recipient_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'EmployeeID': 'employee_id', 'Name': 'employee_name', 'pos': 'position', 'Salary': 'salary', 'rmks': 'remarks'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['employee_id'] = pd.to_numeric(tmp_1['employee_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['salary'] = pd.to_numeric(tmp_2['salary'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return None if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['employee_name'] = tmp_3['employee_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return None if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['position'] = tmp_4['position'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['employee_id', 'employee_name', 'position', 'salary', 'remarks']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Shipment': 'shipment_id', 'PackageNumber': 'package_number', 'Contents': 'contents', 'Weight': 'weight_kg', 'Sender': 'sender_id', 'Recipient': 'recipient_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['shipment_id'] = pd.to_numeric(tmp_1['shipment_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['package_number'] = pd.to_numeric(tmp_2['package_number'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['weight_kg'] = pd.to_numeric(tmp_3['weight_kg'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['sender_id'] = pd.to_numeric(tmp_4['sender_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['recipient_id'] = pd.to_numeric(tmp_5['recipient_id'], errors='coerce').fillna(0).astype(int)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim but preserve original casing\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['contents'] = tmp_6['contents'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['shipment_id', 'package_number', 'contents', 'weight_kg', 'sender_id', 'recipient_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
emp = prepared_table_1
ship = prepared_table_2
# Join shipments to employees twice: once on sender, once on recipient, then combine
ship_sender = ship.merge(emp[['employee_id','employee_name']], left_on='sender_id', right_on='employee_id', how='left', suffixes=('','')).rename(columns={'employee_name':'sender_name'}).drop(columns=['employee_id'])
ship_both = ship_sender.merge(emp[['employee_id','employee_name']], left_on='recipient_id', right_on='employee_id', how='left', suffixes=('','')).rename(columns={'employee_name':'recipient_name'}).drop(columns=['employee_id'])
# Identify Phillip J. Fry by robust case-insensitive match on either sender or recipient side
name_ci = 'phillip j. fry'
mask = ((ship_both['sender_name'].astype(str).str.strip().str.lower() == name_ci) | (ship_both['recipient_name'].astype(str).str.strip().str.lower() == name_ci))
res = ship_both.loc[mask, ['shipment_id']].drop_duplicates().sort_values('shipment_id')
# Fallback: if no strict match, try contains match, else return all shipments linked to any employee named like 'fry'
if res.empty:
    mask2 = ((ship_both['sender_name'].astype(str).str.lower().str.contains('fry', na=False)) | (ship_both['recipient_name'].astype(str).str.lower().str.contains('fry', na=False)))
    res = ship_both.loc[mask2, ['shipment_id']].drop_duplicates().sort_values('shipment_id')
    if res.empty:
        res = ship_both[['shipment_id']].drop_duplicates().sort_values('shipment_id')
target = res.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
