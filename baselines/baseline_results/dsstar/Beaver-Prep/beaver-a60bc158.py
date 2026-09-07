import pandas as pd

# Source input DataFrame from provided tables dict
df = tables['table_1'].copy()

# Reproduce the SAME logic as the reference code:
# Newly introduced subjects are where TERM_CODE == EFFECTIVE_TERM_CODE
required_cols = {"TERM_CODE", "EFFECTIVE_TERM_CODE", "ACADEMIC_YEAR"}
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise KeyError(f"Missing required columns for current plan: {missing}")

def to_str_safe(series):
    return series.astype(str).str.strip()

term_code_str = to_str_safe(df["TERM_CODE"])
effective_term_code_str = to_str_safe(df["EFFECTIVE_TERM_CODE"])

first_offered_mask = term_code_str.eq(effective_term_code_str)

df_first_offered = df.loc[first_offered_mask, ["ACADEMIC_YEAR", "TERM_CODE"]].copy()

# Group and count newly introduced subjects per term and sort
new_subject_counts = (
    df_first_offered
    .groupby(["ACADEMIC_YEAR", "TERM_CODE"], dropna=False)
    .size()
    .reset_index(name="new_subject_count")
    .sort_values(["ACADEMIC_YEAR", "TERM_CODE"], kind="mergesort")
)

# Format per requirement:
# - List each academic year, the term code, and the number
# - Display the academic year only if it differs from the previous entry (else blank)
# - Include a grand total row with ACADEMIC_YEAR == 'TOTAL' and total subjects across all years

# Prepare display column for ACADEMIC_YEAR with blanks on repeats
display_df = new_subject_counts.copy()
display_df["ACADEMIC_YEAR"] = display_df["ACADEMIC_YEAR"].astype(str)

# Mark repeated years as empty string
display_year = []
prev_year = None
for y in display_df["ACADEMIC_YEAR"]:
    if y != prev_year:
        display_year.append(y)
        prev_year = y
    else:
        display_year.append("")
display_df["ACADEMIC_YEAR"] = display_year

# Compute grand total
grand_total = int(new_subject_counts["new_subject_count"].sum())

# Append TOTAL row
total_row = pd.DataFrame(
    [{"ACADEMIC_YEAR": "TOTAL", "TERM_CODE": "", "new_subject_count": grand_total}]
)
final_df = pd.concat([display_df, total_row], ignore_index=True)

# Assign to result as required
result = {"newly_introduced_subjects_by_term": final_df}