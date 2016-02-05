from mongoengine import *
from datetime import datetime

class Person(Document):
    id = SequenceField(primary_key=True)
    mail = StringField(unique=True)
    name = StringField()
    password = StringField()
    company = ReferenceField('Company')
    type = StringField() # admin, leader

class Event(Document):
    id = SequenceField(primary_key=True)
    owner = ReferenceField('Person')
    people = ListField(ReferenceField('Person'))
    things = ListField(ReferenceField('Thing'))
    name = StringField()
    place = ReferenceField('Place')

class Place(Document):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    description = StringField()

class Company(Document):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    status = StringField(default='trialling')
    joined = DateTimeField(default=datetime.now)

class Notification(Document):
    id = SequenceField(primary_key=True)
    title = StringField()
    body = StringField()
    company = DateTimeField(default=datetime.now)
    person = ReferenceField('Person')

class Thing(Document):
    id = SequenceField(primary_key=True)
    title = StringField()
    body = StringField()
