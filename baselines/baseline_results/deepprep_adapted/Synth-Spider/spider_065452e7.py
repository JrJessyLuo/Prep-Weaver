import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Pages", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Pages'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Pages']
    if _dtype == "datetime64":
        table_1['Pages'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Pages'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Pages'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Pages'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Book_ID', 'Title', 'Pages'])
    # SelectCol
    _cols = [c for c in ['Book_ID', 'Title', 'Pages'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="rk", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['rk'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['rk']
    if _dtype == "datetime64":
        table_1['rk'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['rk'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['rk'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['rk'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Book_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Book_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Book_ID']
    if _dtype == "datetime64":
        table_1['Book_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Book_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Book_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Book_ID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Book_ID', 'rk'])
    # SelectCol
    _cols = [c for c in ['Book_ID', 'rk'] if c in table_1.columns]
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
books_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
reviews_prepared = prepared_table_2

# Assume books_prepared and reviews_prepared are synthesized as specified.
# Ensure numeric types for correct comparison/join semantics.
books_prepared['Book_ID'] = pd.to_numeric(books_prepared['Book_ID'], errors='coerce')
books_prepared['Pages'] = pd.to_numeric(books_prepared['Pages'], errors='coerce')
reviews_prepared['Book_ID'] = pd.to_numeric(reviews_prepared['Book_ID'], errors='coerce')
reviews_prepared['rk'] = pd.to_numeric(reviews_prepared['rk'], errors='coerce')

# Integrate
merged = books_prepared.merge(reviews_prepared, on='Book_ID', how='left')

# Find the book with the smallest number of pages and return its rank (rk)
min_pages = merged['Pages'].min()
answer_row = merged.loc[merged['Pages'] == min_pages]
# If multiple books tie, pick the first; if rk missing, it will return NaN
answer_value = answer_row['rk'].iloc[0] if not answer_row.empty else None

result = pd.DataFrame({'answer': [answer_value]})

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
