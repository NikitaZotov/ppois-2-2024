from datetime import date

from model.winner import Winner

class Tournament():

    def __init__(self, title: str, date: date, sport: str, winner: Winner, prize: int):
        self.title = title.capitalize()
        self.date = date
        self.sport = sport.capitalize()
        self.winner = winner
        self.prize = prize

    @property
    def winner_prize(self) -> int: return int(0.6 * self.prize)
        
    def dict(self):
        
        return {"Title": self.title, "Date": self.date,
                "Sport": self.sport, "Winner": str(self.winner),
                "Prize": self.prize, "Winner's prize": self.winner_prize}

        
    
