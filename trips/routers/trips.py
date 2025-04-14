from fastapi import APIRouter
from services.aviasales_api import aviasales

router = APIRouter(prefix='/trips', tags=['trips'])

@router.get('/read')
async def read_tickets(origin: str, destination: str):
    await aviasales.aviasales_flights(origin=origin, destination=destination)