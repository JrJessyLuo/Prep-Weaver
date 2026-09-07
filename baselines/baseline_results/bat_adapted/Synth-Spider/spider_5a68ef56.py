import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Receipt','Ordinal','Attribute','Value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Price','Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5','Flavor','Food']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_receipts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_catalog = prepared_table_2

# Assume prepared_receipts and prepared_catalog are provided as DataFrames
r = prepared_receipts.copy()
# Filter to item rows
r = r[r['Attribute'].str.lower() == 'item']

# Parse receipt item code in Value into up to 5 dash-separated parts
# e.g., '70-M-CH-DZ' -> parts[0]='70', parts[1]='M', parts[2]='CH', parts[3]='DZ', parts[4]=None
parts = r['Value'].astype(str).str.split('-', n=4, expand=True)
parts = parts.rename(columns={0:'Id_Part1',1:'Id_Part2',2:'Id_Part3',3:'Id_Part4',4:'Id_Part5'})
r_parsed = pd.concat([r[['Receipt','Value']], parts], axis=1)

# Normalize None-like strings to actual None for matching
for c in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    r_parsed[c] = r_parsed[c].where(r_parsed[c].notna(), None)

c = prepared_catalog.copy()
# Ensure catalog Id parts are strings; treat 'None' literal as missing
for ccol in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    c[ccol] = c[ccol].astype(object)
    c[ccol] = c[ccol].apply(lambda x: None if pd.isna(x) or str(x).strip().lower() in {'none','nan',''} else str(x))

# Align types for join by coercing receipt parts similarly
for rcol in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    r_parsed[rcol] = r_parsed[rcol].apply(lambda x: None if pd.isna(x) or str(x).strip().lower() in {'none','nan',''} else str(x))

# Perform composite join on all available parts (exact match including Nones)
merge_keys = ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']
linked = r_parsed.merge(c, how='inner', on=merge_keys)

# Filter for goods costing more than 13 dollars
linked = linked[linked['Price'] > 13]

# Get distinct receipt numbers
answer = linked['Receipt'].dropna().drop_duplicates().sort_values().astype(str).tolist()

result = {
    'answer': answer,
    'evidence_preview': linked[['Receipt','Value','Flavor','Food','Price']].head(10).to_dict(orient='records')
}

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
