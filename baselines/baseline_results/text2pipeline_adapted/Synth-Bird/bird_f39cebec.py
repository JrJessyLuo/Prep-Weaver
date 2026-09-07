import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'hero_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'hero_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['hero_id', 'superhero_name', 'full_name', 'hair_colour_id', 'skin_colour_id', 'race_id', 'publisher_id', 'aid', 'height_weight', '"1"', '"2"', '"3"']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'power_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'power_name', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['power_id', 'power_name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'attribute_id', 'new_name': 'power_id'}, {'old_name': 'attribute_value', 'new_name': 'value'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'hero_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'power_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'value', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['hero_id', 'power_id', 'value']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'hero_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['hero_id'] = pd.to_numeric(tmp_1['hero_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['hero_id', 'superhero_name', 'full_name', 'hair_colour_id', 'skin_colour_id', 'race_id', 'publisher_id', 'aid', 'height_weight', '"1"', '"2"', '"3"']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'power_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['power_name'] = tmp_1['power_name'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['power_id', 'power_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'attribute_id': 'power_id', 'attribute_value': 'value'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['hero_id'] = pd.to_numeric(tmp_1['hero_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['power_id'] = pd.to_numeric(tmp_2['power_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['value'] = pd.to_numeric(tmp_3['value'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['hero_id', 'power_id', 'value']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
hp = prepared_table_3.merge(prepared_table_1[["hero_id","superhero_name"]], on="hero_id", how="left")
# Count distinct powers per hero (treat any row as a power association)
counts = hp.groupby(["hero_id","superhero_name"], as_index=False)["power_id"].nunique().rename(columns={"power_id":"power_count"})
# Find max and corresponding hero(s)
max_count = counts["power_count"].max()
result = counts[counts["power_count"] == max_count]
# In case of ties, keep all; project required columns
target = result.sort_values(["power_count","superhero_name"], ascending=[False, True])[["superhero_name","power_count"]]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
