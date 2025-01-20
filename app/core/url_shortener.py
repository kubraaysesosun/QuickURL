import re

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.cache import get_cached_url, cache_url
from app.metrics import REQUEST_COUNT, CACHE_HITS, CACHE_MISSES
from app.models.url import URL
from app.schemas.url import URLCreateIn, URLResponseOut

from app.services.url_parser import generate_short_url


class URLValidator:
    @staticmethod
    def is_valid_url(url):
        url_regex = re.compile(
            r'^(https?://)?' 
            r'(www\.)?'      
            r'[a-zA-Z0-9.-]+'
            r'\.[a-zA-Z]{2,}' 
            r'(/.*)?$',
            re.IGNORECASE
        )
        return bool(url_regex.match(url))

class UrlShortenerCore:

    @staticmethod
    def create_url_short(url: URLCreateIn, db: Session):
        REQUEST_COUNT.labels(endpoint='/url').inc()
        cached_url = get_cached_url(url.long_url)
        if cached_url:
            CACHE_HITS.inc()
            return URLResponseOut(short_url=f"http://localhost:8000/{cached_url}")

        CACHE_MISSES.inc()
        if URLValidator.is_valid_url(url=url.long_url):
            short_url = generate_short_url(original_url=url.long_url)
            cache_url(url.long_url, short_url)
            new_url = URL(long_url=url.long_url, short_url=short_url)
            db.add(new_url)
            db.commit()
            db.refresh(new_url)

            return URLResponseOut(short_url=f"http://localhost:8000/{new_url.short_url}")

        raise HTTPException(status_code=500, detail="Invalid URL.")

    @staticmethod
    def redirect_to_long_url(short_url: str, db: Session):
        REQUEST_COUNT.labels(endpoint='/{short_url}').inc()
        cached_long_url = get_cached_url(short_url)
        if cached_long_url:
            CACHE_HITS.inc()
            return URLCreateIn(long_url=cached_long_url)

        CACHE_MISSES.inc()
        url_entry = db.query(URL).filter(URL.short_url == short_url).first()
        if not url_entry:
            raise HTTPException(status_code=404, detail="Short URL not found")

        cache_url(short_url, url_entry.long_url)
        return URLCreateIn(long_url=url_entry.long_url)


url_shortener_core = UrlShortenerCore