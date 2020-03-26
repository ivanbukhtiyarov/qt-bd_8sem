
from PyQt5.QtWidgets import (QMainWindow, QWidget,
        QPushButton, QLineEdit, QInputDialog, QComboBox, QTreeView, QVBoxLayout, QHBoxLayout)

import myDatabase

class MainWindow(QMainWindow):

    def __init__(self, dataBaseName):
        super().__init__()
        #self._dataBase = SqliteDatabase(dataBaseName)
        self._dataBase = myDatabase.MyDataBase(dataBaseName)

        self._view = QTreeView()
        self._buttonAdd = QPushButton("Add")
        self._buttonAdd.clicked.connect(self.getItems)

        self._buttonExe = QPushButton("Exe")
        #self._buttonExe.clicked.connect(self.getItems)

        self.initUi()

    def initUi(self):
        self.setGeometry(300,300,200,200)
        self.setWindowTitle('ShitName')
        #self.setWindowIcon(QIcon(''))

        w = QWidget()

        mainLayout = QVBoxLayout()
        w.setLayout(mainLayout)

        self.setCentralWidget(w)

        mainLayout.addWidget(self._view)
        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(self._buttonAdd)

        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(self._buttonExe)

    def getItems(self):
        items = ["a", "b", "c"]

        num, ok = QInputDialog.getInt(self, "week", "enter a number")
        if not ok:
            return None
        room, ok = QInputDialog.getText(self, "room", "enter a room name")
        if not ok:
            return None
        subject, ok = QInputDialog.getItem(self, "subject", "select a subject", items, 0, False)
        if not ok:
            return None
        else:
            return res
            

