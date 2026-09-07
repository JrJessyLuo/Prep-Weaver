import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['document_id','category_prefix','connector','topic','document_description']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['document_id','process_id','process_status_code','process_outcome_part1','process_outcome_part2']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['process_id','process_name','process_description']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_documents = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_document_processes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_process_metadata = prepared_table_3

# Assume prepared_documents, prepared_document_processes, prepared_process_metadata are DataFrames

# Build the document title string to match the question
prepared_documents = prepared_documents.assign(document_title=(prepared_documents['category_prefix'].astype(str).str.strip() + ' ' + prepared_documents['connector'].astype(str).str.strip() + ' ' + prepared_documents['topic'].astype(str).str.strip()))

# Filter to the document titled "Travel to Brazil"
doc_filtered = prepared_documents[prepared_documents['document_title'].str.casefold() == 'travel to brazil']

# Join documents to their processes
joined = doc_filtered.merge(prepared_document_processes, on='document_id', how='inner')

# Normalize process_id types for joining
prepared_process_metadata_norm = prepared_process_metadata.copy()
prepared_process_metadata_norm['process_id'] = prepared_process_metadata_norm['process_id'].astype(str).str.replace('"', '').str.strip()
joined['process_id'] = joined['process_id'].astype(str).str.strip()

# Join to process metadata to get process_name
final = joined.merge(prepared_process_metadata_norm[['process_id','process_name']], on='process_id', how='left')

# Select the process_name (deduplicate if multiple rows)
answer = final['process_name'].dropna().unique().tolist()

# If multiple, choose unique names; result variable should be a string or list as needed
result = answer[0] if len(answer) == 1 else answer

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
