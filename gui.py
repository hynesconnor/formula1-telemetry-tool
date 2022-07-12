import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import script
import pandas as pd

# CONSTANTS
CWD = os.getcwd()

events = pd.read_csv(CWD + '/formula/data/events.csv')
drivers = pd.read_csv(CWD + '/formula/data/drivers.csv')

# list of years
year = events.columns
year = year[1:len(year)].to_list()
year.insert(0, 'Select Year')


driver_name = drivers

location = ['Select Location']
session = ['FP1','FP2', 'FP3', 'Sprint Qualifying', 'Sprint', 'Qualifying', 'Race']
driver_name = ['Select Driver']
analysis_type = ['Lap Time', 'Fastest Lap']


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.UIComponents()

    def initUI(self):
        self.setFixedSize(560, 320)
        self.move(200, 100)
        self.setWindowTitle('Formula 1 Analytics')
        self.setWindowIcon(QtGui.QIcon(CWD + '/formula/img/f1.png'))

    def UIComponents(self):
        layout = QVBoxLayout()

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

        layout.addWidget(label_year)
        layout.addWidget(self.drop_year)
        layout.addWidget(label_prix)
        layout.addWidget(self.drop_grand_prix)
        layout.addWidget(label_session)
        layout.addWidget(self.drop_session)
        layout.addWidget(label_d1)
        layout.addWidget(self.drop_driver1)
        layout.addWidget(label_d2)
        layout.addWidget(self.drop_driver2)
        layout.addWidget(label_analysis)
        layout.addWidget(self.drop_analysis)
        layout.addWidget(self.run_button)

        #self.drop_year.activated.connect(self.update_lists)
        self.drop_year.currentTextChanged.connect(self.update_lists)
        
        self.run_button.clicked.connect(self.button_listen)

        self.setLayout(layout)
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

    def button_listen(self, input_data):
        input_data = self.current_text()
        print(input_data)
        script.main(input_data)

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

