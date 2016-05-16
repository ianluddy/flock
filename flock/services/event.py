from flock.app import db_wrapper as db
from notification import notify
from flask import abort

def get(company_id, event_id=None, start=None, end=None, hide_expired=False, limit=None, offset=None, sort_by=None,
        sort_dir=None, user_id=None):
    return db.event_get(
        company_id=company_id,
        event_id=event_id,
        start=start,
        end=end,
        hide_expired=hide_expired,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_dir=sort_dir,
        user_id=user_id
    )

def add(event):
    _validate_event(event)
    db.event_add(event)
    notify(u'{} added a new Event - <b>%s</b>' % event['title'], action='add', target='event')

def update(event):
    _validate_event(event)
    db.event_update(event)
    notify(u'{} updated an Event - <b>%s</b>' % event['title'], action='edit', target='event')

def delete(event):
    db.event_delete(event['id'])
    notify(u'{} deleted an Event - <b>%s</b>' % event['title'], action='delete', target='event')

def _validate_event(event):
    if event['start'] > event['end']:
        abort(400, 'Start time needs to be before end time')