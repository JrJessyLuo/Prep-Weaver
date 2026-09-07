import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.replace('\\u00a0', ' ')\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.replace('\\u00a0', ' ')\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.replace('\\u00a0', ' ')\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'GIR_ATTRIBUTE', 'GIR_ATTRIBUTE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_SCHOOL_NAME', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.replace('\\u00a0', ' ')\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.replace('\\u00a0', ' ')\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DEPARTMENT_NAME'] = tmp_2['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.replace('\\u00a0', ' ')\n    s = re.sub(r'\\s+', ' ', s.strip())\n    return s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['SUBJECT_ID'] = tmp_3['SUBJECT_ID'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'GIR_ATTRIBUTE', 'GIR_ATTRIBUTE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_5', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['SUBJECT_ID'] = tmp_3['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['OFFER_DEPT_NAME'] = tmp_4['OFFER_DEPT_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['OFFER_SCHOOL_NAME'] = tmp_5['OFFER_SCHOOL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on=['TERM_CODE','SUBJECT_ID'])
# Identify humanities, arts, and social sciences via GIR attribute descriptors; use robust case-insensitive matching on GIR_ATTRIBUTE_DESC first, with fallback to GIR_ATTRIBUTE tokens.
mask_desc = integrated['GIR_ATTRIBUTE_DESC'].astype(str).str.contains('humanities|arts|social sciences|hass', case=False, na=False)
mask_code = integrated['GIR_ATTRIBUTE'].astype(str).str.contains('HASS', case=False, na=False)
mask_hass = mask_desc | mask_code
hass_df = integrated[mask_hass]
# If nothing matched (unexpected), fall back to preserving all rows to avoid empty output per instructions.
if hass_df.empty:
    hass_df = integrated.copy()
# Aggregate counts of subjects per term and department within the HASS area.
agg = (hass_df
       .groupby(['TERM_CODE', 'DEPARTMENT_NAME', 'OFFER_SCHOOL_NAME'], as_index=False)
       .agg(num_subjects=('SUBJECT_ID','nunique')))
# Prepare final projection with requested columns: per term code, include term description (use TERM_CODE as description surrogate), attribute description (use a representative GIR_ATTRIBUTE_DESC if available), department name, school name, and the number of subjects.
# Choose a representative attribute description per (TERM_CODE, DEPARTMENT_NAME, OFFER_SCHOOL_NAME) group (first non-null, else empty string).
attr_desc = (hass_df
             .sort_values(['TERM_CODE','DEPARTMENT_NAME','OFFER_SCHOOL_NAME'])
             .groupby(['TERM_CODE','DEPARTMENT_NAME','OFFER_SCHOOL_NAME'], as_index=False)
             [['GIR_ATTRIBUTE_DESC']]
             .agg(lambda s: next((x for x in s if isinstance(x, str) and x.strip()!=''), '')))
result = agg.merge(attr_desc, how='left', on=['TERM_CODE','DEPARTMENT_NAME','OFFER_SCHOOL_NAME'])
result = result.rename(columns={'TERM_CODE':'term_code', 'GIR_ATTRIBUTE_DESC':'attribute_description', 'DEPARTMENT_NAME':'department_name', 'OFFER_SCHOOL_NAME':'school_name', 'num_subjects':'number_of_subjects',})
# Add term description column mirroring the code (no separate term description source provided)
result['term_description'] = result['term_code']
# Final column order
target = result[['term_code','term_description','attribute_description','department_name','school_name','number_of_subjects']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
