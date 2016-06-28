from datetime import timedelta
from random import randint, choice
from werkzeug.exceptions import abort
import models as mo
from constants import *
from models import *
from utils import random_password, validate_password, evaluate_permissions
from mongoengine import NotUniqueError, DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash

class Database():
    """
    Wrapper for the database layer
    """
    def __init__(self, db, cfg):
        self.db = db
        self.cfg = cfg
        if cfg['database']['reset']:
            self.reset_database()
        self.add_defaults()
        if cfg['database']['add_test_data']:
            self.add_test_data()
        self.add_indexes()

    #### Utils ####

    def add_indexes(self):
        pass
        # self.db.person.createIndex({"company": 1, "email": 1})

    def add_defaults(self):
        for collection_name, data in DEFAULT_DATA.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                doc(**document).save()

    def reset_database(self):
        Person.drop_collection()
        Role.drop_collection()
        Place.drop_collection()
        Event.drop_collection()
        Company.drop_collection()
        Notification.drop_collection()

    def add_test_data(self):
        for collection_name, data in TEST_DATA.iteritems():
            doc = getattr(mo, collection_name)
            for document in data:
                try:
                    doc(**document).save()
                except NotUniqueError:
                    pass
        self.create_random_events()
        self.create_random_notifications()

    def create_random_events(self):
        meetings = [
            ("Daily Stand Up", "Daily meeting to report on the day's upcoming tasks as well as any potential problems"),
            ("Greeting Clients", "Get-together to greet new clients"),
            ("Weekly Retrospective", "Weekly meeting to analyse the week's events and identify any issues"),
            ("Marketing Brainstorm", "Monthly marketing brainstorm to identify growth points"),
            ("Weekly One-to-One", "Weekly meeting between staff and managers to identify any issues and discuss developments"),
        ]
        id = -1
        for i in range(-7, 7):
            for j in range(25):
                id -= 1
                hour = randint(6, 18)
                start = datetime.utcnow() + timedelta(days=i)
                start = start.replace(hour=hour, minute=0)
                end = start.replace(hour=hour + 1)
                title, description = choice(meetings)
                Event(
                    id=id,
                    start=start,
                    end=end,
                    company=-1,
                    people=[randint(-10, -1), randint(-10, -1)],
                    place=randint(-10, -1),
                    owner=randint(-10, -1),
                    title=title,
                    description=description
                ).save()

    def create_random_notifications(self):
        notifications = [
            u'<b>{}</b> created a new Event',
            u'<b>{}</b> edited an Event',
            u'<b>{}</b> removed an Event',
            u'<b>{}</b> added a new Person',
            u'<b>{}</b> added a new Place',
        ]
        id = -1
        for i in range(-7, 0):
            for j in range(25):
                id -= 1
                owner = Person.objects.get(id=randint(-10, -1))
                Notification(
                    id=id,
                    stamp=(datetime.utcnow() + timedelta(days=i)).replace(hour=randint(6, 18), minute=0),
                    company=-1,
                    owner=owner.id,
                    body=choice(notifications).format(owner.name)
                ).save()

    #### User Account ####

    def register_user(self, name, email, password, company):
        validate_password(password)

        new_company = Company(name=company)

        try:
            owner = Person(name=name, email=email.lower(), password=generate_password_hash(password), company=new_company)
            owner.save()
        except NotUniqueError:
            abort(400, 'Email address already in use :(')

        try:
            new_company.owner = owner
            new_company.save()
        except NotUniqueError:
            abort(400, 'Company name already in use :(')

    def permissions_get(self, user_id):
        try:
            role_id = self.person_get(user_id=user_id).role.id
            return self.role_get(role_id=role_id).permissions
        except DoesNotExist:
            return None

    def activate_user(self, token, name, password):
        validate_password(password)
        try:
            Person.objects(token=token).update_one(
                name=name,
                password=generate_password_hash(password),
                active=True
            )
        except DoesNotExist:
            abort(400, "Invitation expired. A new invitation will need to be sent. Please contact your Organisation's administrator.")

    def update_password(self, user_id, password):
        validate_password(password)
        Person.objects(id=user_id).update_one(
            password=generate_password_hash(password)
        )

    def generate_token(self, email):
        token = account_token()
        Person.objects(email=email).update_one(token=token, invite=True)
        return token

    def authenticate_user(self, email, password):
        try:
            user = self.person_get(email=email)
            if check_password_hash(user.password, password):
                return user.id, user.company.id
            abort(400, 'Password is incorrect :(')
        except DoesNotExist:
            abort(400, 'Email address not registered :(')

    def reset_user(self, email):
        new_password = random_password()
        try:
            user = self.person_get(email=email)
            user.password = generate_password_hash(new_password)
            user.save()
            return new_password
        except DoesNotExist:
            abort(400, 'Email address not registered :(')

    #### Person ####

    def person_delete(self, person_id):
        Person.objects(id=person_id).delete()

    def person_update(self, update):

        if 'role' in update:
            role = Role.objects(id=update['role']).get()
            Person.objects(id=int(update['id'])).update_one(
                role=role,
                role_name=role.name,
                role_theme=role.theme,
            )

        person = Person.objects(id=int(update['id']))
        person.update_one(**update)
        return person.first().name

    def person_add(self, new_person):

        # Role
        role = Role.objects(id=new_person['role']).get()
        new_person['role'] = role
        new_person['role_name'] = role.name
        new_person['role_theme'] = role.theme

        # Company
        new_person['company'] = Company.objects(id=new_person['company_id']).get()
        del new_person['company_id']

        # Email can either be a unique email address or can not exist
        if not new_person['email']:
            del new_person['email']
        else:
            new_person['email'] = new_person['email'].lower()

        try:
            return Person(**new_person).save()
        except NotUniqueError:
            abort(400, 'That email address is already in use.')

    def person_get(self, company_id=None, role_id=None, user_id=None, email=None, search=None, sort_by=None,
                   sort_dir=None, token=None, limit=None, offset=None):

        query = {}

        if company_id:
            query['company'] = int(company_id)

        if user_id:
            query['_id'] = int(user_id)
            return Person.objects.get(__raw__=query)

        if email:
            query['email'] = email.lower()
            return Person.objects.get(__raw__=query)

        if token:
            query['token'] = token
            try:
                return Person.objects.get(__raw__=query)
            except DoesNotExist:
                return None

        if role_id:
            query['role'] = int(role_id)
            return Person.objects(__raw__=query)

        if search:
            # TODO - deal with multiple search terms
            # TODO - search status. ie. active, invitation pending etc
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'email': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'role_name': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}}
            ]

        results = Person.objects(__raw__=query)
        count = len(results)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit is not None and offset is not None:
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results, count

    #### Event ####

    def event_add(self, event):
        # TODO - deal with recurring events
        return Event(**event).save()

    def event_update(self, event):
        # TODO - deal with recurring events
        people = [self.person_get(user_id=user_id) for user_id in event['people']] if event['people'] else None
        Event.objects(id=event['id']).update_one(
            title=event['title'],
            description=event['description'],
            start=event['start'],
            end=event['end'],
            people=people,
            place=self.place_get(place_id=event['place']),
        )

    def event_delete(self, event_id):
        Event.objects(id=event_id).delete()

    def event_get(self, company_id=None, event_id=None, start=None, end=None, hide_expired=False, place_id=None, limit=None,
            offset=None, sort_by=None, sort_dir='asc', user_id=None):

        query = {}

        if event_id:
            query['_id'] = int(event_id)
            return Event.objects(__raw__=query)

        if company_id:
            query['company'] = int(company_id)

        if place_id:
            query['place'] = int(place_id)

        if hide_expired:
            query['start'] = {'$gte': datetime.now()}

        if start:
            query['start'] = {'$gte': datetime.strptime(start, '%Y-%m-%d')}

        if end:
            query['end'] = {'$lte': datetime.strptime(end, '%Y-%m-%d')}

        if user_id:
            query['$or'] = [
                {'owner': user_id},
                {'people': user_id},
            ]

        results = Event.objects(__raw__=query)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit:
            offset = 0 if offset is None else offset
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results

    #### Place ####

    def place_get(self, company_id=None, place_id=None, search=None, sort_by=None, sort_dir=None, limit=None,
                  offset=None):

        query = {}

        if company_id is not None:
            query['company'] = company_id

        if place_id is not None:
            query['_id'] = int(place_id)
            return Place.objects.get(__raw__=query)

        if search:
            query['$or'] = [
                {'name': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'address': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'email': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}},
                {'phone': {'$options': 'i', '$regex': u'.*{}.*'.format(search)}}
            ]

        results = Place.objects(__raw__=query)
        count = len(results)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit is not None and offset is not None:
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results, count

    def place_delete(self, place_id):
        Place.objects(id=place_id).delete()

    def place_add(self, place):
        try:
            return Place(**place).save()
        except NotUniqueError:
            abort(400, 'A Place with that name is already registered')

    def place_update(self, place):
        Place.objects(id=int(place['id'])).update_one(
            name=place['name'],
            phone=place['phone'],
            email=place['email'],
            address=place['address']
        )

    #### Company ####

    def company_get(self, company_id):
        return Company.objects.get(id=company_id)

    #### Role ####

    def role_get(self, company_id=None, role_id=None, rank=None):

        query = {}

        if rank is not None:
            query['rank'] = {'$lte': rank}

        if company_id:
            query['company'] = int(company_id)
            return Role.objects(__raw__=query)

        if role_id:
            query['_id'] = int(role_id)
            return Role.objects.get(__raw__=query)

    def role_add(self, role, company_id):

        if Role.objects(company=company_id, name=role['name']):
            abort(400, 'A Role with this name already exists.')

        role['company'] = company_id
        role['rank'] = evaluate_permissions(role['permissions'])
        Role(**role).save()

    def role_update(self, role):
        Role.objects(id=role['id']).update_one(
            theme=role['theme'],
            name=role['name'],
            permissions=role['permissions'],
            rank=evaluate_permissions(role['permissions'])
        )

    def person_role_update(self, role):
        role = Role.objects.get(id=role['id'])
        Person.objects(role=role).update(
            role=role,
            role_name=role.name,
            role_theme=role.theme
        )

    def role_delete(self, role_id):
        Role.objects(id=role_id).delete()

    #### Notifications ####

    def notification_get(self, company_id, limit=None, offset=None, sort_by=None, sort_dir=None):

        results = Notification.objects(company=company_id)

        if sort_by:
            results = results.order_by('-' + sort_by if sort_dir == 'asc' else sort_by)

        if limit is not None and offset is not None:
            start = int(offset) * int(limit)
            end = start + int(limit)
            results = results[start:end]

        return results

    def notification_add(self, company_id, owner_id, body, action, target, message=None):
        Notification(
            stamp=datetime.now(),
            company=company_id,
            owner=owner_id,
            body=body,
            action=action,
            target=target,
            message=message,
        ).save()
