import pandas as pd

df_pat = tables["table_1"].copy()
df_lab = tables["table_2"].copy()

# Parse dates
df_lab["Date"] = pd.to_datetime(df_lab["Date"], errors="coerce")
df_pat["Birthday"] = pd.to_datetime(df_pat["Birthday"], errors="coerce")

# 1994 lab exams with GOT (AST) in normal range (assumed 10-40 inclusive)
lab_1994_normal_got = df_lab[
    (df_lab["Date"].dt.year == 1994) &
    (df_lab["GOT"].notna()) &
    (df_lab["GOT"].between(10, 40, inclusive="both"))
]

ids = lab_1994_normal_got["ID"].dropna().astype("int64").unique()

out = (
    df_pat[df_pat["ID"].isin(ids)][["ID", "SEX", "Birthday"]]
    .drop_duplicates()
    .sort_values("ID")
    .reset_index(drop=True)
)

result = {"patients_normal_GOT_1994": out}
