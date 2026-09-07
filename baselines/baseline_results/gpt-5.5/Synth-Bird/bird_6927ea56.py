import pandas as pd

cards = tables["table_1"]
sets = tables["table_2"]

# Get Coldsnap set code (fallback to known code "CSP" if not found)
coldsnap_codes = sets.loc[sets["name"].eq("Coldsnap"), "code"].dropna().unique().tolist()
set_code = coldsnap_codes[0] if coldsnap_codes else "CSP"

csp_cards = cards.loc[cards["setCode"].eq(set_code)].copy()

total_cards = csp_cards["uuid"].nunique(dropna=True)
cmc7_cards = csp_cards.loc[csp_cards["convertedManaCost"].eq(7), "uuid"].nunique(dropna=True)

percentage = (cmc7_cards / total_cards * 100) if total_cards else 0.0

result = {
    "cmc7_percentage_coldsnap": pd.DataFrame(
        {"set": ["Coldsnap"], "setCode": [set_code], "percentage_cmc7": [percentage]}
    )
}
