from flock.app import db_wrapper as db
from flock.utils import random_uuid
from flock.constants import PROFILE_IMAGE_TYPES, PROFILE_IMAGE_DIR
from flask import abort
from flock.services import mail, person
import os

def reset(email):
    new_password = db.reset_user(email)
    mail.reset(email, new_password)

def upload_image(user_id, input_file):
    extension = input_file.filename.split('.')[-1]

    if extension not in PROFILE_IMAGE_TYPES:
        abort(400, 'File type not supported. Try a JPG or PNG instead.')

    filename = "{}/{}.{}".format(PROFILE_IMAGE_DIR, random_uuid(), extension)
    input_file.save(os.path.join("static/", filename))

    person.update({'image': filename, 'id': user_id})
