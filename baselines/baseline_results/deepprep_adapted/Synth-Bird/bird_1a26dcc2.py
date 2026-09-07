import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Title", mode="mode")
    # MissingValueImputation
    table_1["Title"] = table_1["Title"].fillna(table_1["Title"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OwnerDisplayName", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     # normalize whitespace; keep original casing trimmed
    #     return " ".join(str(s).split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        # normalize whitespace; keep original casing trimmed
        return " ".join(str(s).split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OwnerDisplayName"] = table_1["OwnerDisplayName"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     val = row.get('OwnerDisplayName', None)
    #     if val is None:
    #         return False
    #     return str(val).strip().lower() == 'community'
    # """)
    # Filter
    def filter_func(row):
        val = row.get('OwnerDisplayName', None)
        if val is None:
            return False
        return str(val).strip().lower() == 'community'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Id', 'PostTypeId', 'OwnerDisplayName', 'Tags', 'Title', 'Body'])
    # SelectCol
    _cols = [c for c in ['Id', 'PostTypeId', 'OwnerDisplayName', 'Tags', 'Title', 'Body'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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

prepared_table_1 = _prep_1(tables['table_7'])
prepared_posts = prepared_table_1

# Start from the prepared single table
posts = prepared_posts.copy()

# Filter posts authored by Community
community_posts = posts[posts['OwnerDisplayName'].fillna('').str.strip().str.lower() == 'community']

# Define helper to detect R usage via tags or text
def uses_r(row):
    tags = str(row.get('Tags', '')).lower()
    title = str(row.get('Title', '')).lower()
    body = str(row.get('Body', '')).lower()
    # Tag-based detection: explicit <r> tag or common variants
    tag_hit = ('<r>' in tags) or ('<r-language>' in tags) or ('<rstats>' in tags)
    # Text-based detection: look for ' r ' as a word or common markers like 'r:' or backticked r
    # Keep it simple and conservative to reduce false positives with 'R' as a single letter
    text_hit = (
        ' r ' in f' {title} ' or ' r ' in f' {body} '
        or ' r-language' in title or ' r language' in title
        or ' rstudio' in title or ' rstudio' in body
        or ' rscript' in title or ' rscript' in body
        or '`r`' in title or '`r`' in body
    )
    return tag_hit or text_hit

if not community_posts.empty:
    r_mask = community_posts.apply(uses_r, axis=1)
    r_count = int(r_mask.sum())
    total = int(len(community_posts))
    percentage = (r_count / total * 100.0) if total > 0 else 0.0
else:
    r_count = 0
    total = 0
    percentage = 0.0

result = pd.DataFrame({
    'total_community_posts': [total],
    'r_posts': [r_count],
    'percentage_r_posts': [percentage]
})

target = result

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
