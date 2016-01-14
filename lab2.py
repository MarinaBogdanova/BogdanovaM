import sys

from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QMainWindow):

    def newFile(self):
        self.textEdit.setText("")

    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self)
        try:
            openfile = open(filename, 'r')
            text = openfile.read()
            self.textEdit.setText(text)
            openfile.close()
        except FileNotFoundError:
            pass

    def saveFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self)
        try:
            savefile = open(filename, 'w')
            text = self.textEdit.toPlainText()
            savefile.write(text)
            savefile.close()
        except FileNotFoundError:
            pass

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(800, 600)
        self.setWindowTitle("NotePad--")

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        newact = QtGui.QAction('New', self)
        self.connect(newact, QtCore.SIGNAL('triggered()'), self.newFile)

        opwnact = QtGui.QAction('Open..', self)
        self.connect(opwnact, QtCore.SIGNAL('triggered()'), self.openFile)

        saveact = QtGui.QAction('Save as..', self)
        self.connect(saveact, QtCore.SIGNAL('triggered()'), self.saveFile)

        exitact = QtGui.QAction('Exit', self)
        self.connect(exitact, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(newact)
        file.addAction(opwnact)
        file.addAction(saveact)
        file.addAction(exitact)

app = QtGui.QApplication(sys.argv)
qb = MainWindow()
qb.show()
sys.exit(app.exec_())