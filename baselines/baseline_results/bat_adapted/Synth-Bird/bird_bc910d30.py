import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'ALP']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    prepared['ALP'] = pd.to_numeric(prepared['ALP'], errors='coerce')
    target = prepared[['ID', 'Date', 'ALP']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import numpy as np
    df = table_1.copy()
    df = df.rename(columns={df.columns[0]: 'row_type'})
    long = df.melt(id_vars=['row_type'], var_name='ID', value_name='cell')
    wide = long.pivot_table(index='ID', columns='row_type', values='cell', aggfunc='first').reset_index()
    wide = wide.rename(columns={'attribute': 'attr', 'value': 'val'})
    wide['attr'] = wide['attr'].astype(str)
    wide['val'] = wide['val'].replace({'nan': np.nan, 'NaN': np.nan, 'None': np.nan})
    prepared = wide.pivot_table(index='ID', columns='attr', values='val', aggfunc='first').reset_index()
    prepared['ID'] = prepared['ID'].astype(str)
    target = prepared[['ID', 'Admission']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_labs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_demographics = prepared_table_2

# Assume prepared tables already synthesized as per target schemas
# prepared_labs: columns [ID, Date, ALP] with ALP as numeric where possible
# prepared_demographics: columns [ID, Admission]

# Join labs with demographics on patient ID
joined = prepared_labs.merge(prepared_demographics, on='ID', how='inner')

# Define ALP normal range (example adult reference: 44–147 IU/L). Adjust if dataset-specific ranges are known.
ALP_LOW, ALP_HIGH = 44, 147

# Coerce ALP to numeric
joined['ALP_num'] = pd.to_numeric(joined['ALP'], errors='coerce')

# Filter to rows with ALP within normal range
within_normal = joined[(joined['ALP_num'] >= ALP_LOW) & (joined['ALP_num'] <= ALP_HIGH)]

# Determine treatment setting from Admission: '+' = inpatient, '-' = outpatient (per table_2 sample semantics)
# Aggregate counts by setting
result = within_normal.assign(
    setting=within_normal['Admission'].map({'+': 'inpatient', '-': 'outpatient'})
).groupby('setting', dropna=False).size().reset_index(name='count')

# If a single label is needed (e.g., which setting they were treated as), pick the setting with the higher count
most_common = result.sort_values('count', ascending=False).head(1)

answer = {
    'counts_by_setting': result.to_dict(orient='records'),
    'most_common_setting': None if most_common.empty else most_common.iloc[0]['setting']
}

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
