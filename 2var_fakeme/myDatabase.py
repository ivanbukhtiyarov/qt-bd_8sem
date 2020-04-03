
from myModel import *

from peewee import *

import datetime


mainDatabase = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = mainDatabase

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

def initDatabase():
    cook = Cook.create(name = "Papanister", restaurant = "shokoladnik")
    event = Event.create(name = "vruchenie oscara", date = datetime.datetime(2020, 2, 1, 12, 0))
    dish = Dish.create(name = "myasnoi salat oshibka sapera", calorie = 100, cook = cook, event = event)
    drink = Drink.create(name = "russian vodka", count = 25, event = event)
    ingredient = Ingredient.create(name = "list'ya salata", count = 55, dish = dish)
    recipe = Recipe.create(author = "Papanister", dish = dish)

class MyDataBase:
    def __init__(self, name):
        mainDatabase.init(name)
        mainDatabase.connect()
        mainDatabase.create_tables(BaseModel.__subclasses__())
        try:
            initDatabase()
        except IntegrityError:
            print("init canceled")
            #pass

    def dishes(self):
        return [i.name for i in Dish.select()]

    def authors(self):
        return [i.author for i in Recipe.select(Recipe.author).distinct()]

    def maxDrinkCount(self):
        return Drink.select(fn.MAX(Drink.count)).scalar()

    def add(self, num, dish_name, name):
        try:
            dish = Dish.get(Dish.name == dish_name)
        except DoesNotExist:
            return
        Ingredient.create(name = name, count = num, dish = dish)

    def first(self, name):
        tmp = [(i.name, i.calorie) for i in Dish.select().join(Recipe).where(Recipe.author == name)]
        print(tmp)
        return MyModel(tmp, ['name', 'cal'])

    def second(self, sub_str):
        tmp = [(i.cook.restaurant, i.cook.name, i.name) for i in Dish.select().join(Cook).where(Dish.name.contains(sub_str)).order_by(Cook.restaurant)]
        print(tmp)
        return MyModel(tmp, ['restaurant', 'cook name', 'dish name'])

    def third(self, num, date):
        tmp = [(i.dish.event.name, i.name, i.count) for i in Ingredient.select().join(Dish).join(Event).join(Drink).where((Drink.count < num) & (Event.date > date)).distinct()]
        print(tmp)
        return MyModel(tmp, ['event name', 'ingredient name', 'count'])


