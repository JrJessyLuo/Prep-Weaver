import pandas as pd
import numpy as np

rooms = tables["table_10"].copy()
major_uses = tables["table_2"].copy()

room_key_col = "fac_room_key"
room_major_key_col = "MAJOR_USE_KEY"
major_key_col = "FCLT_MAJOR_USE_KEY"

rooms["_major_use_key"] = pd.to_numeric(rooms[room_major_key_col], errors="coerce").astype("Int64")
major_uses["_major_use_key"] = pd.to_numeric(major_uses[major_key_col], errors="coerce").astype("Int64")

major_uses = major_uses[["_major_use_key", "MAJOR_USE", "DESCRIPTION", "ASSIGNABLE"]].drop_duplicates(
    subset=["_major_use_key"],
    keep="last"
)

df = rooms.merge(major_uses, on="_major_use_key", how="left")

df["_major_use_code"] = (
    df["MAJOR_USE"]
    .combine_first(df["MAJOR_USE_DESC"])
    .astype("string")
    .str.strip()
)

df["_major_use_description"] = (
    df["DESCRIPTION"]
    .combine_first(df["MAJOR_USE_DESC"])
    .astype("string")
    .str.strip()
)

exclude_zuse = (
    df["_major_use_code"].str.upper().str.startswith("ZUSE.", na=False)
    | df["_major_use_description"].str.upper().str.startswith("ZUSE.", na=False)
)

df = df.loc[~exclude_zuse].copy()

df["_assignable_status"] = np.where(
    pd.to_numeric(df["ASSIGNABLE"], errors="coerce").eq(1),
    "ASSIGNABLE",
    "NON-ASSIGNABLE"
)

df["_area"] = pd.to_numeric(df["AREA"], errors="coerce")

detail = (
    df.groupby(["_assignable_status", "_major_use_description"], dropna=False)
    .agg(
        **{
            "Total Number of Rooms": (room_key_col, "size"),
            "Total Area": ("_area", "sum"),
            "Average Area": ("_area", "mean"),
        }
    )
    .reset_index()
)

status_order = {"ASSIGNABLE": 0, "NON-ASSIGNABLE": 1}
detail["_status_order"] = detail["_assignable_status"].map(status_order)

detail = detail.sort_values(
    ["_status_order", "_major_use_description"],
    ascending=[True, True],
    na_position="last",
    kind="mergesort"
).reset_index(drop=True)

rows = []

for status, group in detail.groupby("_assignable_status", sort=False):
    for _, r in group.iterrows():
        rows.append({
            "_row_type": "detail",
            "_actual_assignable_status": r["_assignable_status"],
            "_actual_major_use_description": "" if pd.isna(r["_major_use_description"]) else str(r["_major_use_description"]),
            "Total Number of Rooms": r["Total Number of Rooms"],
            "Total Area": r["Total Area"],
            "Average Area": r["Average Area"],
        })
    
    status_df = df[df["_assignable_status"].eq(status)]
    rows.append({
        "_row_type": "subtotal",
        "_actual_assignable_status": "",
        "_actual_major_use_description": "",
        "Total Number of Rooms": len(status_df),
        "Total Area": status_df["_area"].sum(),
        "Average Area": status_df["_area"].mean(),
    })

rows.append({
    "_row_type": "grand_total",
    "_actual_assignable_status": "",
    "_actual_major_use_description": "",
    "Total Number of Rooms": len(df),
    "Total Area": df["_area"].sum(),
    "Average Area": df["_area"].mean(),
})

out = pd.DataFrame(rows)

is_detail = out["_row_type"].eq("detail")

out["Assignable Status"] = np.where(is_detail, out["_actual_assignable_status"], "")
out["Major Use Description"] = np.where(is_detail, out["_actual_major_use_description"], "")

prev_status = out["_actual_assignable_status"].shift()
prev_desc = out["_actual_major_use_description"].shift()

out.loc[is_detail & out["_actual_assignable_status"].eq(prev_status), "Assignable Status"] = ""
out.loc[is_detail & out["_actual_major_use_description"].eq(prev_desc), "Major Use Description"] = ""

final = out[
    [
        "Assignable Status",
        "Major Use Description",
        "Total Number of Rooms",
        "Total Area",
        "Average Area",
    ]
].reset_index(drop=True)

result = {
    "rooms_by_assignable_status_and_major_use": final
}
