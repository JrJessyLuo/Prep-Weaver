import pandas as pd
import re

# Source table (already loaded in `tables`)
df1 = tables["table_2"].copy()

# Match reference logic: look for hometown/home_state attributes (none exist in the data)
attrs_of_interest = {"hometown", "home_state"}
df1["attribute_norm"] = df1["attribute"].astype(str).str.strip().str.lower()
subset = df1[df1["attribute_norm"].isin(attrs_of_interest)].copy()

pattern = re.compile(r"\b(maryland|md)\b", flags=re.IGNORECASE)
subset["value_str"] = subset["value"].astype(str)
subset["is_md"] = subset["value_str"].apply(lambda x: bool(pattern.search(x)) if pd.notna(x) else False)

md_rows = subset[subset["is_md"]].copy()
md_member_count = md_rows["member_id"].nunique()

answer_df = pd.DataFrame({"members_from_maryland_hometowns": [md_member_count]})

result = {"answer": answer_df}