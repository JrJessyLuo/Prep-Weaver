import pandas as pd
import numpy as np

def _parse_oracle_date(s):
    dt = pd.to_datetime(s, format="%d-%b-%y", errors="coerce")
    mask = dt.notna() & (dt.dt.year > 2035)
    dt.loc[mask] = dt.loc[mask] - pd.DateOffset(years=100)
    return dt

# Base: fiscal periods and fiscal quarters by financial aid year + academic year
time_month = tables["table_2"].copy()

time_month["FINANCIAL_AID_YEAR_KEY"] = pd.to_numeric(
    time_month["FINANCIAL_AID_YEAR"], errors="coerce"
).astype("Int64")
time_month["ACADEMIC_YEAR_KEY"] = pd.to_numeric(
    time_month["ACADEMIC_YEAR"], errors="coerce"
).astype("Int64")

tm = time_month.dropna(subset=["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"]).copy()

base = (
    tm.groupby(["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"], as_index=False)
      .agg(
          number_of_fiscal_periods=("fiscal_period", "nunique"),
          number_of_quarters=("FY_QUARTER_CODE", "nunique")
      )
)

# Academic term dates
term_frames = []
for tbl_name in ["table_5", "table_3"]:
    if tbl_name in tables:
        t = tables[tbl_name].copy()
        if "term_code" in t.columns:
            t = t.rename(columns={"term_code": "TERM_CODE"})
        cols = [
            "TERM_CODE",
            "FINANCIAL_AID_YEAR",
            "ACADEMIC_YEAR",
            "TERM_START_DATE",
            "TERM_END_DATE",
        ]
        available_cols = [c for c in cols if c in t.columns]
        term_frames.append(t[available_cols])

terms = pd.concat(term_frames, ignore_index=True).drop_duplicates()

terms["TERM_CODE"] = terms["TERM_CODE"].astype(str).str.strip()
terms["TERM_START_DT"] = _parse_oracle_date(terms["TERM_START_DATE"])
terms["TERM_END_DT"] = _parse_oracle_date(terms["TERM_END_DATE"])
terms["FINANCIAL_AID_YEAR_KEY"] = pd.to_numeric(
    terms.get("FINANCIAL_AID_YEAR"), errors="coerce"
).astype("Int64")
terms["ACADEMIC_YEAR_KEY"] = pd.to_numeric(
    terms.get("ACADEMIC_YEAR"), errors="coerce"
).astype("Int64")

term_date_lookup = (
    terms[["TERM_CODE", "TERM_START_DT", "TERM_END_DT"]]
    .dropna(subset=["TERM_CODE"])
    .sort_values(["TERM_CODE", "TERM_START_DT", "TERM_END_DT"])
    .drop_duplicates(subset=["TERM_CODE"], keep="first")
)

term_col = "ACADEMIC_TERM" if "ACADEMIC_TERM" in tm.columns else "ACADEMIC_TERM_CODE"

term_map = (
    tm[["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY", term_col]]
    .dropna(subset=[term_col])
    .rename(columns={term_col: "TERM_CODE"})
    .copy()
)
term_map["TERM_CODE"] = term_map["TERM_CODE"].astype(str).str.strip()

term_dates = (
    term_map.merge(term_date_lookup, on="TERM_CODE", how="left")
            .groupby(["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"], as_index=False)
            .agg(
                start_term_date=("TERM_START_DT", "min"),
                end_term_date=("TERM_END_DT", "max")
            )
)

# Department-level term parameters: distinct department/term combinations
dept_term_params = pd.DataFrame(
    columns=[
        "FINANCIAL_AID_YEAR_KEY",
        "ACADEMIC_YEAR_KEY",
        "number_of_distinct_department_level_term_parameters",
    ]
)

if "table_9" in tables:
    dept_terms = tables["table_9"].copy()
    dept_terms["TERM_CODE"] = dept_terms["TERM_CODE"].astype(str).str.strip()
    dept_terms["DEPARTMENT_CODE"] = dept_terms["DEPARTMENT_CODE"].astype(str).str.strip()

    lookup_from_time = term_map.drop_duplicates(
        subset=["TERM_CODE", "FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"]
    )

    lookup_from_terms = (
        terms[["TERM_CODE", "FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"]]
        .dropna(subset=["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"])
        .drop_duplicates()
    )

    term_year_lookup = (
        pd.concat([lookup_from_time, lookup_from_terms], ignore_index=True)
        .drop_duplicates(subset=["TERM_CODE", "FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"])
    )

    dept_terms_joined = (
        dept_terms[["TERM_CODE", "DEPARTMENT_CODE"]]
        .dropna(subset=["TERM_CODE", "DEPARTMENT_CODE"])
        .merge(term_year_lookup, on="TERM_CODE", how="left")
        .dropna(subset=["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"])
    )

    dept_terms_joined["department_level_term_parameter"] = (
        dept_terms_joined["DEPARTMENT_CODE"].astype(str)
        + "|"
        + dept_terms_joined["TERM_CODE"].astype(str)
    )

    dept_term_params = (
        dept_terms_joined
        .groupby(["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"], as_index=False)
        .agg(
            number_of_distinct_department_level_term_parameters=(
                "department_level_term_parameter",
                "nunique",
            )
        )
    )

# Final result
out = (
    base.merge(term_dates, on=["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"], how="left")
        .merge(dept_term_params, on=["FINANCIAL_AID_YEAR_KEY", "ACADEMIC_YEAR_KEY"], how="left")
)

out["number_of_distinct_department_level_term_parameters"] = (
    out["number_of_distinct_department_level_term_parameters"].fillna(0).astype(int)
)

out["start_term_date"] = out["start_term_date"].dt.strftime("%Y-%m-%d")
out["end_term_date"] = out["end_term_date"].dt.strftime("%Y-%m-%d")

out = (
    out.rename(
        columns={
            "FINANCIAL_AID_YEAR_KEY": "financial_aid_year",
            "ACADEMIC_YEAR_KEY": "academic_year",
        }
    )
    [
        [
            "financial_aid_year",
            "academic_year",
            "number_of_fiscal_periods",
            "number_of_quarters",
            "start_term_date",
            "end_term_date",
            "number_of_distinct_department_level_term_parameters",
        ]
    ]
    .sort_values(["financial_aid_year", "academic_year"])
    .reset_index(drop=True)
)

result = {"financial_aid_academic_year_summary": out}
