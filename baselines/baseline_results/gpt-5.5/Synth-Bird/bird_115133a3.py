import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Build a fallback school name from table_1 parts
t1["school_name_fallback"] = (
    t1[["school_part1", "school_part2"]]
    .fillna("")
    .astype(str)
    .agg(" ".join, axis=1)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)
t1.loc[t1["school_name_fallback"].eq(""), "school_name_fallback"] = pd.NA

# Parse dates in table_2
t2["OpenDate_dt"] = pd.to_datetime(t2["OpenDate"], errors="coerce")
t2["ClosedDate_dt"] = pd.to_datetime(t2["ClosedDate"], errors="coerce")

# Join SAT writing scores to school directory info
m = t1.merge(t2, left_on="cds", right_on="CDSCode", how="inner")

# Filter: opened after 1991 OR closed before 2000
mask = (m["OpenDate_dt"] > pd.Timestamp("1991-12-31")) | (m["ClosedDate_dt"] < pd.Timestamp("2000-01-01"))
m = m.loc[mask].copy()

# Prefer directory school name, else fallback from table_1
m["school_name"] = m["School"].where(m["School"].notna(), m["school_name_fallback"])

# If multiple rows per school, compute mean writing score per CDS
out = (
    m.groupby("cds", as_index=False)
     .agg(
         school_name=("school_name", "first"),
         avg_writing_score=("AvgScrWrite", "mean"),
         communication_number=("Phone", "first"),
     )
     .sort_values(["avg_writing_score", "school_name"], ascending=[False, True], na_position="last")
     .reset_index(drop=True)
)

result = {"schools_writing_scores": out}
