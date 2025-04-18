from pydantic_settings import BaseSettings, SettingsConfigDict
from motor.motor_asyncio import AsyncIOMotorClient
from celery import Celery
import ssl


class Settings(BaseSettings):
    #Mongo Settings
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
    
    #API settings
    API_KEY: str

    #PATH
    CITIES_JSON_PATH: str
    AIROPORT_JSON_PATH: str
    
    REDIS_HOST: str
    REDIS_PORT: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    BASE_URL: str
    
    @property
    def MONGODB_CLIENT(self):
        return AsyncIOMotorClient(f'mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@'
                f'{self.ME_CONFIG_MONGODB_HOST}:{self.ME_CONFIG_MONGODB_PORT}') 
        
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
settings = Settings()

ssl_settings = {"ssl_cert_reqs": ssl.CERT_NONE}

celery = Celery(
    'celery-worker',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)