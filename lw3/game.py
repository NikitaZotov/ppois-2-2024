from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from support import *
from timer import Timer
from menu_manager import MenuManager
from sound_manager import SoundManager
import pickle


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface: pygame.Surface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
        pygame.display.set_caption('Super Mario Bros')
        self.clock = None
        self.sound_manager = SoundManager()

        self.state = 'MAIN MENU'
        self.menu_manager = MenuManager(self)
        self.game_begin = False

        self.tmx_maps = {0: load_pygame('worlds/1-1/W11.tmx')}

        self.level_frames = None
        self.import_assets()

        self.world_timer = Timer(400000)
        self.game_over_timer = Timer(2000)

        self.current_stage: Level = Level(self, self.tmx_maps[0], self.level_frames)
        self.game_end = False
        self.world = '1-1'
        self.player_lives = 3
        self.player_coins = 0
        self.player_score = 0

    @staticmethod
    def save(scoreboard_results):
        with open('scoreboard.pickle', 'wb') as file:
            pickle.dump(scoreboard_results, file)

    @staticmethod
    def load():
        with open('scoreboard.pickle', 'rb') as file:
            scoreboard_results = pickle.load(file)
        return scoreboard_results

    def import_assets(self):
        self.level_frames = {
            'coin': import_folder('images', 'coin'),
            'player': import_sub_folders('images', 'mario', 'mario0'),
            'player1': import_sub_folders('images', 'mario', 'mario1'),
            'player2': import_sub_folders('images', 'mario', 'mario2'),
            'goomba': import_sub_folders('images', 'goomba')
        }

    def game_over(self):
        self.sound_manager.stop('overworld')
        self.sound_manager.play('game_over', 0, 0.5)
        self.display_surface.fill('black')
        self.current_stage.game_ui.game_end = True
        self.state = 'GAME OVER'

    def game_win(self):
        self.display_surface.fill('black')
        self.current_stage.game_ui.game_end = True
        self.state = 'GAME WIN'

    def update_scoreboard(self, nickname):
        scoreboard_results = self.load()
        scoreboard_results.sort(key=lambda a: a[1])
        scoreboard_results.pop(0)
        scoreboard_results.append((nickname, self.player_score))
        self.save(scoreboard_results)

    def time_update(self):
        if not self.world_timer.active:
            if not self.game_end:
                self.game_end = True
                self.game_over_timer.activate()
            if not self.game_over_timer.active:
                self.game_over()
            else:
                self.game_over_timer.update()
        if not self.game_end:
            self.world_timer.update()
        elif self.game_end and self.world_timer.active:
            if int(self.world_timer.current_time) <= 400000:
                self.world_timer.current_time += 1000
                self.player_score += 5

    def run(self):
        self.time_update()
        delta_time = self.clock.tick() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.current_stage.run(delta_time)

    def main_loop(self):
        while True:
            if self.state == 'GAME':
                if not self.game_begin:
                    self.clock = pygame.Clock()
                    self.world_timer.activate()
                    self.game_begin = True
                self.run()
            else:
                self.menu_manager.update(self.state)
            pygame.display.update()
