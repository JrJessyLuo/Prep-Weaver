import pandas as pd
import numpy as np

buildings = tables["table_6"].copy()
rooms = tables["table_2"].copy()

# Standardize building keys
buildings["building_key"] = buildings["FCLT_BUILDING_KEY"].astype(str).str.strip()
rooms["building_key"] = rooms["BUILDING_KEY"].astype(str).str.strip()

# Exclude building subdivisions/components
parent = buildings["PARENT_BUILDING_NUMBER"]
non_subdivision_mask = parent.isna() | parent.astype(str).str.strip().isin(["", "nan", "None"])
buildings = buildings.loc[non_subdivision_mask].copy()

# Display residence building uses as RESIDENTIAL
building_use = buildings["BUILDING_USE"].astype(str).str.strip()
building_type = buildings["BUILDING_TYPE"].astype(str).str.strip()

res_mask = (
    building_use.str.upper().isin(["RES", "RESIDENCE", "RESIDENTIAL"])
    | building_use.str.upper().str.contains("RESID", na=False)
    | building_type.str.upper().str.contains("RESID", na=False)
)

buildings["Building Use"] = np.where(res_mask, "RESIDENTIAL", building_use)
buildings["Building Use"] = buildings["Building Use"].replace(["nan", "None", ""], "UNKNOWN")

# Building counts and gross square footage by use
building_summary = (
    buildings.groupby("Building Use", dropna=False)
    .agg(
        **{
            "Number of Buildings": ("building_key", "nunique"),
            "Gross Square Footage": ("EXT_GROSS_AREA", "sum"),
        }
    )
    .reset_index()
)

# Unique organizations associated with rooms in the included buildings
room_orgs = rooms.merge(
    buildings[["building_key", "Building Use"]],
    on="building_key",
    how="inner"
)

org_summary = (
    room_orgs.groupby("Building Use", dropna=False)
    .agg(**{"Number of Organizations": ("ORGANIZATION_KEY", "nunique")})
    .reset_index()
)

out = building_summary.merge(org_summary, on="Building Use", how="left")
out["Number of Organizations"] = out["Number of Organizations"].fillna(0)

# Total row across all building uses
total_row = pd.DataFrame(
    [
        {
            "Building Use": "TOTAL",
            "Number of Buildings": buildings["building_key"].nunique(),
            "Gross Square Footage": buildings["EXT_GROSS_AREA"].sum(),
            "Number of Organizations": room_orgs["ORGANIZATION_KEY"].nunique(),
        }
    ]
)

out = pd.concat(
    [out.sort_values("Building Use", kind="stable"), total_row],
    ignore_index=True
)

# Round numeric values to integers and format with thousands separators
for col in ["Number of Buildings", "Gross Square Footage", "Number of Organizations"]:
    out[col] = out[col].round(0).astype("int64").map(lambda x: f"{x:,}")

result = {"building_use_summary": out}
