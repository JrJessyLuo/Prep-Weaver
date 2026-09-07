import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['TERM_CODE','SUBJECT_ID','SUBJECT_CODE','SUBJECT_NUMBER','SUBJECT_TITLE','DEPARTMENT_CODE','DEPARTMENT_NAME','GIR_ATTRIBUTE','GIR_ATTRIBUTE_DESC','COMM_REQ_ATTRIBUTE','COMM_REQ_ATTRIBUTE_DESC','TUITION_ATTRIBUTE','TUITION_ATTRIBUTE_DESC','WRITE_REQ_ATTRIBUTE','WRITE_REQ_ATTRIBUTE_DESC']
    df = table_1[cols].copy()
    id_cols = ['TERM_CODE','SUBJECT_ID','SUBJECT_CODE','SUBJECT_NUMBER']
    df = df.groupby(id_cols, as_index=False).agg({c: 'first' for c in cols if c not in id_cols})
    target = df[cols]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','COURSE_NUMBER','HGN_CODE','HGN_CODE_DESC']].copy()
    prepared = prepared.drop_duplicates(subset=['TERM_CODE','SUBJECT_ID'], keep='first')
    target = prepared[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','COURSE_NUMBER','HGN_CODE','HGN_CODE_DESC']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_offerings = prepared_table_2

# Merge prepared tables on term and subject to align department/school info with subject records
merged = prepared_subjects.merge(
    prepared_offerings,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="inner"
)

# Define a boolean indicating humanities, arts, and social sciences subjects.
# If there is an explicit attribute/descriptor column that marks HASS/Humanities/Arts/Social Sciences,
# search across available attribute description columns.
attr_cols = [
    "GIR_ATTRIBUTE_DESC",
    "COMM_REQ_ATTRIBUTE_DESC",
    "TUITION_ATTRIBUTE_DESC",
    "WRITE_REQ_ATTRIBUTE_DESC",
]

pattern = r"(humanities|arts|social\s*sciences|hass)"
mask = pd.Series(False, index=merged.index)
for c in attr_cols:
    if c in merged.columns:
        mask = mask | merged[c].astype(str).str.contains(pattern, case=False, na=False)

hass = merged[mask].copy()

# For each term code, produce requested fields and count of subjects
result = (
    hass.groupby(["TERM_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"], dropna=False)
        .agg(num_subjects=("SUBJECT_ID", "nunique"))
        .reset_index()
)

# Attach term description and attribute description evidence per term if available.
# If a term description column exists (e.g., TERM_DESC) it would be merged here; since it's not present,
# we will derive a simple description placeholder equal to TERM_CODE.
result["TERM_DESCRIPTION"] = result["TERM_CODE"]

# Attribute description: provide an aggregated sample of matching attribute descriptions as evidence per term
def collect_attrs(df):
    vals = []
    for c in attr_cols:
        if c in df.columns:
            vals.extend(df[c].dropna().astype(str).unique().tolist())
    # Keep concise unique list
    return ", ".join(sorted(set(vals))[:3])

attr_by_term = (
    hass.groupby("TERM_CODE").apply(collect_attrs).reset_index(name="ATTRIBUTE_DESCRIPTION")
)

final = result.merge(attr_by_term, on="TERM_CODE", how="left")[
    [
        "TERM_CODE",
        "TERM_DESCRIPTION",
        "ATTRIBUTE_DESCRIPTION",
        "OFFER_DEPT_NAME",
        "OFFER_SCHOOL_NAME",
        "num_subjects",
    ]
].sort_values(["TERM_CODE", "OFFER_SCHOOL_NAME", "OFFER_DEPT_NAME"]).reset_index(drop=True)

target = final

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
