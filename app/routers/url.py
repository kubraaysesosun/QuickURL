from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.url_shortener import url_shortener_core
from app.schemas.url import URLCreateIn, URLResponseOut
from app.db import get_db

router = APIRouter()

@router.post("/url", response_model=URLResponseOut)
def create_short_url(url: URLCreateIn, db: Session = Depends(get_db)):
    return url_shortener_core.create_url_short(url=url, db=db)


@router.get("/{short_url}", response_model=URLCreateIn)
def redirect_to_long_url(short_url: str, db: Session = Depends(get_db)):
    return url_shortener_core.redirect_to_long_url(short_url=short_url, db=db)