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

def get_race_data(input_data):

    #['2022', 'Austria', 'FP1', 'VER', 'VER', 'Lap Time']

    race = ff1.get_session(int(input_data[0]), input_data[1], input_data[2])
    race.load()

    if input_data[5] == 'Lap Time':
        plot_laptime(race, input_data)
    elif input_data == 'Fastest Lap':
        plot_fastest_lap(race, input_data)


def plot_laptime(race, input_data):
    laps_d1 = race.laps.pick_driver(input_data[3])
    laps_d2 = race.laps.pick_driver(input_data[4])

    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])

    fig, ax = plt.subplots()

    ax.plot(laps_d1['LapNumber'], laps_d1['LapTime'], color = color1, label = input_data[3])
    ax.plot(laps_d2['LapNumber'], laps_d2['LapTime'], color = color2, label = input_data[4])

    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')

    ax.legend()
    plt.suptitle(f"Lap Time Comparison \n" f"{race.event['EventName']} {race.event.year}")

    plt.show()

def plot_fastest_lap(race, input_data):
    laps_d1 = race.laps.pick_driver(input_data[3])
    laps_d2 = race.laps.pick_driver(input_data[4])

    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])

    fig, ax = plt.subplots()


def main(input_data):
    get_race_data(input_data)


