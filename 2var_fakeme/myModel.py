
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex

#Стандартная модель с переопределенными где надо функциями
class MyModel(QAbstractTableModel):
    #Считаем что items - двойной список(список строк)
    #labels - просто имена колонок
    def __init__(self, items, labels):
        super().__init__()
        self.list = items.copy()
        self.colLabels = labels.copy()

    def rowCount(self, parent = QModelIndex()):
        return len(self.list)

    def columnCount(self, parent = QModelIndex()):
        return len(self.colLabels)
    
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QVariant(self.colLabels[section])
        return QVariant()

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return QVariant()
        val = ''
        if role == QtCore.Qt.DisplayRole:
            #просто вернем значение из списка(только постараемся избежать ошибок)
            try:
                tmp = self.list[index.row()]
                val = tuple(tmp)[index.column()]
            except IndexError:
                pass
        return val





