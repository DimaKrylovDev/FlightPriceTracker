from fastapi import APIRouter
from services.aviasales_api import Aviasales
from schemas.trips import Flight, Towns
from core.utils import get_town_by_trip
from db.models.trips import Trips

router = APIRouter(prefix='/trips', tags=['trips'])

@router.post('/choice')
async def choice_towns(request: Towns):
    res_dict = request.dict()
    await Trips.insert(res_dict)
    return {'message': 'OKOKOK'}

@router.get('/read')
async def read_tickets():
    user = await get_town_by_trip()
    res = await Aviasales.aviasales_flights(origin=user['origin'], destination=user['destination'])
    return Flight(
            trip_number=res.get('trip_number'), 
            departure_date=res.get('departure_date'),
            arrival_date=res.get('arrival_date'),
            airline=res.get('airline'),
            price=res.get('price'),
            currency=res.get('currency', 'RUB')
        )