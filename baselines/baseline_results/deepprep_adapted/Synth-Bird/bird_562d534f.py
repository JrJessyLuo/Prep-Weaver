import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['event_id', 'event_name'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['event_id', 'event_name'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['event_id', 'event_name'])
    # SelectCol
    _cols = [c for c in ['event_id', 'event_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['budget_id', 'link_to_event'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['budget_id', 'link_to_event'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['budget_id', 'link_to_event'])
    # SelectCol
    _cols = [c for c in ['budget_id', 'link_to_event'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['budget_id', 'link_to_event'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['budget_id', 'link_to_event'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="expense_id", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()""")
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["expense_id"] = table_1["expense_id"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="link_to_budget", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["link_to_budget"] = table_1["link_to_budget"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="link_to_member", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["link_to_member"] = table_1["link_to_member"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['expense_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['expense_id'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['expense_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['expense_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['expense_id', 'link_to_budget', 'link_to_member'])
    # SelectCol
    _cols = [c for c in ['expense_id', 'link_to_budget', 'link_to_member'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="last_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.title()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["last_name"] = table_1["last_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="first_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.title()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["first_name"] = table_1["first_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'first_name', 'last_name'])
    # SelectCol
    _cols = [c for c in ['member_id', 'first_name', 'last_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
budgets = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
expenses = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
members = prepared_table_4

events_f = events[['event_id','event_name']]
budgets_f = budgets[['budget_id','link_to_event']]
expenses_f = expenses[['expense_id','link_to_budget','link_to_member']]
members_f = members[['member_id','first_name','last_name']]

# Join budgets to events to get event context
be = budgets_f.merge(events_f, left_on='link_to_event', right_on='event_id', how='inner')
# Filter to the specific event name
be_lol = be[be['event_name'] == 'Laugh Out Loud']
# Join expenses to the filtered budgets (proxy for attendance via member involvement)
exp_for_event = expenses_f.merge(be_lol[['budget_id']], left_on='link_to_budget', right_on='budget_id', how='inner')
# Map to members and construct full names
member_hits = exp_for_event.merge(members_f, left_on='link_to_member', right_on='member_id', how='inner')
member_hits['full_name'] = member_hits['first_name'] + ' ' + member_hits['last_name']
# Deduplicate names
answer = sorted(member_hits['full_name'].dropna().unique().tolist())
print(answer)

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
