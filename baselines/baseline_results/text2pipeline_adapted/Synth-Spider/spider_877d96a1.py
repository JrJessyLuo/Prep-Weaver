import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'PassThroughFallback', 'params': {'reason': 'fallback_passthrough_after_pipeline_generation_failure: Your previous one-table transform_chain was invalid: ValueError: operation(s) outside benchmark dc_ops space: Filter. Use only table_indices [0], correct the chain, and return JSON only.', 'source_table': 'table_1'}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'city_code', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['city_code', 'city_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['city_code'] = tmp_0['city_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['city_code', 'city_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
_frames = []
if isinstance(prepared_table_1, pd.DataFrame) and not prepared_table_1.empty:
    _tmp = prepared_table_1.copy()
    _tmp['__prepared_table__'] = 'prepared_table_1'
    _frames.append(_tmp)
if isinstance(prepared_table_2, pd.DataFrame) and not prepared_table_2.empty:
    _tmp = prepared_table_2.copy()
    _tmp['__prepared_table__'] = 'prepared_table_2'
    _frames.append(_tmp)
target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
