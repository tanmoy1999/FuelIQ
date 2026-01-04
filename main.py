#%% Import Libs
import pandas as pd
from datetime import datetime

#%% Functions

def get_bool(prompt):
    while True:
        val = input(prompt).strip().lower()
        if val in ("y", "yes"):
            return True
        if val in ("n", "no"):
            return False
        print("Invalid input. Enter y/n.")

#%% create df
df = pd.DataFrame()
df = pd.DataFrame(columns=["date","fuel_price","amount","total_distance_covered", "fuel_filled","full_tank_flag"])
#%% get values and set constants
date = datetime.now().date()
fuel_price = float(input('Price of Fuel: '))
amount = float(input('Amount Paid: '))
total_distance_covered = float(input('Total Distance Covered: '))
fuel_filled = 0.0
full_tank_flag = get_bool("Full tank? (y/n): ")

#%% calculate
fuel_filled = round(amount/fuel_price,2)

#%% put it in df

df.loc[len(df)] = [date,fuel_price,amount,total_distance_covered,fuel_filled,full_tank_flag]
df

#%% final json
df.to_json(orient="records",date_format="iso")

#%% export



# %%
