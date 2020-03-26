
from peewee import *


mainDatabase = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = mainDatabase

class Faculty(BaseModel):
    #faculty_id = AutoField()
    name = CharField()
    house = CharField()
    institute = CharField()

class Student(BaseModel):
    name = CharField()
    #faculty = ForeignKeyField(Faculty, column_name="faculty_id")
    faculty = ForeignKeyField(Faculty)

class Teacher(BaseModel):
    #teacher_id = AutoField()
    name = CharField()
    experience = IntegerField()
    #subject = ForeignKeyField(Subject, column_name="sub_id")

class Subject(BaseModel):
    #sub_id = AutoField()
    name = CharField()
    #teacher = ForeignKeyField(Teacher, column_name="teacher_id", backref="subject")
    teacher = ForeignKeyField(Teacher, backref="subject")
    sem = IntegerField()
    #faculty = ForeignKeyField(Faculty, column_name="faculty_id")
    faculty = ForeignKeyField(Faculty)

class Seminar(BaseModel):
    #subject = ForeignKeyField(Subject, column_name="sub_id")
    subject = ForeignKeyField(Subject)
    week = IntegerField()
    room = CharField()

class Lecture(BaseModel):
    #subject = ForeignKeyField(Subject, column_name="sub_id")
    subject = ForeignKeyField(Subject)
    topic = CharField()
    duration = IntegerField()



class MyDataBase:
    def __init__(self, name):
        mainDatabase = SqliteDatabase(name)
        try:
            mainDatabase.connect()
        except peewee.InterfaceError:
            mainDatabase.create_tables([Faculty, Teacher, Subject, Seminar, Lecture])



