import pandas as pd

conf = tables["table_1"].copy()
participants = tables["table_2"].copy()

# count distinct participants per conference
cnt = (
    participants.groupby("conf_id", as_index=False)
    .agg(number_of_participants=("staff_ID", "nunique"))
)

out = (
    conf.merge(cnt, how="left", left_on="Conference_ID", right_on="conf_id")
    .assign(number_of_participants=lambda d: d["number_of_participants"].fillna(0).astype(int))
    [["Conference_Name", "Year", "number_of_participants"]]
)

result = {"conference_participants": out}
