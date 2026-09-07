import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1.copy()
    source['Date'] = pd.to_datetime(source['Date'], errors='coerce')
    target = source[['TransactionID','Date','Time','GasStationID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    filtered = table_1.loc[table_1['GasStationID'].eq('ChainID'), ['StationID', 'Value']]
    target = filtered.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_station_metadata = prepared_table_2

# Assume prepared_transactions and prepared_station_metadata are provided by BAT per the target schemas.

# If station metadata contains multiple attributes, first select the attribute that represents country.
# In the provided schema, table_2 encodes attributes with a name in the original GasStationID column.
# We expect BAT to have already filtered to rows where the attribute name corresponds to country (e.g., 'Country'),
# but if not, attempt to infer by common attribute names.

station_meta = prepared_station_metadata.copy()
# If the metadata still includes mixed attributes, you would filter by an attribute column.
# Here we assume 'Value' holds country for each StationID.
station_meta = station_meta.rename(columns={"Value": "Country"})

# Merge transactions with station country
tx = prepared_transactions.merge(station_meta, left_on="GasStationID", right_on="StationID", how="left")

# Filter to the target date
tx["Date"] = pd.to_datetime(tx["Date"])  # ensure datetime
subset = tx[tx["Date"].dt.date == pd.to_datetime("2012-08-25").date()].copy()

# Build a sortable timestamp
subset["Time"] = pd.to_datetime(subset["Time"], format="%H:%M:%S", errors="coerce").dt.time
subset = subset.sort_values(["Date", "Time", "TransactionID"]).reset_index(drop=True)

# Take the first paid customer of the day (earliest transaction)
first_row = subset.iloc[0] if len(subset) > 0 else None

# Produce final answer: country of the gas station for that first transaction
answer = None if first_row is None else first_row.get("Country", None)

result = {"answer": answer}

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
