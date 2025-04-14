from beanie import Document
from datetime import datetime

class Trips(Document):
    trip_number: int
    departure_date: datetime
    arrival_date: datetime
    departure_airport: str | None
    airline: str
    flight_link: str | None
    price: int
    currency: str
    
    class Settings:
        collection = 'trips'