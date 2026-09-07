import pandas as pd
import json

# Pivot expenses key-value table to wide
exp = tables["table_2"].pivot_table(
    index=["expense_id", "expense_description", "expense_date"],
    columns="attribute",
    values="value",
    aggfunc="first",
).reset_index()

# Find the expense containing 'Posters' in the description
posters_exp = exp[exp["expense_description"].astype(str).str.contains(r"\bPosters\b", case=False, na=False)].copy()

# Get linked budget record id(s)
budget_keys = posters_exp["link_to_budget"].dropna().astype(str).unique()

# Load budget category mapping from table_1
cat_row = tables["table_1"].loc[tables["table_1"]["budget_id"].eq("category"), "rec_json"].iloc[0]
cat_map = json.loads(cat_row)

# Map budget key(s) to category
out = pd.DataFrame(
    {"budget_category": [cat_map.get(budget_keys[0])] if len(budget_keys) else [None]}
)

result = {"posters_budget_category": out}
