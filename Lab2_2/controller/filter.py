from datetime import date

from model.winner import Winner

class Filter:

    def __init__(self, title: str|None=None, date: date|None=None, 
                 sport: str|None=None, winner_name: str|None=None,
                 winner_surname: str|None=None, winner_middlename: str|None=None, 
                 prize_range: list[int]|list[None]=[None, None],
                 winner_prize_range: list[int]|list[None]=[None, None],
                 page_number: int=1, size: int=10):
        
        self.title = title
        self.date = date
        self.sport = sport
        self.winner_name = winner_name
        self.winner_surname = winner_surname
        self.winner_middlename = winner_middlename
        self.prize_range = prize_range
        self.winner_prize_range = winner_prize_range
        self.page_number = page_number
        self.page_size = size