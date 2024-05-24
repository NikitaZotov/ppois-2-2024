from source.models.result import BestResult, Result
import json
import random
import source.constants as constants


class JSONManager:
    def __init__(self):
        self.file_name_for_records_by_score_per_move: str = "../resources/json/records_per_move.json"
        self.file_name_for_records_by_score_per_second: str = "../resources/json/records_per_second.json"
        self.file_name_for_board: str = "../resources/json/levels.json"

    def get_records_by_score_per_second_from_json(self):
        with open(self.file_name_for_records_by_score_per_second, "r") as json_file:
            records: list = json.load(json_file)
        return sorted(records, key=lambda record: -record["score"] / record["time"])

    def get_records_by_score_per_move_from_json(self):
        with open(self.file_name_for_records_by_score_per_move, "r") as json_file:
            records: list = json.load(json_file)
        return sorted(records, key=lambda record: -record["score"] / record["moves"])

    def add_best_result_for_score_per_move(self, best_result):
        with open(self.file_name_for_records_by_score_per_move, "r") as json_file:
            current_records: list = json.load(json_file)

        result: BestResult = BestResult(best_result.name, best_result.time, best_result.moves, best_result.score)
        current_records.append(result.__dict__())

        with open("../resources/json/records_per_move.json", "w") as json_file:
            json.dump(current_records, json_file)

    def add_best_result_for_score_per_second(self, best_result):
        with open(self.file_name_for_records_by_score_per_second, "r") as json_file:
            current_records: list = json.load(json_file)

        result: BestResult = BestResult(best_result.name, best_result.time, best_result.moves, best_result.score)
        current_records.append(result.__dict__())

        with open("../resources/json/records_per_second.json", "w") as json_file:
            json.dump(current_records, json_file)

    def is_best_result_for_score_per_move(self, result: Result):
        with open(self.file_name_for_records_by_score_per_move) as json_file:
            data = json.load(json_file)
            if len(data) == 0:
                return True
            best_result_for_score_per_move = max(data, key=lambda x: x["score"] / x["moves"])
            max_score_per_move_value = best_result_for_score_per_move["score"] / best_result_for_score_per_move["moves"]
            if max_score_per_move_value < result.get_score_per_move():
                return True
            return False

    def is_best_result_for_score_per_second(self, result: Result):
        with open(self.file_name_for_records_by_score_per_second) as json_file:
            data = json.load(json_file)
            if len(data) == 0:
                return True
            best_result_for_score_per_time = max(data, key=lambda x: x["score"] / x["time"])
            max_score_per_second_value = best_result_for_score_per_time["score"] / best_result_for_score_per_time[
                "time"]
            if max_score_per_second_value < result.get_score_per_second():
                return True
            return False

    def get_board(self):
        board = []
        with open(self.file_name_for_board) as file:
            json_data = file.read()
            data: dict = json.loads(json_data)
            board: list = data[random.choice(constants.LEVEL_NAMES)]
        return board
