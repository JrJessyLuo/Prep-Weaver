import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['student_id', 'bio_data', 'residence_type', 'residence_number']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'student_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'event_date', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['event_id', 'event_type_code', 'student_id', 'event_date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['student_id', 'bio_data', 'residence_type', 'residence_number']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['student_id'] = pd.to_numeric(tmp_0['student_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['event_date'] = pd.to_datetime(tmp_1['event_date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['event_id', 'event_type_code', 'student_id', 'event_date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='student_id')
# Select required output: students who have any event, with biographical data and event date
cols = ['student_id', 'bio_data', 'residence_type', 'residence_number', 'event_date']
target = integrated[cols]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
