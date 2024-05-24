import pygame
from pygame.locals import *
import source.constants as constants
from source.windows.game_window import GameWindow


class TimeSelectionWindow:
    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode(constants.WINDOW_SIZE)
        self.font: pygame.font.Font = pygame.font.Font("../resources/fonts/Cinzel-VariableFont_wght.ttf", 18)
        self.font.set_bold(True)
        self.menu_time_text: list = ["1 min", "2 min", "5 min"]
        self.menu_time_rect: list = []
        self.background: pygame.Surface = pygame.image.load("../resources/images/menu_background.jpeg")
        self.background_rect: pygame.Rect = self.background.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 2))
        self.dark_surface: pygame.Surface = pygame.Surface(
            (constants.WIDTH, constants.HEIGHT + constants.SCOREBOARD_HEIGHT))
        self.dark_surface.set_alpha(128)
        self.dark_surface.fill((0, 0, 0))
        self.back_text: pygame.Surface = self.font.render("Back", True, (255, 255, 255))
        self.back_rect: pygame.Rect = self.back_text.get_rect(center=(constants.WIDTH / 2, 380))

        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.dark_surface, (0, 0))

        pygame.display.set_caption("Jewel Quest")
        for i in range(len(self.menu_time_text)):
            text: pygame.Surface = self.font.render(self.menu_time_text[i], True, (255, 255, 255))
            h_position: int = 150 + i * 50
            text_rect: pygame.Rect = text.get_rect(center=(constants.WIDTH / 2, h_position))
            self.menu_time_rect.append(text_rect)
            self.screen.blit(text, text_rect)
        self.screen.blit(self.back_text, self.back_rect)

    def run(self):
        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running: bool = False

                if event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.menu_time_rect[0].collidepoint(x, y):
                        game: GameWindow = GameWindow(time=60)
                        game.run()
                        pygame.display.update()
                        running: bool = False
                    if self.menu_time_rect[1].collidepoint(x, y):
                        game: GameWindow = GameWindow(time=120)
                        game.run()
                        pygame.display.update()
                        running: bool = False
                    if self.menu_time_rect[2].collidepoint(x, y):
                        game: GameWindow = GameWindow(time=300)
                        game.run()
                        pygame.display.update()
                        running: bool = False
                    if self.back_rect.collidepoint(x, y):
                        from source.windows.game_mode_window import GameModeWindow
                        game: GameModeWindow = GameModeWindow()
                        game.run()
                        pygame.display.update()
                        running: bool = False

            pygame.display.update()
