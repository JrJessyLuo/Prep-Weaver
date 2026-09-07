import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Count(table_name="table_1")
    # Count -> statistic_table
    _stat_row = pd.DataFrame({'operator': ['Count(table_name="table_1")'], 'statistic_name': ['count'], 'value': [len(table_1)]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Id', 'Score', 'ouid'])
    # SelectCol
    _cols = [c for c in ['Id', 'Score', 'ouid'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Score", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Score'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Score']
    if _dtype == "datetime64":
        table_1['Score'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Score'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Score'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Score'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return pd.notnull(row[\"Score\"]) and row[\"Score\"] > 5
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return pd.notnull(row[\"Score\"]) and row[\"Score\"] > 5
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ouid'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ouid'], how='any').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Age", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Age'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Age']
    if _dtype == "datetime64":
        table_1['Age'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Age'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Age'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Age'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Age", mode="median")
    # MissingValueImputation
    table_1["Age"] = table_1["Age"].fillna(table_1["Age"].median())

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Id', 'Age'])
    # SelectCol
    _cols = [c for c in ['Id', 'Age'] if c in table_1.columns]
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
prepared_posts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_users = prepared_table_2

# Assume prepared_posts and prepared_users are already materialized per the target schemas
# Join posts to users on owner user id
joined = prepared_posts.merge(prepared_users, left_on='ouid', right_on='Id', how='left')

# Consider posts with score > 5
eligible = joined[joined['Score'] > 5]

# Define elder user criterion (e.g., Age >= 65). Exclude rows with missing Age from the elder count but include them in denominator only if ownership should be counted regardless of known age; here we only count posts with known age in denominator to avoid bias.
known_age = eligible[eligible['Age'].notna()]
if len(known_age) == 0:
    result = 0.0
else:
    elders = known_age[known_age['Age'] >= 65]
    result = (len(elders) / len(known_age)) * 100.0

answer = result

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
