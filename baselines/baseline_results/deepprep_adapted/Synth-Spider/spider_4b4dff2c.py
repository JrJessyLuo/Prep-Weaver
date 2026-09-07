import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="affiliation_id", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     v = str(val).strip().strip('"')
    #     return v.isdigit()
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        v = str(val).strip().strip('"')
        return v.isdigit()
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['affiliation_id'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="affiliation_id", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     # remove surrounding quotes (handles patterns like ""0"")
    #     v = v.strip('"').strip("'").strip()
    #     # if still wrapped due to doubled quotes, strip again
    #     v = v.strip('"').strip("'").strip()
    #     return v
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        v = str(s).strip()
        # remove surrounding quotes (handles patterns like ""0"")
        v = v.strip('"').strip("'").strip()
        # if still wrapped due to doubled quotes, strip again
        v = v.strip('"').strip("'").strip()
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["affiliation_id"] = table_1["affiliation_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="affiliation_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['affiliation_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['affiliation_id']
    if _dtype == "datetime64":
        table_1['affiliation_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['affiliation_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['affiliation_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['affiliation_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['affiliation_id', 'name'])
    # SelectCol
    _cols = [c for c in ['affiliation_id', 'name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
affiliations_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
author_papers_prepared = prepared_table_2

# Compose paper_id for counting per paper
app = author_papers_prepared.copy()
# ensure types are strings and handle possible NaNs
app['paper_prefix'] = app['paper_prefix'].astype(str)
app['paper_suffix'] = app['paper_suffix'].astype(str)
app['paper_id'] = app['paper_prefix'] + '-' + app['paper_suffix']

# Join with affiliations to get names
merged = app.merge(affiliations_prepared, on='affiliation_id', how='inner')

# Filter for Stanford University affiliation name (case-insensitive exact match)
stanford = merged[merged['name'].str.strip().str.lower() == 'stanford university']

# Derive year from paper_prefix if it encodes year (e.g., 'D15' -> 2015, 'P03' -> 2003)
# Heuristic: take trailing 2 digits of prefix as year within 1900-2099 by mapping 00-24 -> 2000-2024, else 1900s/2010s may vary. For 2000-2009, match 00-09.
pp = stanford['paper_prefix'].str.extract(r'([A-Za-z])(\d{2})')
stanford_years = stanford.copy()
stanford_years['yy'] = pd.to_numeric(pp[1], errors='coerce')
# Map yy 00-09 to 2000-2009
stanford_years['year'] = stanford_years['yy'].where(stanford_years['yy'].between(0,9), pd.NA)
stanford_years['year'] = stanford_years['year'].apply(lambda v: 2000+int(v) if pd.notna(v) else pd.NA)

# Keep only rows with years in 2000-2009
stanford_2000s = stanford_years[stanford_years['year'].between(2000, 2009, inclusive='both')]

# Count distinct papers
result = pd.DataFrame({ 'answer': [stanford_2000s['paper_id'].nunique()] })

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
