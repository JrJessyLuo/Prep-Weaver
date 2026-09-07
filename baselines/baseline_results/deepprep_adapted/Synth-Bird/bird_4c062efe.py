import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="last_name", mode="mode")
    # MissingValueImputation
    table_1["last_name"] = table_1["last_name"].fillna(table_1["last_name"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'first_name', 'last_name', 'link_to_major'])
    # SelectCol
    _cols = [c for c in ['member_id', 'first_name', 'last_name', 'link_to_major'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['member_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['member_id'], keep='last').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['major_id', 'major_info'])
    # SelectCol
    _cols = [c for c in ['major_id', 'major_info'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['major_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['major_id'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="major_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["major_id"] = table_1["major_id"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="major_info", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # normalize whitespace around hierarchy separators
    #     txt = str(s).strip()
    #     parts = [p.strip() for p in txt.split("::")]
    #     return "::".join(parts)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # normalize whitespace around hierarchy separators
        txt = str(s).strip()
        parts = [p.strip() for p in txt.split("::")]
        return "::".join(parts)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["major_info"] = table_1["major_info"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['major_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['major_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_student_club_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_majors = prepared_table_2

target = prepared_student_club_members.merge(prepared_majors, left_on='link_to_major', right_on='major_id', how='inner')
# major_info format: 'Major::Department::College'. We need members whose Department is 'Art and Design Department'.
parts = target['major_info'].str.split('::', n=2, expand=True)
target['department'] = parts[1]
filtered = target[target['department'] == 'Art and Design Department']
filtered['full_name'] = filtered['first_name'].str.strip() + ' ' + filtered['last_name'].str.strip()
answer = filtered[['full_name']].drop_duplicates().sort_values('full_name')

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
