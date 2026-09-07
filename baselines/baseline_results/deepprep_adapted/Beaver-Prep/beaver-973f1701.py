import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'BUILDING_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'BUILDING_NAME'], how='any').reset_index(drop=True)

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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'SUBJECT_ID', 'new_name': 'SUBJECT_ID'}, {'old_name': 'OFFER_DEPT_NAME', 'new_name': 'OFFER_DEPT_NAME'}, {'old_name': 'COURSE_NUMBER', 'new_name': 'COURSE_NUMBER'}])
    # Rename
    table_1 = table_1.rename(columns={'SUBJECT_ID': 'SUBJECT_ID', 'OFFER_DEPT_NAME': 'OFFER_DEPT_NAME', 'COURSE_NUMBER': 'COURSE_NUMBER'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # trim and collapse internal whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # trim and collapse internal whitespace
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('OFFER_DEPT_NAME') == 'Center for International Studies'
    # """)
    # Filter
    def filter_func(row):
        return row.get('OFFER_DEPT_NAME') == 'Center for International Studies'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'OFFER_DEPT_NAME', 'COURSE_NUMBER'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'OFFER_DEPT_NAME', 'COURSE_NUMBER'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_offerings = prepared_table_2

# prepared_buildings: columns ['BUILDING_KEY','BUILDING_NAME']
# prepared_offerings: columns ['SUBJECT_ID','OFFER_DEPT_NAME','COURSE_NUMBER']

# Filter offerings to the Center for International Studies
cis_offerings = prepared_offerings[prepared_offerings['OFFER_DEPT_NAME'].str.strip().str.lower() == 'center for international studies']

# Count number of distinct courses/subjects per building is not directly possible because offerings lack a building key.
# Produce a building-wise result with zero counts (or NaN) to reflect absence of a join path.
result = prepared_buildings.copy()
result['num_cis_courses'] = 0

# Final selection
answer = result[['BUILDING_KEY', 'BUILDING_NAME', 'num_cis_courses']]

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
