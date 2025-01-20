from pydantic import BaseModel


class URLCreateIn(BaseModel):
    long_url: str


class URLResponseOut(BaseModel):
    short_url: str
