import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Id', 'ViewCount', 'CommentCount', 'PostTypeId'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Id', 'ViewCount', 'CommentCount', 'PostTypeId'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes like ""7153""
    #     s2 = str(s).strip()
    #     s2 = re.sub(r'^"+|"+$', '', s2)
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove surrounding quotes like ""7153""
        s2 = str(s).strip()
        s2 = re.sub(r'^"+|"+$', '', s2)
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id"] = table_1["Id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ViewCount", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ViewCount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ViewCount']
    if _dtype == "datetime64":
        table_1['ViewCount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ViewCount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ViewCount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ViewCount'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CommentCount", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CommentCount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CommentCount']
    if _dtype == "datetime64":
        table_1['CommentCount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CommentCount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CommentCount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CommentCount'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="PostTypeId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['PostTypeId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['PostTypeId']
    if _dtype == "datetime64":
        table_1['PostTypeId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['PostTypeId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['PostTypeId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['PostTypeId'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['ViewCount'] == 1910
    # """)
    # Filter
    def filter_func(row):
        return row['ViewCount'] == 1910
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Id', 'ViewCount', 'CommentCount', 'PostTypeId'])
    # SelectCol
    _cols = [c for c in ['Id', 'ViewCount', 'CommentCount', 'PostTypeId'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
prepared_posts = prepared_table_1

prepared_posts['ViewCount_num'] = pd.to_numeric(prepared_posts['ViewCount'], errors='coerce')
prepared_posts['CommentCount_num'] = pd.to_numeric(prepared_posts['CommentCount'], errors='coerce')
# Identify the post with 1910 views
target = prepared_posts.loc[prepared_posts['ViewCount_num'] == 1910, ['Id','CommentCount_num']]
# If multiple, pick all; final answer may aggregate or present
answer = target

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
