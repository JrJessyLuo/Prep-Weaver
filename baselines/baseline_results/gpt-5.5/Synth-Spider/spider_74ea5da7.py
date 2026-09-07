import pandas as pd

students = tables["table_1"].copy()
cities = tables["table_2"].copy()

students["first_name"] = students["Fname_part1"].fillna("").astype(str) + students["Fname_part2"].fillna("").astype(str)

md_students = students.merge(cities[["city_code", "state"]], on="city_code", how="left")
md_students = md_students[md_students["state"].eq("MD")]

out = md_students[["first_name", "LName"]].rename(columns={"LName": "last_name"}).reset_index(drop=True)

result = {"students_in_md": out}
