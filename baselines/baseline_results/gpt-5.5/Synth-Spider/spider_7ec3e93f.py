import pandas as pd

# Tables
addr_types = tables["table_1"].copy()
student_addr_raw = tables["table_2"].copy()

# Clean address type lookup
addr_types["address_type_code"] = addr_types["address_type_code"].astype(str).str.strip()
addr_types["address_type_description"] = addr_types["address_type_description"].astype(str).str.strip()

# table_2 is transposed: rows are field names, columns are records -> transpose to normal form
student_addr = (
    student_addr_raw
    .set_index("student_address_id")
    .T
    .reset_index(drop=True)
)

# Most common address_type_code
student_addr["address_type_code"] = student_addr["address_type_code"].astype(str).str.strip()
most_common_code = student_addr["address_type_code"].value_counts(dropna=True).idxmax()

# Return code + description
out = (
    pd.DataFrame({"address_type_code": [most_common_code]})
    .merge(addr_types, on="address_type_code", how="left")
    [["address_type_code", "address_type_description"]]
)

result = {"most_common_student_address_type": out}
