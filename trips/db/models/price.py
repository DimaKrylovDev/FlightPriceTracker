from beanie import Document
from datetime import datetime

class Price(Document):
    trip_number: str
    update_date: datetime
    price: int
    currency: str
    