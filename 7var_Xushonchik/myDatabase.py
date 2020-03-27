
import datetime

from peewee import *

from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, QVariant

class MyModel(QAbstractTableModel):
    def __init__(self, items, labels):
        super().__init__()
        self.list = items.copy()
        self.colLabels = labels.copy()

    def rowCount(self, parent):
        return len(self.list)

    def columnCount(self, parent):
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
            try:
                tmp = self.list[index.row()]
                val = tuple(tmp)[index.column()]
            except IndexError:
                pass
        return val






mainDatabase = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = mainDatabase

class Store(BaseModel):
    name = CharField(unique = True)
    adress = CharField()

class Product(BaseModel):
    name = CharField(unique = True)
    praise = IntegerField()
    store = ForeignKeyField(Store)

class Storage(BaseModel):
    adress = CharField(unique = True)
    product = ForeignKeyField(Product, backref="storage")

class Rate(BaseModel):
    author = CharField()
    stars = IntegerField()
    product = ForeignKeyField(Product)

class Supply(BaseModel):
    product = ForeignKeyField(Product)
    count = IntegerField()
    date = DateTimeField()

class Cashier(BaseModel):
    store = ForeignKeyField(Store)
    name = CharField(unique = True)
    salary = IntegerField()


def initDatabase():
    tmp_store = Store(name = "6shesterechka", adress = "prospect nezavisimosti 17")
    tmp_store.save()
    tmp_product = Product(name = "anti-coronovirus", praise = 999999, store = tmp_store)
    tmp_product.save()
    tmp_supply = Supply(product = tmp_product, count = 1, date = datetime.datetime(2024, 10, 1, 12, 24))
    tmp_supply.save()
    tmp_product = Product(name = "mal'chik", praise = 100000*1000000, store = tmp_store)
    tmp_product.save()
    tmp_storage = Storage(adress = "u drakoshi", product = tmp_product)
    tmp_storage.save()
    tmp_rate = Rate(author = "na zabore", stars = 3, product = tmp_product)
    tmp_rate.save()
    tmp_supply = Supply(product = tmp_product, count = 33, date = datetime.datetime(1999, 10, 1, 12, 24))
    tmp_supply.save()
    tmp_cash = Cashier(store = tmp_store, name = "Petya", salary = 1)
    tmp_cash.save()


class MyDataBase:
    def __init__(self, name):
        mainDatabase.init(name)
        mainDatabase.connect()
        mainDatabase.create_tables([Store, Product, Storage, Rate, Supply, Cashier])
        try:
            initDatabase()
        except IntegrityError:
            print("database init canceled")


    def stores(self):
        return [i.name for i in Store.select()]

    def products(self):
        return [i.name for i in Product.select()]

    def products_in_supply(self):
        return {i.product.name : None for i in Supply.select()}.keys()

    def find_sub(self, name):
        return Subject.select().where(Subject.name == name).get()

    def students(self):
        return [i.name for i in Student.select()]

    def add(self, num, room, sub, topic):
        finded_sub = self.find_sub(sub)
        if finded_sub is None:
            return
        sem = Seminar(subject = self.find_sub(sub), week = num, room = room, topic = topic)
        sem.save()

    #def query(self, string):
        #res = None
        #try:
            #res = self._query(num)()
        #except KeyError:
            #pass
        #return res

    def first(self, name):
        tmp = [(str(i.date), i.count) for i in Supply.select().join(Product).where(Product.name == name)]
        print(tmp)
        return MyModel(tmp, ["supplies of '"+name+"'"])

    def second(self, name):
        tmp_f = Faculty.select().where(Faculty.name == name).get()
        #tmp = [(i.name, i.experience) for i in Teacher.select().where(Teacher.subject.faculty == tmp_f).ordered_by(Teacher.experience)]
        tmp = [(i.name, i.experience) for i in Teacher.select().join(Subject).where(Subject.faculty == tmp_f).order_by(Teacher.experience)]
        print(tmp)
        return MyModel(tmp, ['name', 'experience'])

    def third(self, num, name):
        tmp_st = Student.select().where(Student.name == name).get()
        #tmp_sub = [i for i in Subject.select().where(Subject.faculty == tmp_st.faculty)]
        tmp = [(i.subject.name, i.topic, i.subject.sem) for i in Seminar.select().join(Subject).where(Subject.faculty == tmp_st.faculty & Seminar.week < num)]
        print(tmp)
        #tmp = [(i.name, i.experience) for i in Teacher.select().where(Teacher.subject.faculty == tmp_f)]
        return MyModel(tmp, ['subject', 'topic', 'sem'])



