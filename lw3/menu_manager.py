from settings import *
from main_menu import MainMenu
from loading_menu import LoadingMenu
from scoreboard_menu import ScoreboardMenu
from game_over_menu import GameOverMenu
from win_menu import WinMenu
from save_result_menu import SaveResultMenu
from reference_menu import ReferenceMenu
from timer import Timer
import pickle


class MenuManager:
    def __init__(self, game):
        self.game = game

        self.main_menu = MainMenu()

        self.loading_menu = LoadingMenu()
        self.loading_game_flag = False
        self.loading_game_timer = Timer(2000)

        self.scoreboard_menu = ScoreboardMenu(self.game)

        self.reference_menu = ReferenceMenu()

        self.game_over_menu = GameOverMenu()
        self.game_over_flag = False
        self.game_over_timer = Timer(3500)

        self.win_menu = WinMenu()
        self.game_win_flag = False
        self.game_win_timer = Timer(4000)

        self.save_result_menu = SaveResultMenu()

    def loading_game(self):
        self.loading_menu.update(self.game)
        if not self.loading_game_flag:
            self.loading_game_flag = True
            self.loading_game_timer.activate()
        self.loading_game_timer.update()
        if not self.loading_game_timer.active:
            self.game.sound_manager.play('overworld', 9999999, 0.5)
            self.game.state = 'GAME'

    def game_over(self):
        self.game_over_menu.update(self.game)
        if not self.game_over_flag:
            self.game_over_flag = True
            self.game_over_timer.activate()
        self.game_over_timer.update()
        if not self.game_over_timer.active:
            pygame.quit()
            sys.exit()

    def game_win(self):
        self.win_menu.update(self.game)
        if not self.game_win_flag:
            self.game_win_flag = True
            self.game_win_timer.activate()
        self.game_win_timer.update()
        if not self.game_win_timer.active:
            if self.new_best():
                self.game.display_surface.fill('black')
                self.game.state = 'NEW RECORD'
            else:
                pygame.quit()
                sys.exit()

    def new_best(self):
        with open('scoreboard.pickle', 'rb') as file:
            scoreboard = pickle.load(file)
        scoreboard.sort(key=lambda a: a[1])
        return scoreboard[0][1] < self.game.player_score

    def update(self, state):
        self.game.display_surface.fill(0)
        match state:
            case 'MAIN MENU':
                self.main_menu.update(self.game)
            case 'SCOREBOARD':
                self.scoreboard_menu.update()
            case 'REFERENCE':
                self.reference_menu.update(self.game)
            case 'LOADING GAME':
                self.loading_game()
            case 'GAME OVER':
                self.game_over()
            case 'GAME WIN':
                self.game_win()
            case 'NEW RECORD':
                self.save_result_menu.update(self.game)
