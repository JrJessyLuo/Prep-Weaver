import pandas as pd

# --- Extract birthdays from table_1 (wide, with attributes in rows) ---
t1 = tables["table_1"].copy()

# Clean column names like '"4526214"' -> '4526214'
t1.columns = [c[1:-1] if isinstance(c, str) and len(c) >= 2 and c.startswith('"') and c.endswith('"') else c for c in t1.columns]

bday_row = t1.loc[t1["ID"].astype(str).str.strip().eq("Birthday")]
if bday_row.empty:
    birthdays = pd.DataFrame(columns=["patient_id", "Birthday"])
else:
    bday_row = bday_row.iloc[0].drop(labels=["ID"])
    birthdays = (
        bday_row.rename_axis("patient_id")
        .reset_index(name="Birthday")
    )
    birthdays["patient_id"] = birthdays["patient_id"].astype(str)
    birthdays["Birthday"] = pd.to_datetime(birthdays["Birthday"], errors="coerce")

# --- Filter lab examinations in October 1991 from table_2 ---
t2 = tables["table_2"].copy()
t2["Date"] = pd.to_datetime(t2["Date"], errors="coerce")

oct_1991_mask = (t2["Date"] >= pd.Timestamp("1991-10-01")) & (t2["Date"] < pd.Timestamp("1991-11-01"))
oct_1991_ids = t2.loc[oct_1991_mask, "ID"].dropna().astype(int).astype(str).unique()

# --- Compute ages as of year 1999 (use 1999-12-31 as reference) ---
ref_date = pd.Timestamp("1999-12-31")
ages = (
    birthdays.loc[birthdays["patient_id"].isin(oct_1991_ids), ["patient_id", "Birthday"]]
    .dropna(subset=["Birthday"])
    .assign(age_as_of_1999=lambda d: (ref_date - d["Birthday"]).dt.days / 365.25)
)

avg_age = ages["age_as_of_1999"].mean()

result = {
    "average_age_oct_1991_examined_as_of_1999": pd.DataFrame(
        {"average_age_as_of_1999": [avg_age]}
    )
}
