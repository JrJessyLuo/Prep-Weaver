import pandas as pd
import re

# Tables already loaded in scope as `tables`
df_events = tables["table_1"]        # events
df_budget_wide = tables["table_2"]   # student_club_budget (wide)
df_expense = tables["table_4"]       # student_club_expense

# ----------------------------
# Identify advertisement-related expenses
# ----------------------------
ad_pattern = re.compile(
    r"\b(ad|advert|advertis|poster|posters|post\s*card|post\s*cards|flyer|flyers|banner|banners|print|printing|brochure|brochures)\b",
    re.IGNORECASE,
)

df_expense = df_expense.copy()
df_expense["is_ad_related"] = df_expense["expense_description"].fillna("").apply(
    lambda s: bool(ad_pattern.search(s))
)
df_ad_expenses = df_expense[df_expense["is_ad_related"]].copy()

# ----------------------------
# Unpivot budget from wide to long (kept for parity with reference logic)
# ----------------------------
id_col = "budget_id"
event_cols = [c for c in df_budget_wide.columns if c != id_col]

df_budget_long = df_budget_wide.melt(
    id_vars=[id_col],
    value_vars=event_cols,
    var_name="event_id",
    value_name="amount",
)
df_budget_long["amount"] = pd.to_numeric(df_budget_long["amount"], errors="coerce")
df_budget_long = df_budget_long.dropna(subset=["amount"]).copy()

# ----------------------------
# Choose join strategy as in reference code
# ----------------------------
ad_budget_vals = (
    df_ad_expenses["link_to_budget"].dropna().astype(str).unique().tolist()
)
budget_id_set = set(df_budget_wide["budget_id"].dropna().astype(str).unique())
ad_budget_not_in_budget_id = [v for v in ad_budget_vals if v not in budget_id_set]

def compute_ad_cost_by_event_via_budgetid():
    df_ad_with_event = df_ad_expenses.merge(
        df_budget_long[["budget_id", "event_id"]],
        left_on="link_to_budget",
        right_on="budget_id",
        how="inner",
    )
    ad_cost_by_event = (
        df_ad_with_event.groupby("event_id", as_index=False)["cost"]
        .sum()
        .rename(columns={"cost": "total_ad_cost"})
        .sort_values("total_ad_cost", ascending=False)
    )
    return ad_cost_by_event

def compute_ad_cost_by_event_via_eventcol():
    budget_event_cols_set = set(event_cols)
    df_ad2 = df_ad_expenses.copy()
    df_ad2["event_id"] = df_ad2["link_to_budget"].astype(str)
    df_ad2 = df_ad2[df_ad2["event_id"].isin(budget_event_cols_set)].copy()
    ad_cost_by_event = (
        df_ad2.groupby("event_id", as_index=False)["cost"]
        .sum()
        .rename(columns={"cost": "total_ad_cost"})
        .sort_values("total_ad_cost", ascending=False)
    )
    return ad_cost_by_event

use_budget_id_join = (len(ad_budget_vals) > 0) and (len(ad_budget_not_in_budget_id) == 0)
ad_cost_by_event = (
    compute_ad_cost_by_event_via_budgetid()
    if use_budget_id_join
    else compute_ad_cost_by_event_via_eventcol()
)

# ----------------------------
# Final answer: event with highest advertisement spend
# ----------------------------
if ad_cost_by_event.empty:
    answer_df = pd.DataFrame(columns=["event_name"])
else:
    top_row = ad_cost_by_event.head(1)
    answer_df = (
        top_row.merge(df_events[["event_id", "event_name"]], on="event_id", how="left")[
            ["event_name"]
        ]
    )

result = {"event_with_highest_ad_spend": answer_df}