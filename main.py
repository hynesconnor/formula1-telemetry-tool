# imports
import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1 import api

import pandas as pd
import numpy as np
import datetime

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# enables cache, allows storage of race data locally
ff1.Cache.enable_cache('formula/cache')

# patches matplotlib for time delta support! wow!
ff1.plotting.setup_mpl(mpl_timedelta_support = True, color_scheme = 'fastf1')

year = 2022
grand_prix = 'Austria' # 'FP1', 'FP2', 'FP3', 'Q', 'S', 'SQ', 'R'
session = 'R'


race = ff1.get_session(year, grand_prix, session)
race.load()

driver1 = 'RIC' # ['HAM' 'VER' 'BOT' 'LEC' 'OCO' 'SAI' 'RIC' 'PER' 'NOR' 'ALO' 'STR' 'GAS'
                #'VET' 'GIO' 'RUS' 'TSU' 'RAI' 'MSC' 'LAT' 'MAZ']
driver2 = 'NOR'

laps_d1 = race.laps.pick_driver(driver1)
laps_d2 = race.laps.pick_driver(driver2)

print(laps_d1['LapTime'])
print(laps_d1.columns)

# plotting

color1 = ff1.plotting.team_color('FER')
color2 = ff1.plotting.team_color('RBR')

fig, ax = plt.subplots()


ax.plot(laps_d1['LapNumber'], laps_d1['LapTime'], color = color1, label = driver1)
ax.plot(laps_d2['LapNumber'], laps_d2['LapTime'], color = color2, label = driver2)

ax.set_xlabel('Lap Number')
ax.set_ylabel('Lap Time')

ax.legend()
plt.suptitle(f"Lap Time Comparison \n" f"{race.event['EventName']} {race.event.year}")

plt.show()





