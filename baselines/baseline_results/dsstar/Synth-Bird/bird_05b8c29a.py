import pandas as pd

# Tables are already loaded in scope as `tables`
sets_df = tables["table_1"]
translations_df = tables["table_2"]

# Verify in sets_df that the 180-card set in the Ravnica block has code == "DIS"
ravnica_180 = sets_df.loc[
    (sets_df["block"] == "Ravnica") & (sets_df["baseSetSize"] == 180),
    ["id", "name", "code", "block", "baseSetSize"]
].copy()

codes = ravnica_180["code"].dropna().unique().tolist()

# Extract languages for setCode DIS from translations_df
dis_mask = translations_df["language_setCode"].astype(str).str.endswith("|DIS", na=False)
dis_translations = translations_df.loc[dis_mask, ["id", "translation", "language_setCode"]].copy()
dis_translations["language"] = dis_translations["language_setCode"].str.split("|", n=1).str[0]

languages = sorted(dis_translations["language"].dropna().unique().tolist())

# Final answer table
answer_df = pd.DataFrame({"language": languages})

# Required output variable
result = {"languages_for_ravnica_180_set_DIS": answer_df}