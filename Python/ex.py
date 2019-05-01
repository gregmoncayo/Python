import sys
from PyQT5 import QtGui, QtCore

class Window(QtGui.QMainWindow):
	def __init__(self):
            super(Window, self).__init__()
            self.setGeometry(50, 50, 500, 300)
            self.setWindowTitle("Pyqt tuts!")
            btn = QtGui.QPushButton("Quit", self)
            btn.clicked.connect()

app = QtGui.QApplication(sys.argv)
Gui = Window()
sys.exit(app.exec_())
