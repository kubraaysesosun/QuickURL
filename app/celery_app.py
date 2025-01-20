from celery import Celery
from celery.schedules import crontab


SHORT_URL_LENGTH = 6

def create_celery():
    app = Celery(
        "app",
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0"
    )

    app.conf.beat_schedule = {
        "delete-expired-urls-every-hour": {
            "task": "app.celery_tasks.delete_expired_urls",
            "schedule": crontab(minute=0, hour="*"),  # Every hour
        },
    }

    app.conf.timezone = "UTC"

    return app

celery = create_celery()
