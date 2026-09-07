import numpy as np
import pandas as pd

t1 = tables["table_1"].copy()  # races: id -> zz
t2 = tables["table_2"].copy()

# Filter superhero(s) by height and weight
mask = np.isclose(t2["height_cm"].astype(float), 188.0, equal_nan=False) & np.isclose(
    t2["weight_kg"].astype(float), 108.0, equal_nan=False
)
f = t2.loc[mask].copy()

# combined_ids format inferred as: gender|eye|hair|skin|race|publisher|alignment
f["race_id"] = (
    f["combined_ids"].astype(str).str.split("|").str[4].astype(float).round().astype("Int64")
)

out = f.merge(t1, left_on="race_id", right_on="id", how="left")[["zz"]].rename(columns={"zz": "race"})
out = out.drop_duplicates().reset_index(drop=True)

result = {"race": out}
