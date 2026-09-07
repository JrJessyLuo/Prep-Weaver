import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'patient_id'}, {'old_name': 'Date', 'new_name': 'lab_date'}, {'old_name': 'CRE', 'new_name': 'creatinine'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'patient_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'lab_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'creatinine', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'lab_date', 'creatinine']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': "fallback_passthrough_after_pipeline_generation_failure: KeyError: 'Birthday'", 'source_table': 'table_2'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ID': 'patient_id', 'Date': 'lab_date', 'CRE': 'creatinine'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['patient_id'] = tmp_1['patient_id'].astype(str)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['lab_date'] = pd.to_datetime(tmp_2['lab_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['creatinine'] = pd.to_numeric(tmp_3['creatinine'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['patient_id', 'lab_date', 'creatinine']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
lab = prepared_table_1.copy()
demo_raw = prepared_table_2.copy()

# Reshape the wide metadata table into long form, then pivot to Attribute-Value pairs per subject key
# The first row contains attribute names per subject key, the second row contains the corresponding values.
# Columns except 'ID' are subject keys (as strings).
value_row_mask = demo_raw['ID'].astype(str).str.strip().str.lower() == 'value'
attr_row_mask = demo_raw['ID'].astype(str).str.strip().str.lower() == 'attribute'

if attr_row_mask.any() and value_row_mask.any():
    attr_row = demo_raw[attr_row_mask].iloc[0]
    value_row = demo_raw[value_row_mask].iloc[0]
    # Build a tidy DataFrame with columns: subject_key, attribute, value
    tidy_records = []
    for col in demo_raw.columns:
        if col == 'ID':
            continue
        subject_key = str(col)
        attribute = str(attr_row[col]) if col in attr_row else None
        value = value_row[col] if col in value_row else None
        tidy_records.append({'subject_key': subject_key, 'attribute': attribute, 'value': value})
    tidy = pd.DataFrame(tidy_records)
    # We need birthday for age. Normalize attribute names case-insensitively and pick Birthday values.
    tidy['attribute_norm'] = tidy['attribute'].astype(str).str.strip().str.lower()
    bday = tidy[tidy['attribute_norm'].str.contains('birthday', case=False, na=False)].copy()
    # Each subject_key should have a single birthday value
    demo = bday[['subject_key', 'value']].rename(columns={'value': 'birthday_str'}).drop_duplicates('subject_key')
else:
    # Fallback: empty demo
    demo = pd.DataFrame(columns=['subject_key', 'birthday_str'])

# Merge labs with demographics by linking lab.patient_id to demo.subject_key
lab2 = lab.copy()
lab2['patient_id'] = lab2['patient_id'].astype(str)
demo['subject_key'] = demo['subject_key'].astype(str)
merged = lab2.merge(demo, left_on='patient_id', right_on='subject_key', how='left')

# Parse dates and compute age at lab date where possible
# Convert lab_date and birthday
merged['lab_date_dt'] = pd.to_datetime(merged['lab_date'], errors='coerce')
merged['birthday_dt'] = pd.to_datetime(merged['birthday_str'], errors='coerce')

# Determine abnormal creatinine using a broad adult reference if no flags present
# Keep non-null numeric creatinine
merged = merged[merged['creatinine'].notna()].copy()
merged['cre_abnormal'] = (merged['creatinine'] < 0.5) | (merged['creatinine'] > 1.2)
lab_abn = merged[merged['cre_abnormal']].copy()

# Compute age in years at time of lab where both dates available
age_mask = lab_abn['lab_date_dt'].notna() & lab_abn['birthday_dt'].notna()
lab_abn.loc[age_mask, 'age_years'] = ((lab_abn.loc[age_mask, 'lab_date_dt'] - lab_abn.loc[age_mask, 'birthday_dt']).dt.days / 365.25).astype(float)

# Identify patients who aren't 70 yet at time of abnormal creatinine
younger = lab_abn[lab_abn['age_years'].notna() & (lab_abn['age_years'] < 70)].copy()

# Count unique patients
count_val = younger['patient_id'].nunique()

target = pd.DataFrame({'count_under_70_with_abnormal_creatinine': [int(count_val)]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
