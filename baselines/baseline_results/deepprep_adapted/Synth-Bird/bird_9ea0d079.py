import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['attr', 'val', 'prefix', 'id_core', 'suffix'])
    # SelectCol
    _cols = [c for c in ['attr', 'val', 'prefix', 'id_core', 'suffix'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="prefix", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove any double quotes appearing in the string (e.g., '""2"' -> '2')
    #     s = s.replace('"', '')
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove any double quotes appearing in the string (e.g., '""2"' -> '2')
        s = s.replace('"', '')
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["prefix"] = table_1["prefix"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="id_core", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = s.replace('"', '')
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = s.replace('"', '')
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["id_core"] = table_1["id_core"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="suffix", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = s.replace('"', '')
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = s.replace('"', '')
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["suffix"] = table_1["suffix"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attr", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # strip surrounding/embedded quotes
    #     s = s.replace('"', '')
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # strip surrounding/embedded quotes
        s = s.replace('"', '')
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attr"] = table_1["attr"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="val", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = s.replace('"', '')
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = s.replace('"', '')
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["val"] = table_1["val"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="patient_id", func="""
    # def compute(row):
    #     # patient_id = prefix + id_core + suffix (already de-quoted/trimmed)
    #     p = '' if row.get('prefix') is None else str(row.get('prefix'))
    #     c = '' if row.get('id_core') is None else str(row.get('id_core'))
    #     x = '' if row.get('suffix') is None else str(row.get('suffix'))
    #     return f"{p}{c}{x}"
    # """)
    # AddNewColumn
    def compute(row):
        # patient_id = prefix + id_core + suffix (already de-quoted/trimmed)
        p = '' if row.get('prefix') is None else str(row.get('prefix'))
        c = '' if row.get('id_core') is None else str(row.get('id_core'))
        x = '' if row.get('suffix') is None else str(row.get('suffix'))
        return f"{p}{c}{x}"
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["patient_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['patient_id', 'attr', 'val'])
    # SelectCol
    _cols = [c for c in ['patient_id', 'attr', 'val'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
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
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'UA'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'UA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_lab_ua", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Coerce UA to numeric; non-numeric placeholders become NaN
    #     df["UA"] = pd.to_numeric(df["UA"], errors="coerce")
    # 
    #     # Ensure Date remains a clean string in YYYY-MM-DD (already standardized upstream)
    #     df["Date"] = df["Date"].astype(str)
    # 
    #     return df[["ID", "Date", "UA"]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Coerce UA to numeric; non-numeric placeholders become NaN
        df["UA"] = pd.to_numeric(df["UA"], errors="coerce")

        # Ensure Date remains a clean string in YYYY-MM-DD (already standardized upstream)
        df["Date"] = df["Date"].astype(str)

        return df[["ID", "Date", "UA"]]
    prepared_lab_ua = process_tables(table_1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['prepared_lab_ua'])
    # Terminate
    result = {'prepared_lab_ua': prepared_lab_ua}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients_long_attrs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs = prepared_table_2

# Prepared inputs assumed: labs, patients_long_attrs
# 1) Normalize patients_long_attrs patient_id by removing surrounding quotes if any
pla = patients_long_attrs.copy()
pla['patient_id'] = pla['patient_id'].astype(str).str.replace('^\"|\"$', '', regex=True)

# 2) Extract a single sex value per patient from long attributes
# Common attribute names could be 'Sex', 'Gender', etc.; prefer Sex if multiple
sex_map = (pla[pla['attr'].str.lower().isin(['sex','gender'])]
             .assign(sex=lambda d: d['val'].astype(str).str.strip().str.lower()
                                   .map({'m':'male','male':'male','f':'female','female':'female'})
                                   .fillna(d['val'].astype(str)))
             [['patient_id','sex']]
             .dropna()
             .drop_duplicates(subset=['patient_id'], keep='first'))

# 3) Clean UA and determine abnormality
lb = labs.copy()
lb['UA'] = pd.to_numeric(lb['UA'], errors='coerce')
# Assume adult reference: males 3.4-7.0 mg/dL, females 2.4-6.0 mg/dL
# We'll first merge sex, then flag abnormal by sex-specific ranges
merged = lb.merge(sex_map, left_on='ID', right_on='patient_id', how='inner')

# Define sex-specific ranges
def ua_abnormal(row):
    ua = row['UA']
    if pd.isna(ua):
        return False
    sx = str(row.get('sex','')).lower()
    if sx == 'male':
        return (ua < 3.4) or (ua > 7.0)
    if sx == 'female':
        return (ua < 2.4) or (ua > 6.0)
    # If unknown sex, exclude from abnormal set for this question
    return False

merged['abnormal_ua'] = merged.apply(ua_abnormal, axis=1)

# 4) Restrict to abnormal UA rows
abn = merged[merged['abnormal_ua']]

# 5) Count unique patients by sex among abnormal UA
unique_patients = abn.dropna(subset=['sex']).drop_duplicates(subset=['patient_id'])
counts = unique_patients['sex'].str.lower().value_counts()
male_count = int(counts.get('male', 0))
female_count = int(counts.get('female', 0))

# 6) Compute ratio male:female as a string; handle zero division
ratio = f"{male_count}:{female_count}" if female_count != 0 else (f"{male_count}:0" if male_count>0 else "0:0")

answer = {
    'male_count': male_count,
    'female_count': female_count,
    'ratio_male_to_female': ratio
}

target = pd.Series(answer)

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
