import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.loc[:, ['expense_id','expense_description','expense_date','attribute','value']].copy()
    df['expense_id'] = df['expense_id'].astype('string').str.strip()
    df['expense_description'] = df['expense_description'].astype('string').str.strip()
    df['attribute'] = df['attribute'].astype('string').str.strip()
    df['value'] = df['value'].astype('string').str.strip()
    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce')
    target = df.drop_duplicates(subset=['expense_id','expense_description','expense_date','attribute','value']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import json
    category_row = table_1.loc[table_1['budget_id'].eq('category'), 'rec_json'].iloc[0]
    parsed = json.loads(category_row)
    target = pd.DataFrame(list(parsed.items()), columns=['budget_record_id', 'category_name'])
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_expenses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_budget_categories = prepared_table_2

# prepared_expenses: keep as-is from table_1
prepared_expenses = table_1.copy()

# prepared_budget_categories: parse and explode the 'category' mapping from table_2
cat_row = table_2[table_2['budget_id'] == 'category']
if not cat_row.empty:
    cat_map = pd.read_json(cat_row.iloc[0]['rec_json'], typ='series')
    prepared_budget_categories = pd.DataFrame({'budget_record_id': cat_map.index, 'category_name': cat_map.values})
else:
    prepared_budget_categories = pd.DataFrame(columns=['budget_record_id','category_name'])

# Link expenses to budget categories via the 'link_to_budget' attribute value
link_rows = prepared_expenses[prepared_expenses['attribute'] == 'link_to_budget'][['expense_id','expense_description','expense_date','value']].rename(columns={'value':'budget_record_id'})

linked = link_rows.merge(prepared_budget_categories, on='budget_record_id', how='left')

# Find the expense whose description mentions 'Posters' and return its category
mask = linked['expense_description'].str.contains('Posters', case=False, na=False)
result = linked.loc[mask, ['expense_description','category_name']].drop_duplicates()

# If multiple, pick unique categories; the final answer expects the category label
answer = result['category_name'].iloc[0] if not result.empty else None

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
