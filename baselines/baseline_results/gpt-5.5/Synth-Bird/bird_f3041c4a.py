import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Find set code(s) for cards with "Angel of Mercy" in the name
set_codes = (
    t1.loc[t1["name"].astype(str).str.contains("Angel of Mercy", case=False, na=False), "setCode"]
    .dropna()
    .unique()
)

# Extract setCode from "language_setCode" (format: "Language|SETCODE")
t2_work = t2.copy()
t2_work["setCode"] = t2_work["language_setCode"].astype(str).str.split("|", n=1, expand=True)[1]

num_translations = int(t2_work.loc[t2_work["setCode"].isin(set_codes)].shape[0])

result = {
    "translations_count": pd.DataFrame({"number_of_translations": [num_translations]})
}
