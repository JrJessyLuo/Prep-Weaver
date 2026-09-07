import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Institution_ID', 'new_name': 'Institution_ID'}, {'old_name': 'Institution_Name', 'new_name': 'Institution_Name'}, {'old_name': 'Location', 'new_name': 'Location'}])
    # Rename
    table_1 = table_1.rename(columns={'Institution_ID': 'Institution_ID', 'Institution_Name': 'Institution_Name', 'Location': 'Location'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Institution_Name", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove one layer of surrounding quotes if present
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     # collapse repeated whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove one layer of surrounding quotes if present
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # collapse repeated whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Institution_Name"] = table_1["Institution_Name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Location", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Location"] = table_1["Location"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Institution_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Institution_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Institution_ID']
    if _dtype == "datetime64":
        table_1['Institution_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Institution_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Institution_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Institution_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Institution_ID', 'Institution_Name', 'Location'])
    # SelectCol
    _cols = [c for c in ['Institution_ID', 'Institution_Name', 'Location'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # CodeGeneration(table_names=['table_1'], target_table="table_1_prepared", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    #     country_cols = ["Canada","United Kindom","United States"]
    #     long_df = df.melt(id_vars=[c for c in df.columns if c not in country_cols],
    #                       value_vars=country_cols,
    #                       var_name="country",
    #                       value_name="Institution_ID")
    #     long_df = long_df.dropna(subset=["Institution_ID"])
    #     return long_df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()
        country_cols = ["Canada","United Kindom","United States"]
        long_df = df.melt(id_vars=[c for c in df.columns if c not in country_cols],
                          value_vars=country_cols,
                          var_name="country",
                          value_name="Institution_ID")
        long_df = long_df.dropna(subset=["Institution_ID"])
        return long_df
    table_1_prepared = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1_prepared", columns=['staff_ID', 'name', 'Institution_ID'])
    # SelectCol
    _cols = [c for c in ['staff_ID', 'name', 'Institution_ID'] if c in table_1_prepared.columns]
    table_1_prepared = table_1_prepared[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1_prepared", subset=['staff_ID'], keep="first")
    # Deduplicate
    table_1_prepared = table_1_prepared.drop_duplicates(subset=['staff_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1_prepared'])
    # Terminate
    result = {'table_1_prepared': table_1_prepared}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['huiyi_id', 'yuangong_id', 'role'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['huiyi_id', 'yuangong_id', 'role'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['huiyi_id', 'yuangong_id', 'role'])
    # SelectCol
    _cols = [c for c in ['huiyi_id', 'yuangong_id', 'role'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="role", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes if present, trim, normalize spacing/case
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     s = " ".join(s.split())
    #     return s.title()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove surrounding quotes if present, trim, normalize spacing/case
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        s = " ".join(s.split())
        return s.title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["role"] = table_1["role"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['huiyi_id', 'yuangong_id', 'role'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['huiyi_id', 'yuangong_id', 'role'], keep='first').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Conference_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Conference_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Conference_ID', 'Conference_Info'])
    # SelectCol
    _cols = [c for c in ['Conference_ID', 'Conference_Info'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
prepared_institutions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_staff = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_participation = prepared_table_3
prepared_table_4 = _prep_4(tables['table_1'])
prepared_conferences = prepared_table_4

# prepared_institutions: columns [Institution_ID, Institution_Name, Location]
inst = prepared_institutions.copy()

# prepared_staff: columns [staff_ID, name, Institution_ID]
# If prepared_staff still has country columns, first melt and pick non-null as Institution_ID.
staff = prepared_staff.copy()

# prepared_participation: columns [huiyi_id, yuangong_id, role]
part = prepared_participation.copy()

# prepared_conferences: columns [Conference_ID, Conference_Info]
conf = prepared_conferences.copy()

# 1) Conferences in 2004
conf_2004 = conf[conf['Conference_Info'].astype(str).str.contains('2004', na=False)]

# 2) Participations linked to those 2004 conferences
part_2004 = part.merge(conf_2004, left_on='huiyi_id', right_on='Conference_ID', how='inner')

# 3) Staff who participated in 2004
staff_2004 = part_2004.merge(staff, left_on='yuangong_id', right_on='staff_ID', how='inner')

# 4) Institutions that had at least one participating staff in 2004
inst_with_participation = staff_2004[['Institution_ID']].dropna().drop_duplicates()

# 5) Institutions with no staff participation in 2004
result = inst.merge(inst_with_participation, on='Institution_ID', how='left', indicator=True)
result = result[result['_merge'] == 'left_only'][['Institution_Name', 'Location']]

answer = result.reset_index(drop=True)

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
