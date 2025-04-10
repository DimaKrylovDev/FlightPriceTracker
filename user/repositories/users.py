from db.database import async_session_maker
from db.models import User
from sqlalchemy import insert, select, update, delete
from schemas.auth import SUser
from pydantic import EmailStr

class AuthRepository:
    @staticmethod
    async def get_one_or_none(**values):
        async with async_session_maker() as session:
            query = select(User).filter_by(**values)
            result = await session.execute(query)
            return result.mapping().one_or_none()
    
    @staticmethod
    async def get_by_id(id_: int) -> SUser:
        async with async_session_maker() as session:
            query = select(User).where(User.id == id_)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    @staticmethod
    async def get_by_email(email_: EmailStr):
        async with async_session_maker() as session:
            query = select(User).where(User.email == email_)
            result = await session.execute(query)
            return result.scalars().first()
        
    @staticmethod
    async def create(**values) -> SUser:
        async with async_session_maker() as session:
            query = insert(User).values(**values)
            await session.execute(query)
            await session.commit()
    
    @staticmethod
    async def update(id_,**values) -> SUser:
        async with async_session_maker() as session:
            query = update(User).where(User.id == id_).values(**values)
            await session.execute(query)
            await session.commit() 
    
    @staticmethod
    async def delete(id_) -> SUser:
        async with async_session_maker() as session:
            query = delete(User).where(User.id == id_)
            await session.execute(query)
            await session.commit()