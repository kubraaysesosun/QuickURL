from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.celery_app import create_celery
from app.config import settings
from app.db import Base, engine
from app.routers import url
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app

# Create alembic tables
Base.metadata.create_all(bind=engine)

# FastAPI uygulaması
app = FastAPI()

@app.get("/")
async def read_root():
    return {"BASE_URL": settings.BASE_URL}

@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )
# Include Routers
app.include_router(url.router)

# Celery integration
celery = create_celery()

@app.on_event("startup")
def startup_event():
    import subprocess
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except subprocess.CalledProcessError as e:
        print("Migration failed:", e)


# Prometheus Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)