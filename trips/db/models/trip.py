from beanie import Document
from datetime import datetime

class Trip(Document):
    trip_number: str
    departure_date: datetime
    arrival_date: datetime
    departure_airport: str
    arrival_airpost: str
    flight_link: str