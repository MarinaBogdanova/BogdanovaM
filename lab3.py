import json
from pprint import pprint
import sys
from PyQt4 import QtGui, QtCore


class Entry:
    def __init__(self, key, value):
        self.l = QtGui.QLabel(key)
        self.t = QtGui.QLineEdit(value)

    def getLabel(self):
        return self.l

    def getTextEdit(self):
        return self.t


class ControlButtons:
    def __init__(self, widget, saveCB, prevCB=None, nextCB=None):
        self.prev = QtGui.QPushButton('<<')
        self.save = QtGui.QPushButton('save')
        self.next = QtGui.QPushButton('>>')

        if prevCB != None:
            widget.connect(self.prev, QtCore.SIGNAL('clicked()'), prevCB)
        else:
            self.prev.setDisabled(True)
        if nextCB != None:
            widget.connect(self.next, QtCore.SIGNAL('clicked()'), nextCB)
        else:
            self.next.setDisabled(True)
        widget.connect(self.save, QtCore.SIGNAL('clicked()'), saveCB)

    def getPrevButton(self):
        return self.prev

    def getSaveButton(self):
        return self.save

    def getNextButton(self):
        return self.next


class WidgetStore:
    grid = QtGui.QGridLayout()
    ox = 1

    def __init__(self):
        self.entries = []
        self.grid.setSpacing(10)

    def getEntries(self):
        return self.entries

    def addEntry(self, e):
        self.grid.addWidget(e.getLabel(), self.ox, 0)
        self.grid.addWidget(e.getTextEdit(), self.ox, 1)
        self.entries.append(e)
        self.ox += 1

    def addControlButtons(self, cb):
        self.grid.addWidget(cb.getPrevButton(), self.ox, 0)
        self.grid.addWidget(cb.getSaveButton(), self.ox, 1)
        self.grid.addWidget(cb.getNextButton(), self.ox, 3)
        self.controlbuttons = cb
        self.ox += 1

    def getGrid(self):
        return self.grid

    def clear(self):
        for k in range(len(self.entries)):
            # self.grid.removeWidget(self.entries[k].getLabel())
            self.entries[k].getLabel().deleteLater()
            # self.grid.removeWidget(self.entries[k].getTextEdit())
            self.entries[k].getTextEdit().deleteLater()
        if hasattr(self, 'controlbuttons'):
            self.controlbuttons.getPrevButton().deleteLater()
            self.controlbuttons.getSaveButton().deleteLater()
            self.controlbuttons.getNextButton().deleteLater()
            del self.controlbuttons
        del self.entries
        self.entries = []
        ox = 1


class ErrorFile(Exception):
    pass

class MainWindow(QtGui.QWidget):
    data = []
    datafile = 'data.json'

    def getData(self):
        with open(self.datafile, encoding='utf-8') as infile:
            try:
                return json.load(infile)
            except OSError:
                raise ErrorFile
            except ValueError:
                raise ErrorFile
            # except Exception as e:
            #     raise e

    def slotPrev(self):
        self.key -= 1
        self.update()

    def slotNext(self):
        self.key += 1
        self.update()

    def slotSave(self):
        for e in self.widgetstore.getEntries():
            self.data[self.key][e.getLabel().text()] = e.getTextEdit().text()
        with open(self.datafile, 'w') as outfile:
            try:
                json.dump(self.data, outfile, indent= 4, ensure_ascii=False)
            except:
                pass

    def update(self):

        self.widgetstore.clear()

        try:
            self.data = self.getData()
            for k in self.data[self.key]:
                e = Entry(k, self.data[self.key][k])
                self.widgetstore.addEntry(e)

            saveCB = self.slotSave
            if self.key == 0:
                prevCB = None
            else:
                prevCB = self.slotPrev
            if self.key + 1 >= len(self.data):
                nextCB = None
            else:
                nextCB = self.slotNext
            cb = ControlButtons(self, saveCB, prevCB, nextCB)
            self.widgetstore.addControlButtons(cb)

            self.setLayout(self.widgetstore.getGrid())
        except ErrorFile:
            pass

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.widgetstore = WidgetStore()
        self.key = 0
        self.update()

        self.resize(800, 600)
        self.setWindowTitle("Lab3")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())