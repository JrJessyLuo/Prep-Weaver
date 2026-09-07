import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'UN']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'UN']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_labs = prepared_table_1

# prepared_labs is synthesized from table_1 with columns [ID, Date, UN]
# Define the borderline threshold for UN (domain-specific; adjust if known). Here we assume the upper normal limit is 20 mg/dL and "just within the borderline of passing" means UN equals the upper limit.
upper_norm = 20.0

# Ensure numeric UN
prepared_labs['UN_num'] = pd.to_numeric(prepared_labs['UN'], errors='coerce')

# Identify patients with any measurement exactly at the borderline threshold
borderline_ids = prepared_labs.loc[prepared_labs['UN_num'] == upper_norm, 'ID'].dropna().unique()

# If patient demographics (Sex, Birthday) are in another table, they should be integrated here.
# Since only table_1 is provided and it lacks Sex/Birthday, we assume they are available elsewhere as `prepared_demo` with columns [ID, Sex, Birthday].
# Example integration (uncomment when prepared_demo is available):
# target = pd.DataFrame({'ID': borderline_ids}).merge(prepared_demo[['ID','Sex','Birthday']], on='ID', how='left')

# Placeholder output using only IDs if demographics are unavailable
target = pd.DataFrame({'ID': borderline_ids})

# Final expected columns per question: ID, sex, birthday
# If demographics were merged, ensure correct column names
# target = target.rename(columns={'Sex': 'sex', 'Birthday': 'birthday'})

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
