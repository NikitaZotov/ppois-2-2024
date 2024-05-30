import pygame
import sys
from Model.game import Game
from View.button import Button
from View.table_record import TableRecord
from View.about import About


class Menu:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.start_menu()

    def start_menu(self):
        pygame.init()
        clock = pygame.time.Clock()
        play = Button(120, 40, screen=self.screen)
        table = Button(120, 40, screen=self.screen)
        readme = Button(130, 40, screen=self.screen)
        quit = Button(120, 40, screen=self.screen)
        title_text = "PONG"
        game_font = pygame.font.Font("freesansbold.ttf", 64)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.quit()
            self.screen.fill((0, 0, 0))
            title_font = game_font.render(title_text, False, (200, 200, 200))
            self.screen.blit(title_font, (self.screen_width / 2 - 100, 100))
            play.draw(300, 400, "Play", action=self.game)
            table.draw(500, 400, "Table", action=self.table_record)
            readme.draw(700, 400, "About", action=self.about)
            quit.draw(900, 400, "Quit", action=self.quit)
            pygame.display.flip()
            clock.tick(30)

    def game(self):
        game = Game(self.screen_width, self.screen_height, self.screen)

    def table_record(self):
        table_record = TableRecord(self.screen_width, self.screen_height, self.screen)

    def about(self):
        about = About(self.screen_width, self.screen_height, self.screen)

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    menu = Menu()