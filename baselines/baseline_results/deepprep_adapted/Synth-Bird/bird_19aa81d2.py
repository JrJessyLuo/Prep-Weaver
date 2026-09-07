import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="value", target_columns=['hometown', 'state', 'zip'], func="""
    # import re
    # def split(val):
    #     if val is None:
    #         return {"hometown": None, "state": None, "zip": None}
    #     s = str(val).strip()
    #     # Try patterns like: "City, ST 12345" or "City, ST" or "City ST 12345"
    #     m = re.match(r'^(.*?)[,\s]+([A-Za-z]{2})(?:\s+(\d{5})(?:-\d{4})?)?$', s)
    #     if m:
    #         city, st, z = m.groups()
    #         return {"hometown": city.strip(), "state": st.upper(), "zip": z}
    #     return {"hometown": s, "state": None, "zip": None}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"hometown": None, "state": None, "zip": None}
        s = str(val).strip()
        # Try patterns like: "City, ST 12345" or "City, ST" or "City ST 12345"
        m = re.match(r'^(.*?)[,\s]+([A-Za-z]{2})(?:\s+(\d{5})(?:-\d{4})?)?$', s)
        if m:
            city, st, z = m.groups()
            return {"hometown": city.strip(), "state": st.upper(), "zip": z}
        return {"hometown": s, "state": None, "zip": None}
    for _c in ['hometown', 'state', 'zip']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['value']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['hometown', 'state', 'zip']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['value'])

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'hometown', 'new_name': 'value_for_pivot'}])
    # Rename
    table_1 = table_1.rename(columns={'hometown': 'value_for_pivot'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # Pivot(table_name="table_1", index="member_id", columns="attribute", values="value_for_pivot", aggfunc="first")
    # Pivot
    table_1 = table_1.pivot_table(index='member_id', columns='attribute', values='value_for_pivot', aggfunc='first').reset_index()

    # ---------------- Step 4 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_members", func="""
    # import pandas as pd
    # import re
    # 
    # def process_tables(df: pd.DataFrame) -> pd.DataFrame:
    #     out = pd.DataFrame()
    #     out["member_id"] = df["member_id"] if "member_id" in df.columns else df.index
    # 
    #     # Pivot likely created a 'hometown' attribute column; keep it as hometown
    #     hometown = df["hometown"] if "hometown" in df.columns else None
    #     out["hometown"] = hometown
    # 
    #     def parse_state_zip(val):
    #         if val is None or (isinstance(val, float) and pd.isna(val)):
    #             return (None, None)
    #         s = str(val).strip()
    #         m = re.match(r'^(.*?)[,\s]+([A-Za-z]{2})(?:\s+(\d{5})(?:-\d{4})?)?$', s)
    #         if m:
    #             _city, st, z = m.groups()
    #             return (st.upper() if st else None, z)
    #         return (None, None)
    # 
    #     parsed = out["hometown"].apply(lambda v: pd.Series(parse_state_zip(v), index=["state_from_hometown","zip_from_hometown"]))
    # 
    #     # If there are explicit 'state'/'zip' attributes from pivot, prefer them; else use parsed
    #     state_attr = df["state"] if "state" in df.columns else None
    #     zip_attr = df["zip"] if "zip" in df.columns else None
    # 
    #     out["state"] = (state_attr if state_attr is not None else pd.Series([None]*len(out))).combine_first(parsed["state_from_hometown"])
    #     out["zip"] = (zip_attr if zip_attr is not None else pd.Series([None]*len(out))).combine_first(parsed["zip_from_hometown"])
    # 
    #     return out[["member_id","hometown","state","zip"]]
    # """)
    # CodeGeneration

    def process_tables(df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        out["member_id"] = df["member_id"] if "member_id" in df.columns else df.index

        # Pivot likely created a 'hometown' attribute column; keep it as hometown
        hometown = df["hometown"] if "hometown" in df.columns else None
        out["hometown"] = hometown

        def parse_state_zip(val):
            if val is None or (isinstance(val, float) and pd.isna(val)):
                return (None, None)
            s = str(val).strip()
            m = re.match(r'^(.*?)[,\s]+([A-Za-z]{2})(?:\s+(\d{5})(?:-\d{4})?)?$', s)
            if m:
                _city, st, z = m.groups()
                return (st.upper() if st else None, z)
            return (None, None)

        parsed = out["hometown"].apply(lambda v: pd.Series(parse_state_zip(v), index=["state_from_hometown","zip_from_hometown"]))

        # If there are explicit 'state'/'zip' attributes from pivot, prefer them; else use parsed
        state_attr = df["state"] if "state" in df.columns else None
        zip_attr = df["zip"] if "zip" in df.columns else None

        out["state"] = (state_attr if state_attr is not None else pd.Series([None]*len(out))).combine_first(parsed["state_from_hometown"])
        out["zip"] = (zip_attr if zip_attr is not None else pd.Series([None]*len(out))).combine_first(parsed["zip_from_hometown"])

        return out[["member_id","hometown","state","zip"]]
    prepared_members = process_tables(table_1)

    # ---------------- Step 5 ----------------
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
    # CodeGeneration(table_names=['table_1'], target_table="zip_ref_prepared", func="""
    # import pandas as pd
    # import numpy as np
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # First column is the row-label key (type/shi/xian)
    #     row_key_col = df.columns[0]
    #     df = df.rename(columns={row_key_col: "row_key"})
    # 
    #     # Melt wide zip columns into long: (row_key, zip, value)
    #     long_df = df.melt(id_vars=["row_key"], var_name="zip", value_name="value")
    # 
    #     # Normalize keys
    #     long_df["row_key"] = long_df["row_key"].astype(str).str.strip().str.lower()
    # 
    #     # Keep only city/county rows (drop type and others)
    #     key_map = {"shi": "city", "xian": "county"}
    #     long_df = long_df[long_df["row_key"].isin(key_map.keys())].copy()
    #     long_df["field"] = long_df["row_key"].map(key_map)
    # 
    #     # Pivot to columns: zip, city, county
    #     out = long_df.pivot_table(index="zip", columns="field", values="value", aggfunc="first").reset_index()
    # 
    #     # Zip formatting: keep digits, zero-pad to 5 where possible
    #     out["zip"] = out["zip"].astype(str).str.replace(r"\D+", "", regex=True)
    #     out.loc[out["zip"].str.len().between(1,4), "zip"] = out.loc[out["zip"].str.len().between(1,4), "zip"].str.zfill(5)
    # 
    #     # Add state_abbr (cannot infer from provided table alone; leave null)
    #     out["state_abbr"] = np.nan
    # 
    #     # Ensure required columns exist
    #     for c in ["city","county","state_abbr"]:
    #         if c not in out.columns:
    #             out[c] = np.nan
    # 
    #     return out[["zip","city","county","state_abbr"]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # First column is the row-label key (type/shi/xian)
        row_key_col = df.columns[0]
        df = df.rename(columns={row_key_col: "row_key"})

        # Melt wide zip columns into long: (row_key, zip, value)
        long_df = df.melt(id_vars=["row_key"], var_name="zip", value_name="value")

        # Normalize keys
        long_df["row_key"] = long_df["row_key"].astype(str).str.strip().str.lower()

        # Keep only city/county rows (drop type and others)
        key_map = {"shi": "city", "xian": "county"}
        long_df = long_df[long_df["row_key"].isin(key_map.keys())].copy()
        long_df["field"] = long_df["row_key"].map(key_map)

        # Pivot to columns: zip, city, county
        out = long_df.pivot_table(index="zip", columns="field", values="value", aggfunc="first").reset_index()

        # Zip formatting: keep digits, zero-pad to 5 where possible
        out["zip"] = out["zip"].astype(str).str.replace(r"\D+", "", regex=True)
        out.loc[out["zip"].str.len().between(1,4), "zip"] = out.loc[out["zip"].str.len().between(1,4), "zip"].str.zfill(5)

        # Add state_abbr (cannot infer from provided table alone; leave null)
        out["state_abbr"] = np.nan

        # Ensure required columns exist
        for c in ["city","county","state_abbr"]:
            if c not in out.columns:
                out[c] = np.nan

        return out[["zip","city","county","state_abbr"]]
    zip_ref_prepared = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="zip_ref_prepared", column_name="city", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s if s != '' and s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    zip_ref_prepared["city"] = zip_ref_prepared["city"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="zip_ref_prepared", column_name="county", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s if s != '' and s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    zip_ref_prepared["county"] = zip_ref_prepared["county"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['zip_ref_prepared'])
    # Terminate
    result = {'zip_ref_prepared': zip_ref_prepared}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
members_hometown = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
zip_lookup_long = prepared_table_2

# Assume prepared tables are available as dataframes: members_hometown, zip_lookup_long
# Integration on ZIP if member ZIP exists; otherwise fall back to state text on members_hometown

# 1) Join members to ZIP lookup to enrich with state via ZIP
merged = members_hometown.merge(zip_lookup_long[['zip','state_abbr']], on='zip', how='left')

# 2) Determine member_state: prefer explicit state on member, else state_abbr from ZIP
# Normalize state names/abbreviations to compare with Maryland
state_map = {
    'md': 'Maryland', 'maryland': 'Maryland'
}

def norm_state(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    key = s.lower()
    return state_map.get(key, s)

merged['member_state'] = merged['state'].apply(norm_state)
merged['zip_state'] = merged['state_abbr'].apply(norm_state)
merged['final_state'] = merged['member_state'].where(merged['member_state'].notna(), merged['zip_state'])

# 3) Count how many members have hometowns in Maryland
answer = int((merged['final_state'] == 'Maryland').sum())

result = {'answer': answer}

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
