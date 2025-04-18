from fastapi import FastAPI
import uvicorn
from db.database import init
from contextlib import asynccontextmanager
from routers import trips 
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(router=trips.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)