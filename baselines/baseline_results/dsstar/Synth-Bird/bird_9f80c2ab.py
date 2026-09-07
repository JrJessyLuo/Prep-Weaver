import pandas as pd

# tables['table_1'] = accounts (bird_9f80c2ab_input_0.pkl)
# tables['table_2'] = crime (bird_9f80c2ab_input_1.pkl)
accounts = tables["table_1"]
crime_raw = tables["table_2"]

# ----------------------------
# Load & prep crime table (district-by-metric)
# ----------------------------
crime = crime_raw.copy().rename(columns={"district_id": "metric_code"})
crime_district_by_metric = crime.set_index("metric_code").T
crime_district_by_metric.index.name = "district_id"

# Locate the metric used for “crimes in 1995” (reuse base-code heuristic)
candidate_metric_codes = ["A16", "A15", "A14", "A13", "A12", "A11", "A10", "A9", "A8", "A7", "A6", "A5", "A4"]
available_metrics = set(crime_district_by_metric.columns)

metric_1995 = None
for m in candidate_metric_codes:
    if m in available_metrics:
        metric_1995 = m
        break

if metric_1995 is None:
    numeric_scores = []
    for m in crime_district_by_metric.columns:
        s = pd.to_numeric(crime_district_by_metric[m], errors="coerce")
        valid = s.notna().sum()
        if valid == 0:
            continue
        med = s.median()
        numeric_scores.append((m, valid, med))
    numeric_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
    metric_1995 = numeric_scores[0][0]

crime_1995 = pd.to_numeric(crime_district_by_metric[metric_1995], errors="coerce")
districts_1995_over_4000 = (
    crime_district_by_metric.loc[crime_1995 > 4000, [metric_1995]]
    .rename(columns={metric_1995: "crimes_1995"})
    .reset_index()
)

# Ensure district_id is numeric for joining with accounts table
districts_1995_over_4000["district_id"] = pd.to_numeric(districts_1995_over_4000["district_id"], errors="coerce")
districts_1995_over_4000 = districts_1995_over_4000.dropna(subset=["district_id"])
districts_1995_over_4000["district_id"] = districts_1995_over_4000["district_id"].astype(int)

# ----------------------------
# Filter accounts to districts with at least one account opened in year >= 1997
# (opening date in either fdm or fdt)
# ----------------------------
fdm_dt = pd.to_datetime(accounts["fdm"], errors="coerce")
fdt_dt = pd.to_datetime(accounts["fdt"], errors="coerce")

opened_ge_1997 = (fdm_dt.dt.year >= 1997) | (fdt_dt.dt.year >= 1997)
districts_with_open_ge_1997 = set(accounts.loc[opened_ge_1997, "district_id"].dropna().astype(int).unique())

# ----------------------------
# Intersect with "crimes_1995 > 4000" districts & compute mean crimes_1995
# ----------------------------
intersected = districts_1995_over_4000[
    districts_1995_over_4000["district_id"].isin(districts_with_open_ge_1997)
].copy()

mean_crimes_1995 = intersected["crimes_1995"].mean()

answer_df = pd.DataFrame(
    {"average_crimes_1995": [mean_crimes_1995]}
)

result = {"average_crimes_1995": answer_df}