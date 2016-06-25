from flask import request, redirect, url_for, render_template, session, abort
from functools import wraps
from utils import json_response
from constants import PAGE_SIZE, SESSION_DURATION
from services import notification as notification_service
from services import role as role_service
from services import account as account_service
from services import event as event_service
from services import person as person_service
from services import place as place_service
from flock.app import db_wrapper
import json
from datetime import datetime
from time import time
import __builtin__
app = __builtin__.flock_app

def auth(permissions=None):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):

            session['stamp'] = time()
            if session.get('user_id') is None:
                session.clear()
                abort(403, 'You are no longer logged in!')

            user_permissions = db_wrapper.permissions_get(session['user_id'])
            for permission in permissions or []:
                if not user_permissions or permission not in user_permissions:
                    abort(400, "You don't have permission to do this!")

            return test_func(*args, **kwargs)
        return wrapper
    return actualDecorator

def parse_args(string_args=None, int_args=None, json_args=None, bool_args=None):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            input = request.form
            output = {}
            for key in string_args or []:
                output[key] = input.get(key)

            for key in int_args or []:
                output[key] = int(input.get(key, 0))

            for key in json_args or []:
                input_json = input.get(key)
                output[key] = json.loads(input_json) if input_json else input_json

            for key in bool_args or []:
                output[key] = bool(input.get(key, False))

            return test_func(output, *args, **kwargs)
        return wrapper
    return actualDecorator

@app.route('/heartbeat')
def heartbeat():
    if 'stamp' not in session or time() - session['stamp'] > SESSION_DURATION:
        session.clear()
        abort(403, 'You are no longer logged in!')
    return "Still logged in :)", 200

@app.route('/')
def root():
    if session.get('user_id') is None:
        return redirect(url_for('login'))

    permissions = db_wrapper.permissions_get(session['user_id'])
    if permissions is None:
        return redirect(url_for('login'))

    return render_template(
        'index.html',
        user_name=session['user_name'],
        user_id=session['user_id'],
        company_id=session['company_id'],
        company_name=session['company_name'],
        permissions=permissions
    )

@app.route('/templates')
def templates():
    return app.send_static_file('hb_templates/templates.html')

#### User Account/Session ####

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/activate/<token>')
def activate_form(token):
    person = db_wrapper.person_get(token=token)

    # Can't find user by this token so they must be active
    if not person:
        return render_template(
            'login.html',
            error_msg="Woops, we couldn't find your invitation. You'll need to ask your administrator to send a new one. "
        )

    # Account already activated
    if person.active:
        return render_template(
            'login.html',
            info_msg="Your account has already been activated. You can log in now."
        )

    return render_template('activate.html', token=token, name=person.name, email=person.email)

@app.route('/activate', methods=['POST'])
@parse_args(string_args=['token', 'name', 'password', 'email'])
def activate_account(account):
    db_wrapper.activate_user(
        account['token'],
        account['name'],
        account['password']
    )
    session['user_id'], session['user_name'], session['company_id'], session['company_name'], session['email'] = \
        db_wrapper.authenticate_user(account['email'], account['password'])
    return 'Account Activated :)', 200

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/registration')
def registration():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
@parse_args(string_args=['email', 'name', 'password', 'company'])
def register(user):
    db_wrapper.register_user(
        user["name"],
        user["email"],
        user["password"],
        user["company"]
    )
    return login_user()

@app.route('/user', methods=['GET'])
def user():
    return json_response(person_service.get(session['company_id'], email=session['email']).to_dict())

@app.route('/user', methods=['POST'])
@parse_args(string_args=['phone', 'name'])
def user_post(user):
    user.update({
        'id': session['user_id'],
        'email': session['email']
    })
    person_service.update(user)
    session['user_name'] = user['name']
    return 'Account Updated', 200

@app.route('/password', methods=['POST'])
@parse_args(string_args=['new', 'current'])
def password_post(password):
    db_wrapper.authenticate_user(session['email'], password['current'])
    db_wrapper.update_password(session['email'], password['new'])
    return "Password Updated", 200

@app.route('/login_user', methods=['POST'])
@parse_args(string_args=['password', 'email'])
def login_user(user):
    session['user_id'], session['user_name'], session['company_id'], session['company_name'], session['email'] = \
        db_wrapper.authenticate_user(user['email'], user['password'])
    return 'Logged in :)', 200

@app.route('/reset_user', methods=['POST'])
def reset_user():
    account_service.reset(request.form.get("email"))
    return 'Password reset. You should receive an email shortly :)', 200

#### People ####

@app.route('/people', methods=['DELETE'])
@auth(['edit_people'])
@parse_args(int_args=['id'], string_args=['name'])
def people_delete(person):
    person_service.delete(person["id"], session['user_id'], session['company_id'])
    return u'{} has been deleted'.format(person["name"]), 200

@app.route('/people', methods=['GET'])
@auth()
def people():
    data, count = person_service.get(
        session['company_id'],
        search=request.args.get('search'),
        sort_by=request.args.get('sort_by'),
        sort_dir=request.args.get('sort_dir'),
        limit=int(request.args.get('limit', PAGE_SIZE)),
        offset=int(request.args.get('offset', 0))
    )
    return json_response({'data': data, 'count': count})

@app.route('/people', methods=['PUT'])
@auth(['edit_people'])
@parse_args(string_args=['name', 'email', 'phone'], bool_args=['invite'], int_args=['id', 'role'])
def people_put(person):
    person['company'] = session['company_id']
    person_service.update(person)
    return u'{} has been updated'.format(person['name']), 200

@app.route('/people', methods=['POST'])
@auth(['edit_people'])
@parse_args(string_args=['name', 'email', 'phone'], bool_args=['invite'], int_args=['role'])
def people_post(person):
    person['company'] = session['company_id']
    person_service.add(person, session['user_id'], session['company_id'])
    return u'{} has been added'.format(person['name']), 200

@app.route('/people/invite', methods=['POST'])
@auth(['edit_people'])
def people_invite():
    email = request.form.get("email")
    person_service.invite(email, session['user_id'], session['company_id'])
    return u'Invitation has been sent to {}'.format(email), 200

#### Places ####

@app.route('/places', methods=['DELETE'])
@auth(['edit_places'])
def places_delete():
    place_service.delete(request.form.get("id"))
    return u'{} has been deleted'.format(request.form.get("name")), 200

@app.route('/places', methods=['GET'])
@auth()
def places():
    data, count = place_service.get(
        session['company_id'],
        search=request.args.get('search'),
        sort_by=request.args.get('sort_by'),
        sort_dir=request.args.get('sort_dir'),
        limit=int(request.args.get('limit', PAGE_SIZE)),
        offset=int(request.args.get('offset', 0))
    )
    return json_response({'data': data, 'count': count})

@app.route('/places', methods=['POST'])
@auth(['edit_places'])
@parse_args(string_args=['name', 'email', 'phone', 'address'], int_args=['id'])
def places_add(place):
    place['company'] = session['company_id']
    place_service.add(place)
    return u'{} has been added'.format(place['name']), 200

@app.route('/places', methods=['PUT'])
@auth(['edit_places'])
@parse_args(string_args=['name', 'email', 'phone', 'address'], int_args=['id'])
def places_update(place):
    place['company'] = session['company_id']
    place_service.update(place)
    return u'{} has been updated'.format(place['name']), 200

#### Events ####

@app.route('/events', methods=['GET'])
@auth()
def events():
    return json_response(event_service.get(
        session['company_id'],
        event_id=int(request.args.get('id', 0)),
        user_id=int(request.args.get('user_id', 0)),
        start=request.args.get('start'),
        end=request.args.get('end'),
        hide_expired='hide_expired' in request.args,
        limit=int(request.args.get('limit', PAGE_SIZE)) if 'limit' in request.args else None,
        sort_dir=request.args.get('sort_dir'),
        sort_by=request.args.get('sort_by'),
        offset=int(request.args.get('offset', 0)) if 'offset' in request.args else None,
    ))

@app.route('/events', methods=['POST'])
@auth(['edit_events'])
@parse_args(string_args=['title', 'description', 'start', 'end'], int_args=['place'], json_args=['people'])
def events_post(event):
    event.update({
        'owner': session['user_id'],
        'company': session['company_id'],
        'people': [int(person_id) for person_id in event['people']],
        'start': datetime.strptime(event['start'], '%a %b %d %Y %H:%M'),
        'end': datetime.strptime(event['end'], '%a %b %d %Y %H:%M'),
    })
    event_service.add(event)
    return u'{} Event Added'.format(event['title'])

@app.route('/events', methods=['PUT'])
@auth(['edit_events'])
@parse_args(string_args=['title', 'description', 'start', 'end'], int_args=['id', 'place'], json_args=['people'])
def events_put(event):
    event.update({
        'owner': session['user_id'],
        'company': session['company_id'],
        'people': [int(person_id) for person_id in event['people']],
        'start': datetime.strptime(event['start'], '%a %b %d %Y %H:%M'),
        'end': datetime.strptime(event['end'], '%a %b %d %Y %H:%M'),
    })
    event_service.update(event)
    return u'{} Event Updated'.format(event['title'])

@app.route('/events', methods=['DELETE'])
@auth(['edit_events'])
@parse_args(int_args=['id'], string_args=['title'])
def events_delete(event):
    event_service.delete(event)
    return u'{} Event Deleted'.format(event['title'])

#### Roles ####

@app.route('/roles', methods=['GET'])
@auth()
def roles():
    return json_response(role_service.get(company_id=session['company_id'], user_id=session['user_id']))

@app.route('/roles', methods=['PUT'])
@auth(['edit_system_settings'])
@parse_args(int_args=['id'], string_args=['theme', 'name'], json_args=['permissions'])
def roles_update(role):
    role_service.update(role)
    return u'{} Role Updated'.format(role['name']), 200

@app.route('/roles', methods=['POST'])
@auth(['edit_system_settings'])
@parse_args(string_args=['theme', 'name'], json_args=['permissions'])
def roles_add(role):
    role_service.add(role, session['company_id'])
    return u'{} Role Added'.format(role["name"]), 200

@app.route('/roles', methods=['DELETE'])
@auth(['edit_system_settings'])
def roles_delete():
    role_id = request.form.get("id")
    role = role_service.get(role_id=role_id)
    role_service.delete(role_id)
    return u'{} Role Deleted'.format(role.name), 200

#### Notifications ####

@app.route('/notifications', methods=['GET'])
@auth()
def notifications():
    return json_response(notification_service.get(
        company_id=session['company_id'],
        limit=int(request.args.get('limit', PAGE_SIZE)),
        offset=int(request.args.get('offset', 0)),
        sort_by=request.args.get('sort_by'),
        sort_dir=request.args.get('sort_dir')
    ))