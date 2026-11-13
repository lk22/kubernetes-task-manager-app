from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

from .database import Base, engine, get_db
from .models import Task as TaskModel

# RETTELSE: Tilføjet cache_tasks i importen, hvis den ligger der
from .cache import (
    get_cached_tasks,
    set_cached_tasks,          # <-- Tilføjet her
    invalidate_tasks_cache
)

app = FastAPI(title="Task Management API")

# Create database tables
Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool

    model_config = {"from_attributes": True}

@app.get("/")
def root():
    return {"message": "Welcome to the Task Management API"}



@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):

    cached_tasks = get_cached_tasks()

    if cached_tasks is not None:
        return cached_tasks

    tasks = db.query(TaskModel).all()

    result = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
        for task in tasks
    ]

    return result


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = TaskModel(
        id=str(uuid4()),
        title=task.title,
        description=task.description,
        completed=False
    )

    db.add(new_task)
    db.commit()

    # invalidate_tasks_cache() # Invalidate the cache after creating a new task
    set_cached_tasks([{
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed": new_task.completed
    }])

    db.refresh(new_task)

    return new_task


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    completed: bool,
    db: Session = Depends(get_db)
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = completed

    db.commit()

    invalidate_tasks_cache() # Invalidate the cache after updating a task

    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    invalidate_tasks_cache() # Invalidate the cache after deleting a task

    return {"message": "Task deleted"}
