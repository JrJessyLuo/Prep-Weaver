import pandas as pd
import numpy as np

org = tables["table_1"].copy()
rooms = tables["table_10"].copy()

# Aggregate room statistics by organization
rooms["_organization_key_join"] = pd.to_numeric(rooms["ORGANIZATION_KEY"], errors="coerce")
room_stats = (
    rooms.dropna(subset=["_organization_key_join"])
    .groupby("_organization_key_join", as_index=False)
    .agg(
        total_area=("AREA", "sum"),
        number_of_rooms=("fac_room_key", "count"),
        average_room_area=("AREA", "mean"),
    )
)

# Join organizations to room statistics
org["_organization_key_join"] = pd.to_numeric(org["organization_key"], errors="coerce")
df = org.merge(room_stats, on="_organization_key_join", how="left")

# Exclude Cambridge-MIT Institute
text_cols = [
    c for c in ["ORGANIZATION", "ORGANIZATION_NAME", "DESCRIPTION", "HR_DEPARTMENT_NAME"]
    if c in df.columns
]
combined_text = df[text_cols].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
normalized_text = combined_text.str.replace(r"[^a-z0-9]+", "", regex=True)

exclude_cmi = (
    normalized_text.str.contains(r"cambridgemitinstitute|cambridgemitinst", regex=True, na=False)
    | df.get("ORGANIZATION", pd.Series("", index=df.index)).fillna("").astype(str).str.upper().eq("CMI")
)
df = df.loc[~exclude_cmi].copy()

# Fill missing room stats
df["total_area"] = df["total_area"].fillna(0)
df["number_of_rooms"] = df["number_of_rooms"].fillna(0)

# Formatted organization name by level
levels = pd.to_numeric(df["ORGANIZATION_LEVEL"], errors="coerce").fillna(1).astype(int)
df["formatted_name"] = [
    " " * max(level - 1, 0) + str(name)
    for level, name in zip(levels, df["ORGANIZATION_NAME"])
]

# Assignable label
df["assignable_status"] = np.where(
    pd.to_numeric(df["ASSIGNABLE"], errors="coerce").fillna(0).astype(int).eq(1),
    "ASSIGNABLE",
    "NON-ASSIGNABLE",
)

def fmt_int(x):
    if pd.isna(x):
        return ""
    return f"{int(round(float(x))):,}"

df["total_area"] = df["total_area"].map(fmt_int)
df["number_of_rooms"] = df["number_of_rooms"].map(fmt_int)
df["average_room_area"] = df["average_room_area"].map(fmt_int)

out = pd.DataFrame({
    "organization_id": pd.to_numeric(df["ORGANIZATION_ID"], errors="coerce").astype("Int64"),
    "organization_number": pd.to_numeric(df["ORGANIZATION_NUMBER"], errors="coerce").round().astype("Int64"),
    "organization_level": pd.to_numeric(df["ORGANIZATION_LEVEL"], errors="coerce").astype("Int64"),
    "formatted_name": df["formatted_name"],
    "assignable": df["assignable_status"],
    "total_area": df["total_area"],
    "number_of_rooms": df["number_of_rooms"],
    "average_room_area": df["average_room_area"],
})

if "ORGANIZATION_SORT" in df.columns:
    out = out.loc[df.sort_values("ORGANIZATION_SORT").index.intersection(out.index)]
    out = out.reset_index(drop=True)
else:
    out = out.sort_values(
        ["organization_level", "organization_number", "organization_id"],
        na_position="last"
    ).reset_index(drop=True)

result = {"organization_room_summary": out}
