import pandas as pd

# --- Prepare district-level attributes from the transposed table_2 ---
df2 = tables["table_2"].copy()
value_cols = [c for c in df2.columns if c != "district_id"]

long = df2.melt(
    id_vars="district_id",
    value_vars=value_cols,
    var_name="district_id_num",
    value_name="value"
)
long["district_id_num"] = pd.to_numeric(long["district_id_num"], errors="coerce").astype("Int64")

wide = (
    long.pivot_table(index="district_id_num", columns="district_id", values="value", aggfunc="first")
    .reset_index()
    .rename(columns={"district_id_num": "district_id"})
)

# Find crimes in 1995 column (typically A15 in the District table)
crimes95_cols = [c for c in wide.columns if str(c).strip().upper().startswith("A15")]
crimes95_col = crimes95_cols[0] if crimes95_cols else None

if crimes95_col is None:
    avg_val = float("nan")
else:
    wide["crimes_1995"] = pd.to_numeric(wide[crimes95_col], errors="coerce")

    # --- Accounts opened starting from 1997 ---
    acc = tables["table_1"].copy()
    d1 = pd.to_datetime(acc["fdm"], errors="coerce")
    d2 = pd.to_datetime(acc["fdpo"], errors="coerce")
    d3 = pd.to_datetime(acc["fdt"], errors="coerce")
    acc["open_date"] = d1.combine_first(d2).combine_first(d3)

    recent_districts = set(
        acc.loc[acc["open_date"].dt.year.ge(1997, fill_value=False), "district_id"]
        .dropna()
        .astype(int)
        .unique()
    )

    eligible = wide[
        wide["district_id"].astype("Int64").isin(recent_districts) &
        (wide["crimes_1995"] > 4000)
    ]

    avg_val = eligible["crimes_1995"].mean()

result = {
    "average_crimes_1995": pd.DataFrame({"average_crimes_1995": [avg_val]})
}
