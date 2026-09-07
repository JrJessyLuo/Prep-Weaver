import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['Shipment','BaoZhuangHao','Contents','Weight','FaSongRen','ShouHuoRen']].sort_values(['Shipment','BaoZhuangHao']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_shipments = prepared_table_1

target = prepared_shipments
# Map sender names if available; here we infer 'John Zoidfarb' corresponds to sender ID values where name mapping is external.
# If a name-to-ID map is not provided, attempt exact match on a 'sender_name' column if present.
if 'sender_name' in target.columns:
    answer_rows = target[target['sender_name'].str.lower() == 'john zoidfarb']
else:
    # Fallback heuristic: if question implies a specific sender ID mapping is known elsewhere, replace 'john_zoidfarb_id' accordingly.
    john_zoidfarb_id = None  # set by upstream name resolution if available
    if john_zoidfarb_id is not None and 'FaSongRen' in target.columns:
        answer_rows = target[target['FaSongRen'] == john_zoidfarb_id]
    else:
        # Without a name-to-ID mapping, cannot filter reliably; return empty.
        answer_rows = target.iloc[0:0]

# The final answer requires the 'Contents' values for John's packages.
final_answer = list(answer_rows['Contents'])

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
