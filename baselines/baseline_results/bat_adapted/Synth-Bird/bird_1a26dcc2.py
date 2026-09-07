import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['Id','PostTypeId','OwnerDisplayName','Tags']].copy()
    prepared['OwnerDisplayName'] = prepared['OwnerDisplayName'].replace({'None': pd.NA})
    prepared['Tags'] = prepared['Tags'].replace({'None': pd.NA})
    prepared = prepared.groupby(['Id','PostTypeId'], as_index=False).agg({'OwnerDisplayName': 'first', 'Tags': 'first'})
    target = prepared[['Id','PostTypeId','OwnerDisplayName','Tags']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_posts = prepared_table_1

# Start from the prepared single-table output
posts = prepared_posts.copy()

# Filter to posts authored by Community (case-insensitive, strip None)
community_posts = posts[posts['OwnerDisplayName'].fillna('').str.lower() == 'community']

# Define a helper to detect R-language usage from the Tags field
# The dataset uses StackExchange-like tag format: e.g., "<r><regression>"
# We'll treat a post as R-related if it contains the exact tag <r> or variants like <r-language>
# (adjust pattern as needed for the corpus)
tag_series = community_posts['Tags'].fillna('')
uses_r_mask = tag_series.str.contains(r'<r(>|-language>|-project>|-studio>|-markdown>|-shiny>)', case=False, regex=True)

# Compute percentage
total = len(community_posts)
r_count = int(uses_r_mask.sum())
percentage_r = (r_count / total * 100.0) if total > 0 else 0.0

answer = {
    'total_community_posts': int(total),
    'r_posts': r_count,
    'percentage_r': percentage_r
}

target = pd.DataFrame([answer])

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
