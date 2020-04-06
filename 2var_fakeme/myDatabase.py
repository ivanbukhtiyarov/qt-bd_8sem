
from myModel import *

from peewee import *

import datetime


#Инициализируем датабазу но пока без имени файла он будет потом
mainDatabase = SqliteDatabase(None)

#Спец класс от которого будем наследовать все остальные чтоб было проще
class BaseModel(Model):
    class Meta:
        database = mainDatabase

#Ниже описываются таблицы

#Мероприятие
class Event(BaseModel):
    name = CharField()                           #Название
    date = DateTimeField()                       #Дата

#Повар
class Cook(BaseModel):
    name = CharField(unique = True)              #Имя
    restaurant = CharField()                     #Ресторан
    #backref = "dish" in Dish                    #Блюдо

#Блюдо
class Dish(BaseModel):
    name = CharField(unique = True)              #Название
    calorie = IntegerField()                     #Калорийность
    cook = ForeignKeyField(Cook, backref="dish") #Повар
    event = ForeignKeyField(Event)               #Мероприятие

#Напиток
class Drink(BaseModel):
    name = CharField(unique = True)              #Название
    count = IntegerField()                       #Количество
    event = ForeignKeyField(Event)               #Мероприятие

#Ингредиент
class Ingredient(BaseModel):
    name = CharField(unique = True)              #Название
    count = IntegerField()                       #Количество
    dish = ForeignKeyField(Dish)                 #Блюдо

#Рецепт
class Recipe(BaseModel):
    author = CharField()                         #Автор
    dish = ForeignKeyField(Dish)                 #Блюдо

#Функция по начальному заполнению датабазы
def initDatabase():
    cook = Cook.create(name = "Papanister", restaurant = "shokoladnik")
    event = Event.create(name = "vruchenie oscara", date = datetime.datetime(2020, 2, 1, 12, 0))
    dish = Dish.create(name = "myasnoi salat oshibka sapera", calorie = 100, cook = cook, event = event)
    drink = Drink.create(name = "russian vodka", count = 25, event = event)
    ingredient = Ingredient.create(name = "list'ya salata", count = 55, dish = dish)
    recipe = Recipe.create(author = "Papanister", dish = dish)

#Специальный класс для взаимодействия с датабазой
class MyDataBase:
    def __init__(self, name):
        #Тут открываем файл
        mainDatabase.init(name)
        mainDatabase.connect()
        #Создаем в бд структуры таблиц (Так как мы все таблицы наследовали от BaseModel то просто получим наследников)
        mainDatabase.create_tables(BaseModel.__subclasses__())
        try:
            #Пытаемя заполнить(может неполучиться потому что там есть уникальные поля)
            initDatabase()
        except IntegrityError:
            #Если не получилось то и ладно
            #print("init canceled")
            pass

    #Вернем имена всех блюд(они уже уникальны)
    def dishes(self):
        return [i.name for i in Dish.select()]

    #Вернем уникальные имена авторов
    def authors(self):
        return [i.author for i in Recipe.select(Recipe.author).distinct()]

    #Вернем максимальное кол напитков
    def maxDrinkCount(self):
        return Drink.select(fn.MAX(Drink.count)).scalar()

    #Функция добавления ингредиента
    def add(self, num, dish_name, name):
        try:
            #Пытаемся получить блюдо по его имени
            dish = Dish.get(Dish.name == dish_name)
        except DoesNotExist:
            #Если не получилось то вываливаемя и ничего не делаем
            return
        #Создаем ингредиент в бд
        Ingredient.create(name = name, count = num, dish = dish)

    #Первый запрос
    def first(self, name):
        tmp = [(i.name, i.calorie) for i in Dish.select().join(Recipe).where(Recipe.author == name)]
        #print(tmp)
        return MyModel(tmp, ['Название', 'ККал.'])

    #Второй запрос
    def second(self, sub_str):
        tmp = [(i.cook.restaurant, i.cook.name, i.name) for i in Dish.select().join(Cook).where(Dish.name.contains(sub_str)).order_by(Cook.restaurant)]
        #print(tmp)
        return MyModel(tmp, ['Ресторан', 'Имя повара', 'Блюдо'])

    #Третий запрос
    def third(self, num, date):
        tmp = [(i.dish.event.name, i.name, i.count) for i in Ingredient.select().join(Dish).join(Event).join(Drink).where((Drink.count < num) & (Event.date > date)).distinct()]
        #print(tmp)
        return MyModel(tmp, ['Мероприятие', 'Ингредиент', 'Кол-во'])


