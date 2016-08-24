from mongoengine import Document, SequenceField, IntField, StringField, BooleanField, ReferenceField, ListField, DateTimeField
from mongoengine import PULL, DENY, NULLIFY
from constants import PROFILE_IMAGE_DIR
from datetime import datetime
from utils import account_token, capitalise, random_uuid


# TODO - add indexes

class Base(object):

    def to_dict(self):
        return self.to_mongo()

class Place(Document, Base):
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    address = StringField(nullable=False)
    email = StringField()
    phone = StringField()
    company = ReferenceField('Company', nullable=False)

class Thing(Document, Base):
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    description = StringField(nullable=True)
    company = ReferenceField('Company', nullable=False)

class Role(Document, Base):
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    name = StringField(nullable=False)
    theme = StringField(nullable=False)
    company = ReferenceField('Company', nullable=False)
    permissions = ListField(StringField(nullable=False), nullable=False)
    rank = IntField(nullable=False, default=0)

class Person(Document, Base):
    # TODO - allow email to be registered with multiple companies
    meta = {
        'indexes': [
            {'fields': ('company', 'name'), 'unique': True}
        ]
    }
    id = SequenceField(primary_key=True)
    email = StringField(unique=True, nullable=False)
    phone = StringField(nullable=True)
    name = StringField()
    invite = BooleanField(default=True)
    active = BooleanField(default=False)
    password = StringField(min_length=8)
    image = StringField(default="{}{}".format(PROFILE_IMAGE_DIR, "placeholder.png"))
    company = ReferenceField('Company', nullable=False)
    role = ReferenceField('Role', nullable=False, reverse_delete_rule=DENY)
    role_name = StringField(nullable=False)
    role_theme = StringField(nullable=False)
    token = StringField()

    def generate_token(self):
        self.token = account_token()
        return self.token

    @property
    def initials(self):
        return ''.join(name[0].upper() for name in self.name.split())

    def to_dict(self):
        output = self.to_mongo()
        if 'password' in output:
            del output['password']
        return output

class Event(Document, Base):
    id = SequenceField(primary_key=True)
    title = StringField(nullable=False)
    description = StringField(nullable=True)
    owner = ReferenceField('Person', reverse_delete_rule=NULLIFY)
    start = DateTimeField(nullable=False)
    end = DateTimeField()
    people = ListField(ReferenceField('Person', reverse_delete_rule=PULL))
    things = ListField(ReferenceField('Thing', reverse_delete_rule=PULL))
    place = ReferenceField('Place', reverse_delete_rule=DENY)
    company = ReferenceField('Company', nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'people': sorted(
                [{'initials': person.initials, 'name': person.name, 'theme': person.role_theme, 'id': person.id} for person in self.people],
                key=lambda x: x['theme']
            ),
            'start': str(self.start),
            'end': str(self.end),
            'owner': self.owner.name if self.owner else None,
            'place': {
                'name': self.place.name if self.place else None,
                'id': self.place.id if self.place else None,
            }
        }

class Company(Document, Base):
    id = SequenceField(primary_key=True)
    name = StringField(unique=True)
    status = StringField(default='trialling')
    created = DateTimeField(default=datetime.now)
    owner = ReferenceField('Person', reverse_delete_rule=DENY)

    def save(self, *args, **kwargs):

        # Create default Roles
        admin = Role(name='Administrator', theme='success', rank=40, company=self,
             permissions=[
                 'edit_events', 'edit_people', 'edit_places', 'edit_system_settings'
             ]
        ).save()
        Role(name='Regular User', theme='primary', rank=18, company=self,
             permissions=[
                 'edit_events', 'edit_people', 'edit_places'
             ]
        ).save()
        Role(name='Read-Only User', theme='warning', rank=0, company=self,
             permissions=[
                 'view_events', 'view_people', 'view_places'
             ]
        ).save()

        # Set owner as Admin
        self.owner.update(
            role=admin,
            role_name=admin.name,
            role_theme=admin.theme,
            active=True
        )

        return super(Company, self).save(*args, **kwargs)

class Notification(Document, Base):
    id = SequenceField(primary_key=True)
    stamp = DateTimeField(default=datetime.now)
    body = StringField()
    image = StringField()
    message = StringField(nullable=True)
    action = StringField(nullable=False, default='action')
    target = StringField(nullable=False, default='message')
    company = ReferenceField('Company')
    owner = ReferenceField('Person')

    def to_dict(self):
        output = self.to_mongo()
        output['stamp'] = str(output['stamp'])
        return output

class EmailRule(Document, Base):
    id = SequenceField(primary_key=True)
    roles = ListField(ReferenceField('Role'))
    added = BooleanField(default=False)
    edited = BooleanField(default=False)
    deleted = BooleanField(default=False)
    company = ReferenceField('Company')
    object = StringField()
    all = BooleanField(default=False) # Eg. All Events or just relevant Events
    enabled = BooleanField(default=True)

    def to_dict(self):
        output = self.to_mongo()
        output['roles'] = sorted(
            [{'name': role.name, 'theme': role.theme, 'id': role.id} for role in self.roles],
            key=lambda x: x['name']
        )
        output['object'] = self.plural
        return output

    @property
    def plural(self):
        return {
            "event": "Events",
            "person": "People",
            "place": "Places",
        }[str(self.object)]