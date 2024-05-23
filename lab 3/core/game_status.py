from enum import Enum


# class syntax
class GameStatus:
    run_status = False

    @staticmethod
    def set_run():
        GameStatus.run_status = True

    @staticmethod
    def set_pause():
        GameStatus.run_status = False

