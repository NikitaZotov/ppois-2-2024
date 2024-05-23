import json


class LeaderboardManager:
    def __init__(self):
        self.leaderboard = []

    def read_leaderboard_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.leaderboard = data['records']
        except FileNotFoundError:
            pass

    def write_leaderboard_to_file(self, filename):
        try:
            # Сортировка по убыванию счета
            sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x['score'], reverse=True)
            if len(sorted_leaderboard) > 10:
                sorted_leaderboard.pop()
            with open(filename, 'w') as file:
                json.dump({"records": sorted_leaderboard}, file, indent=4)
        except Exception as e:
            pass

    def add_record_to_leaderboard(self, name, score):
        new_record = {"name": name, "score": score}
        self.leaderboard.insert(0, new_record)
