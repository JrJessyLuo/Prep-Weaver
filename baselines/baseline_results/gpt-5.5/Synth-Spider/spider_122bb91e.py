import pandas as pd

# --- Planets: build full planet name ---
planets = tables["table_1"].copy()
name_parts = ["Name_Part1", "Name_Part2", "Name_Part3"]
planets["planet_name"] = planets[name_parts].apply(
    lambda r: " ".join([str(x) for x in r.tolist() if pd.notna(x)]), axis=1
)

omicron_id = planets.loc[planets["planet_name"].eq("Omicron Persei 8"), "PlanetID"]
omicron_id = int(omicron_id.iloc[0]) if len(omicron_id) else None

# --- Shipments: pivot transposed key/value table into normal columns ---
t2 = tables["table_2"].copy()
ship_long = t2.melt(id_vars=["ShipmentID"], var_name="Shipment", value_name="value")
shipments = (
    ship_long.pivot_table(index="Shipment", columns="ShipmentID", values="value", aggfunc="first")
    .reset_index()
)
shipments["Shipment"] = pd.to_numeric(shipments["Shipment"], errors="coerce").astype("Int64")
if "Planet" in shipments.columns:
    shipments["Planet"] = pd.to_numeric(shipments["Planet"], errors="coerce").astype("Int64")

# --- People: unpivot diagonal-ish table to get PersonID -> Name ---
t3 = tables["table_3"].copy()
people = (
    t3.stack(dropna=True)
      .reset_index()
      .rename(columns={"level_0": "row", "level_1": "PersonID", 0: "Name"})
)
people["PersonID"] = pd.to_numeric(people["PersonID"], errors="coerce").astype("Int64")

zapp_ids = people.loc[people["Name"].eq("Zapp Brannigan"), "PersonID"].dropna().unique().tolist()

# --- Packages: filter and count distinct packages meeting either condition ---
packages = tables["table_4"].copy()

shipments_to_omicron = set()
if omicron_id is not None and "Planet" in shipments.columns:
    shipments_to_omicron = set(
        shipments.loc[shipments["Planet"].eq(omicron_id), "Shipment"].dropna().astype(int).tolist()
    )

pkg_on_omicron = packages["Shipment"].isin(shipments_to_omicron)
pkg_sent_by_zapp = packages["Sender"].isin(zapp_ids) if len(zapp_ids) else False

selected = packages.loc[pkg_on_omicron | pkg_sent_by_zapp, ["Shipment", "PackageNumber"]].drop_duplicates()
count_packages = int(len(selected))

result = {
    "number_of_packages": pd.DataFrame({"number_of_packages": [count_packages]})
}
