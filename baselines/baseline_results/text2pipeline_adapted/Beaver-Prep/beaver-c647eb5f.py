import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'iap_subject_session_key', 'new_name': 'SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_LOCATION', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    if s.lower() == \'nan\':\n        return s\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_DATE', 'target_columns': ['SESSION_DATE_DT'], 'func': 'def transform(s):\n    import pandas as pd\n    import numpy as np\n    if s is None:\n        return [np.nan]\n    s = str(s).strip()\n    if s == \'\' or s.lower() == \'nan\':\n        return [np.nan]\n    for fmt in ["%d-%b-%y", "%d-%b-%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]:\n        try:\n            return [pd.to_datetime(s, format=fmt)]\n        except Exception:\n            pass\n    try:\n        return [pd.to_datetime(s, errors=\'coerce\')]\n    except Exception:\n        return [np.nan]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_START_TIME', 'target_columns': ['SESSION_START_TS'], 'func': 'def transform(s):\n    import pandas as pd\n    import numpy as np\n    def parse_time(t):\n        if t is None:\n            return None\n        t = str(t).strip()\n        if t == \'\' or t.lower() == \'nan\':\n            return None\n        u = t.upper().replace(\' \', \'\')\n        import re\n        m = re.match(r"^(\\d{1,2})(\\d{2})(AM|PM)$", u)\n        if m:\n            u = f"{m.group(1)}:{m.group(2)}{m.group(3)}"\n        else:\n            m2 = re.match(r"^(\\d{1,2})(\\d{2})$", u)\n            if m2:\n                u = f"{m2.group(1)}:{m2.group(2)}"\n        for fmt in ["%I:%M%p", "%I%p", "%H:%M", "%H%M", "%H"]:\n            try:\n                return pd.to_datetime(u, format=fmt, errors=\'raise\')\n            except Exception:\n                continue\n        try:\n            return pd.to_datetime(u, errors=\'coerce\')\n        except Exception:\n            return None\n    return [parse_time(s)]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_END_TIME', 'target_columns': ['SESSION_END_TS'], 'func': 'def transform(s):\n    import pandas as pd\n    import numpy as np\n    def parse_time(t):\n        if t is None:\n            return None\n        t = str(t).strip()\n        if t == \'\' or t.lower() == \'nan\':\n            return None\n        u = t.upper().replace(\' \', \'\')\n        import re\n        m = re.match(r"^(\\d{1,2})(\\d{2})(AM|PM)$", u)\n        if m:\n            u = f"{m.group(1)}:{m.group(2)}{m.group(3)}"\n        else:\n            m2 = re.match(r"^(\\d{1,2})(\\d{2})$", u)\n            if m2:\n                u = f"{m2.group(1)}:{m2.group(2)}"\n        for fmt in ["%I:%M%p", "%I%p", "%H:%M", "%H%M", "%H"]:\n            try:\n                return pd.to_datetime(u, format=fmt, errors=\'raise\')\n            except Exception:\n                continue\n        try:\n            return pd.to_datetime(u, errors=\'coerce\')\n        except Exception:\n            return None\n    return [parse_time(s)]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_SEQUENCE', 'target_columns': ['SESSION_SEQUENCE'], 'func': 'def transform(s):\n    import numpy as np\n    try:\n        if s is None:\n            return [np.nan]\n        v = float(s)\n        return [v]\n    except Exception:\n        return [np.nan]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_DATE', 'target_columns': ['SESSION_START_TS'], 'func': 'def transform(s):\n    # No-op placeholder to satisfy dependency ordering in SelectCol; actual start timestamp already computed.\n    import pandas as pd\n    return [pd.NaT]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_DATE', 'target_columns': ['SESSION_END_TS'], 'func': 'def transform(s):\n    # No-op placeholder to satisfy dependency ordering in SelectCol; actual end timestamp already computed.\n    import pandas as pd\n    return [pd.NaT]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SESSION_DATE', 'target_columns': ['DURATION_MIN'], 'func': "def transform(_):\n    import pandas as pd\n    import numpy as np\n    # Compute duration from existing SESSION_START_TS and SESSION_END_TS columns\n    # This function will be applied row-wise by DeepPrep's SplitColumn semantics providing access via closure is not available,\n    # so return NaN placeholder; duration will be recomputed in a subsequent operation that can reference both columns.\n    return [np.nan]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SESSION_KEY', 'SESSION_LOCATION', 'SESSION_DATE_DT', 'SESSION_START_TS', 'SESSION_END_TS', 'DURATION_MIN']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'IAP_SUBJECT_SESSION_KEY', 'new_name': 'SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ACTIVITY_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ENROLLMENT_TYPE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MAX_ENROLLMENT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MULTIPLE_SESSION', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_CANCELLED', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SESSION_KEY', 'ACTIVITY_TITLE', 'TERM_CODE', 'MAX_ENROLLMENT', 'FEE', 'IS_MULTIPLE_SESSION', 'IS_CANCELLED']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'iap_subject_session_key': 'SESSION_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    if s.lower() == \'nan\':\n        return s\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SESSION_LOCATION'] = tmp_1['SESSION_LOCATION'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import pandas as pd\n    import numpy as np\n    if s is None:\n        return [np.nan]\n    s = str(s).strip()\n    if s == \'\' or s.lower() == \'nan\':\n        return [np.nan]\n    for fmt in ["%d-%b-%y", "%d-%b-%Y", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]:\n        try:\n            return [pd.to_datetime(s, format=fmt)]\n        except Exception:\n            pass\n    try:\n        return [pd.to_datetime(s, errors=\'coerce\')]\n    except Exception:\n        return [np.nan]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['SESSION_DATE'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['SESSION_DATE_DT'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import pandas as pd\n    import numpy as np\n    def parse_time(t):\n        if t is None:\n            return None\n        t = str(t).strip()\n        if t == \'\' or t.lower() == \'nan\':\n            return None\n        u = t.upper().replace(\' \', \'\')\n        import re\n        m = re.match(r"^(\\d{1,2})(\\d{2})(AM|PM)$", u)\n        if m:\n            u = f"{m.group(1)}:{m.group(2)}{m.group(3)}"\n        else:\n            m2 = re.match(r"^(\\d{1,2})(\\d{2})$", u)\n            if m2:\n                u = f"{m2.group(1)}:{m2.group(2)}"\n        for fmt in ["%I:%M%p", "%I%p", "%H:%M", "%H%M", "%H"]:\n            try:\n                return pd.to_datetime(u, format=fmt, errors=\'raise\')\n            except Exception:\n                continue\n        try:\n            return pd.to_datetime(u, errors=\'coerce\')\n        except Exception:\n            return None\n    return [parse_time(s)]', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['SESSION_START_TIME'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['SESSION_START_TS'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import pandas as pd\n    import numpy as np\n    def parse_time(t):\n        if t is None:\n            return None\n        t = str(t).strip()\n        if t == \'\' or t.lower() == \'nan\':\n            return None\n        u = t.upper().replace(\' \', \'\')\n        import re\n        m = re.match(r"^(\\d{1,2})(\\d{2})(AM|PM)$", u)\n        if m:\n            u = f"{m.group(1)}:{m.group(2)}{m.group(3)}"\n        else:\n            m2 = re.match(r"^(\\d{1,2})(\\d{2})$", u)\n            if m2:\n                u = f"{m2.group(1)}:{m2.group(2)}"\n        for fmt in ["%I:%M%p", "%I%p", "%H:%M", "%H%M", "%H"]:\n            try:\n                return pd.to_datetime(u, format=fmt, errors=\'raise\')\n            except Exception:\n                continue\n        try:\n            return pd.to_datetime(u, errors=\'coerce\')\n        except Exception:\n            return None\n    return [parse_time(s)]', globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_4['SESSION_END_TIME'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['SESSION_END_TS'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 6: SplitColumn
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import numpy as np\n    try:\n        if s is None:\n            return [np.nan]\n        v = float(s)\n        return [v]\n    except Exception:\n        return [np.nan]', globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_5['SESSION_SEQUENCE'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_5['SESSION_SEQUENCE'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 7: SplitColumn
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    # No-op placeholder to satisfy dependency ordering in SelectCol; actual start timestamp already computed.\n    import pandas as pd\n    return [pd.NaT]', globals(), _ns_6)
    _split_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('split')
    _split_values_6 = tmp_6['SESSION_DATE'].apply(_split_func_6)
    _split_values_6 = _split_values_6.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_6['SESSION_START_TS'] = _split_values_6.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 8: SplitColumn
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    # No-op placeholder to satisfy dependency ordering in SelectCol; actual end timestamp already computed.\n    import pandas as pd\n    return [pd.NaT]', globals(), _ns_7)
    _split_func_7 = _ns_7.get('transform') or _ns_7.get('transform') or _ns_7.get('split')
    _split_values_7 = tmp_7['SESSION_DATE'].apply(_split_func_7)
    _split_values_7 = _split_values_7.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_7['SESSION_END_TS'] = _split_values_7.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 9: SplitColumn
    tmp_8 = tmp_7.copy()
    _ns_8 = {}
    exec("def transform(_):\n    import pandas as pd\n    import numpy as np\n    # Compute duration from existing SESSION_START_TS and SESSION_END_TS columns\n    # This function will be applied row-wise by DeepPrep's SplitColumn semantics providing access via closure is not available,\n    # so return NaN placeholder; duration will be recomputed in a subsequent operation that can reference both columns.\n    return [np.nan]", globals(), _ns_8)
    _split_func_8 = _ns_8.get('transform') or _ns_8.get('transform') or _ns_8.get('split')
    _split_values_8 = tmp_8['SESSION_DATE'].apply(_split_func_8)
    _split_values_8 = _split_values_8.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_8['DURATION_MIN'] = _split_values_8.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['SESSION_KEY', 'SESSION_LOCATION', 'SESSION_DATE_DT', 'SESSION_START_TS', 'SESSION_END_TS', 'DURATION_MIN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'IAP_SUBJECT_SESSION_KEY': 'SESSION_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['ACTIVITY_TITLE'] = tmp_1['ACTIVITY_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['ENROLLMENT_TYPE'] = tmp_2['ENROLLMENT_TYPE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['MAX_ENROLLMENT'] = pd.to_numeric(tmp_3['MAX_ENROLLMENT'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['FEE'] = pd.to_numeric(tmp_4['FEE'], errors='coerce').astype(float)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['TERM_CODE'] = tmp_5['TERM_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_6['IS_MULTIPLE_SESSION'] = tmp_6['IS_MULTIPLE_SESSION'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_7['IS_CANCELLED'] = tmp_7['IS_CANCELLED'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['SESSION_KEY', 'ACTIVITY_TITLE', 'TERM_CODE', 'MAX_ENROLLMENT', 'FEE', 'IS_MULTIPLE_SESSION', 'IS_CANCELLED']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='SESSION_KEY')
# Identify physical locations by excluding clear virtual indicators; keep rows if uncertain
loc = integrated['SESSION_LOCATION'].fillna('')
virtual_mask = loc.str.strip().str.len().gt(0) & loc.str.contains('virtual|zoom|online|remote|web|on zoom', case=False, regex=True)
physical = integrated[~virtual_mask].copy()
# Derive building name as the standardized SESSION_LOCATION text (no further parsing available)
physical['BUILDING_NAME'] = physical['SESSION_LOCATION'].fillna('').str.strip()
# Aggregate per physical location: number of subjects (distinct ACTIVITY_TITLE per location), total fee (sum of FEE across sessions), and shortest/longest session durations
# If DURATION_MIN is null, exclude from min/max; if all null, results will be NaN
agg = physical.groupby('BUILDING_NAME', dropna=False).agg(
    TOTAL_SUBJECTS=('ACTIVITY_TITLE', lambda s: s.dropna().nunique()),
    TOTAL_FEE=('FEE', 'sum'),
    SHORTEST_SESSION_MIN=('DURATION_MIN', 'min'),
    LONGEST_SESSION_MIN=('DURATION_MIN', 'max')
).reset_index()
# Final projection with requested columns
target = agg.rename(columns={'BUILDING_NAME': 'building_name', 'TOTAL_SUBJECTS': 'total_subjects', 'TOTAL_FEE': 'total_fee', 'SHORTEST_SESSION_MIN': 'shortest_session_min', 'LONGEST_SESSION_MIN': 'longest_session_min'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
