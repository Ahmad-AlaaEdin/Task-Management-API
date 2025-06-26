from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import create_task, get_tasks, get_task, update_task, delete_task
from datetime import datetime, timezone

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create(task_data: TaskCreate, session: Session = Depends(get_session)):
    task_data.title = task_data.title.strip()
    if not task_data.title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    now = datetime.now(timezone.utc)
    if task_data.due_date and task_data.due_date < now:
        raise HTTPException(status_code=400, detail="Due date cannot be in the past")
    
    task = Task.from_orm(task_data)
    return create_task(task, session)

@router.get("/", response_model=list[TaskResponse])
def read_all(session: Session = Depends(get_session)):
    return get_tasks(session)

@router.get("/{task_id}", response_model=TaskResponse)
def read(task_id: int, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update(task_id: int, updates: TaskUpdate, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    return update_task(session, task)

@router.delete("/{task_id}", status_code=204)
def delete(task_id: int, session: Session = Depends(get_session)):
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
