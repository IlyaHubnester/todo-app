from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db import session_dependency
from todo.models import Task, TaskSchema, TaskSchemaUpdate

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/tasks")

@router.post("/create")
async def create_task(data: TaskSchema,
                      session: AsyncSession = Depends(session_dependency)):
    task = Task(**data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

@router.put("/update/{task_id}")
async def update_task(task_id, data: TaskSchemaUpdate,
                      session: AsyncSession = Depends(session_dependency)):
    await session.execute(update(Task).where(Task.id == task_id),
                                 data.model_dump(exclude_unset=True))
    await session.commit()

@router.delete("/delete/{task_id}")
async def delete_task(task_id,
                      session: AsyncSession = Depends(session_dependency)):
    await session.execute(delete(Task).where(Task.id == task_id))
    await session.commit()

@router.get("/")
async def list_tasks(session: AsyncSession = Depends(session_dependency)):
    result = await session.execute(select(Task).order_by(Task.id))
    return result.scalars().all()