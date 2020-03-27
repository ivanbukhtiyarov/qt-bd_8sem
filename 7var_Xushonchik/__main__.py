#!/usr/bin/python3


import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (QMainWindow, QWidget,
        QPushButton, QLineEdit, QInputDialog, QDialog, QDialogButtonBox, QComboBox, QFormLayout, QLabel, QSpinBox, QTreeView, QVBoxLayout, QHBoxLayout)

from PyQt5 import QtCore
import myDatabase


class myDialog(QDialog):

    def __init__(self, l):
        super().__init__()
        layout = QFormLayout()
        super().setLayout(layout)
        for i, j in l:
            layout.addRow(QLabel(i), j)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


class MainWindow(QMainWindow):

    def __init__(self, dataBaseName):
        super().__init__()
        self._dataBase = myDatabase.MyDataBase(dataBaseName)


        self._view = QTreeView()

        self._buttonAdd = QPushButton("Add")
        self._buttonAdd.clicked.connect(self.getItems)

        #self._layout = QHBoxLayout()
        #self._qSpinBox = QSpinBox()
        #self._qComboBox = QComboBox()

        self._buttons = [(QPushButton("Exe1"), self.on1), (QPushButton("Exe2"), self.on2), (QPushButton("Exe3"), self.on3)]
        for i, j in self._buttons:
            i.clicked.connect(j)
        

        #self._combox = QComboBox()
        #self._combox.currentTextChanged.connect(self.comboChanged)
        #self._combox.addItems(self._dictexe.keys())

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

        #tmpLayout = QHBoxLayout()
        #mainLayout.addLayout(tmpLayout)
        #tmpLayout.addWidget(QLabel("add shit"))
        #tmpLayout.addWidget(self._buttonAdd)

        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        #tmpLayout.addWidget(self._combox)
        #tmpLayout.addLayout(self._layout)
        for i, j in self._buttons:
            tmpLayout.addWidget(i)


    #Темы лекций дисциплин семестра X
    def on1(self):
        l = [("popa", QComboBox())]
        l[0][1].addItems(self._dataBase.products_in_supply()) 
        d = myDialog(l)
        if d.exec() == QDialog.Accepted:
            model = self._dataBase.first(l[0][1].currentText())
            self.setModel(model)

    #Имена и стажи преподавателей дисциплин на факультете с названием X,отсортированные по убыванию стажа
    def on2(self):
        model = self._dataBase.second(self._qComboBox.currentText())
        self.setModel(model)

    #Названия дисциплин, темы семинаров и номера семестров, которые посещает студент с именем X до начала недели Y
    def on3(self):
        model = self._dataBase.third(self._qSpinBox.value(), self._qComboBox.currentText())
        self.setModel(model)


    def setModel(self, model):
        if model is None:
            return
        self._view.setModel(model)

    def getItems(self):
        items = self._dataBase.subjects()

        num, ok = QInputDialog.getInt(self, "week", "enter a number")
        if not ok:
            return None
        room, ok = QInputDialog.getText(self, "room", "enter a room name")
        if not ok:
            return None
        subject, ok = QInputDialog.getItem(self, "subject", "select a subject", items, 0, False)
        if not ok:
            return None
        
        topic, ok = QInputDialog.getText(self, "topic", "enter a topic")
        if not ok:
            return None

        self._dataBase.add(num, room, subject, topic)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow("test.bd")
    w.show()

    sys.exit(app.exec_())


