import pickle
import os

class Leaderboard:
    def __init__(self):
        self.records = []
        self.file_path="../configurations/leaderboard.pkl"

    def add_record(self, name, score):
        if self.is_higher_score(score):
            self.records.append((name, score))

    def get_leaderboard(self):
        sorted_records = sorted(self.records, key=lambda x: x[1], reverse=True)
        return sorted_records

    def is_higher_score(self, score):
        if len(self.records)==0:
            return True
        for _, existing_score in self.records:
            if score <= existing_score:
                return False
        return True

    def save(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                leaderboard_obj = pickle.load(f)
            self.records = leaderboard_obj.records
        else:
            self.records = []
