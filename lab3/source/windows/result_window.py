import pygame
import source.constants as constants
from source.models.result import Result, BestResult
from pygame.locals import *
from source.controllers.json_manager import JSONManager
from source.models.input_box import TextInputBox


class ResultWindow:
    def __init__(self, score, moves, time):
        pygame.init()
        self.json_manager: JSONManager = JSONManager()
        self.font: pygame.font.Font = pygame.font.Font("../resources/fonts/Cinzel-VariableFont_wght.ttf", 18)
        self.winner_name_input_box = TextInputBox(100, 320, 200, 30, self.font)
        self.result: Result = Result(time, moves, score)
        self.default_sound: pygame.mixer.Sound = pygame.mixer.Sound("../resources/sounds/default_result_sound.mp3")
        self.screen: pygame.Surface = pygame.display.set_mode(constants.WINDOW_SIZE)
        self.font.set_bold(True)
        self.result_points_text: list = ["Time: " + str(self.result.time // 60) + " min " + str(self.result.time % 60) + " sec",
                                   "Moves: " + str(self.result.moves), "Score: " + str(self.result.score),
                                   "Score per move: " + str(self.result.get_score_per_move()),
                                   "Score per second: " + str(self.result.get_score_per_second())]
        self.result_points_rect: list = []
        self.background: pygame.Surface = pygame.image.load("../resources/images/menu_background.jpeg")
        self.background_rect: pygame.Rect = self.background.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 2))
        self.dark_surface: pygame.Surface = pygame.Surface((constants.WIDTH, constants.HEIGHT + constants.SCOREBOARD_HEIGHT))
        self.dark_surface.set_alpha(128)
        self.dark_surface.fill((0, 0, 0))
        self.ok_text: pygame.Surface = self.font.render("OK", True, (255, 255, 255))
        self.ok_rect: pygame.Rect = self.ok_text.get_rect(center=(constants.WIDTH / 2, 380))
        self.best_result_text: pygame.Surface = self.font.render("IT'S THE BEST RESULT!", True, (255, 255, 255))
        self.best_result_rect: pygame.Rect = self.best_result_text.get_rect(center=(constants.WIDTH / 2, 50))

        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.dark_surface, (0, 0))
        pygame.display.set_caption("Jewel Quest")
        if self.json_manager.is_best_result_for_score_per_second(self.result) or self.json_manager.is_best_result_for_score_per_move(self.result):
            self.screen.blit(self.best_result_text, self.best_result_rect)

        for i in range(len(self.result_points_text)):
            text: pygame.Surface = self.font.render(self.result_points_text[i], True, (255, 255, 255))
            h_position: int = 100 + i * 50
            text_rect: pygame.Rect = text.get_rect(center=(constants.WIDTH / 2, h_position))
            self.result_points_rect.append(text_rect)
            self.screen.blit(text, text_rect)
        self.screen.blit(self.ok_text, self.ok_rect)

    def run(self):
        # game loop
        running: bool = True
        self.default_sound.play()
        while running:
            if self.json_manager.is_best_result_for_score_per_second(self.result) or self.json_manager.is_best_result_for_score_per_move(self.result):
                self.winner_name_input_box.draw(self.screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running: bool = False
                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.ok_rect.collidepoint(x, y):
                        from source.windows.menu_window import MenuWindow
                        if self.json_manager.is_best_result_for_score_per_second(self.result):
                            winner_name = self.winner_name_input_box.text
                            best_result = BestResult(winner_name, self.result.time, self.result.moves,
                                                     self.result.score)
                            if len(winner_name) == 0:
                                continue
                            self.json_manager.add_best_result_for_score_per_second(best_result)
                        if self.json_manager.is_best_result_for_score_per_move(self.result):
                            winner_name = self.winner_name_input_box.text
                            best_result = BestResult(winner_name, self.result.time, self.result.moves,
                                                     self.result.score)
                            if len(winner_name) == 0:
                                continue
                            self.json_manager.add_best_result_for_score_per_move(best_result)
                        menu: MenuWindow = MenuWindow()
                        menu.run()
                        pygame.display.update()
                        running = False
                self.winner_name_input_box.handle_event(event)

            pygame.display.update()

