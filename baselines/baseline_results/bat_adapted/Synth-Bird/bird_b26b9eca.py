import pandas as pd
import numpy as np

def _prep_1(table_1):
    filtered = table_1.loc[table_1['rtype'].eq('S'), ['cds', 'sname_prefix', 'sname_suffix', 'NumGE1500']]
    target = filtered.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import numpy as np
    src = table_1.copy()
    needed = ['CDSCode','School','AdmFName1','AdmLName1','AdminEmail','Email','AdmEmail','District','County']
    src = src.rename(columns={c: c.strip() for c in src.columns})
    src = src.assign(**{c: (src[c] if c in src.columns else np.nan) for c in needed})
    target = src[needed]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_sat = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_directory = prepared_table_2

# Assume prepared_sat and prepared_directory are materialized per the table_targets

# 1) Integrate on CDS code
merged = prepared_sat.merge(prepared_directory, left_on='cds', right_on='CDSCode', how='inner')

# 2) Identify the school with the maximum number of test takers scoring >=1500
# Coerce NumGE1500 to numeric in case of type drift
merged['NumGE1500'] = pd.to_numeric(merged['NumGE1500'], errors='coerce')

# Reconstruct a readable school name fallback from SAT table if needed
sat_name = (merged['sname_prefix'].fillna('') + ' ' + merged['sname_suffix'].fillna('')).str.strip()
merged['school_name'] = merged['School'].fillna(sat_name).replace('', sat_name)

# Select the row with the highest NumGE1500
best = merged.loc[merged['NumGE1500'].idxmax()]

# Choose an administrator email from available columns in priority order
email_cols = ['AdminEmail', 'AdmEmail', 'Email']
admin_email = None
for col in email_cols:
    if col in merged.columns and pd.notna(best.get(col)) and str(best.get(col)).strip() != '':
        admin_email = str(best.get(col)).strip()
        break

# Prepare final answer with school name and admin email
answer = {
    'school_name': best['school_name'],
    'administrator_email': admin_email
}

target = pd.DataFrame([answer])

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
