import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'publisher_id', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'superhero_name', 'full_name', 'gid', 'eid', 'hcid', 'scid', 'rid', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['publisher_id'] = pd.to_numeric(tmp_0['publisher_id'], errors='coerce').astype(float)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['id', 'superhero_name', 'full_name', 'gid', 'eid', 'hcid', 'scid', 'rid', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Select the superhero with id == 38 and return its publisher_id as the best available proxy for publisher name since no publishers lookup table is provided.
match = df[df['id'] == 38]
if match.empty:
    # fallback: try string/int tolerant match
    match = df[df['id'].astype('Int64') == 38]
# Project the most relevant available publisher information
target = match[['id', 'publisher_id']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
