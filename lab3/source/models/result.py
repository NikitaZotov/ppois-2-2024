class Result:
    def __init__(self, time: int, moves: int, score: int):
        self.time: int = time
        self.moves: int = moves
        self.score: int = score

    def get_score_per_move(self):
        if self.moves == 0:
            return 1
        return round(self.score / self.moves, 1)

    def get_score_per_second(self):
        return round(self.score / self.time, 1)

    def __dict__(self):
        return {"time": self.time,
                "moves": self.moves,
                "score": self.score}


class BestResult(Result):
    def __init__(self, name: str, time: int, moves: int, score: int):
        super().__init__(time, moves, score)
        self.name: str = name

    def __dict__(self):
        result: dict = super().__dict__()
        result["name"] = self.name
        return result
