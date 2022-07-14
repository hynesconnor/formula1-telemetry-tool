import sys
import os
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import threading
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QPushButton
import script
import pandas as pd

# CONSTANTS
CWD = os.getcwd()

events = pd.read_csv(CWD + '/formula/data/events.csv')
drivers = pd.read_csv(CWD + '/formula/data/drivers.csv')
placeholder_path = CWD + '/formula/img/placeholder.png'
#plot_path = CWD + '/formula/plot/plot.png'

# list of years
year = events.columns
year = year[1:len(year)].to_list()
year.insert(0, 'Select Year')


driver_name = drivers

location = ['Select Location']
session = ['FP1','FP2', 'FP3', 'Sprint Qualifying', 'Sprint', 'Qualifying', 'Race']
driver_name = ['Select Driver']
analysis_type = ['Lap Time', 'Fastest Lap', 'Fastest Sectors']


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.UIComponents()

    def initUI(self):
        self.setFixedSize(880, 500)
        self.move(200, 100)
        self.setWindowTitle('Formula 1 Analytics')
        self.setWindowIcon(QtGui.QIcon(CWD + '/formula/img/f1.png'))

    def UIComponents(self):
        options_layout = QVBoxLayout()
        img_layout = QHBoxLayout()
        img_layout.addLayout(options_layout)

        self.drop_year = QComboBox()
        self.drop_grand_prix = QComboBox()
        self.drop_session = QComboBox()
        self.drop_driver1 = QComboBox()
        self.drop_driver2 = QComboBox()
        self.drop_analysis = QComboBox()

        label_year = QLabel('Year:')
        label_prix = QLabel('Grand Prix Location:')
        label_session = QLabel('Session:')
        label_d1 = QLabel('Driver 1:')
        label_d2 = QLabel('Driver 2:')
        label_analysis = QLabel('Analysis Type:')

        self.run_button = QPushButton('Run Analysis')

        self.drop_year.addItems(year)
        self.drop_grand_prix.addItems(location)
        self.drop_session.addItems(session)
        self.drop_driver1.addItems(driver_name)
        self.drop_driver2.addItems(driver_name)
        self.drop_analysis.addItems(analysis_type)

        options_layout.addWidget(label_year)

        options_layout.addWidget(self.drop_year)
        options_layout.addWidget(label_prix)
        options_layout.addWidget(self.drop_grand_prix)
        options_layout.addWidget(label_session)
        options_layout.addWidget(self.drop_session)
        options_layout.addWidget(label_d1)
        options_layout.addWidget(self.drop_driver1)
        options_layout.addWidget(label_d2)
        options_layout.addWidget(self.drop_driver2)
        options_layout.addWidget(label_analysis)
        options_layout.addWidget(self.drop_analysis)
        options_layout.addWidget(self.run_button)

        #self.drop_year.activated.connect(self.update_lists)
        self.drop_year.currentTextChanged.connect(self.update_lists)
        
        self.run_button.clicked.connect(self.thread)

        self.img_plot = QLabel()
        self.img_plot.setPixmap(QPixmap(placeholder_path).scaledToWidth(625))
        img_layout.addWidget(self.img_plot)

        self.setLayout(img_layout)
        self.show()

        
    # listens for change in inputs, responds to each change with updated list of desired inputs.
    def current_text(self):
        input_data = []
        text = self.drop_year.currentText()
        input_data.append(text)
        text = self.drop_grand_prix.currentText()
        input_data.append(text)
        text = self.drop_session.currentText()
        input_data.append(text)
        text = self.drop_driver1.currentText()
        input_data.append(text)
        text = self.drop_driver2.currentText()
        input_data.append(text)
        text = self.drop_analysis.currentText()
        input_data.append(text)
        return input_data

    def display_plot(self, plot_path):
        self.img_plot.setPixmap(QPixmap(plot_path).scaledToWidth(625))
  
    # testing thread, repurpose for loading indicator
    def thread(self):
        thread_script = threading.Thread(target = self.button_listen)
        thread_script.start()

    # listens for button press, runs main script, 
    def button_listen(self):
        input_data = self.current_text()
        print(input_data)
        script.get_race_data(input_data)
        plot_path = os.getcwd() + (f'/formula/plot/{input_data[5]}.png')
        self.display_plot(plot_path)
        

    def update_lists(self): # update comboboxes drop_grand_prix, drop_driver1, drop_driver2
        self.drop_grand_prix.clear()
        self.drop_driver1.clear()
        self.drop_driver2.clear()
        sel_year = self.drop_year.currentText()
        self.drop_grand_prix.addItems(events[str(sel_year)].dropna().to_list())
        self.drop_driver1.addItems(drivers[str(sel_year)].dropna().to_list())
        self.drop_driver2.addItems(drivers[str(sel_year)].dropna().to_list())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())

