from core.config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import MetaData
from redis import Redis

engine = create_async_engine(settings.POSTGRES_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class Base(DeclarativeBase):
    metadata = MetaData()