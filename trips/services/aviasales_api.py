from db.models.trips import Trips
from core.config import settings
from schemas.trips import Flight
import aiohttp
from core.utils import city_code, check_trip

class Aviasales:
    async def aviasales_flights(self, origin: str, destination: str):
        origin_code = city_code(origin)
        destination_code = city_code(destination)
        url = f"https://api.travelpayouts.com/v1/prices/cheap?origin={origin_code}&destination={destination_code}&one_way=true&token={settings.API_KEY}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                json_response = await response.json()
                if json_response['success']:
                    data = json_response.get('data')
                    data_destination = data[destination_code]
                    flight_data = data_destination['0']
                    flight = Flight(
                        trip_number=flight_data.get('flight_number'), 
                        departure_date=flight_data.get('departure_at'),
                        arrival_date=flight_data.get('return_at'),
                        airline=flight_data.get('airline'),
                        price=flight_data.get('price'),
                        currency=flight_data.get('currency', 'RUB')
                    )
                    flight_dict = flight.dict()
                    await check_trip(flight_dict['trip_number'])
                    res = Trips(**flight_dict)
                    await res.insert()
                    return flight_dict
