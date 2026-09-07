import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'UN', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'UN', 'Date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['UN'] = pd.to_numeric(tmp_1['UN'], errors='coerce').astype(float)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Date'] = pd.to_datetime(tmp_2['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ID', 'UN', 'Date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Define a plausible clinical reference range for Urea Nitrogen (UN) in mg/dL.
# Common adult range ~7-20 mg/dL; interpret 'borderline of passing' as values exactly at the lower or upper limit.
lower, upper = 7.0, 20.0
# Select rows where UN is exactly on the boundary.
borderline = df[df['UN'].isin([lower, upper])]
# The question asks for ID, sex, and birthday, but only IDs are available in the selected evidence.
# Provide IDs; sex and birthday are unavailable in provided tables. Preserve available fields only.
target = borderline[['ID']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
