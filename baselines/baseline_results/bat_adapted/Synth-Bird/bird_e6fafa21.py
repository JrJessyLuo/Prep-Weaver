import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Id','PostTypeId','ParentId','ouid','OwnerDisplayName','AnswerCount']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    users = table_1[['Id','xm']].copy()
    users['xm'] = users['xm'].where(users['xm'].notna(), None)
    target = users.groupby('Id', as_index=False).agg({'xm': lambda s: s.dropna().iloc[0] if len(s.dropna()) else None})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_posts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_users = prepared_table_2

posts_users = prepared_posts.merge(prepared_users, left_on='ouid', right_on='Id', how='inner')
# Filter to answers owned by csgillespie
ans_by_csg = posts_users[(posts_users['PostTypeId'] == 2) & (posts_users['xm'].str.lower() == 'csgillespie')]
# Join answers back to their parent questions to read the AnswerCount per question
questions = prepared_posts[prepared_posts['PostTypeId'] == 1][['Id', 'AnswerCount']].rename(columns={'Id': 'QuestionId'})
ans_with_q = ans_by_csg.merge(questions, left_on='ParentId', right_on='QuestionId', how='left')
# For the post (question) that got the most number of answers owned by csgillespie, count answers per parent question
counts_per_q = ans_with_q.groupby('ParentId', dropna=True).size().reset_index(name='answers_by_csg')
# Identify the question with the maximum count of csgillespie-owned answers
if counts_per_q.empty:
    result = 0
else:
    max_qid = counts_per_q.sort_values(['answers_by_csg','ParentId'], ascending=[False, True]).iloc[0]['ParentId']
    # Retrieve total number of answers that question received (AnswerCount); fallback to counting if missing
    row = ans_with_q[ans_with_q['ParentId'] == max_qid].iloc[0]
    if 'AnswerCount' in row and not pd.isna(row['AnswerCount']):
        result = int(row['AnswerCount'])
    else:
        # Fallback: count all answers to that question from prepared_posts
        total_answers = prepared_posts[(prepared_posts['PostTypeId'] == 2) & (prepared_posts['ParentId'] == max_qid)]
        result = int(len(total_answers))
result_df = pd.DataFrame([{'answer': result}])

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
