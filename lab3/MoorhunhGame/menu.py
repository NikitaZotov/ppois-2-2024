import pygame
import constant
from game import Game
from sound import Sound
from background import Background
from leaderboard import Leaderboard


class Menu:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.sound = Sound()
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load("images/icon.bmp")
        self.caption = "Moorhunh"
        self.screen = pygame.display.set_mode((constant.WINDOW_X, constant.WINDOW_Y))
        self.background = Background(self.screen, 0, 0)
        self.background.set_menu_background()
        self.flag = True

    def start_app(self):
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)
        pygame.display.set_mode((constant.WINDOW_X, constant.WINDOW_Y))
        self.sound.start_menu_music()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("Button was klicked")
                        position = pygame.mouse.get_pos()
                        if self.background.background_number == 5:
                            print(self.background.background_number)
                            if position[0] > 653 and position[0] < 678 and position[1] > 72 and position[1] < 97:
                                self.background.set_menu_background()
                                self.background.background_number = 0
                                self.flag = True
                                self.sound.choose()
                        elif self.background.background_number == 6:
                            if position[0] > 734 and position[0] < 759 and position[1] > 101 and position[1] < 126:
                                self.background.set_menu_background()
                                self.background.background_number = 0
                                self.flag = True
                                self.sound.choose()
                        else:
                            self.call_menu_functions()
            if self.flag:
                self.background.check_coords_position(pygame.mouse.get_pos())
                self.background.print_background()
            # self.find_coords()
            if self.background.background_number == 5:
                leaderboard = Leaderboard(self.screen)
                leaderboard.print_leaderboard()
            pygame.display.update()
            self.clock.tick(constant.FPS)
        pygame.quit()

    def call_menu_functions(self):
        if self.background.background_number == 1:
            print("restart game")
            self.game = Game(self.screen)
            pygame.mouse.set_pos(400, 300)
            pygame.mouse.set_visible(False)
            play_agan = self.game.start_game()
            pygame.mouse.set_visible(True)
            if play_agan == True:
                self.call_menu_functions()
            else:
                self.sound.start_menu_music()
        elif self.background.background_number == 2:
            self.flag = False
            self.background.set_record_menu()
        elif self.background.background_number == 3:
            self.flag = False
            self.background.set_reference_menu()
        elif self.background.background_number == 4:
            self.running = False

    def find_coords(self):
        pygame.draw.rect(self.screen, (0, 0, 255), (734, 101, 25, 25))
        pygame.display.flip()
