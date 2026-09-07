import pandas as pd

countries = tables["table_1"]
drivers = tables["table_2"]

dublin_country_ids = countries.loc[countries["Capital"].eq("Dublin"), "Country_Id"]

max_points = drivers.loc[drivers["Country"].isin(dublin_country_ids), "Points"].max()

result = {
    "max_driver_points_from_dublin_capital_country": pd.DataFrame(
        {"max_points": [max_points]}
    )
}
