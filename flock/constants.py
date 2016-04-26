# Stuff that doesn't change
# -*- coding: utf-8 -*-

SESSION_DURATION = 1800
SECRET_KEY = "\x13`4\xf5\x90:(Qs\xa2\x0f\xd8\xbe\xee\x1b5Ae!\x9b\xd4\xe8\xf1\x94"
PERMISSIONS = [
    'view_events',
    'edit_events',
    'view_people',
    'edit_people',
    'view_places',
    'edit_places',
    'edit_system_settings'
]

# TODO - use non dev server
MAIL_AUTH = ("api", "key-97da181732b95a21257c270bd2215529")
MAIL_SERVER = "https://api.mailgun.net/v3/sandboxd4ff99d2df0b4dbbb94cc9e08a0391d1.mailgun.org/messages"
MAIL_SENDER = "Flock Notifications <notifications@tryflock.com>"

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
            'theme': 'success'
        },
        {
            'id': -2,
            'name': 'Trainee',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'danger'
        },
        {
            'id': -3,
            'name': 'Connector',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'warning'
        },
        {
            'id': -4,
            'name': 'Independent',
            'permissions': ['edit_events', 'edit_people', 'edit_places'],
            'company': -1,
            'theme': 'info'
        },
        {
            'id': -5,
            'name': 'Student',
            'permissions': ['view_events', 'view_people', 'view_places'],
            'company': -1,
            'theme': 'primary'
        },
        {
            'id': -6,
            'name': 'External',
            'permissions': [],
            'company': -1,
            'theme': 'info'
        }
    ],
    'Person': [
        {
            "id": -1,
            "mail": "ian@tryflock.com",
            "name": "Ian Luddy",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            'phone': '083-4554553'
        },
        {
            "id": -2,
            "mail": "dani@tryflock.com",
            "name": "Dani Brown",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -1,
            "role_name": "Manager",
            "role_theme": "success",
            'phone': '083-4322123'
        },
        {
            "id": -3,
            "mail": "kacper@tryflock.com",
            "name": "Kacper Oppegård",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -1,
            "role_name": "Manager",
            "role_theme": "success",
            'phone': '083-3676362'
        },
        {
            "id": -4,
            "mail": "牛禹凡@tryflock.com",
            "name": "牛禹凡",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning",
            'phone': '083-5512122'
        },
        {
            "id": -5,
            "mail": "jürgen@tryflock.com",
            "name": "Jürgen Wexler",
            "invite": True,
            "active": False,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -3,
            "role_name": "Connector",
            "role_theme": "warning"
        },
        {
            "id": -6,
            "mail": "erskine@tryflock.com",
            "name": "Erskine Abrams",
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
            "mail": "joe@tryflock.com",
            "name": "Joe Bloggs",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -8,
            "mail": "jim@tryflock.com",
            "name": "Jim Bloggs",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -9,
            "mail": "jaylin@tryflock.com",
            "name": "Jaylin Adcock",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -10,
            "mail": "gyles@tryflock.com",
            "name": "Gyles Traviss",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -11,
            "mail": "dan@tryflock.com",
            "name": "Dan White",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -12,
            "mail": "gary@tryflock.com",
            "name": "Gary Black",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
        },
        {
            "id": -13,
            "mail": "mary@tryflock.com",
            "name": "Mary O' Sullivan",
            "invite": True,
            "active": True,
            "password": "pbkdf2:sha1:1000$Ejjo3uqM$04d48dc71ce6460f6454f403ef6e331ce7acfad3",
            "company": -1,
            "role": -2,
            "role_name": "Trainee",
            "role_theme": "danger"
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
            'mail': 'info@gec.ie',
            'phone': '01-7997991',
            'company': -1
        },
        {
            'id': -2,
            'name': 'Starbucks Westmoreland St.',
            'address': '12 Westmoreland St, Dublin 8',
            'mail': 'info@starbucks.ie',
            'phone': '01-7447865',
            'company': -1
        },
        {
            'id': -3,
            'name': 'Cafe Noto',
            'address': '2 Thomas St, Dublin 8',
            'mail': 'info@noto.ie',
            'phone': '01-7732321',
            'company': -1
        },
        {
            'id': -4,
            'name': 'St Kevins Library',
            'address': '2 Kevin Street, Dublin 8',
            'mail': 'info@kevinstlibrary.ie',
            'phone': '01-4141412',
            'company': -1
        },
        {
            'id': -5,
            'name': 'Galway Office',
            'address': '12 William St, Galway',
            'mail': 'galway@tryflock.com',
            'phone': '091-755795',
            'company': -1
        },
        {
            'id': -6,
            'name': 'Room 101',
            'address': 'Head Office, Dublin 8',
            'mail': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -7,
            'name': 'Room 102',
            'address': 'Head Office, Dublin 8',
            'mail': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -8,
            'name': 'Room 103',
            'address': 'Head Office, Dublin 8',
            'mail': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -9,
            'name': 'Room 104',
            'address': 'Head Office, Dublin 8',
            'mail': 'info@tryflock.com',
            'phone': '01-5551234',
            'company': -1
        },
        {
            'id': -10,
            'name': 'Cork Office',
            'address': '12 Bridge Street, Cork',
            'mail': 'cork@tryflock.com',
            'phone': '07-5551234',
            'company': -1
        },
    ]
}