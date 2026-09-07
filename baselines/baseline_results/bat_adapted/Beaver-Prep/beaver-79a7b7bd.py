import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']].copy()
    df['MOIRA_LIST_KEY'] = df['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member','MOIRA_LIST_MEMBER_MIT_ID']].copy()
    df['moira_list_member'] = df['moira_list_member'].astype('string').str.strip()
    df['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(df['MOIRA_LIST_MEMBER_MIT_ID'], errors='coerce').round().astype('Int64')
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member','MOIRA_LIST_MEMBER_MIT_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['MOIRA_LIST_OWNER_KEY','OWNER_TYPE']].copy()
    prepared = prepared.drop_duplicates(subset=['MOIRA_LIST_OWNER_KEY','OWNER_TYPE'])
    target = prepared[['MOIRA_LIST_OWNER_KEY','OWNER_TYPE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.loc[:, ['MIT_ID', 'HR_DEPARTMENT_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_membership = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_owners = prepared_table_3
prepared_table_4 = _prep_4(tables['table_8'])
prepared_people = prepared_table_4

# Assume prepared_* DataFrames are provided

# 1) Keep only active Moira mailing lists
lists = prepared_lists.copy()
lists = lists[(lists['IS_MOIRA_MAILING_LIST'] == 'Y') & (lists['IS_ACTIVE'] == 'Y')]

# 2) Join membership to lists (restrict to selected lists)
mem = prepared_membership.merge(lists[['MOIRA_LIST_KEY','MOIRA_LIST_NAME']], on='MOIRA_LIST_KEY', how='inner')

# 3) Resolve owner type for each membership row
mem = mem.merge(prepared_owners[['MOIRA_LIST_OWNER_KEY','OWNER_TYPE']], on='MOIRA_LIST_OWNER_KEY', how='left')

# 4) Link members to people/departments and filter to departments starting with 'Computer Science'
# Normalize MIT_IDs to string for join consistency
mem['MOIRA_LIST_MEMBER_MIT_ID'] = mem['MOIRA_LIST_MEMBER_MIT_ID'].astype(str).str.strip()
people = prepared_people.copy()
people['MIT_ID'] = people['MIT_ID'].astype(str).str.strip()
mem = mem.merge(people[['MIT_ID','HR_DEPARTMENT_NAME']], left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID', how='inner')
mem = mem[mem['HR_DEPARTMENT_NAME'].notna()]
mem = mem[mem['HR_DEPARTMENT_NAME'].str.startswith('Computer Science', na=False)]

# 5) Compute per-list counts: subscribers and owners
# Subscribers: count distinct members per list
subs = (mem.groupby(['MOIRA_LIST_KEY','MOIRA_LIST_NAME'])['MOIRA_LIST_MEMBER_MIT_ID']
          .nunique().reset_index(name='NUM_SUBSCRIBERS'))

# Owners: count unique owner keys per list using all membership rows (owners repeat across rows);
# we can derive owners per list by grouping mem by list and counting distinct MOIRA_LIST_OWNER_KEY
owners = (mem.groupby(['MOIRA_LIST_KEY','MOIRA_LIST_NAME'])['MOIRA_LIST_OWNER_KEY']
            .nunique().reset_index(name='NUM_OWNERS'))

per_list = subs.merge(owners, on=['MOIRA_LIST_KEY','MOIRA_LIST_NAME'], how='outer').fillna({'NUM_SUBSCRIBERS':0,'NUM_OWNERS':0})

# 6) Determine a single OWNER_TYPE per list.
# If multiple owner types appear for a list, label as 'MIXED'; otherwise the sole type.
owner_types_per_list = (mem.groupby(['MOIRA_LIST_KEY','MOIRA_LIST_NAME'])['OWNER_TYPE']
                          .agg(lambda s: 'MIXED' if s.dropna().nunique()>1 else (s.dropna().iloc[0] if s.dropna().size>0 else 'UNKNOWN'))
                          .reset_index(name='OWNER_TYPE'))

per_list = per_list.merge(owner_types_per_list, on=['MOIRA_LIST_KEY','MOIRA_LIST_NAME'], how='left')
per_list['OWNER_TYPE'] = per_list['OWNER_TYPE'].fillna('UNKNOWN')

# 7) Prepare detailed rows and subtotals/totals with display rules
# Detailed rows
detail = per_list[['OWNER_TYPE','MOIRA_LIST_NAME','NUM_OWNERS','NUM_SUBSCRIBERS']].copy()

# Subtotals per OWNER_TYPE
subtot = (detail.groupby('OWNER_TYPE')[['NUM_OWNERS','NUM_SUBSCRIBERS']]
                .sum().reset_index())
subtot['MOIRA_LIST_NAME'] = 'SUBTOTAL'
subtot['OWNER_TYPE'] = subtot['OWNER_TYPE']  # keep type label for subtotal rows

# Grand total row
grand = pd.DataFrame({
    'OWNER_TYPE': ['TOTAL'],
    'MOIRA_LIST_NAME': ['TOTAL'],
    'NUM_OWNERS': [detail['NUM_OWNERS'].sum()],
    'NUM_SUBSCRIBERS': [detail['NUM_SUBSCRIBERS'].sum()]
})

# 8) Concatenate with ordering by OWNER_TYPE, then list name
# Sort detail within each OWNER_TYPE by list name
detail_sorted = detail.sort_values(['OWNER_TYPE','MOIRA_LIST_NAME']).reset_index(drop=True)

# Insert display rule: suppress repeating OWNER_TYPE if same as previous; keep 'SUBTOTAL'/'TOTAL' as given
def apply_display_rule(df):
    shown = []
    prev = None
    for _, r in df.iterrows():
        cur = r['OWNER_TYPE']
        if r['MOIRA_LIST_NAME'] in ('SUBTOTAL','TOTAL'):
            shown.append(cur)
            prev = None  # reset group after subtotal/total
        else:
            if cur == prev:
                shown.append('')
            else:
                shown.append(cur)
                prev = cur
    df = df.copy()
    df['OWNER_TYPE'] = shown
    return df

# Build final output sequence: for each OWNER_TYPE block, detail rows then its subtotal
blocks = []
for ot in sorted(detail['OWNER_TYPE'].unique()):
    d = detail_sorted[detail_sorted['OWNER_TYPE'] == ot]
    st = subtot[subtot['OWNER_TYPE'] == ot]
    block = pd.concat([d, st], ignore_index=True)
    blocks.append(block)
final_df = pd.concat(blocks + [grand], ignore_index=True)
final_df = apply_display_rule(final_df)

# Columns as requested: ownership type (with suppression), list name, number of owners, number of subscribers
answer = final_df[['OWNER_TYPE','MOIRA_LIST_NAME','NUM_OWNERS','NUM_SUBSCRIBERS']]

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
