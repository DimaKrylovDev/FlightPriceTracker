from db.models.trips import Trips
from core.config import settings
from schemas.trips import Flight
import aiohttp


class Aviasales:
    async def aviasales_flights(self, origin: str, destination: str):
        url = f"https://api.travelpayouts.com/v1/prices/cheap?origin={origin}&destination={destination}&one_way=true&token={settings.API_KEY}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                json_response = await response.json()
                if json_response['success']:
                    data = json_response.get('data')
                    data_destination = data[destination]
                    flight_data = data_destination['0']
                    print(data)
                    flight = Flight(
                        trip_number=flight_data.get('flight_number'), 
                        departure_date=flight_data.get('departure_at'),
                        arrival_date=flight_data.get('return_at'),
                        departure_airport = None,
                        airline=flight_data.get('airline'),
                        flight_link=None,
                        price=flight_data.get('price'),
                        currency=flight_data.get('currency', 'RUB')
                    )
                    print(type(flight))
                    flight_dict = flight.dict()
                    res = Trips(**flight_dict)
                    await res.insert()

aviasales = Aviasales()