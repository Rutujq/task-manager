from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    title: str
    description: str
    due_date: str
    priority: str

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added", "task": task}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks):
        return {"error": "Invalid ID"}
    
    tasks[task_id] = task.dict()
    return {"message": "Updated", "task": tasks[task_id]}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        return {"error": "Invalid ID"}
    
    return tasks.pop(task_id)

@app.get("/search/{keyword}")
def search_tasks(keyword: str):
    return [
        task for task in tasks
        if keyword.lower() in task["title"].lower()
    ]