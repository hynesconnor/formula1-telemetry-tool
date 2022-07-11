# imports
import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1 import api

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# enables cache, allows storage of race data locally
ff1.Cache.enable_cache('formula/cache')
# patches matplotlib for time delta support
ff1.plotting.setup_mpl(mpl_timedelta_support = True, color_scheme = 'fastf1')



YEAR = 2022
GRAND_PRIX = 'Austria' 
SESSION = 'R' # 'FP1', 'FP2', 'FP3', 'Q', 'S', 'SQ', 'R'

driver1 = 'LEC'
driver2 = 'SAI'

def get_race_data():
    race = ff1.get_session(YEAR, GRAND_PRIX, SESSION)
    race.load()
    return race

def plot_laptime(race):
    laps_d1 = race.laps.pick_driver(driver1)
    laps_d2 = race.laps.pick_driver(driver2)

    color1 = ff1.plotting.driver_color(driver1)
    color2 = ff1.plotting.driver_color(driver2)

    fig, ax = plt.subplots()

    ax.plot(laps_d1['LapNumber'], laps_d1['LapTime'], color = color1, label = driver1)
    ax.plot(laps_d2['LapNumber'], laps_d2['LapTime'], color = color2, label = driver2)

    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')

    ax.legend()
    plt.suptitle(f"Lap Time Comparison \n" f"{race.event['EventName']} {race.event.year}")

    plt.show()


def main():
    race = get_race_data()
    plot_laptime(race)

main()
