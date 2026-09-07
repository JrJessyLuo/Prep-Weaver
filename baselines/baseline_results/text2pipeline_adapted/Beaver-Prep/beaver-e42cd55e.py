import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FINANCIAL_AID_YEAR', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FINANCIAL_AID_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FINANCIAL_AID_YEAR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'START_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'END_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FY_QUARTER_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ACADEMIC_TERM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FINANCIAL_AID_YEAR', 'ACADEMIC_YEAR', 'fiscal_period', 'FY_QUARTER_CODE', 'ACADEMIC_TERM', 'START_DATE', 'END_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FY_QUARTER_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FISCAL_YEAR', 'FY_QUARTER_CODE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FINANCIAL_AID_YEAR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_START_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_END_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'TERM_START_DATE', 'TERM_END_DATE', 'FINANCIAL_AID_YEAR', 'ACADEMIC_YEAR']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ACADEMIC_YEAR'] = pd.to_numeric(tmp_0['ACADEMIC_YEAR'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ACADEMIC_YEAR'] = pd.to_numeric(tmp_1['ACADEMIC_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ACADEMIC_YEAR'] = tmp_2['ACADEMIC_YEAR'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['FINANCIAL_AID_YEAR'] = pd.to_numeric(tmp_3['FINANCIAL_AID_YEAR'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['FINANCIAL_AID_YEAR'] = pd.to_numeric(tmp_4['FINANCIAL_AID_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['FINANCIAL_AID_YEAR'] = tmp_5['FINANCIAL_AID_YEAR'].astype(str)
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['START_DATE'] = pd.to_datetime(tmp_6['START_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['END_DATE'] = pd.to_datetime(tmp_7['END_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_8['FY_QUARTER_CODE'] = tmp_8['FY_QUARTER_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_9['ACADEMIC_TERM'] = tmp_9['ACADEMIC_TERM'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['FINANCIAL_AID_YEAR', 'ACADEMIC_YEAR', 'fiscal_period', 'FY_QUARTER_CODE', 'ACADEMIC_TERM', 'START_DATE', 'END_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FY_QUARTER_CODE'] = tmp_0['FY_QUARTER_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['FISCAL_YEAR', 'FY_QUARTER_CODE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ACADEMIC_YEAR'] = tmp_0['ACADEMIC_YEAR'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['FINANCIAL_AID_YEAR'] = tmp_1['FINANCIAL_AID_YEAR'].astype(str)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['TERM_START_DATE'] = pd.to_datetime(tmp_2['TERM_START_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['TERM_END_DATE'] = pd.to_datetime(tmp_3['TERM_END_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['term_code'] = tmp_4['term_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['term_code', 'TERM_START_DATE', 'TERM_END_DATE', 'FINANCIAL_AID_YEAR', 'ACADEMIC_YEAR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge term details into table_1 by academic term
integrated = prepared_table_1.merge(prepared_table_3, how='inner', left_on=['ACADEMIC_TERM'], right_on=['term_code'])

# Normalize potential numeric-like strings for grouping keys from prepared_table_3
integrated['FINANCIAL_AID_YEAR'] = integrated['FINANCIAL_AID_YEAR_y'].astype(str).str.replace('.0','', regex=False).str.strip()
integrated['ACADEMIC_YEAR'] = integrated['ACADEMIC_YEAR_y'].astype(str).str.replace('.0','', regex=False).str.strip()

# Aggregate per Financial Aid Year and Academic Year
agg = integrated.groupby(['FINANCIAL_AID_YEAR','ACADEMIC_YEAR']).agg(
    num_fiscal_periods=('fiscal_period','nunique'),
    num_quarters=('FY_QUARTER_CODE','nunique'),
    start_term_date=('TERM_START_DATE','min'),
    end_term_date=('TERM_END_DATE','max'),
    num_distinct_dept_term_params=('term_code','nunique')
).reset_index()

# Final projection and sorting
cols = ['FINANCIAL_AID_YEAR','ACADEMIC_YEAR','num_fiscal_periods','num_quarters','start_term_date','end_term_date','num_distinct_dept_term_params']
target = agg[cols].sort_values(['FINANCIAL_AID_YEAR','ACADEMIC_YEAR'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
