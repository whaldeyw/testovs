import asyncio

from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine('sqlite+aiosqlite:///db.db', echo=True)


async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class TableClient(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    number = mapped_column(Integer)
    family: Mapped[str] = mapped_column(String(25))
    name: Mapped[str] = mapped_column(String(25))
    middle_name : Mapped[str] = mapped_column(String(25))
    data = mapped_column(Integer)
    inn = mapped_column(Integer)
    responsible: Mapped[str] = mapped_column(String(25))
    status: Mapped[str] = mapped_column(String(25))

class TableUser(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True)
    fio : Mapped[str] = mapped_column(String(25))
    loggin : Mapped[str] = mapped_column(String(25))
    password : Mapped[str] = mapped_column(String(25))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(async_main())


