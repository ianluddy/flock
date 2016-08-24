from flock.app import db_wrapper as db

def get(company_id):
    return db.mail_notification_get(company_id)

def add(company_id, rule):
    db.mail_notification_add(company_id, rule)

def update(rule):
    db.mail_notification_update(rule)

def delete(rule_id):
    return db.mail_notification_delete(rule_id)
