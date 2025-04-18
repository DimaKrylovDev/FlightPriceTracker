from core.config import settings
from beanie import init_beanie
from db.models.trips import Trips
from core.config import settings
from redis import Redis

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, ssl=True, ssl_ca_certs=None)

async def init():
    client = settings.MONGODB_CLIENT
    
    db=client.trips
    print(settings.MONGO_INITDB_ROOT_USERNAME, settings.MONGO_INITDB_ROOT_PASSWORD)
    await init_beanie(database=db, document_models=[Trips])
    