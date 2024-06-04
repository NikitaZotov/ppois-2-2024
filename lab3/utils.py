import json
import os.path

from config import config


def add_score(name: str, score: int):
    if os.path.exists(config["score_file_path"]):
        with open(config["score_file_path"], 'r') as read_file:
            scores: dict[str, int] = json.loads(read_file.read())
    else:
        scores: dict[str, int] = {}

    scores[name] = score
    while len(scores) > 5:
        target = name
        for other_name, other in scores.items():
            if other <= scores[target]:
                target = other_name
        del scores[target]

    with open(config["score_file_path"], 'w') as write_file:
        write_file.write(json.dumps(scores))
