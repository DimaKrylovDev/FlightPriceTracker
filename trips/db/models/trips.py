from beanie import Document
from datetime import datetime

class Trips(Document):
    origin: str
    destination: str
    trip_number: int
    departure_date: datetime
    arrival_date: datetime
    airline: str
    price: int
    currency: str
    created_at: datetime
    
    class Settings:
        collection = 'trips'