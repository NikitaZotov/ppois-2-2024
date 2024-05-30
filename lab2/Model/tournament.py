from datetime import datetime


class Tournament:
    def __init__(self, name_tournament: str, date: datetime, name_sport: str,
                 name_winner: str, prize_pool: float, tournament_id: str = "0"):
        self.tournament_id = tournament_id
        self.name_tournament = name_tournament
        self.date = date
        self.name_sport = name_sport
        self.name_winner = name_winner
        self.prize_pool = prize_pool
        self.prize_winner = prize_pool*0.6

    def print_all(self):
        print(f'ID: {self.tournament_id}, Name: {self.name_tournament}, '
              f'Date: {self.date},Name Sport:{self.name_sport} ,'
              f'Winner: {self.name_winner}, Prize: {self.prize_winner}, ')

    def get_first_name(self):
        name = ' '.split(self.name_winner)
        if len(name) < 3:
            raise Exception('Name must contain at least 3 characters')
        else:
            return name[0]

    def get_last_name(self):
        name = ' '.split(self.name_winner)
        if len(name) < 3:
            raise Exception('Name must contain at least 3 characters')
        else:
            return name[1]

    def get_third_name(self):
        name = ' '.split(self.name_winner)
        if len(name) < 3:
            raise Exception('Name must contain at least 3 characters')
        else:
            return name[2]

    def data_format(self):
        data = [self.tournament_id, self.name_tournament,
                self.date, self.name_sport, self.name_winner, self.prize_pool, self.prize_winner]
        return data
