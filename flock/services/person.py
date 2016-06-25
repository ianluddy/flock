from flock.app import db_wrapper as db
from flask import abort
from flock.services import mail, company
from flock.services.notification import notify

def invite(email, sender_id, company_id):
    recipient = db.person_get(company_id=company_id, email=email)

    if not email or not recipient:
        abort(400, 'No email address registered for this Person, please add one to send an invitation')

    token = db.generate_token(email) if not recipient.token else recipient.token

    mail.invite(
        email,
        db.person_get(company_id, user_id=sender_id).name,
        token
    )

def add(new_person, user_id, company_id):
    if new_person['invite'] and not new_person.get('email'):
        abort(400, 'Please specify an email address to send the invitation to, or uncheck the invitation box.')

    db.person_add(new_person)

    if new_person['invite']:
        invite(new_person['email'], user_id, company_id)

    notify(u'{} added a new Person - <b>%s</b>' % new_person['name'], action='add', target='person')

def update(person):
    db.person_update(person)
    notify(u'{} updated details for <b>%s</b>' % person['name'], action='edit', target='person')

def delete(person_id, user_id, company_id):
    if person_id == user_id:
        abort(400, "You can't delete your own account. Coming soon!")
    if company.get(company_id).owner.id == person_id:
        abort(400, "You can't delete the company's owner")
    user_name = db.person_get(user_id=person_id).name
    db.person_delete(person_id)
    notify(u'{} deleted a Person - <b>%s</b>' % user_name, action='delete', target='person')

def get(company_id=None, role_id=None, email=None, search=None, sort_by=None, sort_dir=None, limit=None,
        offset=None):
    return db.person_get(company_id=company_id, role_id=role_id, search=search, sort_by=sort_by,
                              sort_dir=sort_dir, limit=limit, offset=offset, email=email)