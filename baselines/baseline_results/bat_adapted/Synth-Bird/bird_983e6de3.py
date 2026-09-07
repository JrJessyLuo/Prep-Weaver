import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'WBC']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'WBC']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    target = df.melt(id_vars=['ID'], var_name='patient_id', value_name='value')
    target['patient_id'] = target['patient_id'].astype(str).str.strip('"')
    target = target[['ID','patient_id','value']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
labs_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
demographics_long = prepared_table_2

# Assume labs_prepared has columns: ID (int or str), Date (datetime-like or str), WBC (float)
# Assume demographics_long has columns: ID (attribute name), patient_id (as str), value (str)

# Ensure compatible key types
labs_prepared['ID'] = labs_prepared['ID'].astype(str)
demographics_long['patient_id'] = demographics_long['patient_id'].astype(str)

# Join labs with demographics if needed (not strictly necessary for counting normal WBC, but preserves integration plan)
joined = labs_prepared.merge(demographics_long, left_on='ID', right_on='patient_id', how='left')

# Define normal WBC range (example adult reference: 4.0 to 11.0 x10^3/µL). Adjust if domain-specific ranges are provided elsewhere.
normal_lower, normal_upper = 4.0, 11.0

# Coerce WBC to numeric
joined['WBC_num'] = pd.to_numeric(joined['WBC'], errors='coerce')

# Identify patients accepted to the hospital: interpret presence in labs_prepared as accepted/admitted
# Count unique patients with at least one normal WBC
normal_patients = (
    joined.loc[(joined['WBC_num'] >= normal_lower) & (joined['WBC_num'] <= normal_upper), 'ID']
    .dropna()
    .unique()
)

answer = len(normal_patients)
answer

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
