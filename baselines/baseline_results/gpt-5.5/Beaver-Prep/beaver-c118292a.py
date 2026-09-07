import pandas as pd
import re

# Use the subject/offering table with fall-term offering details
df = tables["table_4"].copy()

# Identify fall-term offerings
if "SO_TERM_CODE" in df.columns and df["SO_TERM_CODE"].notna().any():
    fall_mask = df["SO_TERM_CODE"].astype(str).str.upper().str.endswith("FA")
elif "TERM_CODE" in df.columns and df["TERM_CODE"].notna().any():
    fall_mask = df["TERM_CODE"].astype(str).str.upper().str.endswith("FA")
else:
    fall_mask = df["IS_OFFERED_FALL_TERM"].astype(str).str.upper().eq("Y")

fall = df.loc[fall_mask].copy()

# Use fall instructor list; split multiple instructors into separate rows
fall = fall[["SUBJECT_ID", "SUBJECT_TITLE", "FALL_INSTRUCTORS"]].dropna(
    subset=["SUBJECT_TITLE", "FALL_INSTRUCTORS"]
)

fall["instructor_name"] = fall["FALL_INSTRUCTORS"].astype(str).str.split(r"\s*,\s*")
fall = fall.explode("instructor_name")
fall["instructor_name"] = fall["instructor_name"].astype(str).str.strip()

fall = fall[
    fall["instructor_name"].ne("")
    & ~fall["instructor_name"].str.lower().isin(["nan", "none"])
].copy()

# Normalize names for joining/counting
fall["instructor_name_norm"] = fall["instructor_name"].str.lower().str.replace(r"\s+", " ", regex=True).str.strip()

# Try to find instructor email information if any table contains email-like columns
email_frames = []
for t in tables.values():
    email_cols = [c for c in t.columns if re.search(r"email|e_mail|mail_address", c, flags=re.I)]
    name_cols = [
        c for c in t.columns
        if re.search(r"(instructor|faculty).*name|name.*(instructor|faculty)", c, flags=re.I)
    ]
    for name_col in name_cols:
        for email_col in email_cols:
            tmp = t[[name_col, email_col]].dropna().copy()
            if not tmp.empty:
                tmp = tmp.rename(columns={name_col: "instructor_name", email_col: "instructor_email"})
                tmp["instructor_name_norm"] = (
                    tmp["instructor_name"].astype(str)
                    .str.lower()
                    .str.replace(r"\s+", " ", regex=True)
                    .str.strip()
                )
                tmp["instructor_email"] = tmp["instructor_email"].astype(str).str.strip()
                tmp = tmp[tmp["instructor_email"].str.contains("@", na=False)]
                email_frames.append(tmp[["instructor_name_norm", "instructor_email"]])

if email_frames:
    email_lookup = (
        pd.concat(email_frames, ignore_index=True)
        .drop_duplicates(subset=["instructor_name_norm"])
    )
else:
    email_lookup = pd.DataFrame(columns=["instructor_name_norm", "instructor_email"])

# Count distinct subject titles per instructor
counts = (
    fall.drop_duplicates(["instructor_name_norm", "SUBJECT_TITLE"])
    .groupby("instructor_name_norm", as_index=False)
    .agg(total_number_of_subject_types_per_instructor=("SUBJECT_TITLE", "nunique"))
)

# Final unique subject-title / instructor rows
out = (
    fall.drop_duplicates(["SUBJECT_TITLE", "instructor_name_norm"])
    .merge(email_lookup, on="instructor_name_norm", how="left")
    .merge(counts, on="instructor_name_norm", how="left")
)

out["instructor_email"] = out["instructor_email"].where(out["instructor_email"].notna(), pd.NA)

out = (
    out[[
        "SUBJECT_TITLE",
        "instructor_name",
        "instructor_email",
        "total_number_of_subject_types_per_instructor"
    ]]
    .rename(columns={
        "SUBJECT_TITLE": "subject_title",
        "instructor_name": "instructor_name",
        "instructor_email": "instructor_email"
    })
    .sort_values(["instructor_name", "subject_title"], kind="mergesort")
    .reset_index(drop=True)
)

result = {
    "fall_subject_titles_by_instructor": out
}
