from datetime import datetime
from celery import shared_task
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.url import URL

@shared_task
def delete_expired_urls():
    """Delete URLs where expire_time has passed."""
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        expired_urls = db.query(URL).filter(URL.expire_time < now).all()
        for url in expired_urls:
            db.delete(url)
        db.commit()
        return f"Deleted {len(expired_urls)} expired URLs."
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
