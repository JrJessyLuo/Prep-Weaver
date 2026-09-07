import pandas as pd

# Tables are already loaded in scope as `tables`
cards_df = tables["table_1"]
sets_df = tables["table_2"]

# Verify Coldsnap set code
coldsnap_rows = sets_df[sets_df["name"] == "Coldsnap"]
if coldsnap_rows.empty:
    raise ValueError("No set found with name == 'Coldsnap' in sets table.")
if coldsnap_rows["code"].nunique() != 1:
    raise ValueError(
        f"Expected exactly one unique set code for 'Coldsnap', found: {coldsnap_rows['code'].unique()}"
    )

coldsnap_code = coldsnap_rows["code"].iloc[0]

# Filter cards to Coldsnap
csp_cards_df = cards_df[cards_df["setCode"] == coldsnap_code].copy()

# Compute percentage of cards with convertedManaCost == 7
total_cards_csp = len(csp_cards_df)
count_cmc7 = (csp_cards_df["convertedManaCost"] == 7).sum()
percentage_cmc7 = (count_cmc7 / total_cards_csp * 100) if total_cards_csp else 0.0

# Final answer table
answer_df = pd.DataFrame(
    {"percentage_converted_mana_cost_7": [round(float(percentage_cmc7), 2)]}
)

result = {"answer": answer_df}