# QuickURL: A URL Shortener with Redis Cache and Performance Metrics

## Project Overview
QuickURL is a URL shortening web application built using FastAPI and SQLAlchemy. The project integrates Redis for caching and Prometheus for monitoring performance metrics such as traffic and response times. It also uses Celery for asynchronous task handling to generate short URLs efficiently.

## Features
- **Shorten URLs:** Users can provide a long URL to generate a shortened version.
- **Redirection:** Shortened URLs redirect to their original URLs.
- **Caching:** Redis is used to cache frequently accessed short URLs.
- **Error Handling:** The application handles invalid URLs and non-existent shortened URLs gracefully.
- **Performance Metrics:** Tracks traffic, cache hits/misses, and response times using Prometheus.
- **Asynchronous Task Handling:** Celery is used for generating short URLs asynchronously.

---

## Project Structure
```
quickUrl/
├── app/
│   ├── __init__.py
│   │── core/
│   │   ├── __init__.py
│   │   └── url_shortener.py
│   │──migrations/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   ├── models/
│   │   ├── __init__.py
│   │   └── url.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── url.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── url.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── url_parser.py
│   ├── cache.py
│   ├── celery_app.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── metrics.py
├── tests/
│   ├── __init__.py
│   │── test_routes
│   │── test_services
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis
- Docker and Docker Compose (optional)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/quickurl.git
    cd quickurl
    ```

2. Set up a virtual environment and install dependencies:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt
    ```

3. Set up the `.env` file:
    ```env
    DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/url_shortener
    ```

4. Run database migrations:
    ```bash
    alembic upgrade head
    ```

5. Start the Redis server:
    ```bash
    redis-server
    ```

   6. Start the Celery worker:
       ```bash
       celery -A app.celery_app worker --loglevel=info
       celery -A app.celery_app beat --loglevel=info
 
       ```

7. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

---

### Docker Setup
1. Build and run the containers:
    ```bash
    docker-compose up --build
    ```

2. The application will be available at `http://localhost:8000`.

---

## Endpoints
### 1. Shorten URL
**POST** `/url`

**Request Body:**
```json
{
  "long_url": "https://example.com"
}
```

**Response:**
```json
{
  "short_url": "http://localhost:8000/abc123"
}
```

### 2. Redirect to Original URL
**GET** `/{short_url}`

**Response:**
Redirects to the original URL.

### 3. Metrics
Prometheus metrics are available at `/metrics`.

---

## Prometheus Metrics
- **Total Requests:** Total number of requests received.
- **Cache Hits:** Number of successful cache hits.
- **Cache Misses:** Number of cache misses.
- **Response Time:** Histogram of response times.

---

## Testing
Run the tests using `pytest`:
```bash
pytest
```

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
   