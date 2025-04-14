from fastapi import FastAPI
import uvicorn
from services.aviasales_api import aviasales
from db.database import init
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield
    
app = FastAPI(lifespan=lifespan)

@app.get('/aviasales')
async def choice_town(origin: str, destination: str):
    await aviasales.aviasales_flights(origin, destination)
    

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)