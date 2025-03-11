from pydantic import BaseModel


class DonationBase(BaseModel):
    pass


class Donations(DonationBase):
    """
    DTO for donation models.

    returned when accessing donation models from the API.
    """
    pass


class DeleteDonation(BaseModel):
    pass


class GetDonationsResponse(BaseModel):
    pass


class CreateDonationResponse(BaseModel):
    pass