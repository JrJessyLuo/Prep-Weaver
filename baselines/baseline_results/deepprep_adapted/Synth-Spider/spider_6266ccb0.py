import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="student_id", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove repeated quotes like ""1016"" -> 1016
    #     return re.sub(r'^[\s\"]+|[\s\"]+$', '', str(s))
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove repeated quotes like ""1016"" -> 1016
        return re.sub(r'^[\s\"]+|[\s\"]+$', '', str(s))
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["student_id"] = table_1["student_id"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['student_id', 'StuID', 'attribute_value'])
    # SelectCol
    _cols = [c for c in ['student_id', 'StuID', 'attribute_value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['student_id', 'StuID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['student_id', 'StuID'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['student_id', 'StuID', 'attribute_value'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['student_id', 'StuID', 'attribute_value'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['latitude', 'longitude'])
    # DropColumn
    table_1 = table_1.drop(columns=['latitude', 'longitude'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="state_country", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip()
    #     if "~" not in s:
    #         return s
    #     state, country = s.split("~", 1)
    #     state = state.strip()
    #     country_clean = re.sub(r'[^A-Za-z]', '', country).upper()  # e.g., "U.S.A." -> "USA"
    #     if country_clean in ["US", "USA", "UNITEDSTATES", "UNITEDSTATESOFAMERICA"]:
    #         country_clean = "USA"
    #     return f"{state}~{country_clean}"
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip()
        if "~" not in s:
            return s
        state, country = s.split("~", 1)
        state = state.strip()
        country_clean = re.sub(r'[^A-Za-z]', '', country).upper()  # e.g., "U.S.A." -> "USA"
        if country_clean in ["US", "USA", "UNITEDSTATES", "UNITEDSTATESOFAMERICA"]:
            country_clean = "USA"
        return f"{state}~{country_clean}"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["state_country"] = table_1["state_country"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['city_code', 'city_name', 'state_country'])
    # SelectCol
    _cols = [c for c in ['city_code', 'city_name', 'state_country'] if c in table_1.columns]
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
student_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
cities = prepared_table_2

# Assume prepared tables are provided as dataframes: student_attributes, cities

# 1) Derive country from state_country field
cities2 = cities.copy()
# state_country like 'MD~U.S.A.'; split on '~' and take the last segment as country
cities2['country'] = cities2['state_country'].astype(str).str.split('~').str[-1].str.strip().str.replace('.', '', regex=False).str.upper()

# 2) Identify rows in student_attributes that encode the student's city (attribute name likely 'City' or similar). Since schema is generic, match where attribute_value equals a known city_code by joining on attribute_value=city_code.
student_city = student_attributes.merge(cities2[['city_code','country']], left_on='attribute_value', right_on='city_code', how='inner')

# 3) Count students whose joined country equals 'CHINA'
answer = int((student_city['country'] == 'CHINA').sum())

result = answer

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
