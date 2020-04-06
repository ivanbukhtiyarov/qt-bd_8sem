#!/usr/bin/python3


#Импорт всякого очень интересного и не очень
import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import (QMainWindow, QWidget,
        QPushButton, QLineEdit, QInputDialog, QDialog, QDialogButtonBox, QComboBox, QCalendarWidget,
        QFormLayout, QLabel, QSpinBox, QTreeView, QVBoxLayout, QHBoxLayout)

from PyQt5 import QtCore
#Импортим файл myDatabase.py который написали сами потому что мы могем
import myDatabase


#Чтоб запрашивать данные от пользователя разом напишем диалог
#Диалог он потому что нужно меньше всего переопределять и он работает из коробки
#А главное он просит у пользователя accept или reject и кароч это круто
class myDialog(QDialog):
    #Тупа конструктор
    #l - лист типа [(надпись, виджет с которого будем получать ввод), ...] title - заголовок окошка
    def __init__(self, l, title = "question"):
        #Конструктор родителя а именно КуТэДиалога. super() - это типа батя
        super().__init__()
        #Метод установки заголовка он у родителя поэтому от родителя его и дернем
        super().setWindowTitle(title)
        #лайоут это кароч такая штука которая рамещает на себе виджеты так чтоб их размер не зависил он конкретных размеров окна
        #лайоут все шо надо растянет или сожмет что все по красоте было
        layout = QFormLayout()
        #Поставим лайоут по методу родителя
        super().setLayout(layout)
        #i - надпись j - виджет
        for i, j in l:
            #Лайоут был особый, пацанский поэтому заполняем его вот так вот
            layout.addRow(QLabel(i), j)
        #добавим кнопочков стандартных Ок и Cancel тупа патамушта
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        #и их добавим в лайоут
        layout.addRow(self.buttons)
        #и главное свяжем кнопочки(кнопоко-коборбку) с методоами диалога чтоб кнопки стали как родные
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


class MainWindow(QMainWindow):
    #Тупа конструктор который получает имя бд
    def __init__(self, dataBaseName):
        #Тоже что и выше
        super().__init__()
        #Откроем бд и запомним ее в _myDatabase
        self._myDatabase = myDatabase.MyDataBase(dataBaseName)

        #Там в задании должно быть тривью вот его и скрафтим
        self._view = QTreeView()

        #Тупа кнопочки чтоб по ним там все ето
        self._buttonAdd = QPushButton("Добавление рейтинга")
        #По этой кнопке будем добавлять в базу что надо
        self._buttonAdd.clicked.connect(self.addToDatabase)

        #А вот подъехали кнопочки для запросиков
        #листик состит так [(Кнопочка, функция которая вызовется на клик), ...]
        self._buttons = [(QPushButton("Запрос 1"), self.on1), (QPushButton("Запрос 2"), self.on2), (QPushButton("Запрос 3"), self.on3)]
        #А тут свяжем все кнопочки с функциями через коннект(Специальная КуТэМаджик)
        for i, j in self._buttons:
            i.clicked.connect(j)
        
        #Обычно все так пишут а смысол функции - визуально все насадить
        self.initUi()

    #Ща будем графику пилить
    def initUi(self):
        #Размеры окошка ширина, высота, позиция от левого края экрана, от правого
        self.setGeometry(300,300,200,200)
        #Тупа заголовок
        self.setWindowTitle('7 Вариант (Магазины)')
        #Ниже надо раскоментить чтоб поставить иконку
        #self.setWindowIcon(QIcon('Файл с иконкой'))

        #это на будущее
        w = QWidget()

        #Вертикальный лайоут так хочу так и будет
        mainLayout = QVBoxLayout()
        w.setLayout(mainLayout)

        #Вот оно будущее. Специфика QMainWindow
        self.setCentralWidget(w)

        #Пичкуем наши лайоуты всем чем надо
        mainLayout.addWidget(self._view)

        #Горизонтальный лайоут для кнопочков
        tmpLayout = QHBoxLayout()
        mainLayout.addLayout(tmpLayout)
        tmpLayout.addWidget(self._buttonAdd)
        #i - кнопочка. _ - функция но она нам не нужна
        for i, _ in self._buttons:
            tmpLayout.addWidget(i)


    #Количество товара с наименованием X в поставках
    def on1(self):
        #Напишем чисто по приколу описание запроса к бд
        str_disc = QLabel("Количество товара с наименованием X в поставках")
        #соберем листик для нашего диалога
        l = [("Запрос: ", str_disc), ("Продукт: ", QComboBox())]
        #Комбо бокс это типа выпадающий списков в котором юзер выбирает в данном случае 1 элемент
        #Заполним его товарами которые есть в поставках из бд
        l[1][1].addItems(self._myDatabase.products_in_supply()) 
        #Соберем наш диаложек. Напоминаю "first" - это заголовок
        d = myDialog(l, "Первый запрос")
        #А вот почему мы выбрали диалог exec() - вызывает его, ждет когда его закроют кнопочками ok или cancel и если ok(acceped) то выполним запрос
        if d.exec() == QDialog.Accepted:
            #Выполняем первый запрос у бд и получаем от бд модель которую вставим в нашу view
            model = self._myDatabase.first(l[1][1].currentText())
            self.setModel(model)

    #Адреса складов, работающих с магазинами, организации которых содержат подстроку X (например, «ИП»), отсортированные по цене товара
    def on2(self):
        str_disc = QLabel("Адреса складов, работающих с магазинами,\n организации которых содержат подстроку X (например, «ИП»),\n отсортированные по цене товара")
        #Лайн Едит это строчка для редактирования и написание текста
        l = [("Запрос", str_disc), ("Подстрока в имени компании", QLineEdit())]
        d = myDialog(l, "Второй запрос")
        if d.exec() == QDialog.Accepted:
            model = self._myDatabase.second(l[1][1].text())
            self.setModel(model)

    #Оценка товаров, наименования товаров и адреса магазинов, в которых работают кассиры с зарплатой меньше, чем X, поставки в которые ожидаются позднее даты Y
    def on3(self):
        str_disc = QLabel("Оценка товаров, наименования товаров и адреса магазинов,\n в которых работают кассиры с зарплатой меньше, чем X,\n поставки в которые ожидаются позднее даты Y")
        #Слендарь это календарь
        l = [("Запрос", str_disc), ("Зарплата меньше чем ", QSpinBox()), ("Позже даты", QCalendarWidget())]
        #Спин бокс Это спец поле с чиселками которое мы ограничим сверху макс зп + 1
        #Макс зп возьмем у датабазы
        l[1][1].setMaximum(self._myDatabase.max_salary()+1)
        d = myDialog(l, "Третий запрос")
        if d.exec() == QDialog.Accepted:
            model = self._myDatabase.third(l[1][1].value(), l[2][1].selectedDate().toPyDate())
            self.setModel(model)

    #Установим модель во view проверив что модель есть
    def setModel(self, model):
        if model is None:
            return
        self._view.setModel(model)

    #Добавим че надо в датабазу
    def addToDatabase(self):
        #Инпут Диалог нужен тут только потому что в задании он есть
        #"stars" - заголовок, "enter a ..." - описание, 0 - начальное значение, 0 - мин, 5 - макс.
        #Диалог спросит у пользователя int от 0 до 5. Если нажали ok(кнопочка диаложка) то ok = True если cancel - ok = False
        num, ok = QInputDialog.getInt(self, "Рейтинг (0-5)", "Введите рейтинг", 0, 0, 5)
        #Если ok = False то вывалимся из функции ибо юзер расхотел
        if not ok:
            return None
        #Соберем на диаложек тут все знакомо разве что описание добавления нет патамушта
        l = [("Автор", QLineEdit()), ("Продукт :", QComboBox())]
        l[1][1].addItems(self._myDatabase.products()) 
        d = myDialog(l, "Добавление")
        if d.exec() == QDialog.Accepted:
            #добавим в датабазу
            self._myDatabase.add(num, l[0][1].text(), l[1][1].currentText())


#Это то как все делают чтоб при импорте данного файла куда-то ничего не работало а работало тока тута
if __name__ == "__main__":
    #тут все как положено трогать ничего нельзя потому что так принято
    app = QApplication(sys.argv)

    w = MainWindow("test.bd")
    w.show()

    sys.exit(app.exec_())


