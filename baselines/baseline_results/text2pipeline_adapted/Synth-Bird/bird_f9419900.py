import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'availability', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'availability']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['id', 'name', 'attribute', 'value', 'uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['availability'] = tmp_1['availability'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'availability']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['id', 'name', 'attribute', 'value', 'uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
prepared_table_1['availability_str'] = prepared_table_1['availability'].astype(str).str.strip()
# Define robust matching for Chinese Simplified across typical tokens
# Common representations include: 'Chinese Simplified', 'Chinese (Simplified)', 'zh-Hans', 'zhs', and case variations
patterns = [
    'chinese simplified',
    'chinese (simplified)',
    'zh-hans',
    'zhs',
    'simplified chinese'
]
avail_lower = prepared_table_1['availability_str'].str.lower()
mask = False
for p in patterns:
    mask = mask | avail_lower.str.contains(p, regex=False)
# Fallback: if nothing matched, try a broader 'chinese' catch with 'simplified' anywhere
if mask.sum() == 0:
    mask = avail_lower.str.contains('chinese', regex=False) & avail_lower.str.contains('simplified', regex=False)
# Compute percentage over all cards with non-empty availability strings
denom_series = prepared_table_1['availability_str'].replace({'nan': ''})
denominator = (denom_series != '').sum()
# If denominator would be zero, fall back to total card count
if denominator == 0:
    denominator = len(prepared_table_1)
    numerator = mask.sum()
else:
    numerator = mask.sum()
percentage = (numerator / denominator * 100.0) if denominator > 0 else 0.0
target = __import__('pandas').DataFrame({'percentage_chinese_simplified': [percentage]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
