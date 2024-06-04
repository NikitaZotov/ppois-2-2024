from typing import Optional
import datetime


class SearchModel:
    def __init__(self, name: Optional[str] = None, birthdate: Optional[datetime] = None, sport_name: Optional[str] = None,
                 position: Optional[str] = None, cast: Optional[str] = None, hometown: Optional[str] = None,
                 page_number: int = 1, page_size: int = 10, criteria: str | None = None):
        self.name = name
        self.birthdate = birthdate
        self.position = position
        self.cast = cast
        self.hometown = hometown
        self.sport_name = sport_name
        self.page_number: int = page_number
        self.page_size: int = page_size
        self.criteria = criteria
