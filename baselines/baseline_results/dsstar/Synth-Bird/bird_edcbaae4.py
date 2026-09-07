import re
import pandas as pd

# Input tables are already loaded in `tables`
expenses = tables["table_1"]
members_raw = tables["table_2"]

# --- Normalize the "members" table (it has many duplicate column names) ---
members_wide = members_raw.loc[:, ~members_raw.columns.duplicated()].copy()

id_col = "member_id" if "member_id" in members_wide.columns else members_wide.columns[0]

members_long = (
    members_wide.set_index(id_col)
    .T
    .reset_index()
    .rename(columns={"index": "member_id"})
)

# -----------------------------
# Fuzzy/name-token approach
# -----------------------------
TARGET_FIRST = "sacha"
TARGET_LAST = "harrison"

def _is_missingish(x) -> bool:
    if x is None:
        return True
    s = str(x).strip()
    return s == "" or s.lower() in {"nan", "none", "null"}

def _looks_like_name_value(x) -> bool:
    if _is_missingish(x):
        return False
    s = str(x).strip()
    if len(s) < 2 or len(s) > 60:
        return False
    if any(ch.isdigit() for ch in s):
        return False
    if "@" in s or "http" in s.lower() or s.lower().startswith("rec"):
        return False
    if not re.fullmatch(r"[A-Za-z][A-Za-z'\-\. ]*[A-Za-z\.]?", s):
        return False
    tokens = [t for t in re.split(r"\s+", s) if t]
    if not (1 <= len(tokens) <= 4):
        return False
    if all(len(re.sub(r"[^\w]", "", t)) <= 1 for t in tokens):
        return False
    return True

def _name_score_for_column(series: pd.Series) -> float:
    non_missing = series[~series.apply(_is_missingish)]
    if len(non_missing) == 0:
        return 0.0
    return float(non_missing.apply(_looks_like_name_value).mean())

candidate_cols = [c for c in members_long.columns if c != "member_id"]
col_scores = [(c, _name_score_for_column(members_long[c])) for c in candidate_cols]
scores_df = pd.DataFrame(col_scores, columns=["column", "name_likeness"]).sort_values(
    "name_likeness", ascending=False
)

NAME_LIKENESS_THRESHOLD = 0.25
TOP_K = 12
likely_name_cols = (
    scores_df.loc[scores_df["name_likeness"] >= NAME_LIKENESS_THRESHOLD, "column"]
    .head(TOP_K)
    .tolist()
)

members_text = members_long.copy()
for c in likely_name_cols:
    members_text[c] = members_text[c].astype(str).str.lower()

def _contains_token(series: pd.Series, token: str) -> pd.Series:
    token = re.escape(token.lower())
    return series.str.contains(rf"(?<![a-z]){token}(?![a-z])", regex=True, na=False)

has_first = pd.DataFrame(
    {c: _contains_token(members_text[c], TARGET_FIRST) for c in likely_name_cols}
).any(axis=1)

has_last = pd.DataFrame(
    {c: _contains_token(members_text[c], TARGET_LAST) for c in likely_name_cols}
).any(axis=1)

full_name_match = pd.DataFrame(
    {
        c: (_contains_token(members_text[c], TARGET_FIRST) & _contains_token(members_text[c], TARGET_LAST))
        for c in likely_name_cols
    }
).any(axis=1)

mask = (has_first & has_last) | full_name_match
sacha_rows = members_long.loc[mask].copy()
sacha_member_ids = sacha_rows["member_id"].dropna().unique().tolist()

# --- Filter expenses for Sacha Harrison ---
if "ys" in expenses.columns:
    sacha_expenses = expenses[expenses["ys"].isin(sacha_member_ids)].copy()
else:
    sacha_expenses = expenses.iloc[0:0].copy()

# --- Collect non-null expense item fields and extract "expense kind" (split on '|') ---
key_cols = {"expense_id", "expense_date", "approved", "ys"}
item_cols = [c for c in sacha_expenses.columns if c not in key_cols]

if len(sacha_expenses) == 0 or len(item_cols) == 0:
    expense_kinds_df = pd.DataFrame({"expense_kind": []})
else:
    items_long = (
        sacha_expenses[["expense_id", "expense_date", "ys"] + item_cols]
        .melt(
            id_vars=["expense_id", "expense_date", "ys"],
            value_vars=item_cols,
            var_name="item_field",
            value_name="raw_item",
        )
        .dropna(subset=["raw_item"])
    )

    items_long["expense_kind"] = (
        items_long["raw_item"].astype(str).str.split("|", n=1).str[0].str.strip()
    )

    expense_kinds_df = (
        items_long[["expense_kind"]]
        .dropna()
        .loc[lambda d: d["expense_kind"].astype(str).str.strip().ne("")]
        .drop_duplicates()
        .sort_values("expense_kind")
        .reset_index(drop=True)
    )

# Final answer table
result = {"sacha_harrison_expense_kinds": expense_kinds_df}