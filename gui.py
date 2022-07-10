import sys
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui

app = QtWidgets.QApplication(sys.argv)
windows = QtWidgets.QWidget()

windows.resize(1000, 500)
windows.move(100, 100)

windows.setWindowTitle('Formula 1 Analytics')
windows.setWindowIcon(QtGui.QIcon('formula/img/f1.png'))
windows.show()

sys.exit(app.exec_())

