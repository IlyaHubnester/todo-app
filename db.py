from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.orm import declarative_base

sqlite_url = f"sqlite+aiosqlite:///database.db"

engine = create_async_engine(sqlite_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def session_dependency():
    session = async_scoped_session(session_factory=async_session_maker, scopefunc=current_task)
    async with session() as sess:
        yield sess
        await session.remove()

Base = declarative_base()
