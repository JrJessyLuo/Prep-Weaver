import pandas as pd

# Get Amazo's hero_id from the transposed hero table
t1 = tables["table_1"]
name_row = t1.loc[t1["id"].eq("superhero_name")].iloc[0]
hero_id = (
    name_row.drop(labels=["id"])
    .reset_index()
    .rename(columns={"index": "hero_id", name_row.name: "superhero_name"})
    .loc[lambda d: d["superhero_name"].eq("Amazo"), "hero_id"]
    .astype(int)
    .iloc[0]
)

# Parse hero_power pairs and count Amazo's powers
hp = tables["table_2"].copy()
hp[["hero_id", "power_id"]] = hp["hero_power"].astype(str).str.split("-", n=1, expand=True)
hp["hero_id"] = pd.to_numeric(hp["hero_id"], errors="coerce")

num_powers = int(hp.loc[hp["hero_id"].eq(hero_id), "power_id"].notna().sum())

result = {
    "amazo_power_count": pd.DataFrame([{"superhero_name": "Amazo", "number_of_powers": num_powers}])
}
