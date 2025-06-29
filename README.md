# Task Management API

A modern, production-ready FastAPI application for managing tasks with support for priorities, statuses, and due dates.  
Includes full CRUD operations, pagination, filtering, and automated tests.

---

## Features

- **FastAPI** backend with async support
- **SQLModel** ORM with SQLite (default, easy to swap)
- **CRUD** for tasks (create, read, update, delete)
- **Pagination** and filtering by status/priority
- **Validation** with Pydantic v2
- **Custom error handling**
- **Dockerized** for easy deployment
- **Automated tests** with pytest

---

## Project Structure

```
task-management-api/
│
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── core/                # Core utilities (custom exceptions, etc.)
│   ├── crud/                # CRUD logic
│   ├── db/                  # Database setup
│   ├── models/              # ORM models
│   ├── routers/             # API routers
│   └── schemas/             # Pydantic schemas
│
├── tests/                   # Unit tests
│
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker build file
├── .dockerignore            # Docker ignore rules
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Ahmad-AlaaEdin/Task-Management-API
cd task-management-api

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

### Locally

```bash
# From the project root
uvicorn app.main:app --reload
```

### With Docker

```bash
docker build -t task-api .
docker run -d -p 8000:8000 --name task-api task-api
```

---

## Accessing the API

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## Example API Calls

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Sample Task", "priority": "high"}'
```

### List Tasks

```bash
curl "http://localhost:8000/tasks/"
```

### Update a Task

```bash
curl -X PATCH "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{"description": "Updated description"}'
```

### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

---

## Running Tests

```bash
pytest
```

---
