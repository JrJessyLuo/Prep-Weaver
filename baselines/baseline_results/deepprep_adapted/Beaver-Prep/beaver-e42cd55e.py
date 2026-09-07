import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FISCAL_YEAR', 'fiscal_period', 'FY_QUARTER_CODE', 'START_DATE', 'END_DATE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FISCAL_YEAR', 'fiscal_period', 'FY_QUARTER_CODE', 'START_DATE', 'END_DATE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="START_DATE", date_format="%Y-%m-%d")
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
    table_1['START_DATE'] = table_1['START_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['START_DATE'] = table_1['START_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="END_DATE", date_format="%Y-%m-%d")
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
    table_1['END_DATE'] = table_1['END_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['END_DATE'] = table_1['END_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        table_1['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FINANCIAL_AID_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FINANCIAL_AID_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FINANCIAL_AID_YEAR']
    if _dtype == "datetime64":
        table_1['FINANCIAL_AID_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FINANCIAL_AID_YEAR'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FISCAL_YEAR', 'fiscal_period', 'FY_QUARTER_CODE', 'ACADEMIC_YEAR', 'FINANCIAL_AID_YEAR', 'START_DATE', 'END_DATE'])
    # SelectCol
    _cols = [c for c in ['FISCAL_YEAR', 'fiscal_period', 'FY_QUARTER_CODE', 'ACADEMIC_YEAR', 'FINANCIAL_AID_YEAR', 'START_DATE', 'END_DATE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FISCAL_YEAR', 'fiscal_period'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FISCAL_YEAR', 'fiscal_period'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['FISCAL_YEAR', 'fiscal_period'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['FISCAL_YEAR', 'fiscal_period'], ascending=[True, True])

    # ---------------- Step 9 ----------------
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
    # CastType(table_name="table_1", column="QUARTER_END_FP", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['QUARTER_END_FP'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['QUARTER_END_FP']
    if _dtype == "datetime64":
        table_1['QUARTER_END_FP'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['QUARTER_END_FP'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['QUARTER_END_FP'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['QUARTER_END_FP'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="QUARTER_START_FP", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['QUARTER_START_FP'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['QUARTER_START_FP']
    if _dtype == "datetime64":
        table_1['QUARTER_START_FP'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['QUARTER_START_FP'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['QUARTER_START_FP'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['QUARTER_START_FP'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="QUARTER_START_DATE", date_format="%Y-%m-%d")
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
    table_1['QUARTER_START_DATE'] = table_1['QUARTER_START_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['QUARTER_START_DATE'] = table_1['QUARTER_START_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="QUARTER_END_DATE", date_format="%Y-%m-%d")
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
    table_1['QUARTER_END_DATE'] = table_1['QUARTER_END_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['QUARTER_END_DATE'] = table_1['QUARTER_END_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FISCAL_YEAR', 'FY_QUARTER_CODE', 'QUARTER_START_FP', 'QUARTER_END_FP', 'QUARTER_START_DATE', 'QUARTER_END_DATE'])
    # SelectCol
    _cols = [c for c in ['FISCAL_YEAR', 'FY_QUARTER_CODE', 'QUARTER_START_FP', 'QUARTER_END_FP', 'QUARTER_START_DATE', 'QUARTER_END_DATE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FISCAL_YEAR', 'FY_QUARTER_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FISCAL_YEAR', 'FY_QUARTER_CODE'], keep='last').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FINANCIAL_AID_YEAR", mode="median")
    # MissingValueImputation
    table_1["FINANCIAL_AID_YEAR"] = table_1["FINANCIAL_AID_YEAR"].fillna(table_1["FINANCIAL_AID_YEAR"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="TERM_START_DATE", date_format="%Y-%m-%d")
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
    table_1['TERM_START_DATE'] = table_1['TERM_START_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['TERM_START_DATE'] = table_1['TERM_START_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="TERM_END_DATE", date_format="%Y-%m-%d")
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
    table_1['TERM_END_DATE'] = table_1['TERM_END_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['TERM_END_DATE'] = table_1['TERM_END_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        table_1['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FINANCIAL_AID_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FINANCIAL_AID_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FINANCIAL_AID_YEAR']
    if _dtype == "datetime64":
        table_1['FINANCIAL_AID_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FINANCIAL_AID_YEAR'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ACADEMIC_YEAR', 'FINANCIAL_AID_YEAR', 'term_code', 'TERM_START_DATE', 'TERM_END_DATE'])
    # SelectCol
    _cols = [c for c in ['ACADEMIC_YEAR', 'FINANCIAL_AID_YEAR', 'term_code', 'TERM_START_DATE', 'TERM_END_DATE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_time_months = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_fy_quarters = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_academic_terms = prepared_table_3

# Assume prepared_time_months, prepared_fy_quarters, prepared_academic_terms are dataframes created per targets
# 1) Join months to quarters to be able to count distinct quarters per FA year and academic year
months_quarters = prepared_time_months.merge(
    prepared_fy_quarters,
    on=["FISCAL_YEAR", "FY_QUARTER_CODE"],
    how="left"
)

# 2) Join months to academic terms on academic and FA year to obtain term dates context
mq_terms = months_quarters.merge(
    prepared_academic_terms,
    on=["ACADEMIC_YEAR", "FINANCIAL_AID_YEAR"],
    how="left",
    suffixes=("", "_TERM")
)

# 3) For each FA year and academic year, compute aggregations
# - number of fiscal periods: count of distinct fiscal_period from table_1
# - number of quarters: count of distinct FY_QUARTER_CODE (from either table)
# - start term date: min TERM_START_DATE from academic terms
# - end term date: max TERM_END_DATE from academic terms
# - number of distinct department-level term parameters: proxy as count distinct term_code (no dept table provided)

# Ensure date parsing for min/max (if strings like DD-MON-YY)
for col in ["TERM_START_DATE", "TERM_END_DATE"]:
    if col in mq_terms.columns:
        mq_terms[col] = pd.to_datetime(mq_terms[col], errors="coerce", format="%d-%b-%y")

result = (
    mq_terms.groupby(["FINANCIAL_AID_YEAR", "ACADEMIC_YEAR"]).agg(
        num_fiscal_periods=("fiscal_period", "nunique"),
        num_quarters=("FY_QUARTER_CODE", "nunique"),
        start_term_date=("TERM_START_DATE", "min"),
        end_term_date=("TERM_END_DATE", "max"),
        num_distinct_dept_term_parameters=("term_code", "nunique")
    )
    .reset_index()
)

# If needed, convert dates back to string
if result["start_term_date"].dtype.kind == 'M':
    result["start_term_date"] = result["start_term_date"].dt.strftime("%d-%b-%y")
if result["end_term_date"].dtype.kind == 'M':
    result["end_term_date"] = result["end_term_date"].dt.strftime("%d-%b-%y")

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
