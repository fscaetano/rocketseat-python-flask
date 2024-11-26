import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"
tasks = []

def test_create_task():
    new_task_data = {
        "title": "new task",
        "description": "new task descriuption"
    }

    resopnse =requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert resopnse.status_code == 200

    response_json = resopnse.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"])


def test_get_tasks():
    resopnse =requests.get(f"{BASE_URL}/tasks")
    assert resopnse.status_code == 200

    response_json = resopnse.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_get_task():
    if tasks:
        task_id = tasks[0]

        response =requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response_json = response.json()
        assert "id" in response_json
        assert response_json["id"] == task_id


def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": "Nova descricao",
            "title": "Titulo atualizado"
        }

        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json


        response =requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert "id" in response_json
        assert response_json["id"] == task_id
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]
        

def test_delete_task():
    if tasks:
        task_id = tasks[0]

        response =requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response =requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404

        response =requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404
