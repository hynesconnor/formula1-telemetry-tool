# Formula 1 Telemetry Analysis Tool
A fast, GUI based application, to gain insights into Formula 1 telemetry data.

Query every race and each driver for the 2018-2023 racing seasons. Built leveraging theOehrly's [FastF1](https://github.com/theOehrly/Fast-F1) python package for race data and [PyQt5](https://pypi.org/project/PyQt5/) for the GUI. Currently tested on Windows based operating systems.

![](/mkdwn/demo.gif)

The goal of this project is to provide a simple way to gather driver data for each race. Formula 1 only provides some data for each race such as basic performance metrics, tire history, and lap charts. This is not detailed enough and requires the use of an account.

At the end of each race, Formula 1 releases race data which FastF1 has been built to access. Having direct access to these statistics allows fully customizable methods of analyzing and comparing driver performance. Building this application with a GUI also makes it much faster to generate statistics, especially when you want to quickly switch drivers, races, and analysis types, avoiding the need to constantly edit scripts.

## Installation and Configuration
- Download the latest release [here](https://github.com/hynesconnor/formula1_telemetry_tool/releases).
- Using cmd and pip, navigate to the repository directory and run the following command to install necessary packages: `pip install -r requirements.txt`
- Run `gui.py` to start the program.
- The proper file directory will be created, and the GUI pictured above will open. You can begin running analyses.
- Each time you want to launch the program, run `gui.py`.
- The program makes use of a cache system, allowing it to access previously queried race data. This data can be found in the `/cache` folder and cleared if the file size becomes too large. 
- Compatible with python v3.7 - 3.10.

## Usage
- To run an analysis, select your desired **year, grand prix location, session, driver 1, driver 2,** and finally the **type of analysis**.
- Click the **'Run Analysis'** button to begin and wait for the generated plot to appear on the right of the panel.
- This tool currently supports four analysis functions: **Lap Time, Fastest Lap, Fastest Sectors, and Full Telemetry**.
- Once the plot is displayed, you can click the **'Save Plot to Desktop'** button to save a .png version to your desktop.
    - Important for getting a better view of the plot.
- There is no need to reset the program after analysis. Continue to adjust parameters and generate plots as desired.

## Examples
1) A fastest lap comparison for the 2022 Austrian Grand Prix Race between Esteban Ocon and Carlos Sainz:

![](/mkdwn/fastestlap.png)

2) A lap 21 fastest sectors comparison for the 2022 Bahrain Gran Prix Race between Lewis Hamilton and Lando Norris:

![](/mkdwn/sectors3.png)

3) A full telemetry comparison of the 2022 Austrian Grand Prix Race between Charles Leclerc and Lewis Hamilton:

![](/mkdwn/fulltelem.png)

## Limitations and Issues

- F1 car data is not always complete. This means that depending on the session/track/driver, data will sometimes be missing or incorrect. This could be caused by a number of things like sensor failure, crashes, irregular driving, etc. It tends to be clear where data is incorrect as graphs will generate with sharp lines or missing sections. I've found these issues to be more plentiful with Free Practice sessions. Race sessions tend to have more complete data. 

- When generating average fastest sectors do keep in mind that incorrect plot generation, especially on lap 1 where driving tends to be more erratic, can occur. The plot is drawn using X and Y values coming directly from sensors on the car. This means that if a driver was to go off track, an area will be drawn that is not part of the race track. The same can be seen on lap 1 in the starting area, which is not drawn.

- There is currently an error with the DRS plot on the full telemetry analysis. Working on a fix for this. DRS data is supposed to be a binary but sometimes values are reported as fractional. 

- To make plots more readable, consider downloading to the desktop to view them at a higher DPI. Currently, the plots displayed in app suffer visually do to downscaling. Working on a fix.
