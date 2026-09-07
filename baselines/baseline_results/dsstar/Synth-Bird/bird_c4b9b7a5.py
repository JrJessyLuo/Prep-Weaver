import pandas as pd

# Tables are preloaded in the environment as `tables`
events = tables["table_1"]    # bird_c4b9b7a5_input_0.pkl
budgets = tables["table_2"]   # bird_c4b9b7a5_input_1.pkl
expenses = tables["table_4"]  # student_club_expense.pkl

# --- 1) Identify the "September Meeting" event_id from events table ---
needle = "september meeting"
text_cols = [c for c in events.columns if events[c].dtype == "object" and c != "event_id"]

matches = []
for c in text_cols:
    s = events[c].astype(str)
    m = s.str.contains(needle, case=False, na=False)
    if m.any():
        tmp = events.loc[m, ["event_id", c]].copy()
        tmp.rename(columns={c: "matched_value"}, inplace=True)
        tmp["matched_column"] = c
        matches.append(tmp)

matches_df = pd.concat(matches, ignore_index=True) if matches else pd.DataFrame(
    columns=["event_id", "matched_value", "matched_column"]
)

if matches_df.empty:
    raise ValueError("Could not locate 'September Meeting' in any events column.")

sep_meeting_event_id = matches_df.sort_values(["event_id", "matched_column"]).iloc[0]["event_id"]

# --- 2) Join expenses to budgets, filter to approved Food expenses in September 2019 ---
exp_budget = expenses.merge(
    budgets,
    left_on="link_to_budget",
    right_on="budget_id",
    how="left",
    suffixes=("_expense", "_budget"),
)

exp_budget["expense_date"] = pd.to_datetime(exp_budget["expense_date"], errors="coerce")
approved_norm = exp_budget["approved"].astype(str).str.strip().str.lower()
exp_budget["approved_bool"] = approved_norm.isin(["true", "1", "yes", "y", "t"])

start = pd.Timestamp("2019-09-01")
end = pd.Timestamp("2019-10-01")

sep_food_approved = exp_budget[
    (exp_budget["category"] == "Food")
    & (exp_budget["expense_date"] >= start)
    & (exp_budget["expense_date"] < end)
    & (exp_budget["approved_bool"])
].copy()

# --- 3) Filter those expenses to only budgets linked to "September Meeting" via budgets.lte ---
sep_meeting_food_expenses = sep_food_approved[sep_food_approved["lte"] == sep_meeting_event_id].copy()
total_cost_sep_meeting_food = sep_meeting_food_expenses["cost"].sum(skipna=True)

# Final answer table
answer_df = pd.DataFrame(
    {"total_food_spend": [total_cost_sep_meeting_food]},
    index=pd.Index(["September Meeting"], name="event_name"),
)

result = {"answer": answer_df}