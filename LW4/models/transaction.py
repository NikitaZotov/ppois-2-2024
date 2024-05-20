from datetime import datetime

from pydantic import BaseModel

from models.credit_card import CreditCard


class Transaction(BaseModel):
    sender: CreditCard | None = None
    receiver: CreditCard | None = None
    amount: int | None = None
    timestamp: datetime | None = None
