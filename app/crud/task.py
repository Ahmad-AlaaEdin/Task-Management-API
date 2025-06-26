from sqlmodel import Session, select
from app.models.task import Task

def create_task(task: Task, session: Session) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)

def get_tasks(session: Session) -> list[Task]:
    return session.exec(select(Task)).all()

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
