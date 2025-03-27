from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Foodbank(BaseModel):
    foodbankID: UUID
    companyName: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    isBusiness: bool
    date_added: datetime
