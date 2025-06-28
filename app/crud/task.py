from sqlmodel import Session, select
from app.models.task import Task
from sqlalchemy import func
from typing import List
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
