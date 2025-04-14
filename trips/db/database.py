from core.config import settings
from beanie import init_beanie
from db.models.trips import Trips
from core.config import settings

async def init():
    client = settings.MONGODB_CLIENT
    
    db=client.trips
    print(settings.MONGO_INITDB_ROOT_USERNAME, settings.MONGO_INITDB_ROOT_PASSWORD)
    await init_beanie(database=db, document_models=[Trips])
    