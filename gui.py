import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QVBoxLayout, QLabel

# CONSTANTS
year = ['2022', '2021', '2020', '2019', '2018', '2017']
location = ['Austria']
session = ['FP1','FP2', 'FP3', 'Sprint Qualifying', 'Qualifying', 'Race']
driver_name = ['VER', 'LEC', 'SAI', 'HAM', 'RUS', 'MAG', 'MSC']
analysis_type = ['Lap Time', 'Fastest Lap']

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.UIComponents()

    def initUI(self):
        self.setFixedSize(560, 280)
        self.move(100, 100)
        self.setWindowTitle('Formula 1 Analytics')
        self.setWindowIcon(QtGui.QIcon('formula/img/f1.png'))

    def UIComponents(self):
        layout = QVBoxLayout()

        self.drop_year = QComboBox()
        self.drop_grand_prix = QComboBox()
        self.drop_session = QComboBox()
        self.drop_driver1 = QComboBox()
        self.drop_driver2 = QComboBox()
        self.drop_analysis = QComboBox()

        label_year = QLabel()
        label_prix = QLabel()
        label_session = QLabel()
        label_d1 = QLabel()
        label_d2 = QLabel()
        label_analysis = QLabel()

        label_year.setText('Year:') 
        label_prix.setText('Grand Prix Location:') 
        label_session.setText('Session:') 
        label_d1.setText('Driver 1:') 
        label_d2.setText('Driver 2:') 
        label_analysis.setText('Analysis Type:')

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


 
        self.drop_year.activated.connect(self.current_text)
        self.drop_grand_prix.activated.connect(self.current_text)
        self.drop_session.activated.connect(self.current_text)
        self.drop_driver1.activated.connect(self.current_text)
        self.drop_driver2.activated.connect(self.current_text)
        self.drop_analysis.activated.connect(self.current_text)


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
        print(input_data)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())







#w.setLayout(layout)

#w.show()

#sys.exit(app.exec_())

