from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class School(BaseModel):
    id = AutoField()
    name = CharField()


class SchoolBuilding(BaseModel):
    id = AutoField()
    name = CharField()
    address = CharField()
    school = ForeignKeyField(School, backref="buildings")


class Class(BaseModel):
    id = AutoField()
    name = CharField()
    building = ForeignKeyField(SchoolBuilding, backref="classes")


class Teacher(BaseModel):
    id = AutoField()
    name = CharField()
    surname = CharField()
    patronymic = CharField()


class Course(BaseModel):
    id = AutoField()
    name = CharField()
    type = CharField()
    code = IntegerField(unique=True)
    is_paid = BooleanField()
    is_registration_required = BooleanField()
    teacher = ForeignKeyField(Teacher, backref="courses")
    building = ForeignKeyField(SchoolBuilding, backref="courses")
    start_date = DateField()


class CourseType(BaseModel):
    id = AutoField()
    name = CharField()
    courses = ManyToManyField(Course, backref="course_types")


def create_tables():
    db.connect()
    with db:
        db.create_tables([SchoolBuilding, Teacher, School, Class, Course, CourseType])
