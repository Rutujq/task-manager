import requests

API_URL = "http://127.0.0.1:8000"

def get_tasks():
    return requests.get(f"{API_URL}/tasks").json()

def add_task(title, description, due_date, priority):
    requests.post(f"{API_URL}/tasks", json={
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority
    })

def delete_task(task_id):
    requests.delete(f"{API_URL}/tasks/{task_id}")

def update_task(task_id, title, description, due_date, priority):
    requests.put(f"{API_URL}/tasks/{task_id}", json={
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority
    })

def search_tasks(keyword):
    return requests.get(f"{API_URL}/search/{keyword}").json()