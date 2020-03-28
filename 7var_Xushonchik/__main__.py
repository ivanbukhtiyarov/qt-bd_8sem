#!/usr/bin/python3


import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (QMainWindow, QWidget,
        QPushButton, QLineEdit, QInputDialog, QDialog, QDialogButtonBox, QComboBox, QCalendarWidget,
        QFormLayout, QLabel, QSpinBox, QTreeView, QVBoxLayout, QHBoxLayout)

from PyQt5 import QtCore
import myDatabase


class myDialog(QDialog):

    def __init__(self, l, title = "question"):
        super().__init__()
        super().setWindowTitle(title)
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
        tmpLayout.addWidget(self._buttonAdd)
        #tmpLayout.addWidget(self._combox)
        #tmpLayout.addLayout(self._layout)
        for i, j in self._buttons:
            tmpLayout.addWidget(i)


    #Количество товара с наименованием X в поставках
    def on1(self):
        str_disc = QLabel("Количество товара с наименованием X в поставках")
        l = [("discription", str_disc), ("product :", QComboBox())]
        l[1][1].addItems(self._dataBase.products_in_supply()) 
        d = myDialog(l, "first")
        if d.exec() == QDialog.Accepted:
            model = self._dataBase.first(l[1][1].currentText())
            self.setModel(model)

    #Адреса складов, работающих с магазинами, организации которых содержат подстроку X (например, «ИП»), отсортированные по цене товара
    def on2(self):
        str_disc = QLabel("Адреса складов, работающих с магазинами,\n организации которых содержат подстроку X (например, «ИП»),\n отсортированные по цене товара")
        l = [("discription", str_disc), ("sub string in companies names", QLineEdit())]
        d = myDialog(l, "second")
        if d.exec() == QDialog.Accepted:
            model = self._dataBase.second(l[1][1].text())
            self.setModel(model)

    #Оценка товаров, наименования товаров и адреса магазинов, в которых работают кассиры с зарплатой меньше, чем X, поставки в которые ожидаются позднее даты Y
    def on3(self):
        str_disc = QLabel("Оценка товаров, наименования товаров и адреса магазинов,\n в которых работают кассиры с зарплатой меньше, чем X,\n поставки в которые ожидаются позднее даты Y")
        l = [("discription", str_disc), ("salary less then", QSpinBox()), ("later then", QCalendarWidget())]
        l[1][1].setMaximum(self._dataBase.max_salary()+1)
        d = myDialog(l, "third")
        if d.exec() == QDialog.Accepted:
            #tmp_date = l[1][1].datetime()
            #date = datetime.datetime()
            #model = self._dataBase.first(l[0][1].value(), date)
            model = self._dataBase.third(l[1][1].value(), l[2][1].selectedDate().toPyDate())
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


