'''
This module implements the Triangle Peg Game.
    
'''

import sys, pickle
from PyQt5 import QtWidgets, QtCore, QtGui

class PegGameWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup()

    def setup(self):
        self.setWindowTitle('Triangle Peg Game')
        self.setToolTip("Play the triangle peg game!")
        
        self.peg_game = PegGame(self)
        self.setCentralWidget(self.peg_game)
        
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(exit_action)

        self.show()

    def closeEvent(self, event):
        popup = QuitMessage()
        reply = popup.exec_()
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class PegGame(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()
    
    def setup(self):
        self.board = PegBoard(self) 
        self.new_btn = StartNewGameBtn(self)
        self.quit_btn = QuitBtn(self)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
    
        self.grid.addWidget(self.board, 1, 1, 1, 4)
        self.grid.addWidget(self.new_btn, 2, 1, 1, 1)
        self.grid.addWidget(self.quit_btn, 2, 2, 1, 1)

class PegBoard(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.holes = []
        self.setFixedSize(700, 460)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(0, 0, 0, 255)) 
        self.setPalette(p)
        self.setAutoFillBackground(True) 
        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setSpacing(0)
        self.place_holes()
        self.peg_count = len(self.holes)
    
    def paintEvent(self, event):
        points_list = [QtCore.QPoint(50,455), QtCore.QPoint(650,455), QtCore.QPoint(350,5)]
        triangle = QtGui.QPolygon(points_list)
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = qp.pen()
        pen.setColor(QtCore.Qt.transparent)
        qp.setPen(pen)
        brush = QtGui.QBrush()
        brush.setTextureImage(QtGui.QImage('wood.jpg'))
        qp.setBrush(brush)
        qp.drawPolygon(triangle)
        qp.end()
    
    def place_holes(self):
        for row in range(0,5):
            row_list = [] 
            rowLayout = QtWidgets.QHBoxLayout()
            self.vbox.addLayout(rowLayout)
            rowLayout.addStretch(1)
            for col in range(0,row+1):
                hole = PegHole(self, row, col)
                row_list.append(hole)
                rowLayout.addWidget(hole, 0)
                if row != 2 or col != 1:
                    hole.addPeg()
            rowLayout.addStretch(1)
            self.holes.append(row_list[:])   

class PegHole(QtWidgets.QWidget):
    def __init__(self, parent, row, col):
        self.parent = parent
        QtWidgets.QWidget.__init__(self, parent)
        self.setAcceptDrops(True)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.peg = None
        self.create_icon()
        self.row = row
        self.col = col
       
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    
    def dropEvent(self, event):
        if not self.peg:
            row, col = pickle.loads(event.mimeData().text())
            if(self.check_valid(row, col)):
                self.addPeg()
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def check_valid(self, row, col):
        hopped = None
        if self.row == row:
            if self.col == (col-2):
                hopped = (row, col-1)
            elif self.col == (col+2):
                hopped = (row, col+1)
        elif self.row == (row-2):
            if self.col == col:
                hopped = (row-1, col)
            elif self.col == col-2:
                hopped = (row-1, col-1)
            elif self.col == col+2:
                hopped = (row-1, col+1)
        elif self.row == (row+2):
            if self.col == col:
                hopped = (row+1, col)
            elif self.col == col-2:
                hopped = (row+1, col-1)
            elif self.col == col+2:
                hopped = (row+1, col+1)
        
        if not hopped:
            return False

        if(self.parent.holes[hopped[0]][hopped[1]].peg):
            self.parent.holes[hopped[0]][hopped[1]].deletePeg()
            self.parent.peg_count -= 1
            return True
        else:
            return False
    
    def mousePressEvent(self, event):
        if not self.peg:
            QtWidgets.QWidget.mousePressEvent(self, event)
            return

        self.peg.hide()
        drag = QtGui.QDrag(self)
        data = QtCore.QMimeData()
        data.setText(pickle.dumps((self.row, self.col)))
        drag.setMimeData(data)
        drag.setPixmap(self.peg_icon)
        drag.setHotSpot(self.peg_icon.rect().topLeft())
        dropAction = drag.exec_(QtCore.Qt.MoveAction)
        if dropAction:
            self.deletePeg()
        else:
            self.peg.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawEllipse(QtCore.QPointF(60, 45), 6, 6)
        qp.end()

    def minimumSizeHint(self):
        return QtCore.QSize(120, 90)
    
    def addPeg(self):
        self.peg = Peg(self)
        self.grid.addWidget(self.peg)
    
    def deletePeg(self):
        self.peg.hide()
        del(self.peg)
        self.peg = None
    
    def create_icon(self):
        self.peg_icon = QtGui.QPixmap(22, 22)
        self.peg_icon.fill(QtCore.Qt.transparent)
        qp = QtGui.QPainter()
        qp.begin(self.peg_icon)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtCore.Qt.red)
        qp.setBrush(brush)
        qp.drawEllipse(0, 0, 20, 20)
        qp.end()
        #return icon
   
class Peg(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(parent.size())

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtCore.Qt.red)
        qp.setBrush(brush)
        qp.drawEllipse(QtCore.QPointF(self.width()/2, self.height()/2), 10, 10)
        qp.end()

class QuitMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Do you really want to quit?")
        self.addButton(self.No)
        self.addButton(self.Yes)

class StartNewGameBtn(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Start New Game")
        self.resize(self.sizeHint())

class QuitBtn(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Quit")
        self.clicked.connect(QtWidgets.qApp.quit)
        self.setToolTip("Close the triangle peg game.")
        self.resize(self.sizeHint())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = PegGameWindow()
    app.exec_()