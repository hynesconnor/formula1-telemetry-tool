# imports
import os
import matplotlib
import numpy as np
import pandas as pd
import fastf1 as ff1
from fastf1 import api
from fastf1 import utils
from fastf1 import plotting
from matplotlib.lines import Line2D
from matplotlib import pyplot as plt
#from matplotlib.pyplot import figure, ylabel
from matplotlib.collections import LineCollection

# enables cache, allows storage of race data locally
ff1.Cache.enable_cache('/cache')

# patches matplotlib for time delta support
ff1.plotting.setup_mpl(mpl_timedelta_support = True, color_scheme = 'fastf1')

# gets race data from fastf1 based on input data parameter
# runs appropriate plot function based on user input
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
    elif input_data[5] == 'Full Telemetry':
        plot_full_telemetry(race, input_data)

# takes in speed/distance data for both drivers and determines which is faster
# returns dataframe of which driver was the fastest in each sector
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

# plots a laptime/distance comparison for both specified drivers
# returns a saved version of the generated plot
def plot_laptime(race, input_data):
    plt.clf()
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

    img_path = os.getcwd() + (f'/plot/{input_data[5]}.png')
    plt.savefig(img_path, dpi = 200)


# speed comaprison by distance for the fastest lap of both drivers
# returns a saved version of the generated plot
def plot_fastest_lap(race, input_data):
    plt.clf()
    d1 = input_data[3].split()[0]
    d2 = input_data[4].split()[0]

    fastest_d1 = race.laps.pick_driver(d1).pick_fastest()
    fastest_d2 = race.laps.pick_driver(d2).pick_fastest()

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

    img_path = os.getcwd() + (f'/plot/{input_data[5]}.png')
    plt.savefig(img_path, dpi = 700)


# compares the sector speeds for each driver, and generates a map of the circuit, with color coded sectors for the fastest driver.
# returns a saved version of the generated plot
def plot_fastest_sectors(race, input_data):
    plt.clf()
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
    total_minisectors = 25 # two above desired 
    telemetry['Minisector'] = pd.cut(telemetry['Distance'], total_minisectors, labels = False) + 1
    
    average_speed = telemetry.groupby(['Lap', 'Minisector', 'Driver'])['Speed'].mean().reset_index()
    
    # calls function to returns fastest driver in each sector
    best_sectors = get_sectors(average_speed)
    best_sectors = best_sectors[['Driver', 'Minisector']].rename(columns = {'Driver': 'fastest_driver'})

    # merges telemetry df with minisector df
    telemetry = telemetry.merge(best_sectors, on = ['Minisector'])
    telemetry = telemetry.sort_values(by = ['Distance'])

    telemetry.loc[telemetry['fastest_driver'] == input_data[3].split()[0], 'fastest_driver_int'] = 1
    telemetry.loc[telemetry['fastest_driver'] == input_data[4].split()[0], 'fastest_driver_int'] = 2
    
    # gets x,y data for a single lap. useful for drawing circuit.
    # x,y values can be inconsistent, causing strange behavior.
    single_lap = telemetry.loc[telemetry['Lap'] == 1]
    lap_x = np.array(single_lap['X'].values)
    lap_y = np.array(single_lap['Y'].values)

    # points and segments for drawing lap
    points = np.array([lap_x, lap_y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # grabs which driver (1/2) is fastest # POTENTIAL PROBLEM, ENSURE THIS IS BEST SECTOR DATA
    which_driver = single_lap['fastest_driver_int'].to_numpy().astype(float)

    # getting colormap for two drivers
    color1 = ff1.plotting.driver_color(input_data[3])
    color2 = ff1.plotting.driver_color(input_data[4])
    color1 = matplotlib.colors.to_rgb(color1)
    color2 = matplotlib.colors.to_rgb(color2)
    colors = [color1, color2]
    cmap = matplotlib.colors.ListedColormap(colors)

    lc_comp = LineCollection(segments, norm = plt.Normalize(1, cmap.N), cmap = cmap) #  norm = plt.Normalize(1, cdict.N+1)
    lc_comp.set_array(which_driver)
    lc_comp.set_linewidth(2)

    plt.rcParams['figure.figsize'] = [6.25, 4.70]
    plt.suptitle(f"Average Fastest Sectors \n" f"{race.event['EventName']} {race.event.year} {input_data[2]}") #edit
    plt.gca().add_collection(lc_comp)
    plt.axis('equal')
    plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

    legend_lines = [Line2D([0], [0], color = color1, lw = 1),
                    Line2D([0], [0], color = color2, lw = 1)]

    plt.legend(legend_lines, [input_data[3], input_data[4]])

    img_path = os.getcwd() + (f'/plot/{input_data[5]}.png')
    plt.savefig(img_path, dpi = 200)

# plots a speed, throttle, brake, rpm, gear, and drs comparison for both drivers
# returns a saved version of the generated plot
def plot_full_telemetry(race, input_data): # speed, throttle, brake, rpm, gear, drs 
    plt.clf()
    d1 = input_data[3].split()[0]
    d2 = input_data[4].split()[0]

    fastest_d1 = race.laps.pick_driver(d1).pick_fastest()
    fastest_d2 = race.laps.pick_driver(d2).pick_fastest()

    tel_d1 = fastest_d1.get_car_data().add_distance()
    tel_d1['Brake'] = tel_d1['Brake'].astype(int)
    tel_d2 = fastest_d2.get_car_data().add_distance()
    tel_d2['Brake'] = tel_d2['Brake'].astype(int)

    telem_data_combined = [tel_d1, tel_d2]
    colors = [ff1.plotting.driver_color(input_data[3]), ff1.plotting.driver_color(input_data[4])]

    fig, ax = plt.subplots(6)
    for telem, color in zip(telem_data_combined, colors):
        ax[0].plot(telem['Distance'], telem['Speed'], color = color, linewidth = .75)
        ax[1].plot(telem['Distance'], telem['Throttle'], color = color, linewidth = .75)
        ax[2].plot(telem['Distance'], telem['Brake'], color = color, linewidth = .75) # might have to convert to binary 
        ax[3].plot(telem['Distance'], telem['RPM'], color = color, linewidth = .75)
        ax[4].plot(telem['Distance'], telem['nGear'], color = color, linewidth = .75)
        ax[5].plot(telem['Distance'], telem['DRS'], color = color, linewidth = .75)

    ax[0].set(ylabel = 'Speed')
    ax[1].set(ylabel = 'Throttle')
    ax[2].set(ylabel = 'Brake')
    ax[3].set(ylabel = 'RPM')
    ax[4].set(ylabel = 'Gear')
    ax[5].set(ylabel = 'DRS')

    plt.suptitle(f"Fastest Lap Telemetry - {input_data[3]} vs {input_data[4]} \n {race.event['EventName']} {race.event.year} {input_data[2]}")

    legend_lines = [Line2D([0], [0], color = colors[0], lw = 1),
        Line2D([0], [0], color = colors[1], lw = 1)]

    plt.legend(legend_lines, [input_data[3], input_data[4]])

    img_path = os.getcwd() + (f'/plot/{input_data[5]}.png')
    plt.savefig(img_path, dpi = 200)
