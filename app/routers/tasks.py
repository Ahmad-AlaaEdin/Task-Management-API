from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.db.database import get_session
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, PaginatedTaskResponse
from app.crud.task import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
    count_tasks,
    get_tasks_by_priority,
    get_tasks_by_status,
    get_tasks_by_status_and_priority,
)
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create(task_data: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_data.model_dump())
    return create_task(task, session)


@router.get(
    "/",
    response_model=PaginatedTaskResponse,
    summary="Get all tasks with pagination",
)
def read_all(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of items to return"
    ),
    session: Session = Depends(get_session),
):

    total = count_tasks(session)
    tasks = get_tasks(session, skip=skip, limit=limit)

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with given filters")
    return {"total": total, "skip": skip, "limit": limit, "data": tasks}


@router.get("/{task_id}", response_model=TaskResponse)
def read(task_id: int, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/status/{status}", response_model=list[TaskResponse])
def read_by_status(status: TaskStatus, session: Session = Depends(get_session)):
    tasks = get_tasks_by_status(session, status=status)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with this status")
    return tasks


@router.get("/priority/{priority}", response_model=list[TaskResponse])
def read_by_priority(priority: TaskPriority, session: Session = Depends(get_session)):
    tasks = get_tasks_by_priority(session, priority=priority)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with this priority")
    return tasks


@router.patch("/{task_id}", response_model=TaskResponse)
def update(task_id: int, updates: TaskUpdate, session: Session = Depends(get_session)):
    task = get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    return update_task(session, task)


@router.delete("/{task_id}", status_code=204)
def delete(task_id: int, session: Session = Depends(get_session)):
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
