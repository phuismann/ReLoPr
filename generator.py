import pandas as pd
from pandas import DataFrame
import numpy as np
from datetime import datetime
import holidays


x_4 = -3.92E-10
x_3 = 3.20E-07
x_2 = -7.02E-05
x_1 = 2.10E-03
x_0 = 1.24


def generate_lp(demand: float = 1000, year: int = 2019, country_holidays=None) -> DataFrame:
    """
    Function to generate a household load profile for a given year and specific country holidays.
    :param demand: Yearly electricity demand (kWh/a)
    :param year: Year to generate the load profile for
    :param country_holidays: holiday library object
    :returns df: DataFrame containing the Electricity demand
        columns:
            time: DateTime
            profile: Demand in W for each quarter of an hour
    """

    if country_holidays is None:
        print("You should pass a holiday object f. e. holidays.DE(state='NW')")
        country_holidays = holidays.DE(state="NW")

    origin = pd.Timestamp(f"{2019}-01-01")
    df = pd.DataFrame({"day": [i + 0 for i in range(365)]})
    df["day"] = pd.to_datetime(df["day"], unit="D", origin=origin)
    df["weekday"] = df["day"].map(lambda x: x.strftime("%A"))
    df["is_holiday"] = df["day"].map(lambda x: x in country_holidays)
    df["holiday"] = df["day"].map(lambda x: country_holidays.get(x))

    def convert_to_actual_day(row):
        is_holiday = row["is_holiday"]
        weekday = row["weekday"]
        holiday = row["holiday"]
        if is_holiday and holiday != "Neujahr":
            return "sunday"
        elif is_holiday and holiday == "Neujahr":
            return "saturday"
        elif weekday == "Saturday" or weekday == "Sunday":
            return weekday.lower()
        else:
            return "weekday"
        
    df["actual_weekday"] = df.apply(convert_to_actual_day, axis=1)

    lookup = pd.read_excel("./loadprofile_generator.xlsx")

    def set_time_of_year(row):
        day = row["day"]
        if datetime(year=year - 1, month=11, day=1) < day < datetime(year=year, month=3, day=20):
            return "winter"
        elif datetime(year=year, month=5, day=15) < day < datetime(year=year, month=9, day=14):
            return "summer"
        elif datetime(year=year, month=11, day=1) < day:
            return "winter"
        else:
            return "transition"

    df["timeOfYear"] = df.apply(set_time_of_year, axis=1)
    
    f_t = lambda t: x_4*t**4+x_3*t**3+x_2*t**2+x_1*t+x_0
    
    for i in range(96):
        df[i] = 0
    
    for i, row in df.iterrows():
        time_of_year = row["timeOfYear"]
        actual_weekday = row["actual_weekday"]
        for ii in range(96):
            val = lookup[time_of_year+"_"+actual_weekday].iloc[ii]
            df.loc[i, ii] = val*f_t(i)

    for i in range(96):
        df[i] *= demand / 1000

    profile = []
    for i, row in df.iterrows():
        vals = row[range(96)]
        profile += list(vals)

    time = pd.to_datetime(np.array(range(len(profile))) * 15 * 60, unit='s', origin=origin)
    df = pd.DataFrame(data={"time": time, "profile": profile})
    print(df["profile"].sum() / 4 / 1000, "kWh/a")
    return df
