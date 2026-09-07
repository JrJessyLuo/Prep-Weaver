import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['ProductID','TransactionID','je','jg']].copy()
    prepared['je'] = pd.to_numeric(prepared['je'].astype(str).str.replace('"','', regex=False).str.strip(), errors='coerce')
    prepared['jg'] = pd.to_numeric(prepared['jg'], errors='coerce')
    target = prepared[['ProductID','TransactionID','je','jg']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['ProductID'] = pd.to_numeric(df['ProductID'], errors='coerce')
    target = df[['ProductID','Code','Popis']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_sales = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_products = prepared_table_2

# Assume prepared_sales and prepared_products are provided as dataframes.
# Normalize key types for join
sales = prepared_sales.copy()
prods = prepared_products.copy()

# Coerce ProductID to numeric in both where possible
for df, col in [(sales, 'ProductID'), (prods, 'ProductID')]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing ProductID after coercion
sales = sales.dropna(subset=['ProductID'])
prods = prods.dropna(subset=['ProductID'])

# Aggregate sales per product (count transactions as proxy for best selling)
sales_agg = sales.groupby('ProductID', as_index=False).agg({'TransactionID':'count'})\
                 .rename(columns={'TransactionID':'sales_count'})

# Join to get product names
merged = sales_agg.merge(prods[['ProductID','Popis']], on='ProductID', how='left')

# Rank and select top 5
top5 = merged.sort_values(['sales_count','ProductID'], ascending=[False, True]).head(5)

# Prepare final answer: full product names
answer = top5['Popis'].tolist()

# If needed as a dataframe:
result = top5[['ProductID','Popis','sales_count']]

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
