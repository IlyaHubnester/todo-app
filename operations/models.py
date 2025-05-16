from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from db import Base


class Operation(Base):
    __tablename__ = "operation"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]


class OperationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str = 'CREATED'
