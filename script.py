# imports
import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
from fastf1 import api
from matplotlib.colors import LinearSegmentedColormap


import pandas as pd
import numpy as np

from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

# enables cache, allows storage of race data locally
ff1.Cache.enable_cache('formula/cache')
# patches matplotlib for time delta support
ff1.plotting.setup_mpl(mpl_timedelta_support = True, color_scheme = 'fastf1')

#
#
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

#
#
def get_sectors(average_speed):
    sectors_combined = average_speed.groupby(['Driver', 'Minisector'])['Speed'].mean().reset_index()
    final = pd.DataFrame({
        'Driver': [],
        'Minisector': [],
        'Speed': []
    })
    split_index = int(len(sectors_combined) / 2)

    d1 = sectors_combined[:split_index]
    d2 = sectors_combined[split_index:]

    for i in range(0, len(d1)):
        d1_sector = d1.iloc[[i]].values.tolist()
        d1_speed = d1_sector[0][2]
        d2_sector = d2.iloc[[i]].values.tolist()
        d2_speed = d2_sector[0][2]
        if d1_speed > d2_speed:
            final.loc[len(final)] = d1_sector[0]
        else:
            final.loc[len(final)] = d2_sector[0]

    return final

#
#
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

#
#
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

#
#
def plot_fastest_sectors(race, input_data):
    laps = race.laps
    drivers = [input_data[3].split()[0], input_data[4].split()[0]]

    telemetry = pd.DataFrame()
    
    # list of each driver
    for driver in drivers:
        driver_laps = laps.pick_driver(driver)

        # gets telemetry data for each driver on each lap
        for lap in driver_laps.iterlaps():
            driver_telemtry = lap[1].get_telemetry().add_distance()
            driver_telemtry['Driver'] = driver
            driver_telemtry['Lap'] = lap[1]['LapNumber']

            telemetry = telemetry.append(driver_telemtry)

    # keeping important columns
    telemetry = telemetry[['Lap', 'Distance', 'Driver', 'Speed', 'X', 'Y']]

    # creating minisectors
    total_minsectors = 25 # two above desired 
    total_distance = max(telemetry['Distance'])
    minisector_length = total_distance / total_minsectors
    minisectors = [0]

    # adds minisectors depending on distance of track
    for i in range(0, total_minsectors - 1):
        minisectors.append(minisector_length * (i + 1))

    # no idea
    telemetry['Minisector'] = telemetry['Distance'].apply(
        lambda z: (
            minisectors.index(
                min(minisectors, key = lambda x: abs(x - z))) + 1
        )
    )
    
    average_speed = telemetry.groupby(['Lap', 'Minisector', 'Driver'])['Speed'].mean().reset_index()
    
    
    best_sectors = get_sectors(average_speed)

    best_sectors = best_sectors[['Driver', 'Minisector']].rename(columns = {'Driver': 'fastest_driver'})

    telemetry = telemetry.merge(best_sectors, on = ['Minisector'])
    telemetry = telemetry.sort_values(by = ['Distance'])

    print(telemetry)

    telemetry.loc[telemetry['fastest_driver'] == 'LEC', 'fastest_driver_int'] = 1
    telemetry.loc[telemetry['fastest_driver'] == 'VER', 'fastest_driver_int'] = 2

    
    single_lap = telemetry.loc[telemetry['Lap'] == 1]

    x = np.array(single_lap['X'].values)
    y = np.array(single_lap['Y'].values)

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    dri = single_lap['fastest_driver_int'].to_numpy().astype(float)


    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])

    cmap = cm.get_cmap('ocean', 2)
    lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
    lc_comp.set_array(dri)
    lc_comp.set_linewidth(2)

    plt.rcParams['figure.figsize'] = [12, 5]
    

    plt.suptitle(f"2022 Russian GP \n bla bla bla") #edit

    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    #cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1, 4))
    #cbar.set_ticks(np.arange(1.5, 9.5))
    #cbar.set_ticklabels(['LEC', 'VER'])

    plt.show()


    #laps_d1 = race.laps.pick_driver(input_data[3])
    #laps_d2 = race.laps.pick_driver(input_data[4])


input_data = ['2022', 'Austria', 'Race', 'VER', 'LEC', 'Fastest Sectors']

def main(input_data):
    get_race_data(input_data)

