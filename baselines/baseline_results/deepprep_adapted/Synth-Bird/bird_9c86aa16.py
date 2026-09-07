import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="hasContentWarning", mode="mode")
    # MissingValueImputation
    table_1["hasContentWarning"] = table_1["hasContentWarning"].fillna(table_1["hasContentWarning"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'hasContentWarning'])
    # SelectCol
    _cols = [c for c in ['id', 'hasContentWarning'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="id", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['id']
    if _dtype == "datetime64":
        table_1['id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'fmt', 'sts'])
    # SelectCol
    _cols = [c for c in ['id', 'fmt', 'sts'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_formats = prepared_table_2

# prepared_cards and prepared_formats are produced from table_1 and table_2 respectively
merged = prepared_cards.merge(prepared_formats, on='id', how='inner')

# Filter to format == 'commander' and legal status
subset = merged[(merged['fmt'].str.lower() == 'commander') & (merged['sts'].str.lower() == 'legal')]

# Compute percentage of those without a content warning (assuming 1=yes, 0=no)
if len(subset) == 0:
    result = 0.0
else:
    no_warning = (subset['hasContentWarning'] == 0).sum()
    result = 100.0 * no_warning / len(subset)

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
