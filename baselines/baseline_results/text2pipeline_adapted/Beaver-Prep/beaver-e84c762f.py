import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    s = "" if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s)\n    # normalize whitespace and case, trim\n    s = " ".join(s.split())\n    return s.lower()\n'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME', 'func': 'def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == \'nan\'):\n        return ""\n    s = str(s)\n    # collapse internal whitespace\n    s = " ".join(s.split())\n    return s.strip()\n'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['LAST_NAME', 'FIRST_NAME', 'MIDDLE_NAME'], 'target_column': 'FULL_NAME_ALT', 'func': "def transform(row):\n    ln = row.get('LAST_NAME', '')\n    fn = row.get('FIRST_NAME', '')\n    mn = row.get('MIDDLE_NAME', '')\n    parts = []\n    ln = '' if ln is None or (isinstance(ln, float) and str(ln) == 'nan') else str(ln).strip()\n    fn = '' if fn is None or (isinstance(fn, float) and str(fn) == 'nan') else str(fn).strip()\n    mn = '' if mn is None or (isinstance(mn, float) and str(mn) == 'nan') else str(mn).strip()\n    if ln:\n        parts.append(ln)\n    # build 'Last, First Middle' with proper punctuation/spaces\n    if fn:\n        if parts:\n            parts[-1] = parts[-1] + ','  \n        parts.append(fn)\n    if mn:\n        parts.append(mn)\n    full = ' '.join(parts).strip()\n    # normalize whitespace\n    full = ' '.join(full.split())\n    return full\n"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['FULL_NAME', 'FULL_NAME_ALT'], 'target_column': 'STUDENT_FULL_NAME', 'func': "def transform(row):\n    primary = row.get('FULL_NAME', '')\n    alt = row.get('FULL_NAME_ALT', '')\n    def norm(s):\n        if s is None or (isinstance(s, float) and str(s) == 'nan'):\n            return ''\n        s = str(s).strip()\n        return ' '.join(s.split())\n    primary = norm(primary)\n    alt = norm(alt)\n    return primary if primary else alt\n"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DEPARTMENT_NAME', 'new_name': 'DEPT_NAME'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPT_NAME', 'STUDENT_FULL_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SIS_ADMIN_DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_PHONE_AREA_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'department_phone_number', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_PHONE_AREA_CODE', 'func': "def transform(s):\n    s = str(s).strip()\n    if s.lower() in {'nan', 'none', ''}:\n        return ''\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.replace(' ', '')"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'department_phone_number', 'func': "def transform(s):\n    s = str(s).strip()\n    if s.lower() in {'nan', 'none'}:\n        s = ''\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.replace(' ', '')"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number'], 'target_column': 'DEPARTMENT_PHONE', 'func': "def transform(row):\n    area = row['DEPARTMENT_PHONE_AREA_CODE'] if row['DEPARTMENT_PHONE_AREA_CODE'] is not None else ''\n    num = row['department_phone_number'] if row['department_phone_number'] is not None else ''\n    area = str(area)\n    num = str(num)\n    if area and area.lower() not in {'nan'}:\n        phone = f'({area}) {num}' if num else f'({area})'\n    else:\n        phone = num\n    return phone.replace(' ', '')"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SIS_ADMIN_DEPARTMENT_NAME', 'new_name': 'DEPT_NAME'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPT_NAME', 'DEPARTMENT_PHONE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s)\n    # normalize whitespace and case, trim\n    s = " ".join(s.split())\n    return s.lower()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['DEPARTMENT_NAME'] = tmp_0['DEPARTMENT_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DEPARTMENT'] = tmp_1['DEPARTMENT'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    if s is None or (isinstance(s, float) and str(s) == \'nan\'):\n        return ""\n    s = str(s)\n    # collapse internal whitespace\n    s = " ".join(s.split())\n    return s.strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['FULL_NAME'] = tmp_2['FULL_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(row):\n    ln = row.get('LAST_NAME', '')\n    fn = row.get('FIRST_NAME', '')\n    mn = row.get('MIDDLE_NAME', '')\n    parts = []\n    ln = '' if ln is None or (isinstance(ln, float) and str(ln) == 'nan') else str(ln).strip()\n    fn = '' if fn is None or (isinstance(fn, float) and str(fn) == 'nan') else str(fn).strip()\n    mn = '' if mn is None or (isinstance(mn, float) and str(mn) == 'nan') else str(mn).strip()\n    if ln:\n        parts.append(ln)\n    # build 'Last, First Middle' with proper punctuation/spaces\n    if fn:\n        if parts:\n            parts[-1] = parts[-1] + ','  \n        parts.append(fn)\n    if mn:\n        parts.append(mn)\n    full = ' '.join(parts).strip()\n    # normalize whitespace\n    full = ' '.join(full.split())\n    return full\n", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_3['FULL_NAME_ALT'] = tmp_3[['LAST_NAME', 'FIRST_NAME', 'MIDDLE_NAME']].apply(_concat_func_3, axis=1)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(row):\n    primary = row.get('FULL_NAME', '')\n    alt = row.get('FULL_NAME_ALT', '')\n    def norm(s):\n        if s is None or (isinstance(s, float) and str(s) == 'nan'):\n            return ''\n        s = str(s).strip()\n        return ' '.join(s.split())\n    primary = norm(primary)\n    alt = norm(alt)\n    return primary if primary else alt\n", globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_4['STUDENT_FULL_NAME'] = tmp_4[['FULL_NAME', 'FULL_NAME_ALT']].apply(_concat_func_4, axis=1)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'DEPARTMENT_NAME': 'DEPT_NAME'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['DEPT_NAME', 'STUDENT_FULL_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SIS_ADMIN_DEPARTMENT_NAME'] = tmp_0['SIS_ADMIN_DEPARTMENT_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DEPARTMENT_PHONE_AREA_CODE'] = tmp_1['DEPARTMENT_PHONE_AREA_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['department_phone_number'] = tmp_2['department_phone_number'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = str(s).strip()\n    if s.lower() in {'nan', 'none', ''}:\n        return ''\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.replace(' ', '')", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['DEPARTMENT_PHONE_AREA_CODE'] = tmp_3['DEPARTMENT_PHONE_AREA_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = str(s).strip()\n    if s.lower() in {'nan', 'none'}:\n        s = ''\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.replace(' ', '')", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['department_phone_number'] = tmp_4['department_phone_number'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: Concatenate
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec("def transform(row):\n    area = row['DEPARTMENT_PHONE_AREA_CODE'] if row['DEPARTMENT_PHONE_AREA_CODE'] is not None else ''\n    num = row['department_phone_number'] if row['department_phone_number'] is not None else ''\n    area = str(area)\n    num = str(num)\n    if area and area.lower() not in {'nan'}:\n        phone = f'({area}) {num}' if num else f'({area})'\n    else:\n        phone = num\n    return phone.replace(' ', '')", globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_5['DEPARTMENT_PHONE'] = tmp_5[['DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number']].apply(_concat_func_4, axis=1)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'SIS_ADMIN_DEPARTMENT_NAME': 'DEPT_NAME'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['DEPT_NAME', 'DEPARTMENT_PHONE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='DEPT_NAME')
# Compute counts and longest full-name length per department
integrated['NAME_LEN'] = integrated['STUDENT_FULL_NAME'].astype(str).str.len()
aggr = integrated.groupby(['DEPT_NAME', 'DEPARTMENT_PHONE'], dropna=False).agg(NUM_STUDENTS=('STUDENT_FULL_NAME','count'), LONGEST_NAME_LEN=('NAME_LEN','max')).reset_index()
# Final projection and sort by department name for readability
target = aggr[['DEPT_NAME','DEPARTMENT_PHONE','NUM_STUDENTS','LONGEST_NAME_LEN']].sort_values('DEPT_NAME').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
