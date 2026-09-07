import pandas as pd
import numpy as np

# Tables already provided in-scope
cards = tables["table_1"]  # bird_9c86aa16_input_0.pkl
legal = tables["table_2"]  # bird_9c86aa16_input_1.pkl

# Join on id (NOT uuid)
merged = cards[["id", "uuid", "name", "hasContentWarning"]].merge(
    legal[["id", "uuid", "fmt", "sts"]],
    on="id",
    how="inner",
    suffixes=("_card", "_legal")
)

# Filter to Commander + Legal (exact match)
cmd_legal = merged[(merged["fmt"] == "commander") & (merged["sts"] == "Legal")].copy()

# Compute % where hasContentWarning == 0 OR is null
hcw = cmd_legal["hasContentWarning"]
hcw_num = pd.to_numeric(hcw, errors="coerce")
is_ok = hcw.isna() | (hcw_num == 0)

den = len(cmd_legal)
num = int(is_ok.sum())
pct = (num / den * 100) if den else np.nan

answer_df = pd.DataFrame(
    [{"percentage_no_content_warning": pct}]
)

result = {"answer": answer_df}