# Formula 1 Telemetry Analysis Tool
A fast, GUI based application, to gain insights into Formula 1 telemetry data.

Query every race and each driver for the 2018-2022 racing seasons. Built leveraging theOehrly's [FastF1](https://github.com/theOehrly/Fast-F1) python package for race data and [PyQt5](https://pypi.org/project/PyQt5/) for the GUI. Currently tested on Windows based operating systems.

![](/mkdwn/main_screen.png)
# Installation and Configuration
- Clone the repository to a folder of choice
- Using cmd and pip, navigate to the repository directory and run the following command to install necessary packages: `pip install -r requirements.txt`
- Run `gui.py` to start the program.
- The proper file directory will be created, and the GUI pictured above will open. You can begin running analyses.
- Each time you want to launch the program, run `gui.py`.
- The program makes use of a cache system, allowing it to access previously queried race data. This data can be found in the `/cache` folder and cleared if the file size becomes too large. 
- Compatible with python v3.7 - 3.10.

# Usage
- To run an analysis, select your desired **year, grand prix location, session, driver 1, driver 2,** and finally the **type of analysis**.
- Click the **'Run Analysis'** button to begin and wait for the generated plot to appear on the right of the panel.
- This tool currently supports four analysis functions: **Lap Time, Fastest Lap, Fastest Sectors, and Full Telemetry**.
- Once the plot is displayed, you can click the **'Save Plot to Desktop'** button to save a .png version to your desktop.
    - Important for getting a better view of the plot.
- There is no need to reset the program after analysis. Continue to adjust parameters and generate plots as desired.

# Examples
1) A fastest lap comparison of the 2022 Austrian Grand Prix Race between Esteban Ocon and Carlos Sainz:
![](/mkdwn/fastestlap.png)

2) A fastest sectors comparison of the 2022 Bahrain Gran Prix Race between Lewis Hamilton and Lando Norris:
![](/mkdwn/sectors3.png)

3) A full telemetry comparison of the 2022 Austrian Grand Prix Race between Charles Leclerc and Lewis Hamilton:
![](/mkdwn/fulltelem.png)
