import pandas as pd

# tables are preloaded in scope as a dict of DataFrames
majors = tables["table_1"]   # bird_f6524792_input_0.pkl (majors)
members = tables["table_2"]  # bird_f6524792_input_1.pkl (members)

# Target person
target_first = "Garrett"
target_last = "Gerke"

# Locate Garrett Gerke
garrett = members.loc[
    (members["first_name"] == target_first) & (members["last_name"] == target_last)
].copy()

if garrett.empty:
    raise ValueError(f"No member found for {target_first} {target_last}")

# From the reference output, Garrett's major link is stored in column 'ltm'
if "ltm" not in garrett.columns:
    raise ValueError("Expected 'ltm' column in members table to link to majors, but it was not found.")

major_id = garrett["ltm"].iloc[0]

# Join to majors to get major + department
if "major_id" not in majors.columns:
    raise ValueError("Expected 'major_id' column in majors table, but it was not found.")

major_row = majors.loc[majors["major_id"] == major_id].copy()
if major_row.empty:
    raise ValueError(f"No major found for major_id={major_id}")

# Pick likely name/department columns (robust to minor schema differences)
name_col = "major" if "major" in majors.columns else ("major_name" if "major_name" in majors.columns else None)
dept_col = "department" if "department" in majors.columns else ("dept" if "dept" in majors.columns else None)

if name_col is None:
    raise ValueError("Could not find a major name column (expected 'major' or 'major_name') in majors table.")
if dept_col is None:
    raise ValueError("Could not find a department column (expected 'department' or 'dept') in majors table.")

answer_df = major_row[[name_col, dept_col]].rename(columns={name_col: "major", dept_col: "department"}).reset_index(drop=True)

# Final answer in required format
result = {"answer": answer_df}