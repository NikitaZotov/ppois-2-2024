import pygame
from pygame.locals import *
import source.constants as constants
from source.controllers.json_manager import JSONManager


class RecordsScorePerSecondWindow:
    def __init__(self):
        pygame.init()
        self.json_manager: JSONManager = JSONManager()
        self.screen: pygame.Surface = pygame.display.set_mode(constants.WINDOW_SIZE)
        self.font: pygame.font.Font = pygame.font.Font("../resources/fonts/Cinzel-VariableFont_wght.ttf", 18)
        self.font.set_bold(True)
        self.records_headers: list = ["Place", "Name", "Score", "Time(sec)"]
        self.records: list = self.json_manager.get_records_by_score_per_second_from_json()[:10]
        self.background: pygame.Surface = pygame.image.load("../resources/images/menu_background.jpeg")
        self.background_rect: pygame.Rect = self.background.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 2))
        self.dark_surface: pygame.Surface = pygame.Surface((constants.WIDTH, constants.HEIGHT + constants.SCOREBOARD_HEIGHT))
        self.dark_surface.set_alpha(128)
        self.dark_surface.fill((0, 0, 0))
        self.back_text: pygame.Surface = self.font.render("Back", True, (255, 255, 255))
        self.back_rect: pygame.Rect = self.back_text.get_rect(center=(constants.WIDTH / 2, 380))

        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.dark_surface, (0, 0))

        pygame.display.set_caption("Jewel Quest")
        for i in range(len(self.records_headers)):
            text: pygame.Surface = self.font.render(self.records_headers[i], True, (255, 255, 255))
            w_position: int = 50 + i * 100
            text_rect: pygame.Rect = text.get_rect(center=(w_position, 100))
            self.screen.blit(text, text_rect)

        for i in range(len(self.records)):
            h_position: int = 130 + i * 30
            place: pygame.Surface = self.font.render(str(i+1), True, (255, 255, 255))
            name: pygame.Surface = self.font.render(self.records[i]["name"], True, (255, 255, 255))
            score: pygame.Surface = self.font.render(str(self.records[i]["score"]), True, (255, 255, 255))
            moves: pygame.Surface = self.font.render(str(self.records[i]["moves"]), True, (255, 255, 255))
            place_rect: pygame.Rect = place.get_rect(center=(50, h_position))
            name_rect: pygame.Rect = name.get_rect(center=(150, h_position))
            score_rect: pygame.Rect = score.get_rect(center=(250, h_position))
            moves_rect: pygame.Rect = moves.get_rect(center=(350, h_position))

            self.screen.blit(place, place_rect)
            self.screen.blit(name, name_rect)
            self.screen.blit(score, score_rect)
            self.screen.blit(moves, moves_rect)

        self.screen.blit(self.back_text, self.back_rect)

    def run(self):
        clock: pygame.time.Clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running: bool = False

                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.back_rect.collidepoint(x, y):
                        from source.windows.records_window import RecordsWindow
                        game: RecordsWindow = RecordsWindow()
                        game.run()
                        pygame.display.update()
                        running: bool = False

            pygame.display.update()
