import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Id','Score','ouid']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Id','Age']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_posts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_users = prepared_table_2

# Assume prepared_posts and prepared_users are already materialized per the target schemas
# Join posts to users on owner user id
joined = prepared_posts.merge(prepared_users, left_on='ouid', right_on='Id', how='left')

# Consider posts with score > 5
eligible = joined[joined['Score'] > 5]

# Define elder user criterion (e.g., Age >= 65). Exclude rows with missing Age from the elder count but include them in denominator only if ownership should be counted regardless of known age; here we only count posts with known age in denominator to avoid bias.
known_age = eligible[eligible['Age'].notna()]
if len(known_age) == 0:
    result = 0.0
else:
    elders = known_age[known_age['Age'] >= 65]
    result = (len(elders) / len(known_age)) * 100.0

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
