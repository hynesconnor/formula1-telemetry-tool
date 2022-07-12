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
    elif input_data[5] == 'Fastest Lap':
        plot_fastest_lap(race, input_data)
    elif input_data[5] == 'Fastest Sectors':
        plot_fastest_sectors(race, input_data)

def plot_laptime(race, input_data):
    d1 = input_data[3].split()[0]
    d2 = input_data[4].split()[0]

    laps_d1 = race.laps.pick_driver(d1)
    laps_d2 = race.laps.pick_driver(d2)

    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])

    fig, ax = plt.subplots()

    ax.plot(laps_d1['LapNumber'], laps_d1['LapTime'], color = color1, label = input_data[3])
    ax.plot(laps_d2['LapNumber'], laps_d2['LapTime'], color = color2, label = input_data[4])

    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time')

    ax.legend()
    plt.suptitle(f"Lap Time Comparison \n" f"{race.event['EventName']} {race.event.year} {input_data[2]}")

    plt.show()

def plot_fastest_lap(race, input_data):
    fastest_d1 = race.laps.pick_driver(input_data[3]).pick_fastest()
    fastest_d2 = race.laps.pick_driver(input_data[4]).pick_fastest()

    tel_d1 = fastest_d1.get_car_data().add_distance()
    tel_d2 = fastest_d2.get_car_data().add_distance()

    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])

    fig, ax = plt.subplots()

    ax.plot(tel_d1['Distance'], tel_d1['Speed'], color = color1, label = input_data[3])
    ax.plot(tel_d2['Distance'], tel_d2['Speed'], color = color2, label = input_data[4])

    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('Speed (km/h)')
    ax.legend()
    plt.suptitle(f"Fastest Lap Comparison \n" f"{race.event['EventName']} {race.event.year} {input_data[2]}")

    plt.show()

def plot_fastest_sectors(race, input_data):
    laps = race.laps
    
    laps['RaceLapNumber'] = laps['LapNumber'] - 1

    drivers = [input_data[3].split()[0], input_data[4].split()[0]]

    telemetry = pd.DataFrame()

    for driver in drivers:
        driver_laps = laps.pick_driver(driver)

        for lap in driver_laps.iterlaps():
            driver_telemtry = lap[1].get_telemetry().add_distance()
            driver_telemtry['Driver'] = driver
            driver_telemtry['Lap'] = lap[1]['RaceLapNumber']

            telemetry = telemetry.append(driver_telemtry)

    telemetry = telemetry[['Lap', 'Distance', 'Driver', 'Speed', 'X', 'Y']]


    total_minsectors = 25 # two above desired 

    total_distance = max(telemetry['Distance'])

    minisector_length = total_distance / total_minsectors

    minisectors = [0]

    for i in range(0, total_minsectors - 2):
        minisectors.append(minisector_length * (i + 1))

    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda z: (
            minisectors.index(
                min(minisectors, key = lambda x: abs(x - z))) + 1
        )
    )

    average_speed = telemetry.groupby(['Lap', 'Minisector', 'Driver'])['Speed'].mean().reset_index()

    #average_speed_lap = average_speed.groupby([])

    average_speed.to_csv('C:/Users/Connor/Desktop/formula_one/formula/data/telem.csv')
    print(average_speed)




    #laps_d1 = race.laps.pick_driver(input_data[3])
    #laps_d2 = race.laps.pick_driver(input_data[4])

    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])



    #for driver in drivers:












    
    print('temp')

input_data = ['2022', 'Austria', 'Race', 'VER', 'LEC', 'Fastest Sectors']

def main(input_data):
    get_race_data(input_data)

main(input_data)
