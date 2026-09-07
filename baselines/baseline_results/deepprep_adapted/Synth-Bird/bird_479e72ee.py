import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['member_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['member_id'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_members", func="""
    # import pandas as pd
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     def pick_col(patterns):
    #         # pick first column whose name matches any regex pattern (case-insensitive)
    #         cols = list(df.columns)
    #         for pat in patterns:
    #             rx = re.compile(pat, flags=re.IGNORECASE)
    #             for c in cols:
    #                 if rx.search(str(c)):
    #                     return c
    #         return None
    # 
    #     member_col = pick_col([r'^member_id$'])
    #     # Heuristics for the other fields (common Airtable exports / field naming)
    #     position_col = pick_col([r'position', r'role', r'title'])
    #     tshirt_col = pick_col([r't[_\s-]*shirt', r'tee', r'shirt\s*size', r'size'])
    #     major_link_col = pick_col([r'link.*major', r'major.*link', r'link_to_major', r'major'])
    # 
    #     out = pd.DataFrame()
    #     out["member_id"] = df[member_col] if member_col is not None else pd.NA
    #     out["position"] = df[position_col] if position_col is not None else pd.NA
    #     out["t_shirt_size"] = df[tshirt_col] if tshirt_col is not None else pd.NA
    #     out["link_to_major"] = df[major_link_col] if major_link_col is not None else pd.NA
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        def pick_col(patterns):
            # pick first column whose name matches any regex pattern (case-insensitive)
            cols = list(df.columns)
            for pat in patterns:
                rx = re.compile(pat, flags=re.IGNORECASE)
                for c in cols:
                    if rx.search(str(c)):
                        return c
            return None

        member_col = pick_col([r'^member_id$'])
        # Heuristics for the other fields (common Airtable exports / field naming)
        position_col = pick_col([r'position', r'role', r'title'])
        tshirt_col = pick_col([r't[_\s-]*shirt', r'tee', r'shirt\s*size', r'size'])
        major_link_col = pick_col([r'link.*major', r'major.*link', r'link_to_major', r'major'])

        out = pd.DataFrame()
        out["member_id"] = df[member_col] if member_col is not None else pd.NA
        out["position"] = df[position_col] if position_col is not None else pd.NA
        out["t_shirt_size"] = df[tshirt_col] if tshirt_col is not None else pd.NA
        out["link_to_major"] = df[major_link_col] if major_link_col is not None else pd.NA

        return out
    prepared_members = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="prepared_members", column_name="position", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # normalize whitespace
    #     s = " ".join(s.split())
    #     # keep original casing for complex titles, but remove trailing/leading spaces
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # normalize whitespace
        s = " ".join(s.split())
        # keep original casing for complex titles, but remove trailing/leading spaces
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    prepared_members["position"] = prepared_members["position"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="prepared_members", column_name="t_shirt_size", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s_low = s.lower()
    # 
    #     # normalize common size encodings
    #     mapping = {
    #         "xs": "XS", "x-small": "XS", "extra small": "XS",
    #         "s": "S", "small": "S",
    #         "m": "M", "med": "M", "medium": "M",
    #         "l": "L", "large": "L",
    #         "xl": "XL", "x-large": "XL", "extra large": "XL",
    #         "xxl": "XXL", "2xl": "XXL"
    #     }
    #     s_low_clean = s_low.replace("_", " ").replace("-", " ")
    #     s_low_clean = " ".join(s_low_clean.split())
    #     return mapping.get(s_low_clean, mapping.get(s_low, s.strip()))
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s_low = s.lower()

        # normalize common size encodings
        mapping = {
            "xs": "XS", "x-small": "XS", "extra small": "XS",
            "s": "S", "small": "S",
            "m": "M", "med": "M", "medium": "M",
            "l": "L", "large": "L",
            "xl": "XL", "x-large": "XL", "extra large": "XL",
            "xxl": "XXL", "2xl": "XXL"
        }
        s_low_clean = s_low.replace("_", " ").replace("-", " ")
        s_low_clean = " ".join(s_low_clean.split())
        return mapping.get(s_low_clean, mapping.get(s_low, s.strip()))
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    prepared_members["t_shirt_size"] = prepared_members["t_shirt_size"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="prepared_members", columns=['member_id', 'position', 't_shirt_size', 'link_to_major'])
    # SelectCol
    _cols = [c for c in ['member_id', 'position', 't_shirt_size', 'link_to_major'] if c in prepared_members.columns]
    prepared_members = prepared_members[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['prepared_members'])
    # Terminate
    result = {'prepared_members': prepared_members}
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
    # Sort(table_name="table_1", by=['major_id'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['major_id'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['major_id', 'value'])
    # SelectCol
    _cols = [c for c in ['major_id', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['major_id', 'value'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['major_id', 'value'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
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
members_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
majors_prepared = prepared_table_2

# Assume prepared tables already normalized so that columns exist as named
# Integrate members with majors by the foreign-key-like columns
members_with_majors = members_prepared.merge(majors_prepared.rename(columns={"record_id":"link_to_major"}), on="link_to_major", how="left")

# Identify Business members: either position indicates Business or the major value mentions Business
is_business_position = members_with_majors["position"].astype(str).str.contains("Business", case=False, na=False)
is_business_major = members_with_majors.get("value", pd.Series(index=members_with_majors.index)).astype(str).str.contains("Business", case=False, na=False)

business_mask = is_business_position | is_business_major

# Count members with Medium tee shirt size among Business members
answer = int((members_with_majors["t_shirt_size"].astype(str).str.strip().str.casefold() == "medium") & business_mask).sum()

result = pd.DataFrame({"count_medium_business_members": [answer]})

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
