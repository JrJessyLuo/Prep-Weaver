import pandas as pd
import numpy as np

# Current building metadata (height, alternate names, gross/assignable areas)
fac = tables["table_3"].copy()
fac = fac.rename(columns={"FCLT_BUILDING_KEY": "BUILDING_KEY"})
fac["BUILDING_KEY"] = fac["BUILDING_KEY"].astype(str).str.strip()

fac = fac[
    [
        "BUILDING_KEY",
        "BUILDING_NAME",
        "BUILDING_NAME_LONG",
        "BUILDING_HEIGHT",
        "EXT_GROSS_AREA",
        "ASSIGNABLE_AREA",
        "BUILDING_SORT",
    ]
].drop_duplicates("BUILDING_KEY")

fac = fac.rename(
    columns={
        "BUILDING_NAME": "FAC_BUILDING_NAME",
        "EXT_GROSS_AREA": "FAC_GROSS_SQUARE_FOOTAGE",
        "ASSIGNABLE_AREA": "FAC_ASSIGNABLE_SQUARE_FOOTAGE",
    }
)

# Building address / square footage table
bldg = tables["table_1"].copy()
bldg["BUILDING_KEY"] = bldg["BUILDING_KEY"].astype(str).str.strip()

def optional_col(df, candidates, default=pd.NA):
    for c in candidates:
        if c in df.columns:
            return df[c]
    return pd.Series(default, index=df.index)

bldg_prepped = pd.DataFrame(
    {
        "BUILDING_KEY": bldg["BUILDING_KEY"],
        "ADDR_BUILDING_NAME": bldg["BUILDING_NAME"],
        "BUILDING_STREET_ADDRESS": bldg["BUILDING_STREET_ADDRESS"],
        "CITY": optional_col(bldg, ["BUILDING_CITY", "CITY", "CITY_NAME"]),
        "STATE": optional_col(bldg, ["BUILDING_STATE", "STATE", "STATE_CODE"]),
        "POSTAL_CODE": optional_col(
            bldg,
            ["BUILDING_POSTAL_CODE", "POSTAL_CODE", "ZIP_CODE", "ZIP", "BUILDING_ZIP_CODE"],
        ),
        "BLDG_GROSS_SQUARE_FOOTAGE": bldg["BLDG_GROSS_SQUARE_FOOTAGE"],
        "BLDG_ASSIGNABLE_SQUARE_FOOTAGE": bldg["BLDG_ASSIGNABLE_SQUARE_FOOTAGE"],
    }
).drop_duplicates("BUILDING_KEY")

# Floor-level aggregates
floors = tables["table_5"].copy()
floors["BUILDING_KEY"] = floors["BUILDING_KEY"].astype(str).str.strip()
floors["LEVEL_ID"] = pd.to_numeric(floors["LEVEL_ID"], errors="coerce")

floor_agg = (
    floors.groupby("BUILDING_KEY", as_index=False)
    .agg(
        MIN_FLOOR_LEVEL=("LEVEL_ID", "min"),
        MAX_FLOOR_LEVEL=("LEVEL_ID", "max"),
    )
)

# Room-area aggregates
rooms = tables["table_10"].copy()
rooms["BUILDING_KEY"] = rooms["BUILDING_KEY"].astype(str).str.strip()
rooms["AREA"] = pd.to_numeric(rooms["AREA"], errors="coerce")

room_agg = (
    rooms.groupby("BUILDING_KEY", as_index=False)
    .agg(TOTAL_ROOM_AREA=("AREA", lambda s: s.sum(min_count=1)))
)

# Build one row per building key appearing in the current building/floor/room/address sources
building_keys = pd.concat(
    [
        fac[["BUILDING_KEY"]],
        bldg_prepped[["BUILDING_KEY"]],
        floor_agg[["BUILDING_KEY"]],
        room_agg[["BUILDING_KEY"]],
    ],
    ignore_index=True,
).drop_duplicates()

out = (
    building_keys.merge(fac, on="BUILDING_KEY", how="left")
    .merge(bldg_prepped, on="BUILDING_KEY", how="left")
    .merge(floor_agg, on="BUILDING_KEY", how="left")
    .merge(room_agg, on="BUILDING_KEY", how="left")
)

out["BUILDING_NAME"] = (
    out["ADDR_BUILDING_NAME"]
    .combine_first(out["FAC_BUILDING_NAME"])
    .combine_first(out["BUILDING_NAME_LONG"])
)

out["GROSS_SQUARE_FOOTAGE"] = out["BLDG_GROSS_SQUARE_FOOTAGE"].combine_first(
    out["FAC_GROSS_SQUARE_FOOTAGE"]
)
out["ASSIGNABLE_SQUARE_FOOTAGE"] = out["BLDG_ASSIGNABLE_SQUARE_FOOTAGE"].combine_first(
    out["FAC_ASSIGNABLE_SQUARE_FOOTAGE"]
)

out["TOTAL_ROOM_AREA"] = out["TOTAL_ROOM_AREA"].fillna(0)

final = out[
    [
        "BUILDING_KEY",
        "BUILDING_NAME",
        "BUILDING_HEIGHT",
        "BUILDING_STREET_ADDRESS",
        "CITY",
        "STATE",
        "POSTAL_CODE",
        "GROSS_SQUARE_FOOTAGE",
        "ASSIGNABLE_SQUARE_FOOTAGE",
        "MIN_FLOOR_LEVEL",
        "MAX_FLOOR_LEVEL",
        "TOTAL_ROOM_AREA",
    ]
].sort_values("BUILDING_KEY", kind="mergesort").reset_index(drop=True)

result = {"building_summary": final}
