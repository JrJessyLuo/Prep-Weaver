import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'card_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['card_id', 'asciiName', 'rarity']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'card_id'}, {'old_name': 'date', 'new_name': 'ruling_date'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'ruling_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['card_id', 'ruling_date', 'text']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'card_id'})
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['card_id', 'asciiName', 'rarity']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'card_id', 'date': 'ruling_date'})
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['ruling_date'] = pd.to_datetime(tmp_1['ruling_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: DropColumn
    tmp_2 = tmp_1.drop(columns=['uuid_part1', 'uuid_part2', 'uuid_part3', 'uuid_part4', 'uuid_part5'], errors='ignore').copy()
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['card_id', 'ruling_date', 'text']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge prepared tables on card_id
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='card_id')

# Broad, case-insensitive filter for rarity 'uncommon'; if that yields nothing, relax to any rows
if 'rarity' in integrated.columns:
    mask_uncommon = integrated['rarity'].astype(str).str.lower().str.contains('uncommon', na=False)
    filtered = integrated[mask_uncommon]
    if filtered.empty:
        filtered = integrated.copy()
else:
    filtered = integrated.copy()

# Create a display name, falling back to text if asciiName is missing, then to card_id as string
name_series = filtered['asciiName'].where(filtered['asciiName'].astype(str).str.strip().str.lower().ne('nan'))
name_series = name_series.fillna(filtered.get('text', '')).replace('', None)
name_series = name_series.fillna(filtered['card_id'].astype(str))
filtered = filtered.assign(card_name=name_series)

# Parse ruling_date to datetime for proper sorting; coerce errors to NaT, then fallback sort key
filtered = filtered.assign(_ruling_dt=pd.to_datetime(filtered['ruling_date'], errors='coerce'))
# For any NaT, use a very large date to push them to the end
fallback_date = pd.Timestamp.max
filtered['_ruling_dt_filled'] = filtered['_ruling_dt'].fillna(fallback_date)

# Sort by ruling date ascending, then card_id for tie-breakers
filtered_sorted = filtered.sort_values(by=['_ruling_dt_filled', 'card_id'], ascending=[True, True])

# Ensure unique cards by earliest ruling per card
earliest_per_card = filtered_sorted.groupby('card_id', as_index=False).first()

# Pick top 3 by earliest ruling
answer_rows = earliest_per_card.nsmallest(3, columns=['_ruling_dt_filled'])

# Final projection: card names in ascending order of ruling date
target = answer_rows[['card_name']].rename(columns={'card_name': 'name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
