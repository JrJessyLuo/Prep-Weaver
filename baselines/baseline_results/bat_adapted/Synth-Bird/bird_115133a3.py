import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['cds','school_part1','school_part2','AvgScrWrite']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    directory = table_1[['CDSCode','School','OpenDate','ClosedDate','Phone']].copy()
    directory['OpenDate'] = pd.to_datetime(directory['OpenDate'], errors='coerce').dt.strftime('%Y-%m-%d')
    directory['ClosedDate'] = pd.to_datetime(directory['ClosedDate'], errors='coerce').dt.strftime('%Y-%m-%d')
    target = directory[['CDSCode','School','OpenDate','ClosedDate','Phone']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_scores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_directory = prepared_table_2

# Merge scores with directory on CDS code (as strings to ensure match)
t = prepared_scores.copy()
d = prepared_directory.copy()

t['cds'] = t['cds'].astype(str)
d['CDSCode'] = d['CDSCode'].astype(str)
merged = t.merge(d, left_on='cds', right_on='CDSCode', how='inner')

# Parse dates
merged['OpenDate_parsed'] = pd.to_datetime(merged['OpenDate'], errors='coerce')
merged['ClosedDate_parsed'] = pd.to_datetime(merged['ClosedDate'], errors='coerce')

# Filter: opened after 1991 OR closed before 2000
cond_open = merged['OpenDate_parsed'] > pd.Timestamp('1991-12-31')
cond_closed = (merged['ClosedDate_parsed'].notna()) & (merged['ClosedDate_parsed'] < pd.Timestamp('2000-01-01'))
filtered = merged[cond_open | cond_closed].copy()

# Compose school name preference: use directory School if available; otherwise join parts
name_from_parts = (filtered['school_part1'].fillna('') + ' ' + filtered['school_part2'].fillna('')).str.strip()
filtered['SchoolName'] = filtered['School'].where(filtered['School'].notna() & (filtered['School'].str.strip() != ''), name_from_parts)

# Communication number (phone)
filtered['CommunicationNumber'] = filtered['Phone']

# Ensure writing score numeric
filtered['AvgScrWrite'] = pd.to_numeric(filtered['AvgScrWrite'], errors='coerce')

# Prepare final columns
result = filtered[['SchoolName', 'AvgScrWrite', 'CommunicationNumber']].dropna(subset=['SchoolName', 'AvgScrWrite'])

# The question asks for the average score in writing for those schools, listing each school's name and its score, plus communication number if any.
# If a single overall average is also desired, compute as:
overall_avg = result['AvgScrWrite'].mean()

# Return both the per-school list and the overall average in a dict-like structure
answer = { 'overall_average_writing_score': overall_avg, 'schools': result }

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
