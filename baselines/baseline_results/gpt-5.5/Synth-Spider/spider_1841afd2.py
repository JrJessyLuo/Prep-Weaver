import pandas as pd

clients = tables["table_1"]
invoices = tables["table_2"]
meetings = tables["table_3"]

eligible_client_ids = pd.Index(
    pd.concat(
        [
            invoices["client_id"].dropna(),
            meetings["client_id"].dropna(),
        ],
        ignore_index=True,
    ).unique()
)

out = clients[clients["client_id"].isin(eligible_client_ids)].copy()
out = out.drop_duplicates(subset=["client_id"]).reset_index(drop=True)

result = {
    "clients_with_meeting_or_invoice": out[
        ["client_id", "agency_id", "sic_code", "detail_part1", "detail_part2"]
    ]
}
