from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Flight(BaseModel):
    trip_number: Optional[int] = None
    departure_date: Optional[datetime] = None
    arrival_date: Optional[datetime] = None
    departure_airport: Optional[str] = None
    airline: Optional[str] = None
    flight_link: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = "RUB"  