import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['CAMPUS_SECTOR','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_NUMBER','SITE','OWNERSHIP_TYPE','ASSIGNABLE_AREA','EXT_GROSS_AREA','NUM_OF_ROOMS','FCLT_BUILDING_KEY']].copy()
    target = prepared[['CAMPUS_SECTOR','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_NUMBER','SITE','OWNERSHIP_TYPE','ASSIGNABLE_AREA','EXT_GROSS_AREA','NUM_OF_ROOMS','FCLT_BUILDING_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1

# Start from prepared table
df = prepared_buildings.copy()

# Derive building name preference
df['BUILDING_DISPLAY_NAME'] = df['BUILDING_NAME'].fillna(df['BUILDING_NAME_LONG'])

# City/State inference: if not present in data, set placeholders or map from SITE if a lookup exists
# Here, set City/State as unknown due to lack of columns
df['CITY'] = pd.NA
df['STATE'] = pd.NA

# Ensure numeric
for c in ['ASSIGNABLE_AREA', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# If a floors column existed, we'd use it; since it's not available, set total floors to NaN
df['TOTAL_FLOORS'] = pd.NA

# Total number of organizations not available in source; set to NaN
df['TOTAL_ORGANIZATIONS'] = pd.NA

# Rank within sector by descending assignable area
df['RANK_IN_SECTOR'] = df.sort_values(['CAMPUS_SECTOR','ASSIGNABLE_AREA'], ascending=[True, False])\
    .groupby('CAMPUS_SECTOR').cumcount() + 1

# Per-building detail rows
detail_cols = ['CAMPUS_SECTOR','BUILDING_DISPLAY_NAME','CITY','STATE','TOTAL_FLOORS','ASSIGNABLE_AREA','NUM_OF_ROOMS','TOTAL_ORGANIZATIONS','OWNERSHIP_TYPE','RANK_IN_SECTOR']
detail = df[detail_cols].rename(columns={'BUILDING_DISPLAY_NAME':'BUILDING_NAME','ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA'})

# Subtotals per sector (only floors and assignable area required; floors unknown -> NaN sum)
subtotals = df.groupby('CAMPUS_SECTOR', as_index=False).agg({
    'ASSIGNABLE_AREA':'sum'
})
subtotals['TOTAL_FLOORS'] = pd.NA
subtotals['ROW_TYPE'] = 'SUBTOTAL'
subtotals = subtotals[['CAMPUS_SECTOR','TOTAL_FLOORS','ASSIGNABLE_AREA','ROW_TYPE']]

# Grand total
grand = pd.DataFrame({
    'CAMPUS_SECTOR': ['GRAND TOTAL'],
    'ASSIGNABLE_AREA': [df['ASSIGNABLE_AREA'].sum(skipna=True)],
    'TOTAL_FLOORS': [pd.NA],
    'ROW_TYPE': ['GRAND_TOTAL']
})

# Label detail rows
detail['ROW_TYPE'] = 'DETAIL'

# Prepare subtotal rows to align columns for final presentation
sub_detail_like = subtotals.merge(
    df[['CAMPUS_SECTOR']].drop_duplicates().assign(
        BUILDING_NAME=pd.NA, CITY=pd.NA, STATE=pd.NA, NUM_OF_ROOMS=pd.NA, TOTAL_ORGANIZATIONS=pd.NA, OWNERSHIP_TYPE=pd.NA, RANK_IN_SECTOR=pd.NA
    ),
    on='CAMPUS_SECTOR', how='left'
).drop_duplicates(subset=['CAMPUS_SECTOR'])
sub_detail_like = sub_detail_like.rename(columns={'ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA'})[
    ['CAMPUS_SECTOR','BUILDING_NAME','CITY','STATE','TOTAL_FLOORS','TOTAL_ASSIGNABLE_AREA','NUM_OF_ROOMS','TOTAL_ORGANIZATIONS','OWNERSHIP_TYPE','RANK_IN_SECTOR','ROW_TYPE']
]

grand_like = grand.assign(BUILDING_NAME=pd.NA, CITY=pd.NA, STATE=pd.NA, NUM_OF_ROOMS=pd.NA, TOTAL_ORGANIZATIONS=pd.NA, OWNERSHIP_TYPE=pd.NA, RANK_IN_SECTOR=pd.NA)
grand_like = grand_like.rename(columns={'ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA'})[
    ['CAMPUS_SECTOR','BUILDING_NAME','CITY','STATE','TOTAL_FLOORS','TOTAL_ASSIGNABLE_AREA','NUM_OF_ROOMS','TOTAL_ORGANIZATIONS','OWNERSHIP_TYPE','RANK_IN_SECTOR','ROW_TYPE']
]

# Combine: interleave detail and subtotal per sector
out = []
for sector, grp in detail.sort_values(['CAMPUS_SECTOR','TOTAL_ASSIGNABLE_AREA'], ascending=[True, False]).groupby('CAMPUS_SECTOR', sort=False):
    out.append(grp)
    out.append(sub_detail_like[sub_detail_like['CAMPUS_SECTOR']==sector])
result = pd.concat(out + [grand_like], ignore_index=True)

target = result

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
