from typing import Optional


class SearchModel:
    def __init__(self, name: Optional[str] = None, sport_name: Optional[str] = None, title_min: Optional[int] = None,
                 title_max: Optional[int] = None, rank: Optional[str] = None,
                 page_number: int = 1, page_size: int = 10, criteria: str | None = None):
        self.name = name
        self.sport_name = sport_name
        self.title_min = title_min
        self.title_max = title_max
        self.rank = rank
        self.page_number: int = page_number
        self.page_size: int = page_size
        self.criteria = criteria
