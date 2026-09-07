import pandas as pd

majors = tables["table_1"].copy()
members = tables["table_2"].copy()

# Filter majors in the Art and Design Department
art_design_majors = majors[
    majors["major_info"].astype(str).str.contains("Art and Design Department", case=False, na=False)
][["major_id"]]

# Join members to those majors
out = members.merge(
    art_design_majors,
    left_on="link_to_major",
    right_on="major_id",
    how="inner"
)

out["full_name"] = out["first_name"].astype(str).str.strip() + " " + out["last_name"].astype(str).str.strip()

students_art_design = (
    out[["full_name"]]
    .dropna()
    .drop_duplicates()
    .sort_values("full_name")
    .reset_index(drop=True)
)

result = {"students_art_and_design_department": students_art_design}
