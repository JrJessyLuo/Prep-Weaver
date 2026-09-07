import pandas as pd
import numpy as np

terms = tables["table_2"][["term_code", "TERM_DESCRIPTION", "IS_CURRENT_TERM"]].drop_duplicates().copy()
cis_courses = tables["table_5"][["SIS_COURSE_DESCRIPTION_KEY", "FROM_TERM", "THRU_TERM"]].drop_duplicates().copy()

term_order_map = {
    "FA": 0,
    "JA": 1,
    "SP": 2,
    "SU": 3,
}

def term_to_order(s):
    s = s.astype("string").str.strip()
    out = pd.Series(np.nan, index=s.index, dtype="float64")
    
    out[s.eq("000000")] = -1
    out[s.eq("999999")] = 99999999
    
    mask = out.isna() & s.str.match(r"^\d{4}[A-Za-z]{2}$", na=False)
    year = pd.to_numeric(s[mask].str[:4], errors="coerce")
    suffix_order = s[mask].str[4:].str.upper().map(term_order_map).fillna(9)
    out.loc[mask] = year * 10 + suffix_order
    
    return out

terms["term_order"] = term_to_order(terms["term_code"])
cis_courses["from_order"] = term_to_order(cis_courses["FROM_TERM"])
cis_courses["thru_order"] = term_to_order(cis_courses["THRU_TERM"])

active = terms.merge(cis_courses, how="cross")
active = active[
    (active["from_order"] <= active["term_order"]) &
    (active["term_order"] <= active["thru_order"])
]

counts = (
    active.groupby("term_code", as_index=False)["SIS_COURSE_DESCRIPTION_KEY"]
    .nunique()
    .rename(columns={"SIS_COURSE_DESCRIPTION_KEY": "total_number_of_types_of_CIS_courses"})
)

answer = (
    terms.merge(counts, on="term_code", how="left")
    .assign(total_number_of_types_of_CIS_courses=lambda df: df["total_number_of_types_of_CIS_courses"].fillna(0).astype(int))
    .sort_values("term_order")
    [["term_code", "TERM_DESCRIPTION", "IS_CURRENT_TERM", "total_number_of_types_of_CIS_courses"]]
    .reset_index(drop=True)
)

result = {"term_cis_course_type_counts": answer}
