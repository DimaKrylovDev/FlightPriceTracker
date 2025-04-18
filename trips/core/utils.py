import json
from core.config import settings
from db.models.trips import Trips
from fastapi import HTTPException, status


def city_code(town: str):
    with open(settings.CITIES_JSON_PATH) as json_cities:
        json_cities = json.load(json_cities)
        
    for cities in json_cities:
        if cities['name'] == town:
            return cities['code']   
        
async def check_trip(trip_number: int):
    res = await Trips.find_one({'trip_number': trip_number})
    if res:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This trip already exist")
    
    return None 
    
async def get_town_by_trip():
    res = await Trips.find_one({'trip_number': None})
    if not res:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Email is not registry')
    
    return res