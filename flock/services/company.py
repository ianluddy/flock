from flock.app import db_wrapper as db
from flock.services import mail

def get(company_id):
    return db.company_get(company_id)