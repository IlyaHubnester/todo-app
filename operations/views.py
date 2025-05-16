import asyncio

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from db import session_dependency
from operations.models import Operation, OperationSchema

router = APIRouter(prefix="/api/operations")

async def operation(operation_id, session: AsyncSession = Depends(session_dependency)):
    timer = 0
    while timer < 10:
        await asyncio.sleep(1)
        timer += 1
    await session.execute(update(Operation).where(Operation.id == operation_id),
                          {'status': 'COMPLETED'})
    await session.commit()


@router.post("/create")
async def create_operation(session: AsyncSession = Depends(session_dependency)):
    op = Operation(**OperationSchema().model_dump())
    session.add(op)
    await session.commit()
    await session.refresh(op)
    return op


@router.get("/start/{operation_id}")
async def start_operation(operation_id, background_tasks: BackgroundTasks, session: AsyncSession = Depends(session_dependency)):
    op = await session.execute(select(Operation).where(Operation.id == operation_id))
    if op.scalar_one().status != 'PROCESSING':
        background_tasks.add_task(operation, operation_id, session)
        op.status = 'PROCESSING'
        await session.commit()
    else:
        return 'Operation is already in progress'


@router.get("/")
async def list_operations(session: AsyncSession = Depends(session_dependency)):
    result = await session.execute(select(Operation).order_by(Operation.id))
    return result.scalars().all()
