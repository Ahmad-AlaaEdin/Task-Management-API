import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Management API" in response.json()["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    data = {"title": "Test Task", "description": "Test Description", "priority": "high"}
    response = client.post("/tasks/", json=data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
    # Save ID for later tests
    global created_task_id
    created_task_id = response.json()["id"]


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)


def test_get_task_by_id():
    # Use the ID from the create test
    response = client.get(f"/tasks/{created_task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_task_id


def test_update_task():
    update_data = {"description": "Updated Description", "priority": "medium"}
    response = client.patch(f"/tasks/{created_task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Description"
    assert response.json()["priority"] == "medium"


def test_get_tasks_by_status():
    response = client.get("/tasks/status/pending")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tasks_by_priority():
    response = client.get("/tasks/priority/medium")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_task():
    response = client.delete(f"/tasks/{created_task_id}")
    assert response.status_code == 204


def test_get_deleted_task():
    response = client.get(f"/tasks/{created_task_id}")
    assert response.status_code == 404
