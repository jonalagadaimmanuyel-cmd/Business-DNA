Business DNA backend

FastAPI backend for Business DNA frontend.

Requirements

Install dependencies into a virtualenv:

1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt

Run the app (from the backend folder):

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Endpoints (examples):

- GET /products
- POST /products
- GET /products/{id}
- PUT /products/{id}
- DELETE /products/{id}
- POST /sales
- GET /dashboard
- GET /recommendations
- POST /ask-ai (demo stub)
- GET /report
- POST /sample-data

Set the DATABASE_URL env var to override the default SQLite path if needed.
