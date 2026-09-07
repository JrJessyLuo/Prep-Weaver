import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['budget_id','category','link_to_event']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['link_to_event','link_to_member']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1.copy()
    df.columns = ['member_id'] + [f"{c}__{i}" for i,c in enumerate(df.columns[1:], start=1)]
    attr_row = df[df['member_id'].astype(str).str.lower().eq('attribute')].iloc[0]
    val_row = df[df['member_id'].astype(str).str.lower().eq('value')].iloc[0]
    member_cols = [c for c in df.columns if c != 'member_id']
    long = pd.DataFrame({'member_record_id': [c.split('__',1)[0] for c in member_cols], 'attribute': [attr_row[c] for c in member_cols], 'value': [val_row[c] for c in member_cols]})
    long['attribute'] = long['attribute'].astype(str)
    long = long[long['attribute'].isin(['first_name','last_name'])]
    wide = long.pivot_table(index='member_record_id', columns='attribute', values='value', aggfunc='first').reset_index()
    target = wide[['member_record_id','first_name','last_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_table_2 = _prep_2(tables['table_4'])
prepared_budget = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_event_members = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_members = prepared_table_4

# prepared_members synthesis from table_4 (wide attribute/value). Assumes table_4 has two rows: one 'attribute' header row and one 'value' row, with member record ids as column names.
attr_row = table_4.iloc[0]
val_row = table_4.iloc[1]
member_ids = [c for c in table_4.columns if c != 'member_id']
records = []
for mid in member_ids:
    records.append({
        'member_record_id': mid,
        'first_name': val_row[mid] if attr_row[mid] == 'first_name' else None,
        'last_name': val_row[mid] if attr_row[mid] == 'last_name' else None
    })
# The above naive map only captures one attribute per member due to the pivoted layout with duplicates; instead build a dict of attributes per member id.
member_attrs = {}
for mid in member_ids:
    member_attrs[mid] = {}
# Iterate attribute/value cells for each member id by scanning both rows
# attribute names are in attr_row[mid], values in val_row[mid]
for mid in member_ids:
    attr_name = attr_row[mid]
    attr_val = val_row[mid]
    member_attrs[mid][attr_name] = attr_val
prepared_members = pd.DataFrame([
    {
        'member_record_id': mid,
        'first_name': attrs.get('first_name'),
        'last_name': attrs.get('last_name')
    }
    for mid, attrs in member_attrs.items()
])

# prepared_event_members comes directly from table_3
prepared_event_members = table_3[['link_to_event', 'link_to_member']].copy()

# prepared_budget comes directly from table_2
prepared_budget = table_2[['budget_id', 'category', 'link_to_event']].copy()

# Join budget -> event_members -> members
tmp = prepared_budget.merge(prepared_event_members, on='link_to_event', how='left')
joined = tmp.merge(prepared_members, left_on='link_to_member', right_on='member_record_id', how='left')

# Filter for the specific member 'Sacha Harrison' and select distinct expense categories
target = joined[(joined['first_name'] == 'Sacha') & (joined['last_name'] == 'Harrison')]
answer = sorted(target['category'].dropna().unique().tolist())
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
