import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Build University_ID from tens/units (stored as strings)
t2["University_ID"] = (t2["ID_Tens"].astype(str) + t2["ID_Units"].astype(str)).astype(int)

# Compose full university name
t1["university_name"] = (t1["Uni_Name_Prefix"].fillna("").astype(str) + " " +
                         t1["Uni_Name_Suffix"].fillna("").astype(str)).str.replace(r"\s+", " ", regex=True).str.strip()

merged = t2.merge(t1[["University_ID", "university_name"]], on="University_ID", how="left")

max_research = merged["Research_point"].max()
out = (merged.loc[merged["Research_point"].eq(max_research), ["university_name"]]
            .dropna()
            .drop_duplicates()
            .reset_index(drop=True))

result = {"university_with_most_research_points": out}
