from pydantic_settings import BaseSettings, SettingsConfigDict
from motor.motor_asyncio import AsyncIOMotorClient

class Settings(BaseSettings):    
    #PostgreSQL
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    #JWT settings
    ACCESS_TOKEN_MINUTES: int
    REFRESH_TOKEN_DAYS: int
    EE_SECRET_KEY: str
    ALGORITHM: str

    #Redis settings
    REDIS_HOST: str
    REDIS_PORT: int
    
    @property
    def POSTGRES_URL(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRESQL_HOST}:{self.POSTGRESQL_PORT}/{self.POSTGRES_DB}')
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", from_attributes=True)
    
settings = Settings()

