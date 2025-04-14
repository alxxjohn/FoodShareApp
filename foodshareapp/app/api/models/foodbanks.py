from pydantic import BaseModel
from uuid import UUID


class Foodbank(BaseModel):
    business_id: UUID
    company_name: str
    address: str
    city: str
    state: str
    zipcode: str
    lat: str
    lng: str
    is_foodbank: bool
    assoc_user: UUID
