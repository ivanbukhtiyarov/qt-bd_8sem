
from myModel import *

from peewee import *


mainDatabase = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = mainDatabase

class Faculty(BaseModel):
    #faculty_id = AutoField()
    name = CharField(unique = True)
    house = CharField()
    institute = CharField()

class Student(BaseModel):
    name = CharField(unique = True)
    #faculty = ForeignKeyField(Faculty, column_name="faculty_id")
    faculty = ForeignKeyField(Faculty)

class Teacher(BaseModel):
    #teacher_id = AutoField()
    name = CharField(unique = True)
    experience = IntegerField()
    #subject = ForeignKeyField(Subject, column_name="sub_id")

class Subject(BaseModel):
    #sub_id = AutoField()
    name = CharField(unique = True)
    #teacher = ForeignKeyField(Teacher, column_name="teacher_id", backref="subject")
    teacher = ForeignKeyField(Teacher, backref="subject")
    sem = IntegerField()
    #faculty = ForeignKeyField(Faculty, column_name="faculty_id")
    faculty = ForeignKeyField(Faculty)

class Seminar(BaseModel):
    #subject = ForeignKeyField(Subject, column_name="sub_id")
    subject = ForeignKeyField(Subject)
    week = IntegerField()
    topic = CharField()
    room = CharField()

class Lecture(BaseModel):
    #subject = ForeignKeyField(Subject, column_name="sub_id")
    subject = ForeignKeyField(Subject)
    topic = CharField()
    duration = IntegerField()


def initDatabase():
    print("init")
    tmp_f = Faculty(name = "I-tech", house = "k", institute = "kib")
    tmp_f.save()
    tmp_t = Teacher(name = "Putin", experience = 9999)
    tmp_t.save()
    tmp_s = Subject(name = "TU", teacher = tmp_t, sem = 8, faculty = tmp_f)
    tmp_s.save()
    tmp_st = Student(name = "Petya", faculty = tmp_f)
    tmp_st.save()
    tmp_l = Lecture(topic = "slepping", subject = tmp_s, duration = 8)
    tmp_l.save()


class MyDataBase:
    def __init__(self, name):
        #mainDatabase = SqliteDatabase(name)
        mainDatabase.init(name)
        mainDatabase.connect()
        mainDatabase.create_tables([Faculty, Teacher, Subject, Seminar, Lecture, Student])
        try:
            initDatabase()
        except IntegrityError:
            pass

        #self._query = {"first":self.first, "second":self.second, "third":self.third}

    def subjects(self):
        return [i.name for i in Subject.select()]

    def faculties(self):
        return [i.name for i in Faculty.select()]

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

    def first(self, num):
        #tmp = [i.topic for i in Lecture.select().where(Lecture.subject.sem == num)]
        tmp = [i.topic for i in Lecture.select().join(Subject).where(Subject.sem == num)]
        print(tmp)
        return MyModel(tmp, ['topics'])

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


