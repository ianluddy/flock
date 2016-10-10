# Stuff that doesn't change
# -*- coding: utf-8 -*-

SESSION_DURATION = 1800
SECRET_KEY = "\x13`4\xf5\x90:(Qs\xa2\x0f\xd8\xbe\xee\x1b5Ae!\x9b\xd4\xe8\xf1\x94"
PERMISSIONS = {
    'view_events': 1,
    'edit_events': 2,
    'view_people': 4,
    'edit_people': 5,
    'view_places': 10,
    'edit_places': 11,
    'edit_system_settings': 22
}

MAIL_AUTH = ("api", "key-97da181732b95a21257c270bd2215529")
MAIL_SERVER = "https://api.mailgun.net/v3/tryflock.com/messages"
MAIL_SENDER = "Flock Notifications <notifications@tryflock.com>"


PROFILE_IMAGE_DIR = "img/profile/"
PROFILE_IMAGE_TYPES = ['png', 'jpg', 'gif', 'jpeg']

PAGE_SIZE = 10

DEFAULT_DATA = {
}

TEST_DATA = {
    'Role': [
        {
            'id': -1,
            'name': 'Manager',
            'permissions': ['edit_events', 'edit_people', 'edit_places', 'edit_system_settings'],
            'company': -1,
            'theme': 'success',
            'rank': 40
        },
        {
            'id': -2,
            'name': 'Trainee',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'danger',
            'rank': 18
        },
        {
            'id': -3,
            'name': 'Connector',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'warning',
            'rank': 18
        },
        {
            'id': -4,
            'name': 'Independent',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'info',
            'rank': 18
        },
        {
            'id': -5,
            'name': 'Student',
            'permissions': ['view_events', 'view_people', 'view_places'],
            'company': -1,
            'theme': 'primary',
            'rank': 15
        },
        {
            'id': -6,
            'name': 'External',
            'permissions': [],
            'company': -1,
            'theme': 'info',
            'rank': 0

        }
    ],
    'Person': [
        {
            "id": -1,
            "email": "ian@tryflock.com",
            "name": "Ian Luddy",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            'phone': '083-4554553',
            "image": "img/profile/a1.jpg"
        },
        {
            "id": -2,
            "email": "dani@tryflock.com",
            "name": "Dani Brown",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -1,
            "role_name": "Manager",
            "role_theme": "success",
            'phone': '083-4322123',
            "image": "img/profile/a2.jpg"
        },
        {
            "id": -3,
            "email": "kacper@tryflock.com",
            "name": "Kacper Oppegård",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -1,
            "role_name": "Manager",
            "role_theme": "success",
            'phone': '083-3676362',
            "image": "img/profile/a3.jpg"
        },
        {
            "id": -4,
            "email": "牛禹凡@tryflock.com",
            "name": "牛禹凡",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning",
            'phone': '083-5512122',
            "image": "img/profile/a4.jpg"
        },
        {
            "id": -5,
            "email": "jürgen@tryflock.com",
            "name": "Jürgen Wexler",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning",
            "image": "img/profile/a5.jpg"
        },
        {
            "id": -6,
            "email": "jane@tryflock.com",
            "name": "Jane Abrams",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning"
        },
        {
            "id": -7,
            "email": "joe@tryflock.com",
            "name": "Joe Bloggs",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/a7.jpg"
        },
        {
            "id": -8,
            "email": "jim@tryflock.com",
            "name": "Jim Bloggs",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/a8.jpg"
        },
        {
            "id": -9,
            "email": "harry@tryflock.com",
            "name": "Harry Andrews",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/1.png"
        },
        {
            "id": -10,
            "email": "garry@tryflock.com",
            "name": "Garry Doherty",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/2.png"
        },
        {
            "id": -11,
            "email": "dan@tryflock.com",
            "name": "Dan White",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/3.png"
        },
        {
            "id": -12,
            "email": "gary@tryflock.com",
            "name": "Gary Black",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/4.png"
        },
        {
            "id": -13,
            "email": "mary@tryflock.com",
            "name": "Mary O' Sullivan",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger",
            "image": "img/profile/5.png"
        }
    ],
    'Company': [
        {
            'id': -1,
            'name': 'TryFlock Ltd.',
            'owner': -1
        }
    ],
    'Place': [
        {
            'id': -1,
            'name': 'Guinness Enterprise Centre',
            'address': 'Taylors Lane, Dublin 8',
            'email': 'info@gec.ie',
            'phone': '01-7997991',
            'company': -1
        },
        {
            'id': -2,
            'name': 'Starbucks Westmoreland St.',
            'address': '12 Westmoreland St, Dublin 8',
            'email': 'info@starbucks.ie',
            'phone': '01-7447865',
            'company': -1
        },
        {
            'id': -3,
            'name': 'Cafe Noto',
            'address': '2 Thomas St, Dublin 8',
            'email': 'info@noto.ie',
            'phone': '01-7732321',
            'company': -1
        },
        {
            'id': -4,
            'name': 'St Kevins Library',
            'address': '2 Kevin Street, Dublin 8',
            'email': 'info@kevinstlibrary.ie',
            'phone': '01-4141412',
            'company': -1
        },
        {
            'id': -5,
            'name': 'Galway Office',
            'address': '12 William St, Galway',
            'email': 'galway@tryflock.com',
            'phone': '091-755795',
            'company': -1
        },
        {
            'id': -6,
            'name': 'Room 101',
            'address': 'Head Office, Dublin 8',
            'email': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -7,
            'name': 'Room 102',
            'address': 'Head Office, Dublin 8',
            'email': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -8,
            'name': 'Room 103',
            'address': 'Head Office, Dublin 8',
            'email': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -9,
            'name': 'Room 104',
            'address': 'Head Office, Dublin 8',
            'email': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -10,
            'name': 'Cork Office',
            'address': '12 Bridge Street, Cork',
            'email': 'cork@tryflock.com',
            'phone': '07-5551234',
            'company': -1
        },
    ],
    'EmailRule': [
        {
            'id': -1,
            'added': True,
            'deleted': False,
            'edited': False,
            'roles': [-1, -2, -3],
            'object': 'event',
            'all': True,
            'company': -1
        },
        {
            'id': -2,
            'added': True,
            'deleted': True,
            'edited': True,
            'roles': [-1, -2],
            'object': 'person',
            'company': -1
        },
        {
            'id': -3,
            'added': True,
            'deleted': True,
            'edited': True,
            'roles': [],
            'object': 'place',
            'company': -1
        },
        {
            'id': -4,
            'added': True,
            'deleted': False,
            'edited': True,
            'roles': [],
            'object': 'place',
            'company': -1,
            'enabled': False
        },
        {
            'id': -5,
            'added': True,
            'deleted': False,
            'edited': True,
            'roles': [-1, -2, -3, -4, -5, -6],
            'object': 'place',
            'company': -1,
            'enabled': False
        }
    ]
}