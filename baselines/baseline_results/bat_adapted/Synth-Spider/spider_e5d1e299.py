import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Institution_ID','Institution_Name','Location']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    melted = table_1.melt(id_vars=['staff_ID','name'], value_vars=['Canada','United Kindom','United States'], var_name='country', value_name='Institution_ID')
    melted = melted[melted['Institution_ID'].notna()]
    melted['Institution_ID'] = melted['Institution_ID'].astype('int64')
    target = melted[['staff_ID','name','Institution_ID']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['huiyi_id','yuangong_id','role']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['Conference_ID','Conference_Info']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_institutions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_staff = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_participation = prepared_table_3
prepared_table_4 = _prep_4(tables['table_1'])
prepared_conferences = prepared_table_4

# prepared_institutions: columns [Institution_ID, Institution_Name, Location]
inst = prepared_institutions.copy()

# prepared_staff: columns [staff_ID, name, Institution_ID]
# If prepared_staff still has country columns, first melt and pick non-null as Institution_ID.
staff = prepared_staff.copy()

# prepared_participation: columns [huiyi_id, yuangong_id, role]
part = prepared_participation.copy()

# prepared_conferences: columns [Conference_ID, Conference_Info]
conf = prepared_conferences.copy()

# 1) Conferences in 2004
conf_2004 = conf[conf['Conference_Info'].astype(str).str.contains('2004', na=False)]

# 2) Participations linked to those 2004 conferences
part_2004 = part.merge(conf_2004, left_on='huiyi_id', right_on='Conference_ID', how='inner')

# 3) Staff who participated in 2004
staff_2004 = part_2004.merge(staff, left_on='yuangong_id', right_on='staff_ID', how='inner')

# 4) Institutions that had at least one participating staff in 2004
inst_with_participation = staff_2004[['Institution_ID']].dropna().drop_duplicates()

# 5) Institutions with no staff participation in 2004
result = inst.merge(inst_with_participation, on='Institution_ID', how='left', indicator=True)
result = result[result['_merge'] == 'left_only'][['Institution_Name', 'Location']]

answer = result.reset_index(drop=True)

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
