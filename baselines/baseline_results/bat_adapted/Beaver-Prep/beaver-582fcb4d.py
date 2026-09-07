import pandas as pd
import numpy as np

def _prep_1(table_1):
    core = table_1[['BUILDING_NUMBER','BUILDING_NAME_LONG','BUILDING_NAME','BUILDING_TYPE','DATE_OCCUPIED','OWNERSHIP_TYPE','SITE','PARENT_BUILDING_NUMBER']].copy()
    core['DATE_OCCUPIED'] = pd.to_datetime(core['DATE_OCCUPIED'], errors='coerce', infer_datetime_format=True).dt.strftime('%Y-%m-%d')
    target = core[['BUILDING_NUMBER','BUILDING_NAME_LONG','BUILDING_NAME','BUILDING_TYPE','DATE_OCCUPIED','OWNERSHIP_TYPE','SITE','PARENT_BUILDING_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['BUILDING_NUMBER','BUILDING_STREET_ADDRESS','BUILDING_NAME']].copy()
    prepared = prepared.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first')
    target = prepared[['BUILDING_NUMBER','BUILDING_STREET_ADDRESS','BUILDING_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_buildings_core = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_buildings_address = prepared_table_2

core = prepared_buildings_core.copy()
addr = prepared_buildings_address.copy()

# Merge on BUILDING_NUMBER
merged = core.merge(addr, on='BUILDING_NUMBER', how='left')

# Exclude subdivisions: rows with null PARENT_BUILDING_NUMBER are top-level buildings
not_subdiv = merged[merged['PARENT_BUILDING_NUMBER'].isna()].copy()

# Choose full name preference: use BUILDING_NAME_LONG if present else BUILDING_NAME from core else name from address
def choose_full_name(row):
    for col in ['BUILDING_NAME_LONG', 'BUILDING_NAME_x', 'BUILDING_NAME_y']:
        if col in row and pd.notna(row[col]) and str(row[col]).strip() != '':
            return row[col]
    return None

not_subdiv['FULL_NAME'] = not_subdiv.apply(choose_full_name, axis=1)

# Select and rename columns per request
result_cols = [
    'BUILDING_NUMBER',                    # building number
    'FULL_NAME',                          # full name
    'BUILDING_STREET_ADDRESS',            # street address
    'BUILDING_TYPE',                      # building type
    'DATE_OCCUPIED',                      # occupancy date
    'OWNERSHIP_TYPE',                     # ownership type
    'SITE'                                # site location
]
result = not_subdiv[result_cols].copy()

# Build the three summary rows for owned, leased, all (among not subdivisions and SITE == 'MIT' per question wording)
# If "at MIT" should filter by SITE == 'MIT'. Apply that to both detail rows and counts.
result_at_mit = result[result['SITE'] == 'MIT'].copy()

owned_count = (not_subdiv['SITE'].eq('MIT') & not_subdiv['OWNERSHIP_TYPE'].str.upper().eq('OWNED')).sum()
leased_count = (not_subdiv['SITE'].eq('MIT') & not_subdiv['OWNERSHIP_TYPE'].str.upper().eq('LEASED')).sum()
all_count = result_at_mit.shape[0]

summary_rows = pd.DataFrame([
    {
        'BUILDING_NUMBER': None,
        'FULL_NAME': f"{owned_count} Buildings",
        'BUILDING_STREET_ADDRESS': None,
        'BUILDING_TYPE': None,
        'DATE_OCCUPIED': None,
        'OWNERSHIP_TYPE': None,
        'SITE': None
    },
    {
        'BUILDING_NUMBER': None,
        'FULL_NAME': f"{leased_count} Buildings",
        'BUILDING_STREET_ADDRESS': None,
        'BUILDING_TYPE': None,
        'DATE_OCCUPIED': None,
        'OWNERSHIP_TYPE': None,
        'SITE': None
    },
    {
        'BUILDING_NUMBER': None,
        'FULL_NAME': f"{all_count} Buildings",
        'BUILDING_STREET_ADDRESS': None,
        'BUILDING_TYPE': None,
        'DATE_OCCUPIED': None,
        'OWNERSHIP_TYPE': None,
        'SITE': None
    }
], columns=result_cols)

# Concatenate detailed MIT rows first, then the three summary rows
final_answer = pd.concat([result_at_mit, summary_rows], ignore_index=True)

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
