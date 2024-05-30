from enum import Enum


class State(Enum):
    intro = -1
    main_menu = 0
    settings = 1
    game_play = 2
    score = 3
    rules = 4
    enter_score = 5
