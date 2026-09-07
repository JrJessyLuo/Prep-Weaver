import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['event_id','event_date','event_name','status']].copy()
    prepared['event_date'] = pd.to_datetime(prepared['event_date'], errors='coerce')
    target = prepared[['event_id','event_date','event_name','status']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['expense_id','expense_date','cost','approved','link_to_budget']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['spent'] = pd.to_numeric(df['spent'].astype(str).str.replace('"', '', regex=False), errors='coerce')
    target = df[['budget_id', 'link_to_event', 'spent', 'category', 'event_status']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_expenses = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_budgets = prepared_table_3

# Assume prepared_events, prepared_budgets, prepared_expenses are dataframes synthesized per targets above.

# 1) Join budgets to events via event id
be = prepared_budgets.merge(prepared_events[["event_id","event_date"]], left_on="link_to_event", right_on="event_id", how="inner")

# 2) Coerce types
be["spent"] = pd.to_numeric(be["spent"], errors="coerce")
be["event_date"] = pd.to_datetime(be["event_date"], errors="coerce")
be = be.dropna(subset=["event_date"])  # ensure we can extract year

# 3) Add year and aggregate total spent per year
be["year"] = be["event_date"].dt.year
agg = be.groupby("year", as_index=False)["spent"].sum()

# 4) Extract totals for 2019 and 2020 and compute difference (2019 total - 2020 total)
spent_2019 = float(agg.loc[agg["year"]==2019, "spent"].sum()) if (agg["year"]==2019).any() else 0.0
spent_2020 = float(agg.loc[agg["year"]==2020, "spent"].sum()) if (agg["year"]==2020).any() else 0.0

answer = spent_2019 - spent_2020

target = pd.DataFrame({"year":[2019,2020], "total_spent":[spent_2019, spent_2020]})

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
