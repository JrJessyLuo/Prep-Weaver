import pandas as pd

# Source tables from the provided `tables` dict
tm = tables['table_2']  # TIME_MONTH.pkl
terms = tables['table_5']  # ACADEMIC_TERMS.pkl
term_param = tables['table_4']  # ACADEMIC_TERM_PARAMETER.pkl

# Ensure relevant columns exist (TIME_MONTH)
required_tm_cols = [
    "FINANCIAL_AID_YEAR", "ACADEMIC_YEAR", "fiscal_period", "FY_QUARTER_CODE"
]

# Prepare TIME_MONTH subset and drop rows lacking key years
tm_use = tm[[c for c in required_tm_cols if c in tm.columns]].copy()
tm_use = tm_use.dropna(subset=["FINANCIAL_AID_YEAR", "ACADEMIC_YEAR"])

# Aggregate TIME_MONTH per (FINANCIAL_AID_YEAR, ACADEMIC_YEAR)
tm_agg = (
    tm_use.groupby(["FINANCIAL_AID_YEAR", "ACADEMIC_YEAR"], as_index=False)
    .agg(
        n_fiscal_periods=("fiscal_period", lambda s: s.dropna().nunique()),
        n_quarters=("FY_QUARTER_CODE", lambda s: s.dropna().nunique())
    )
)

# Parse dates in terms and term_param (coerce to datetime)
def parse_dates(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

terms = parse_dates(terms.copy(), ["TERM_START_DATE", "TERM_END_DATE"])
term_param = parse_dates(term_param.copy(), ["TERM_START_DATE", "TERM_END_DATE"])

# Terms: aggregate start/end date per academic year
terms_use = terms.copy()
terms_use = terms_use[[c for c in ["term_code", "ACADEMIC_YEAR", "TERM_START_DATE", "TERM_END_DATE"] if c in terms_use.columns]]
terms_use = terms_use.dropna(subset=["ACADEMIC_YEAR"])
terms_agg = (
    terms_use.groupby("ACADEMIC_YEAR", as_index=False)
    .agg(
        start_term_date=("TERM_START_DATE", lambda s: s.dropna().min() if s.notna().any() else pd.NaT),
        end_term_date=("TERM_END_DATE", lambda s: s.dropna().max() if s.notna().any() else pd.NaT)
    )
)

# Term parameters: compute distinct TERM_PARAMETER per academic year
param_use = term_param.copy()
# Join term_param to terms to get ACADEMIC_YEAR by term_code
if "term_code" in param_use.columns and "term_code" in terms.columns:
    param_use = param_use.merge(
        terms[["term_code", "ACADEMIC_YEAR"]],
        how="left",
        on="term_code",
        suffixes=("", "_from_terms")
    )
# Count distinct TERM_PARAMETER per ACADEMIC_YEAR
group_cols = []
if "ACADEMIC_YEAR" in param_use.columns:
    group_cols.append("ACADEMIC_YEAR")
if "TERM_PARAMETER" in param_use.columns and group_cols:
    param_agg = (
        param_use.dropna(subset=["ACADEMIC_YEAR"])
        .groupby("ACADEMIC_YEAR", as_index=False)
        .agg(n_distinct_dept_term_params=("TERM_PARAMETER", lambda s: s.dropna().nunique()))
    )
else:
    # Create empty frame to merge safely
    param_agg = pd.DataFrame(columns=["ACADEMIC_YEAR", "n_distinct_dept_term_params"])

# Combine all pieces: base on (FINANCIAL_AID_YEAR, ACADEMIC_YEAR)
out = tm_agg.merge(terms_agg, how="left", on="ACADEMIC_YEAR") \
            .merge(param_agg, how="left", on="ACADEMIC_YEAR")

# Sort for readability
out = out.sort_values(["FINANCIAL_AID_YEAR", "ACADEMIC_YEAR"]).reset_index(drop=True)

# Assign final result
result = {"financial_academic_year_summary": out}