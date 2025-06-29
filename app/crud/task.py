from sqlmodel import Session, select
from app.models.task import Task
from sqlalchemy import func
from typing import List
from app.models.task import TaskStatus, TaskPriority


def create_task(task: Task, session: Session) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def get_tasks(session: Session, skip: int = 0, limit: int = 10) -> List[Task]:
    return session.exec(select(Task).offset(skip).limit(limit)).all()


def count_tasks(session: Session) -> int:
    return session.exec(select(func.count()).select_from(Task)).one()


def update_task(session: Session, task: Task) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


def get_tasks_by_status(session: Session, status: TaskStatus) -> List[Task]:
    return session.exec(select(Task).where(Task.status == status)).all()


def get_tasks_by_priority(session: Session, priority: TaskPriority) -> List[Task]:
    return session.exec(select(Task).where(Task.priority == priority)).all()


def get_tasks_by_status_and_priority(
    session: Session, status: TaskStatus, priority: TaskPriority
) -> List[Task]:
    return session.exec(
        select(Task).where(Task.status == status, Task.priority == priority)
    ).all()
