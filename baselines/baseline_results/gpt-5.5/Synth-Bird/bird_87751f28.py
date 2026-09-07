import pandas as pd

clients = tables["table_1"].copy()
districts = tables["table_2"].copy()

parts = clients["personal_info"].astype(str).str.split("#", n=2, expand=True)
clients["birth_date"] = pd.to_datetime(parts[1], errors="coerce")
clients["district_id"] = pd.to_numeric(parts[2], errors="coerce").astype("Int64")

clients_1920 = clients[clients["birth_date"].dt.year.eq(1920)]

merged = clients_1920.merge(districts[["district_id", "kraj"]], on="district_id", how="left")
east_bohemia = merged[merged["kraj"].astype(str).str.strip().str.lower().eq("east bohemia")]

count_clients = east_bohemia["client_id"].nunique()

result = {
    "clients_born_1920_in_east_bohemia_count": pd.DataFrame(
        {"num_clients": [count_clients]}
    )
}
