import sys, pickle
from PyQt5 import QtWidgets, QtCore, QtGui

class Homework3(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup()

    def setup(self):
        self.setWindowTitle("Mouse Mover!")
        self.left_button = LeftButton(self)
        self.right_button = RightButton(self)
        self.top_button = TopButton(self)
        self.bottom_button = BottomButton(self)
        self.pic = DrawImage()
        Image = DrawImage(self)
        self.show()
        Image.show()

class LeftButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Left Button")
        self.clicked.connect(self.direction)
        self.click()
        self.resize(self.sizeHint())
        self.move(20,300)

    def direction(self):
        print("hey")

class RightButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Right Button")
        self.clicked.connect(self.direction)
        self.click()
        self.resize(self.sizeHint())
        self.move(600, 300)

    def direction(self):
        print("hey")

class TopButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Up")
        self.clicked.connect(self.direction)
        self.click()
        self.resize(self.sizeHint())
        self.move(300,20)

    def direction(self):
        print("hey")

class BottomButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Down")
        self.move(300,600)
        self.clicked.connect(self.direction)
        self.click()
        self.resize(self.sizeHint())

    def direction(self):
        print("hey")
            

class DrawImage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFixedSize(700, 1550)
        self.picture = self.paintEvent(self)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 8, QtCore.Qt.SolidLine))
        painter.drawEllipse(100, 100, 100, 100)
        paint = QtGui.QPainter(self)
        paint.setPen(QtGui.QPen(QtCore.Qt.green, 8, QtCore.Qt.SolidLine))
        paint.drawEllipse(200, 200, 200, 200)

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        main_window = Homework3()
        app.exec_()

