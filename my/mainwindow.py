
from PyQt5.QtWidgets import (QMainWindow, QWidget,
        QPushButton, QLineEdit, QInputDialog, QComboBox, QLabel, QSpinBox, QTreeView, QVBoxLayout, QHBoxLayout)

import myDatabase

class MainWindow(QMainWindow):

    def __init__(self, dataBaseName):
        super().__init__()
        #self._dataBase = SqliteDatabase(dataBaseName)
        self._dataBase = myDatabase.MyDataBase(dataBaseName)

        self._dictexe = {"f":(self.firstQuery, self.firstExe), "s":(self.secondQuery, self.secondExe), "t":(self.thirdQuery, self.thirdExe)}

        self._view = QTreeView()
        self._buttonAdd = QPushButton("Add")
        self._buttonAdd.clicked.connect(self.getItems)

        self._layout = QHBoxLayout()
        self._qSpinBox = QSpinBox()
        self._qComboBox = QComboBox()

        self._buttonExe = QPushButton("Exe")
        self._buttonExe.clicked.connect(self.onButtonExe)

        self._combox = QComboBox()
        self._combox.currentTextChanged.connect(self.comboChanged)
        self._combox.addItems(self._dictexe.keys())

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
        tmpLayout.addWidget(QLabel("add shit"))
        tmpLayout.addWidget(self._buttonAdd)

        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(self._combox)
        tmpLayout.addLayout(self._layout)
        tmpLayout.addWidget(self._buttonExe)

    def comboChanged(self, text):
        self._dictexe[text][0]()
        #self._dictexe[self._combox.currentText()]()

    def clearLayout(self):
        while self._layout.count() > 0:
            self._layout.itemAt(0).widget().setParent(None)
            #self._layout.removeItem(self._layout.itemAt(0))

    #Темы лекций дисциплин семестра X
    def firstQuery(self):
        self.clearLayout()
        self._qSpinBox.setValue(0)
        self._layout.insertWidget(1,self._qSpinBox)

    def firstExe(self):
        model = self._dataBase.first(self._qSpinBox.value())
        self.setModel(model)

    #Имена и стажи преподавателей дисциплин на факультете с названием X,отсортированные по убыванию стажа
    def secondQuery(self):
        self.clearLayout()
        self._qComboBox.clear()
        self._qComboBox.addItems(self._dataBase.faculties())
        self._layout.insertWidget(1,self._qComboBox)

    def secondExe(self):
        model = self._dataBase.second(self._qComboBox.currentText())
        self.setModel(model)

    #Названия дисциплин, темы семинаров и номера семестров, которые посещает студент с именем X до начала недели Y
    def thirdQuery(self):
        self.clearLayout()
        self._qComboBox.clear()
        self._qComboBox.addItems(self._dataBase.students())
        self._layout.insertWidget(1, self._qComboBox)
        self._qSpinBox.setValue(0)
        self._layout.insertWidget(1, self._qSpinBox)

    def thirdExe(self):
        model = self._dataBase.third(self._qSpinBox.value(), self._qComboBox.currentText())
        self.setModel(model)


    def setModel(self, model):
        if model is None:
            return
        self._view.setModel(model)

    def onButtonExe(self):
        self._dictexe[self._combox.currentText()][1]()


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

