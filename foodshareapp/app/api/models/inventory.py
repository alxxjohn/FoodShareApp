from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Inventory(BaseModel):
    """
    DTO for inventory models.

    returned when accessing inventory models from the API.
    """

    foodbank_id: UUID
    item_id: UUID
    item_name: str
    item_qty: int
    date_added: datetime
    status: str


class CreateInventory(BaseModel):
    """
    DTO for inventory models.

    returned when accessing inventory models from the API.
    """

    foodbank_id: UUID
    item_id: UUID
    item_name: str
    item_qty: int
    date_added: datetime
    item_status: str


class CreateInventoryResponse(CreateInventory):
    item_id: UUID
    date_added: datetime


class DeleteInventory(BaseModel):
    item_id: UUID
