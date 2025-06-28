from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.db.database import get_session
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    count_tasks,
)
from datetime import datetime, timezone
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create(task_data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_data.model_dump())
    return create_task(task, session)


@router.get("/", response_model=list[TaskResponse])
def read_all(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    session: Session = Depends(get_session),
):
    count = count_tasks(session)
    print(count)
    return get_tasks(session, skip=skip, limit=limit)


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
