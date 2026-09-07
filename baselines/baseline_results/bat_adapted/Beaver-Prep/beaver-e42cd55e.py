import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['FISCAL_YEAR','fiscal_period','FY_QUARTER_CODE','ACADEMIC_YEAR','FINANCIAL_AID_YEAR','START_DATE','END_DATE']].copy()
    prepared['START_DATE'] = pd.to_datetime(prepared['START_DATE'], errors='coerce')
    prepared['END_DATE'] = pd.to_datetime(prepared['END_DATE'], errors='coerce')
    target = prepared[['FISCAL_YEAR','fiscal_period','FY_QUARTER_CODE','ACADEMIC_YEAR','FINANCIAL_AID_YEAR','START_DATE','END_DATE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FISCAL_YEAR','FY_QUARTER_CODE','QUARTER_START_FP','QUARTER_END_FP','QUARTER_START_DATE','QUARTER_END_DATE']].copy()
    prepared['QUARTER_START_DATE'] = pd.to_datetime(prepared['QUARTER_START_DATE'], format='%d-%b-%y', errors='coerce')
    prepared['QUARTER_END_DATE'] = pd.to_datetime(prepared['QUARTER_END_DATE'], format='%d-%b-%y', errors='coerce')
    target = prepared[['FISCAL_YEAR','FY_QUARTER_CODE','QUARTER_START_FP','QUARTER_END_FP','QUARTER_START_DATE','QUARTER_END_DATE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['TERM_START_DATE'] = pd.to_datetime(df['TERM_START_DATE'], format='%d-%b-%y', errors='coerce')
    df['TERM_END_DATE'] = pd.to_datetime(df['TERM_END_DATE'], format='%d-%b-%y', errors='coerce')
    target = df[['ACADEMIC_YEAR','FINANCIAL_AID_YEAR','term_code','TERM_START_DATE','TERM_END_DATE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
