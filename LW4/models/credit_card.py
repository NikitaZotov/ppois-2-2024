from pydantic import BaseModel

from models.card_owner import CardOwner


class CreditCard(BaseModel):
    card_number: int | None = None
    owner: CardOwner | None = None
    payment_limit: int | None = 0
    pin: int | None = 0
    balance: int | None = 0
    is_blocked: bool | None = False
