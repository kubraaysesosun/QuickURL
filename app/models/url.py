from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime, timedelta


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String(2083), nullable=False)  # Maximum URL length for most browsers
    short_url = Column(String(50), unique=True, index=True, nullable=False)
    expire_time = Column(DateTime, nullable=True, default=lambda: datetime.utcnow() + timedelta(days=7))  # Default 7 days expiration
