from pydantic_settings import BaseSettings, SettingsConfigDict
from motor.motor_asyncio import AsyncIOMotorClient

class Settings(BaseSettings):
    #MongoSettings
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str

    ME_CONFIG_BASICAUTH_USERNAME: str
    ME_CONFIG_BASICAUTH_PASSWORD: int
    ME_CONFIG_MONGODB_SERVER: str
    ME_CONFIG_MONGODB_HOST: str
    ME_CONFIG_MONGODB_PORT: int
    ME_CONFIG_MONGODB_ADMINUSERNAME: str
    ME_CONFIG_MONGODB_ADMINPASSWORD: str
    ME_CONFIG_MONGODB_ENABLE_ADMIN: bool
    
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
    def MONGODB_CLIENT(self):
        return AsyncIOMotorClient(f'mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@'
                f'{self.ME_CONFIG_MONGODB_HOST}:{self.ME_CONFIG_MONGODB_PORT}/{self.MONGO_INITDB_DATABASE}')
    
    @property
    def POSTGRES_URL(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRESQL_HOST}:{self.POSTGRESQL_PORT}/{self.POSTGRES_DB}')
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", from_attributes=True)
    
settings = Settings()

