import pandas as pd

majors = tables["table_1"]
students = tables["table_2"]

law_major_ids = majors.loc[
    majors["major_name"].astype(str).str.strip().str.lower().eq("law and constitutional studies"),
    "major_id"
].dropna()

out = (
    students[students["link_to_major"].isin(law_major_ids)]
    [["last_name"]]
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"law_and_constitutional_studies_students_last_names": out}
