import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="IS_MASTER_SECTION", mode="mode")
    # MissingValueImputation
    table_1["IS_MASTER_SECTION"] = table_1["IS_MASTER_SECTION"].fillna(table_1["IS_MASTER_SECTION"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_subject_offerings", func="""
    # import pandas as pd
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Keep only required columns
    #     keep_cols = [
    #         "SUBJECT_OFFERED_SUMMARY_KEY",
    #         "SUBJECT_ID",
    #         "SUBJECT_TITLE",
    #         "TERM_CODE",
    #         "RESPONSIBLE_FACULTY_NAME",
    #         "SECTION_ID",
    #         "IS_MASTER_SECTION",
    #     ]
    #     df = df[keep_cols]
    # 
    #     # Clean instructor name text (needed for distinct-count and longest-length computations later)
    #     def clean_name(x):
    #         if pd.isna(x):
    #             return ""
    #         s = str(x)
    #         s = re.sub(r"\s+", " ", s).strip()
    #         return s
    # 
    #     df["RESPONSIBLE_FACULTY_NAME"] = df["RESPONSIBLE_FACULTY_NAME"].apply(clean_name)
    # 
    #     # Ensure key/id-like fields are strings (safer for later grouping/joins)
    #     for c in ["SUBJECT_OFFERED_SUMMARY_KEY","SUBJECT_ID","TERM_CODE","SECTION_ID","IS_MASTER_SECTION"]:
    #         df[c] = df[c].astype(str)
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Keep only required columns
        keep_cols = [
            "SUBJECT_OFFERED_SUMMARY_KEY",
            "SUBJECT_ID",
            "SUBJECT_TITLE",
            "TERM_CODE",
            "RESPONSIBLE_FACULTY_NAME",
            "SECTION_ID",
            "IS_MASTER_SECTION",
        ]
        df = df[keep_cols]

        # Clean instructor name text (needed for distinct-count and longest-length computations later)
        def clean_name(x):
            if pd.isna(x):
                return ""
            s = str(x)
            s = re.sub(r"\s+", " ", s).strip()
            return s

        df["RESPONSIBLE_FACULTY_NAME"] = df["RESPONSIBLE_FACULTY_NAME"].apply(clean_name)

        # Ensure key/id-like fields are strings (safer for later grouping/joins)
        for c in ["SUBJECT_OFFERED_SUMMARY_KEY","SUBJECT_ID","TERM_CODE","SECTION_ID","IS_MASTER_SECTION"]:
            df[c] = df[c].astype(str)

        return df
    prepared_subject_offerings = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['prepared_subject_offerings'])
    # Terminate
    result = {'prepared_subject_offerings': prepared_subject_offerings}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_subject_offerings = prepared_table_1

# Assume table_1 is already loaded as a DataFrame named table_1
prepared_subject_offerings = table_1[[
    'SUBJECT_OFFERED_SUMMARY_KEY', 'SUBJECT_ID', 'SUBJECT_TITLE', 'TERM_CODE',
    'RESPONSIBLE_FACULTY_NAME', 'SECTION_ID', 'IS_MASTER_SECTION'
]].copy()

# Filter to summer term(s). Adjust the predicate to match the dataset's encoding of summer terms.
# Common encodings are e.g., term codes containing 'SU' or specific summer codes; here we match 'SU'.
summer_mask = prepared_subject_offerings['TERM_CODE'].astype(str).str.contains('SU', case=False, na=False)
summer_offerings = prepared_subject_offerings[summer_mask].copy()

# Normalize instructor names: drop NaNs/empties and strip whitespace
summer_offerings['RESPONSIBLE_FACULTY_NAME'] = summer_offerings['RESPONSIBLE_FACULTY_NAME'].astype(str)
summer_offerings.loc[summer_offerings['RESPONSIBLE_FACULTY_NAME'].str.lower().isin(['nan', 'none', '']), 'RESPONSIBLE_FACULTY_NAME'] = pd.NA

# Compute per offering metrics: number of distinct instructors and max name length
# Group by the offering key; carry a representative subject title
grp = summer_offerings.groupby('SUBJECT_OFFERED_SUMMARY_KEY', dropna=False)

def agg_title(s):
    # Prefer a non-null, most frequent title
    non_null = s.dropna()
    return non_null.mode().iloc[0] if not non_null.empty else None

result = grp.apply(lambda df: pd.Series({
    'SUBJECT_TITLE': agg_title(df['SUBJECT_TITLE']),
    'num_instructors': df['RESPONSIBLE_FACULTY_NAME'].dropna().str.strip().replace('', pd.NA).dropna().nunique(),
    'longest_instructor_name_length': int(df['RESPONSIBLE_FACULTY_NAME'].dropna().str.strip().str.len().max()) if df['RESPONSIBLE_FACULTY_NAME'].dropna().size > 0 else 0
})).reset_index()

# Select final columns
target = result[['SUBJECT_TITLE', 'num_instructors', 'longest_instructor_name_length']]

# The variable 'target' holds the answer table.

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
