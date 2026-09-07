import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['loan_id', 'account_id', 'date', 'status', 'approved_amount', 'duration', 'payments'])
    # SelectCol
    _cols = [c for c in ['loan_id', 'account_id', 'date', 'status', 'approved_amount', 'duration', 'payments'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_loans", func="""
    # import pandas as pd
    # import numpy as np
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Ensure required base columns exist
    #     for c in ["loan_id", "account_id", "date", "status"]:
    #         if c not in df.columns:
    #             df[c] = np.nan
    # 
    #     # Parse if the raw composite field is available; otherwise fill with nulls
    #     if "amount_duration_payments" in df.columns:
    #         def parse_triplet(val):
    #             if pd.isna(val):
    #                 return (np.nan, np.nan, np.nan)
    #             s = str(val).strip()
    #             # expected pattern: amount-duration-payments (payments can be float)
    #             parts = s.split("-")
    #             if len(parts) != 3:
    #                 # try regex fallback
    #                 m = re.match(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*-\s*([0-9]+(?:\.[0-9]+)?)\s*-\s*([0-9]+(?:\.[0-9]+)?)\s*$", s)
    #                 if not m:
    #                     return (np.nan, np.nan, np.nan)
    #                 return (m.group(1), m.group(2), m.group(3))
    #             return (parts[0], parts[1], parts[2])
    # 
    #         parsed = df["amount_duration_payments"].apply(parse_triplet)
    #         df["approved_amount"] = parsed.apply(lambda x: x[0])
    #         df["duration"] = parsed.apply(lambda x: x[1])
    #         df["payments"] = parsed.apply(lambda x: x[2])
    #     else:
    #         df["approved_amount"] = np.nan
    #         df["duration"] = np.nan
    #         df["payments"] = np.nan
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Ensure required base columns exist
        for c in ["loan_id", "account_id", "date", "status"]:
            if c not in df.columns:
                df[c] = np.nan

        # Parse if the raw composite field is available; otherwise fill with nulls
        if "amount_duration_payments" in df.columns:
            def parse_triplet(val):
                if pd.isna(val):
                    return (np.nan, np.nan, np.nan)
                s = str(val).strip()
                # expected pattern: amount-duration-payments (payments can be float)
                parts = s.split("-")
                if len(parts) != 3:
                    # try regex fallback
                    m = re.match(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*-\s*([0-9]+(?:\.[0-9]+)?)\s*-\s*([0-9]+(?:\.[0-9]+)?)\s*$", s)
                    if not m:
                        return (np.nan, np.nan, np.nan)
                    return (m.group(1), m.group(2), m.group(3))
                return (parts[0], parts[1], parts[2])

            parsed = df["amount_duration_payments"].apply(parse_triplet)
            df["approved_amount"] = parsed.apply(lambda x: x[0])
            df["duration"] = parsed.apply(lambda x: x[1])
            df["payments"] = parsed.apply(lambda x: x[2])
        else:
            df["approved_amount"] = np.nan
            df["duration"] = np.nan
            df["payments"] = np.nan

        return df
    prepared_loans = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="prepared_loans", column_name="date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    prepared_loans['date'] = prepared_loans['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        prepared_loans['date'] = prepared_loans['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="prepared_loans", column="approved_amount", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_loans['approved_amount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_loans['approved_amount']
    if _dtype == "datetime64":
        prepared_loans['approved_amount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_loans['approved_amount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_loans['approved_amount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_loans['approved_amount'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="prepared_loans", column="duration", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_loans['duration'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_loans['duration']
    if _dtype == "datetime64":
        prepared_loans['duration'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_loans['duration'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_loans['duration'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_loans['duration'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="prepared_loans", column="payments", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_loans['payments'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_loans['payments']
    if _dtype == "datetime64":
        prepared_loans['payments'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_loans['payments'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_loans['payments'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_loans['payments'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="prepared_loans", columns=['loan_id', 'account_id', 'date', 'status', 'approved_amount', 'duration', 'payments'])
    # SelectCol
    _cols = [c for c in ['loan_id', 'account_id', 'date', 'status', 'approved_amount', 'duration', 'payments'] if c in prepared_loans.columns]
    prepared_loans = prepared_loans[_cols]

    # ---------------- Step 8 ----------------
    # Original operator:
    # Terminate(result=['prepared_loans'])
    # Terminate
    result = {'prepared_loans': prepared_loans}
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
    # StandardizeString(table_name="table_1", column_name="freq_part2", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["freq_part2"] = table_1["freq_part2"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="freq_part1", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["freq_part1"] = table_1["freq_part1"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['freq_part1', 'freq_part2'], target_column="issuance_frequency", func="""
    # def concat(row: pd.Series) -> str:
    #     p1 = "" if row.get("freq_part1") is None or (isinstance(row.get("freq_part1"), float) and pd.isna(row.get("freq_part1"))) else str(row.get("freq_part1")).strip()
    #     p2 = "" if row.get("freq_part2") is None or (isinstance(row.get("freq_part2"), float) and pd.isna(row.get("freq_part2"))) else str(row.get("freq_part2")).strip()
    #     return " ".join([x for x in [p1, p2] if x])
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        p1 = "" if row.get("freq_part1") is None or (isinstance(row.get("freq_part1"), float) and pd.isna(row.get("freq_part1"))) else str(row.get("freq_part1")).strip()
        p2 = "" if row.get("freq_part2") is None or (isinstance(row.get("freq_part2"), float) and pd.isna(row.get("freq_part2"))) else str(row.get("freq_part2")).strip()
        return " ".join([x for x in [p1, p2] if x])
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["issuance_frequency"] = table_1[['freq_part1', 'freq_part2']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['freq_part1', 'freq_part2'])

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['freq_part1', 'freq_part2'])
    # DropColumn
    table_1 = table_1.drop(columns=['freq_part1', 'freq_part2'], errors='ignore')

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['account_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['account_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'district_id', 'date', 'issuance_frequency'])
    # SelectCol
    _cols = [c for c in ['account_id', 'district_id', 'date', 'issuance_frequency'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_loans = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_accounts = prepared_table_2

# Assume prepared_loans and prepared_accounts are available per targets above.

# Filter approved loans in 1997
loans_1997 = prepared_loans.copy()
loans_1997['year'] = pd.to_datetime(loans_1997['date']).dt.year
loans_1997 = loans_1997[(loans_1997['year'] == 1997) & (loans_1997['status'].str.upper() == 'A')]

# Find the minimum approved amount among these
if loans_1997.empty:
    target = pd.DataFrame(columns=['account_id','loan_id','approved_amount','issuance_frequency'])
else:
    min_amt = loans_1997['approved_amount'].min()
    lowest_loans = loans_1997[loans_1997['approved_amount'] == min_amt]

    # Join to accounts to get issuance frequency
    joined = lowest_loans.merge(prepared_accounts[['account_id','issuance_frequency']], on='account_id', how='left')

    # Choose weekly issuance statement rows (keep accounts whose issuance_frequency indicates weekly)
    # Assume weekly indicated by token like 'TYDNE' (Czech for weekly) or 'WEEKLY'
    weekly_mask = joined['issuance_frequency'].fillna('').str.contains(r'(?i)tydn|week', regex=True)
    target = joined.loc[weekly_mask, ['account_id','loan_id','approved_amount','issuance_frequency']].drop_duplicates()

# target is the final answer table

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
