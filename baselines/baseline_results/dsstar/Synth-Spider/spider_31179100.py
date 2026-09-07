import pandas as pd
import numpy as np

# Input tables are provided in `tables`
df_drivers = tables['table_1'].copy()
df_input1 = tables['table_2'].copy()

# Reproduce parsing logic used in the reference to reconstruct Driver-Vehicle mapping

def try_parse_wide_to_long(obj):
    if isinstance(obj, pd.DataFrame):
        df = obj.copy()
    elif isinstance(obj, dict):
        df = pd.DataFrame(obj)
    elif isinstance(obj, (list, tuple)):
        df = pd.DataFrame(obj)
    else:
        raise ValueError(f"Unsupported object type: {type(obj)}")

    if 'Driver_ID' in df.columns:
        wide = df.set_index('Driver_ID')
        def is_int_like(x):
            try:
                int(x)
                return True
            except Exception:
                return False
        veh_cols = [c for c in wide.columns if is_int_like(c)]
        if len(veh_cols) == 0:
            veh_cols = []
            col_map = {}
            for c in wide.columns:
                if isinstance(c, str):
                    import re
                    m = re.search(r'(\d+)$', c)
                    if m:
                        veh_cols.append(c)
                        col_map[c] = int(m.group(1))
            if veh_cols:
                melted = wide[veh_cols].reset_index().melt(id_vars='Driver_ID', var_name='Vehicle_Col', value_name='val')
                melted['Vehicle_ID'] = melted['Vehicle_Col'].map(lambda x: col_map.get(x, np.nan))
                melted = melted.drop(columns=['Vehicle_Col'])
            else:
                raise ValueError("No vehicle-like columns detected")
        else:
            melted = wide[veh_cols].reset_index().melt(id_vars='Driver_ID', var_name='Vehicle_ID', value_name='val')
            melted['Vehicle_ID'] = melted['Vehicle_ID'].astype(int)

        rel = melted[~melted['val'].isna() & (melted['val'] != 0) & (melted['val'] != False)]
        rel = rel[['Driver_ID', 'Vehicle_ID']].drop_duplicates().sort_values(['Driver_ID', 'Vehicle_ID'])
        return rel.reset_index(drop=True)

    df2 = df.copy()
    if df2.index.name is None:
        maybe_driver_cols = [c for c in df2.columns if str(c).lower() in ('driver_id','driverid','driver')]
        if maybe_driver_cols:
            df2 = df2.set_index(maybe_driver_cols[0])

    def is_int_like(x):
        try:
            int(x)
            return True
        except Exception:
            return False

    veh_cols2 = [c for c in df2.columns if is_int_like(c)]
    if len(veh_cols2) == 0:
        veh_cols2 = []
        col_map = {}
        for c in df2.columns:
            if isinstance(c, str):
                import re
                m = re.search(r'(\d+)$', c)
                if m:
                    veh_cols2.append(c)
                    col_map[c] = int(m.group(1))
        if veh_cols2:
            melted = df2[veh_cols2].reset_index().melt(id_vars=df2.index.name, var_name='Vehicle_Col', value_name='val')
            melted.rename(columns={df2.index.name: 'Driver_ID'}, inplace=True)
            melted['Vehicle_ID'] = melted['Vehicle_Col'].map(lambda x: col_map.get(x, np.nan))
            melted = melted.drop(columns=['Vehicle_Col'])
        else:
            raise ValueError("Could not infer vehicle id columns")
    else:
        melted = df2[veh_cols2].reset_index().melt(id_vars=df2.index.name, var_name='Vehicle_ID', value_name='val')
        melted.rename(columns={df2.index.name: 'Driver_ID'}, inplace=True)
        melted['Vehicle_ID'] = melted['Vehicle_ID'].astype(int)

    melted['Driver_ID'] = pd.to_numeric(melted['Driver_ID'], errors='coerce')

    rel = melted[~melted['val'].isna() & (melted['val'] != 0) & (melted['val'] != False)]
    rel = rel[['Driver_ID', 'Vehicle_ID']].dropna().drop_duplicates().sort_values(['Driver_ID', 'Vehicle_ID'])
    rel['Driver_ID'] = rel['Driver_ID'].astype(int)
    rel['Vehicle_ID'] = rel['Vehicle_ID'].astype(int)
    return rel.reset_index(drop=True)

driver_vehicle_long = try_parse_wide_to_long(df_input1)

# Determine drivers who have not driven any cars
all_drivers = set(pd.to_numeric(df_drivers['Driver_ID'], errors='coerce').dropna().astype(int).tolist())
drivers_with_cars = set(driver_vehicle_long['Driver_ID'].dropna().astype(int).tolist())
drivers_without_cars = sorted(list(all_drivers - drivers_with_cars))

answer_df = pd.DataFrame({'Drivers_Without_Cars_Count': [len(drivers_without_cars)]})

result = {
    'drivers_without_cars_count': answer_df
}