from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
from sqlalchemy import text


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=200, index=True)
    description: str | None = Field(default=None, max_length=1000)
    
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        sa_column_kwargs={"server_default": text("'pending'")}
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        sa_column_kwargs={"server_default": text("'medium'")}
    )

    created_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )

    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )

    due_date: datetime | None = Field(default=None)
    assigned_to: str | None = Field(default=None, max_length=100)
