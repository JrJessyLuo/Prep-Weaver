import pandas as pd
import json
import ast

# Tables are already loaded in scope as `tables`
budgets = tables["table_1"]   # bird_dac72c04_input_0.pkl
df = tables["table_2"]        # bird_dac72c04_input_1.pkl

# 1) Filter to expenses whose description contains "Posters"
posters = df[df["expense_description"].astype(str).str.contains("Posters", case=False, na=False)]

# 2) Get the corresponding link_to_budget value(s) for those expenses
posters_link_to_budget = (
    posters.loc[posters["attribute"] == "link_to_budget", ["expense_id", "value"]]
    .rename(columns={"value": "link_to_budget"})
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

def parse_rec_json_to_dict(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return {}
    if isinstance(x, dict):
        return x
    s = str(x).strip()
    if not s:
        return {}
    try:
        return json.loads(s)
    except Exception:
        try:
            return ast.literal_eval(s)
        except Exception:
            return {}

# 3) Flatten budget mappings into (budget_id, budget_rec_id, budget_category)
rows = []
for _, r in budgets.iterrows():
    d = parse_rec_json_to_dict(r["rec_json"])
    for rec_id, cat in d.items():
        rows.append({"budget_id": r["budget_id"], "budget_rec_id": rec_id, "budget_category": cat})

budget_map = (
    pd.DataFrame(rows)
    .dropna(subset=["budget_rec_id"])
    .drop_duplicates()
)

# 4) Join posters -> budget_map using link_to_budget
final_df = (
    posters_link_to_budget.merge(
        budget_map,
        left_on="link_to_budget",
        right_on="budget_rec_id",
        how="left",
    )
    .loc[:, ["expense_id", "link_to_budget", "budget_category", "budget_id"]]
    .sort_values(["expense_id"])
    .reset_index(drop=True)
)

# Final answer table(s) only
result = {"posters_budget_category": final_df}

# Print the desired answer (budget category/categories for Posters)
print(final_df[["budget_category"]].dropna().drop_duplicates().to_string(index=False))