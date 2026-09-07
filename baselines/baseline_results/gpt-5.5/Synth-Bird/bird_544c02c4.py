import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Define "normal" IGG range (mg/dL)
IGG_LOW, IGG_HIGH = 800, 1700

# Patients who have at least one normal IGG measurement
normal_ids = (
    t2.loc[t2["IGG"].between(IGG_LOW, IGG_HIGH, inclusive="both"), "ID"]
      .dropna()
      .astype("int64")
      .unique()
)

# Count how many of those patients were admitted ("+")
admitted_count = (
    t1.loc[
        t1["ID"].isin(normal_ids)
        & t1["Admission"].astype(str).str.strip().eq("+"),
        "ID",
    ]
    .nunique()
)

result = {
    "admitted_patients_with_normal_IGG": pd.DataFrame(
        {"admitted_patients_with_normal_IGG": [admitted_count]}
    )
}
