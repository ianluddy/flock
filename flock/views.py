from flask import request, redirect, url_for, render_template, session, abort
from functools import wraps
from utils import json_response
from constants import PAGE_SIZE
from services import notification as notification_service
from services import role as role_service
from services import account as account_service
from services import event as event_service
from services import person as person_service
from services import place as place_service
from flock.app import db_wrapper
import json
from datetime import datetime
import __builtin__
app = __builtin__.flock_app

def auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            session.clear()
            abort(403, 'You are no longer logged in!')
        # TODO - verify user and company match
        return f(*args, **kwargs)
    return decorated_function

def perm(permissions):
    def actualDecorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            user_permissions = db_wrapper.permissions_get(session['user_id'])
            for permission in permissions:
                if not user_permissions or permission not in user_permissions:
                    abort(400, "You don't have permission to do this :(")
            return test_func(*args, **kwargs)
        return wrapper
    return actualDecorator

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
@auth
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
        return redirect(url_for('login'))

    return render_template('activate.html', token=token, name=person.name, email=person.mail)

@app.route('/activate', methods=['POST'])
def activate_account():
    token = request.form.get("token")
    name = request.form.get("name")
    password = request.form.get("password")
    mail = request.form.get("email")

    db_wrapper.activate_user(token, name, password)
    session['user_id'], session['user_name'], session['company_id'], session['company_name'], session['email'] = \
        db_wrapper.authenticate_user(mail, password)

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
def register():
    db_wrapper.register_user(
        request.form.get("name"),
        request.form.get("mail"),
        request.form.get("password"),
        request.form.get("company"),
    )
    return login_user()

@app.route('/login_user', methods=['POST'])
def login_user():
    session['user_id'], session['user_name'], session['company_id'], session['company_name'], session['email'] = \
        db_wrapper.authenticate_user(request.form.get('mail'), request.form.get('password'))
    return 'Logged in :)', 200

@app.route('/reset_user', methods=['POST'])
def reset_user():
    account_service.reset(request.form.get("mail"))
    return 'Password reset. You should receive an email shortly :)', 200

#### People ####

@app.route('/people', methods=['DELETE'])
@perm(['edit_people'])
@auth
def people_delete():
    if request.form.get("id") == str(session['user_id']):
        abort(400, "You can't delete your own account :)")
    person_service.delete(request.form.get("id"))
    return u'{} has been deleted'.format(request.form.get("name")), 200

@app.route('/people', methods=['GET'])
@auth
def people():
    search = request.args.get("search", None)
    sort_by = request.args.get("sort_by", None)
    sort_dir = request.args.get("sort_dir", None)
    limit = request.args.get("limit", PAGE_SIZE)
    offset = request.args.get("offset", 0)
    data, count = person_service.get(session['company_id'], search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)
    return json_response({'data': data, 'count': count})

@app.route('/people', methods=['PUT'])
@perm(['edit_people'])
@auth
def people_put():
    invite = request.form.get("invite")
    new_person = {
        'id': request.form.get("id"),
        'name': request.form.get("name"),
        'mail': request.form.get("mail"),
        'role': request.form.get("type"),
        'phone': request.form.get("phone"),
        'invite': True if invite else False,
        'company': session['company_id']
    }
    person_service.update(new_person)
    return u'{} has been updated'.format(new_person['name']), 200

@app.route('/people', methods=['POST'])
@perm(['edit_people'])
@auth
def people_post():
    invite = request.form.get("invite")
    new_person = {
        'name': request.form.get("name"),
        'mail': request.form.get("mail"),
        'role': request.form.get("type"),
        'phone': request.form.get("phone"),
        'invite': True if invite else False,
        'company': session['company_id']
    }
    person_service.add(new_person, session['user_id'], session['company_id'])
    return u'{} has been added'.format(new_person['name']), 200


@app.route('/people/invite', methods=['POST'])
@perm(['edit_people'])
@auth
def people_invite():
    email = request.form.get("mail")
    person_service.invite(email, session['user_id'], session['company_id'])
    return u'Invitation has been sent to {}'.format(email), 200

#### Places ####

@app.route('/places', methods=['DELETE'])
@perm(['edit_places'])
@auth
def places_delete():
    place_service.delete(request.form.get("id"))
    return u'{} has been deleted'.format(request.form.get("name")), 200

@app.route('/places', methods=['GET'])
@auth
def places():
    search = request.args.get("search")
    sort_by = request.args.get("sort_by")
    sort_dir = request.args.get("sort_dir")
    limit = request.args.get("limit", PAGE_SIZE)
    offset = request.args.get("offset", 0)
    data, count = place_service.get(session['company_id'], search=search, sort_by=sort_by, sort_dir=sort_dir, limit=limit, offset=offset)
    return json_response({'data': data, 'count': count})

@app.route('/places', methods=['POST'])
@perm(['edit_places'])
@auth
def places_add():
    new_place = {
        'name': request.form.get("name"),
        'mail': request.form.get("email"),
        'phone': request.form.get("phone"),
        'address': request.form.get("address"),
        'company': session['company_id']
    }
    place_service.add(new_place)
    return u'{} has been added'.format(new_place['name']), 200

@app.route('/places', methods=['PUT'])
@perm(['edit_places'])
@auth
def places_update():
    updated_place = {
        'id': request.form.get("id"),
        'name': request.form.get("name"),
        'mail': request.form.get("email"),
        'phone': request.form.get("phone"),
        'address': request.form.get("address"),
        'company': session['company_id']
    }
    place_service.update(updated_place)
    return u'{} has been updated'.format(updated_place['name']), 200

#### Events ####

@app.route('/events', methods=['GET'])
@auth
def events():
    start = request.args.get("start")
    end = request.args.get("end")
    show_expired = request.args.get("show_expired", True)
    limit = request.args.get("limit")
    offset = request.args.get("offset")
    sort_by = request.args.get("sort_by")
    sort_dir = request.args.get("sort_dir")
    user_id = int(request.args.get("user_id", 0))
    return json_response(event_service.get(session['company_id'], start=start, end=end, show_expired=show_expired,
        limit=limit, sort_dir=sort_dir, sort_by=sort_by, offset=offset, user_id=user_id))

@app.route('/events', methods=['POST'])
@auth
def events_post():
    start_date = request.form.get('start_date')
    end_date =request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time =request.form.get('end_time')
    event = {
        'title': request.form.get('title'),
        'owner': session['user_id'],
        'company': session['company_id'],
        'people': [int(person_id) for person_id in json.loads(request.form.get('people'))],
        'place': int(request.form.get('place')),
        'start': datetime.strptime('{} {}'.format(start_date[:15], start_time), '%a %b %d %Y %H:%M'),
        'end': datetime.strptime('{} {}'.format(end_date[:15], end_time), '%a %b %d %Y %H:%M')
    }
    event_service.add(event)
    return u'{} Event Added'.format(event['title'])

#### Roles ####

@app.route('/roles', methods=['GET'])
@auth
def roles():
    return json_response(role_service.get(company_id=session['company_id']))

@app.route('/roles', methods=['PUT'])
@perm(['edit_system_settings'])
@auth
def roles_update():
    role = {
        "theme": request.form.get("theme"),
        "name": request.form.get("name"),
        "permissions": json.loads(request.form.get("permissions")),
        "id": int(request.form.get('id'))
    }
    role_service.update(role)
    return u'{} Role Updated'.format(role['name']), 200

@app.route('/roles', methods=['POST'])
@perm(['edit_system_settings'])
@auth
def roles_add():
    role = {
        "theme": request.form.get("theme"),
        "name": request.form.get("name"),
        "permissions": json.loads(request.form.get("permissions"))
    }
    role_service.add(role, session['company_id'])
    return u'{} Role Added'.format(request.form.get("name")), 200

@app.route('/roles', methods=['DELETE'])
@perm(['edit_system_settings'])
@auth
def roles_delete():
    role_id = request.form.get("id")
    role = role_service.get(role_id=role_id)
    role_service.delete(role_id)
    return u'{} Role Deleted'.format(role.name), 200

#### Notifications ####

@app.route('/notifications', methods=['GET'])
@auth
def notifications():
    limit = request.args.get("limit")
    offset = request.args.get("offset")
    sort_by = request.args.get("sort_by")
    sort_dir = request.args.get("sort_dir")
    return json_response(notification_service.get(company_id=session['company_id'], limit=limit, offset=offset,
                                                  sort_by=sort_by, sort_dir=sort_dir))