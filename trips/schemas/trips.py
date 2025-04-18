from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Flight(BaseModel):
    origin: str = None
    destination: str = None
    trip_number: Optional[int] = None
    departure_date: Optional[datetime] = None
    arrival_date: Optional[datetime] = None
    airline: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = "RUB"
    created_at: datetime = datetime.utcnow()
      
class Towns(BaseModel):
    origin: str
    destination:str