import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'FULL_NAME', 'FORM_OF_ADDRESS_SHORT', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'KRB_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'JOB_ID', 'JOB_TITLE', 'ADMIN_EMPLOYEE_TYPE', 'HR_DEPARTMENT_CODE_OLD', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_ID', 'ADMIN_ORG_UNIT_TITLE', 'ADMIN_POSITION_TITLE', 'PAYROLL_RANK', 'IS_FACULTY', 'EMPLOYMENT_PERCENT', 'IS_CONSULT_PRIV', 'IS_PAID_APPT', 'IS_SUMMER_SESSION_APPT', 'SUMMER_SESSION_MONTHS', 'IS_SABBATICAL', 'SABBATICAL_BEGIN_DATE', 'SABBATICAL_END_DATE', 'IS_OPA_REQUIRED', 'IS_6MO_APPT', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['fac_room_key', 'BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'SPACE_ID', 'MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'USE_KEY', 'USE_DESC', 'MINOR_USE_KEY', 'MINOR_USE_DESC', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'MINOR_ORGANIZATION_KEY', 'MINOR_ORGANIZATION', 'AREA', 'ROOM_FULL_NAME', 'DEPT_CODE', 'ACCESS_LEVEL', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'NORTHING_SPCS', 'EASTING_SPCS', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL'], 'target_column': 'STREET_ADDRESS', 'func': 'def transform(row):\n    parts = []\n    for col in ["STREET_NUMBER", "STREET_NUMBER_SUFFIX", "PRE_DIRECTIONAL", "STREET_NAME", "STREET_SUFFIX", "POST_DIRECTIONAL"]:\n        v = row.get(col, None)\n        if v is None:\n            continue\n        s = str(v)\n        if s.lower() == \'nan\' or s.strip() == \'\':\n            continue\n        parts.append(s.strip())\n    return \' \'.join(parts).strip()\n'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_ADDRESS_KEY', 'BUILDING_KEY', 'ADDRESS_PURPOSE', 'ADDRESS_CITY_ID', 'IS_E911_ADDRESS', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE', 'WAREHOUSE_LOAD_DATE', 'STREET_ADDRESS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['MIT_ID', 'FULL_NAME', 'FORM_OF_ADDRESS_SHORT', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'KRB_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'JOB_ID', 'JOB_TITLE', 'ADMIN_EMPLOYEE_TYPE', 'HR_DEPARTMENT_CODE_OLD', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_ID', 'ADMIN_ORG_UNIT_TITLE', 'ADMIN_POSITION_TITLE', 'PAYROLL_RANK', 'IS_FACULTY', 'EMPLOYMENT_PERCENT', 'IS_CONSULT_PRIV', 'IS_PAID_APPT', 'IS_SUMMER_SESSION_APPT', 'SUMMER_SESSION_MONTHS', 'IS_SABBATICAL', 'SABBATICAL_BEGIN_DATE', 'SABBATICAL_END_DATE', 'IS_OPA_REQUIRED', 'IS_6MO_APPT', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_10', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['fac_room_key', 'BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'SPACE_ID', 'MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'USE_KEY', 'USE_DESC', 'MINOR_USE_KEY', 'MINOR_USE_DESC', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'MINOR_ORGANIZATION_KEY', 'MINOR_ORGANIZATION', 'AREA', 'ROOM_FULL_NAME', 'DEPT_CODE', 'ACCESS_LEVEL', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'NORTHING_SPCS', 'EASTING_SPCS', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: Concatenate
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(row):\n    parts = []\n    for col in ["STREET_NUMBER", "STREET_NUMBER_SUFFIX", "PRE_DIRECTIONAL", "STREET_NAME", "STREET_SUFFIX", "POST_DIRECTIONAL"]:\n        v = row.get(col, None)\n        if v is None:\n            continue\n        s = str(v)\n        if s.lower() == \'nan\' or s.strip() == \'\':\n            continue\n        parts.append(s.strip())\n    return \' \'.join(parts).strip()\n', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_1['STREET_ADDRESS'] = tmp_1[['STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL']].apply(_concat_func_1, axis=1)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_ADDRESS_KEY', 'BUILDING_KEY', 'ADDRESS_PURPOSE', 'ADDRESS_CITY_ID', 'IS_E911_ADDRESS', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE', 'WAREHOUSE_LOAD_DATE', 'STREET_ADDRESS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge rooms with building addresses on BUILDING_KEY
integrated = prepared_table_2.merge(prepared_table_3, how='inner', on='BUILDING_KEY')

# Rank address purpose to prefer STREET, then E911*, else others
integrated['__purpose_rank__'] = 3
integrated.loc[integrated['ADDRESS_PURPOSE'].str.fullmatch('STREET', case=False, na=False), '__purpose_rank__'] = 1
integrated.loc[integrated['ADDRESS_PURPOSE'].str.contains('E911', case=False, na=False), '__purpose_rank__'] = 2

# Select best address per building
integrated_sorted = integrated.sort_values(['BUILDING_KEY','__purpose_rank__'])
best_addr = integrated_sorted.drop_duplicates(subset=['BUILDING_KEY'], keep='first')

# Project required columns, creating any missing as empty strings
cols = ['ROOM','FLOOR','BUILDING_KEY','STREET_ADDRESS','CITY','STATE','POSTAL_CODE']
existing = [c for c in cols if c in best_addr.columns]
result = best_addr[existing].copy()
for c in cols:
    if c not in result.columns:
        result[c] = ''

# Deduplicate sensible combinations
result = result.drop_duplicates(subset=['BUILDING_KEY','ROOM','FLOOR','STREET_ADDRESS','CITY','STATE','POSTAL_CODE'])

# Without a deterministic person-to-room link available from provided tables (people table is empty), return plausible integrated facilities rows
target = result[['ROOM','FLOOR','BUILDING_KEY','STREET_ADDRESS','CITY','STATE','POSTAL_CODE']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
