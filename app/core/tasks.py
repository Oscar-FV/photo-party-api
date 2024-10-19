from celery import shared_task
from app.core.db import SessionLocal
from app.services.events.models import Event

@shared_task
def activate_event(event_id):
    db = SessionLocal()
    try:
        event = db.query(Event).get(event_id)
        if event and not event.is_active:
            event.is_active = True
            db.commit()
            print(f"Event {event.id} is now active!")
        else:
            print(f"Event {event_id} is already active or does not exist.")
    finally:
        db.close()