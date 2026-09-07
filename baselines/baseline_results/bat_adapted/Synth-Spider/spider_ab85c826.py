import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Conference_ID','ConfName_Year']].drop_duplicates(subset=['Conference_ID']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Conference_ID','staff_ID']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_conferences = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_participation = prepared_table_2

# Assume prepared_conferences and prepared_participation are provided as DataFrames
# 1) Parse ConfName_Year into name and year (robust to variations like 'acl#2003', 'ACL#2004', ' Naccl #2003')
def parse_name_year(s):
    if pd.isna(s):
        return pd.Series({'conference_name': None, 'year': None})
    txt = str(s).strip()
    # Normalize separators and spaces
    txt = txt.replace(' ', '')
    parts = txt.split('#')
    if len(parts) == 2:
        name_part, year_part = parts[0], parts[1]
    else:
        # Fallback: last 4-digit year
        m = re.search(r'(\d{4})', txt)
        year_part = m.group(1) if m else None
        name_part = re.sub(r'(\d{4})', '', txt)
    # Normalize casing of name
    conference_name = name_part.strip()
    year = pd.to_numeric(str(year_part).strip(), errors='coerce')
    return pd.Series({'conference_name': conference_name, 'year': year})

conf = prepared_conferences.copy()
conf[['conference_name', 'year']] = conf['ConfName_Year'].apply(parse_name_year)

# 2) Count participants per conference (distinct staff_ID)
part = prepared_participation.copy()
participants = part.dropna(subset=['staff_ID']).groupby('Conference_ID')['staff_ID'].nunique().reset_index(name='num_participants')

# 3) Integrate on Conference_ID
result = conf.merge(participants, on='Conference_ID', how='left')
result['num_participants'] = result['num_participants'].fillna(0).astype(int)

# 4) Final columns per question
target = result[['Conference_ID', 'conference_name', 'year', 'num_participants']]

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
