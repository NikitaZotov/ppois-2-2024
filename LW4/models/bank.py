from pydantic import BaseModel

from models.transaction import Transaction


class Bank(BaseModel):
    name: str | None = None
    cards: list | None = None
    transaction_history: list[Transaction] | None = None
