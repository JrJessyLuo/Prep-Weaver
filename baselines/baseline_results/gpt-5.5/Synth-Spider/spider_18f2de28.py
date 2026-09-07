import pandas as pd

t1 = tables["table_1"]
cities = tables["table_2"]

# Pivot EAV -> wide student table
students = (
    t1.pivot_table(index="StuID", columns="Attribute", values="Value", aggfunc="first")
      .reset_index()
)

# Normalize column names for robust selection
students.columns = [str(c) for c in students.columns]
colmap = {c: c.strip().lower().replace(" ", "_") for c in students.columns}
students_ren = students.rename(columns=colmap)

# Identify first-name, major, and city columns
fname_col = next((c for c in students_ren.columns if c in {"fname", "first_name", "firstname"}), None)
major_col = next((c for c in students_ren.columns if c in {"major", "major_name", "majorcode", "major_code"}), None)
city_col = next((c for c in students_ren.columns if c in {"city", "city_code", "home_city", "hometown"} or "city" in c), None)

# Filter students living in Baltimore (match either city name or city code)
if city_col is None:
    baltimore_students = students_ren.iloc[0:0].copy()
else:
    city_series = students_ren[city_col].astype(str).str.strip()
    # Direct name match
    mask_name = city_series.str.lower().eq("baltimore")
    # Code match via city table (e.g., BAL)
    balt_codes = set(
        cities.loc[cities["city_name"].astype(str).str.strip().str.lower().eq("baltimore"), "city_code"]
        .astype(str).str.strip()
    )
    mask_code = city_series.isin(balt_codes) if balt_codes else False
    baltimore_students = students_ren[mask_name | mask_code].copy()

# Build final output
out_cols = []
if fname_col is not None:
    out_cols.append(fname_col)
if major_col is not None:
    out_cols.append(major_col)

result_df = baltimore_students[out_cols].rename(
    columns={fname_col: "first_name", major_col: "major"}
).drop_duplicates().reset_index(drop=True)

result = {"students_in_baltimore": result_df}
