import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['residence_type', 'residence_number'])
    # DropColumn
    table_1 = table_1.drop(columns=['residence_type', 'residence_number'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="student_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['student_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['student_id']
    if _dtype == "datetime64":
        table_1['student_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['student_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['student_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['student_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['student_id', 'bio_data'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['student_id', 'bio_data'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['student_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['student_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['student_id', 'bio_data'])
    # SelectCol
    _cols = [c for c in ['student_id', 'bio_data'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # CastType(table_name="table_1", column="event_date", dtype="datetime")
    # CastType
    _dtype = 'datetime'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['event_date'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['event_date']
    if _dtype == "datetime64":
        table_1['event_date'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['event_date'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['event_date'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['event_date'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_events", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Robust datetime parsing for mixed formats (e.g., '15/08/2008 22:16:17', '2014-07-15 18:18:15', '04/14/2013 04:14:10.000000')
    #     # Use dayfirst=True to correctly parse dd/mm/YYYY entries; ISO formats remain parseable.
    #     dt = pd.to_datetime(df["event_date"], errors="coerce", dayfirst=True, infer_datetime_format=True)
    # 
    #     out = pd.DataFrame({
    #         "student_id": df["student_id"],
    #         "event_date": dt
    #     })
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Robust datetime parsing for mixed formats (e.g., '15/08/2008 22:16:17', '2014-07-15 18:18:15', '04/14/2013 04:14:10.000000')
        # Use dayfirst=True to correctly parse dd/mm/YYYY entries; ISO formats remain parseable.
        dt = pd.to_datetime(df["event_date"], errors="coerce", dayfirst=True, infer_datetime_format=True)

        out = pd.DataFrame({
            "student_id": df["student_id"],
            "event_date": dt
        })

        return out
    prepared_events = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="prepared_events", subset=['student_id', 'event_date'], how="any")
    # DropNulls
    prepared_events = prepared_events.dropna(subset=['student_id', 'event_date'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="prepared_events", columns=['student_id', 'event_date'])
    # SelectCol
    _cols = [c for c in ['student_id', 'event_date'] if c in prepared_events.columns]
    prepared_events = prepared_events[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['prepared_events'])
    # Terminate
    result = {'prepared_events': prepared_events}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
students_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
events_prepared = prepared_table_2

target = students_prepared.merge(events_prepared, on='student_id', how='inner')[['student_id','bio_data','event_date']]

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
