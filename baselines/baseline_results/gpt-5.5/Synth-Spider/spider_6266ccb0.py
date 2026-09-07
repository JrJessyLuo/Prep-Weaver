import pandas as pd

df1 = tables["table_1"].copy()
cities = tables["table_2"].copy()

# Clean student_id
df1["student_id"] = df1["student_id"].astype(str).str.strip().str.strip('"').str.strip("'")

# Pivot key-value attributes to wide format per student
wide = (
    df1.pivot_table(index="student_id", columns="StuID", values="attribute_value", aggfunc="first")
      .reset_index()
)

# Try to find a direct country column first
country_cols = [c for c in wide.columns if isinstance(c, str) and ("country" in c.lower() or "nation" in c.lower())]

students_in_china = pd.Series([], dtype=str)
if country_cols:
    ccol = country_cols[0]
    students_in_china = wide.loc[
        wide[ccol].astype(str).str.strip().str.lower().eq("china"),
        "student_id"
    ]
else:
    # Otherwise, infer which column contains city codes by matching to table_2.city_code
    city_code_set = set(cities["city_code"].astype(str))
    best_col, best_score = None, -1.0
    for c in wide.columns:
        if c == "student_id":
            continue
        s = wide[c].astype(str)
        score = s.isin(city_code_set).mean()
        if score > best_score:
            best_col, best_score = c, score

    if best_col is not None and best_score > 0:
        tmp = wide[["student_id", best_col]].rename(columns={best_col: "city_code"})
        tmp["city_code"] = tmp["city_code"].astype(str)

        # Extract country from state_country (format like "MD~U.S.A." or "...~China")
        cities2 = cities.copy()
        cities2["country"] = cities2["state_country"].astype(str).str.split("~").str[-1].str.strip()
        cities2["country_norm"] = (
            cities2["country"]
            .str.lower()
            .str.replace(r"[^a-z]", "", regex=True)
        )

        merged = tmp.merge(cities2[["city_code", "country_norm"]], on="city_code", how="left")
        students_in_china = merged.loc[merged["country_norm"].eq("china"), "student_id"]

count_china = int(pd.Series(students_in_china).dropna().nunique())

result = {
    "students_in_china": pd.DataFrame({"number_of_students": [count_china]})
}
