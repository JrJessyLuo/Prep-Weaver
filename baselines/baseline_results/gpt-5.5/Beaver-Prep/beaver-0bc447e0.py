import pandas as pd
import re

df = tables["table_3"].copy()

summer = df[
    df["IS_OFFERED_SUMMER_TERM"].astype(str).str.strip().str.upper().eq("Y")
].copy()

instructor_cols = [c for c in ["FALL_INSTRUCTORS", "SPRING_INSTRUCTORS"] if c in summer.columns]

def split_instructors(x):
    if pd.isna(x):
        return []
    s = str(x).strip()
    if not s or s.lower() in {"nan", "none"}:
        return []
    return [p.strip() for p in re.split(r"\s*,\s*|\s*;\s*", s) if p.strip()]

titles = summer[["SUBJECT_TITLE"]].drop_duplicates()

if instructor_cols:
    long = summer[["SUBJECT_TITLE"] + instructor_cols].melt(
        id_vars="SUBJECT_TITLE",
        value_vars=instructor_cols,
        value_name="instructor"
    )
    long["instructor"] = long["instructor"].apply(split_instructors)
    long = long.explode("instructor")
    long = long[long["instructor"].notna() & long["instructor"].astype(str).str.strip().ne("")]
    long["instructor"] = long["instructor"].astype(str).str.strip()
    long["instructor_name_length"] = long["instructor"].str.len()

    agg = (
        long.groupby("SUBJECT_TITLE", as_index=False)
        .agg(
            number_of_instructors=("instructor", "nunique"),
            longest_instructor_name_length=("instructor_name_length", "max")
        )
    )
else:
    agg = pd.DataFrame(columns=[
        "SUBJECT_TITLE",
        "number_of_instructors",
        "longest_instructor_name_length"
    ])

out = titles.merge(agg, on="SUBJECT_TITLE", how="left")
out["number_of_instructors"] = out["number_of_instructors"].fillna(0).astype(int)
out["longest_instructor_name_length"] = out["longest_instructor_name_length"].fillna(0).astype(int)

out = (
    out.rename(columns={"SUBJECT_TITLE": "subject_title"})
    .sort_values("subject_title")
    .reset_index(drop=True)
)

result = {"summer_subject_instructors": out}
