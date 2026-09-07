import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="circuitRef", func="""
    # def transform_func(s):
    #     return s.strip().lower() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip().lower() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["circuitRef"] = table_1["circuitRef"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['circuitId', 'circuitRef', 'name'])
    # SelectCol
    _cols = [c for c in ['circuitId', 'circuitRef', 'name'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="date", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().replace('"','')
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().replace('"','')
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["date"] = table_1["date"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="raceId", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().replace('"','')
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().replace('"','')
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["raceId"] = table_1["raceId"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="circuitId", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().replace('"','')
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().replace('"','')
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["circuitId"] = table_1["circuitId"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().replace('"','')
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().replace('"','')
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name"] = table_1["name"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="time", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().replace('"','')
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().replace('"','')
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["time"] = table_1["time"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'circuitId', 'name', 'date', 'time'])
    # SelectCol
    _cols = [c for c in ['raceId', 'circuitId', 'name', 'date', 'time'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_circuits = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_races = prepared_table_2

target = prepared_races.merge(prepared_circuits, on='circuitId', how='inner')
ans = target[(target['name_y'] == 'Sepang International Circuit') | (target['circuitRef'] == 'sepang')]
result = ans[['date', 'time']].dropna(subset=['time']).drop_duplicates().sort_values(['date', 'time'])

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
