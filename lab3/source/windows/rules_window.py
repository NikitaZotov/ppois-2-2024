import pygame
from pygame.locals import *
import source.constants as constants
import source.helpers.helper as helper


class RulesWindow:
    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode(constants.WINDOW_SIZE)
        self.font: pygame.font.Font = pygame.font.Font("../resources/fonts/Cinzel-VariableFont_wght.ttf", 18)
        self.rules_font: pygame.font.Font = pygame.font.Font("../resources/fonts/Cinzel-VariableFont_wght.ttf", 14)
        self.font.set_bold(True)
        self.rules_text: pygame.Surface = helper.render_text_with_word_wrap(constants.RULES_TEXT, self.rules_font, 400)
        self.background: pygame.Surface = pygame.image.load("../resources/images/menu_background.jpeg")
        self.background_rect: pygame.Rect = self.background.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 2))
        self.dark_surface: pygame.Surface = pygame.Surface((constants.WIDTH, constants.HEIGHT + constants.SCOREBOARD_HEIGHT))
        self.dark_surface.set_alpha(128)
        self.dark_surface.fill((0, 0, 0))
        self.back_text: pygame.Surface = self.font.render("Back", True, (255, 255, 255))
        self.back_rect: pygame.Rect = self.back_text.get_rect(center=(constants.WIDTH / 2, 390))

        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.dark_surface, (0, 0))
        self.screen.blit(self.rules_text, self.rules_text.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 2)))
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
                        from source.windows.menu_window import MenuWindow
                        game: MenuWindow = MenuWindow()
                        game.run()
                        pygame.display.update()
                        running: bool = False

            pygame.display.update()
