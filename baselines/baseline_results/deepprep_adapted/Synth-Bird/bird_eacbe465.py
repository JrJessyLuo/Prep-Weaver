import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="full_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return ' '.join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return ' '.join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["full_name"] = table_1["full_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="phone", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.lower() in {"nan", "none", "null"}:
    #         return None
    #     # keep digits only
    #     digits = re.sub(r"\D+", "", s)
    #     # if we have 10 digits, format as XXX-XXX-XXXX; otherwise keep digits as-is
    #     if len(digits) == 10:
    #         return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
    #     return digits if digits else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() in {"nan", "none", "null"}:
            return None
        # keep digits only
        digits = re.sub(r"\D+", "", s)
        # if we have 10 digits, format as XXX-XXX-XXXX; otherwise keep digits as-is
        if len(digits) == 10:
            return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
        return digits if digits else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["phone"] = table_1["phone"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'phone', 'full_name'])
    # SelectCol
    _cols = [c for c in ['member_id', 'phone', 'full_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['member_id', 'phone'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['member_id', 'phone'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['member_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['member_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
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
    # DropNulls(table_name="table_1", subset=['link_to_member'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['link_to_member'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_attendance_matrix", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # If the raw extract contains duplicate column names, keep the first occurrence
    #     df = df.loc[:, ~df.columns.duplicated(keep='first')]
    # 
    #     required_cols = [
    #         "link_to_member",
    #         "recD078PnS3x2doBe",
    #         "recP6DJPyi5donvXL",
    #         "rec28ORZgcm1dtqBZ",
    #         "recTjHY5xXhvkCdVT",
    #         "recZ4PkGERzl9ziHO",
    #         "recEFd8s6pkrTt4Pz",
    #         "recEymrwCUKxiiosI",
    #         "recQaxyXBQG5BBtD0",
    #         "recT92PyyZCGq1R68",
    #         "recJMazpPVexyFYTc",
    #         "reccW7q1KkhSKZsea",
    #         "recjHj4BS5A541n9v",
    #         "recL94zpn6Xh6kQii",
    #         "reccSUPwy30AeZLEb",
    #         "recttfySfQnYb68u3",
    #         "recf4UKTfipCzgcSA",
    #         "recro8T1MPMwRadVH",
    #         "recsTO4OZIF9rbubk",
    #         "rec75vvFxgYtHmqxY",
    #         "reco0mr8dXTgs5wWA",
    #         "recuSfhAZIlKba4s2",
    #         "recxBj3tjKTGHqucS",
    #         "recUdRhbhcEO1Hk5r",
    #         "recVsoJJHFI8bgtfw",
    #         "rec4BLdZHS2Blfp4v",
    #     ]
    # 
    #     # Select only columns that actually exist (defensive), but preserve target ordering
    #     existing = [c for c in required_cols if c in df.columns]
    #     out = df[existing].copy()
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # If the raw extract contains duplicate column names, keep the first occurrence
        df = df.loc[:, ~df.columns.duplicated(keep='first')]

        required_cols = [
            "link_to_member",
            "recD078PnS3x2doBe",
            "recP6DJPyi5donvXL",
            "rec28ORZgcm1dtqBZ",
            "recTjHY5xXhvkCdVT",
            "recZ4PkGERzl9ziHO",
            "recEFd8s6pkrTt4Pz",
            "recEymrwCUKxiiosI",
            "recQaxyXBQG5BBtD0",
            "recT92PyyZCGq1R68",
            "recJMazpPVexyFYTc",
            "reccW7q1KkhSKZsea",
            "recjHj4BS5A541n9v",
            "recL94zpn6Xh6kQii",
            "reccSUPwy30AeZLEb",
            "recttfySfQnYb68u3",
            "recf4UKTfipCzgcSA",
            "recro8T1MPMwRadVH",
            "recsTO4OZIF9rbubk",
            "rec75vvFxgYtHmqxY",
            "reco0mr8dXTgs5wWA",
            "recuSfhAZIlKba4s2",
            "recxBj3tjKTGHqucS",
            "recUdRhbhcEO1Hk5r",
            "recVsoJJHFI8bgtfw",
            "rec4BLdZHS2Blfp4v",
        ]

        # Select only columns that actually exist (defensive), but preserve target ordering
        existing = [c for c in required_cols if c in df.columns]
        out = df[existing].copy()

        return out
    prepared_attendance_matrix = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="prepared_attendance_matrix", columns=['link_to_member', 'recD078PnS3x2doBe', 'recP6DJPyi5donvXL', 'rec28ORZgcm1dtqBZ', 'recTjHY5xXhvkCdVT', 'recZ4PkGERzl9ziHO', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recJMazpPVexyFYTc', 'reccW7q1KkhSKZsea', 'recjHj4BS5A541n9v', 'recL94zpn6Xh6kQii', 'reccSUPwy30AeZLEb', 'recttfySfQnYb68u3', 'recf4UKTfipCzgcSA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'rec75vvFxgYtHmqxY', 'reco0mr8dXTgs5wWA', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'rec4BLdZHS2Blfp4v'])
    # SelectCol
    _cols = [c for c in ['link_to_member', 'recD078PnS3x2doBe', 'recP6DJPyi5donvXL', 'rec28ORZgcm1dtqBZ', 'recTjHY5xXhvkCdVT', 'recZ4PkGERzl9ziHO', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recJMazpPVexyFYTc', 'reccW7q1KkhSKZsea', 'recjHj4BS5A541n9v', 'recL94zpn6Xh6kQii', 'reccSUPwy30AeZLEb', 'recttfySfQnYb68u3', 'recf4UKTfipCzgcSA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'rec75vvFxgYtHmqxY', 'reco0mr8dXTgs5wWA', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'rec4BLdZHS2Blfp4v'] if c in prepared_attendance_matrix.columns]
    prepared_attendance_matrix = prepared_attendance_matrix[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['prepared_attendance_matrix'])
    # Terminate
    result = {'prepared_attendance_matrix': prepared_attendance_matrix}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_attendance_wide = prepared_table_2

# 1) Identify the member_id for the given phone
m = prepared_members.copy()
# Normalize phone formatting for robust match
normalize = lambda s: ''.join([c for c in str(s) if c.isdigit()])
phone_norm = normalize('954-555-6240')
m['phone_norm'] = m['phone'].apply(normalize)
member_row = m.loc[m['phone_norm'] == phone_norm]
if member_row.empty:
    result = pd.DataFrame({'answer': [0]})
else:
    member_id = member_row.iloc[0]['member_id']
    # 2) Extract the two event id parts for this member from the wide attendance table
    a = prepared_attendance_wide.copy()
    col_name = member_id  # attendance columns are named exactly as member_id
    if col_name not in a.columns:
        result = pd.DataFrame({'answer': [0]})
    else:
        # Expect two rows: one with a label like 'event_id_part1' and another with actual values
        # Use link_to_member to pivot into a single string per row label
        parts = a[['link_to_member', col_name]].dropna(subset=[col_name])
        # Build event_id by grouping values by event sequence if applicable.
        # Here, the two rows encode two separate events; we count non-empty values in the value row(s).
        # We treat any non-empty string in the member column (excluding the header-like row) as attendance evidence.
        value_rows = parts[parts['link_to_member'] != 'event_id_part1']
        # Count how many non-empty distinct tokens in the member column; tokens separated by whitespace are treated as one id string
        vals = value_rows[col_name].astype(str)
        # If the table structure encodes multiple events across multiple link_to_member rows, count unique non-empty strings
        attended_count = vals.replace('', pd.NA).dropna().nunique()
        result = pd.DataFrame({'answer': [int(attended_count)]})

result

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
