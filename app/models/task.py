from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from sqlalchemy import text
from pydantic import field_validator


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)

    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        sa_column_kwargs={"server_default": text("'pending'")},
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        sa_column_kwargs={"server_default": text("'medium'")},
    )

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    due_date: Optional[datetime]
    assigned_to: str | None = Field(default=None, max_length=100)

    