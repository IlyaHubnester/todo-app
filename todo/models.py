from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from db import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    completed: Mapped[bool]
    deadline: Mapped[Optional[datetime]]


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    completed: bool = False
    deadline: datetime | None = None