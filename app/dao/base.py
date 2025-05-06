from sqlalchemy import select, insert

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(id=model_id)
            )
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
            )
            result = await session.execute(query)

            return result.scalars().one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            await session.execute(query)
            await session.commit()
