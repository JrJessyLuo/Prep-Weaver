import pandas as pd

students = tables["table_1"].copy()
cities = tables["table_2"].copy()

df = students.merge(cities, how="left", left_on="city_code", right_on="cid")

out = (
    df.groupby(["city_code", "city_name"], as_index=False)
      .agg(number_of_students=("StuID", "nunique"))
      .sort_values(["number_of_students", "city_name"], ascending=[False, True])
      .reset_index(drop=True)
)

result = {"students_per_city": out}
