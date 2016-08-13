#!/usr/bin/python
# coding: utf-8

import sys, random
from PyQt4 import QtGui, QtCore

class Widget(QtGui.QMainWindow):
    
    def __init__(self):
        super(Widget, self).__init__()
        self.initUI()
        
    def initUI(self):                
        shuffleAction = QtGui.QAction(QtGui.QIcon("puzzle15/img/shuffle.png"), "Shuffle", self)
        shuffleAction.triggered.connect(self.shufflePanels)
        
        self.toolbar = self.addToolBar("Shuffle")
        self.toolbar.addAction(shuffleAction)
        
        self.setGeometry(800, 200, 400, 444)
        self.setWindowTitle("15puzzle")
        self.setWindowIcon(QtGui.QIcon("puzzle15/img/15.png"))
        self.panels = []
        self.positions = []
        for i in range(16):
            self.positions.append(QtCore.QPoint((i % 4) * 100, 44 + int(i / 4) * 100))
        self.makePanels()
        self.blankPoint = self.positions[15]
        self.show()
        self.raise_()
        self.activateWindow()

    def makePanels(self):
        for number in map(lambda x:x+1, range(15)):
            self.panels.append(Panel(self))
            self.panels[number - 1].number = number
            self.setPanel(number, self.positions[number - 1])
            self.panels[number - 1].setPixmap(QtGui.QPixmap("puzzle15/img/" + str(number) + ".png"))

    def setPanel(self, number, position):
        self.panels[number - 1].setGeometry(position.x(), position.y(), 100, 100)

    def canSlide(self, panel):
        if QtCore.QPoint(panel.pos().x() - 100, panel.pos().y()) == self.blankPoint:
            return True
        elif QtCore.QPoint(panel.pos().x() + 100, panel.pos().y()) == self.blankPoint:
            return True
        elif QtCore.QPoint(panel.pos().x(), panel.pos().y() - 100) == self.blankPoint:
            return True
        elif QtCore.QPoint(panel.pos().x(), panel.pos().y() + 100) == self.blankPoint:
            return True
        else:
            return False

    def slide(self, number):
        if self.canSlide(self.panels[number - 1]):
            position = self.panels[number - 1].pos()
            self.panels[number - 1].move(self.blankPoint)
            self.blankPoint = position

    def isOriginalState(self):
        for number in map(lambda x:x+1, range(15)):
            panelPos = self.panels[number - 1].pos()
            originalPos = self.positions[number - 1]
            if panelPos != originalPos:
                return False
        return True

    def shufflePanels(self):
        shuffleList = map(lambda x:x+1, range(15))
        swapIndex = range(15)
        swapCount = 0
        while(True):
            random.shuffle(swapIndex)
            for number in map(lambda x:x+1, range(15)):
                if number - 1 != swapIndex[number - 1]:
                    tmp = shuffleList[number - 1]
                    shuffleList[number - 1] = shuffleList[swapIndex[number - 1]]
                    shuffleList[swapIndex[number - 1]] = tmp
                    swapCount += 1
            for number in map(lambda x:x+1, range(15)):
                self.setPanel(shuffleList[number - 1], self.positions[number - 1])
            if not self.isOriginalState():
                if swapCount % 2 == 0:
                    break
        self.blankPoint = self.positions[15]


class Panel(QtGui.QLabel):
    def mouseReleaseEvent(self, event):
        self.parentWidget().slide(self.number)
        if self.parentWidget().isOriginalState():
            print("clear!")


def main():
    app = QtGui.QApplication(sys.argv)
    widget = Widget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
