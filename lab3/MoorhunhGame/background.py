import pygame
import constant
import random
from sound import Sound


class Background:
    def __init__(self, screen,x,y):
        pygame.init()
        self.x_pos = x
        self.y_pos = y
        self.screen = screen
        self.background_number = 0
        # self.set_game_background()
        # self.save_main_background = self.background

    def create_scale_background(self, scale):
        if scale > 1:
            self.background = pygame.transform.scale(self.background, (1440, 720))
        else:
            self.background = self.save_main_background
        if self.x_pos < -400:
            self.x_pos = -400
        self.screen.blit(self.background, (0, 0))

    def print_background(self, x=constant.START_POSX, y=constant.START_POSY):
        # print(x)
        self.screen.blit(self.background, (x, y))

    def set_game_background(self):
        number = random.randint(0,4)
        if number == 0:
            self.background = pygame.image.load("images/background.bmp").convert()
        elif number == 1:
            self.background = pygame.image.load("images/background.png").convert_alpha()
        elif number == 2:
            self.background = pygame.image.load("images/background1.png").convert_alpha()
        else:
            self.background = pygame.image.load("images/background2.png").convert_alpha()
        self.save_main_background = self.background

    def check_coords_position(self,position):
        number = self.background_number
        if position[0] > 150 and position[0] < 360:
            if position[1] > 190 and position[1] < 240:
                self.set_menu_background(1)
                self.background_number = 1
            elif position[1] > 240 and position[1] < 290:
                self.set_menu_background(2)
                self.background_number = 2
            elif position[1] > 290 and position[1] < 340:
                self.set_menu_background(3)
                self.background_number = 3
            elif position[1] > 340 and position[1] < 390:
                self.set_menu_background(4)
                self.background_number = 4
            else:
                self.set_menu_background()
                self.background_number = 0
        else:
            self.set_menu_background()
            self.background_number = 0
        if number != self.background_number and self.background_number != 0:
            sound = Sound()
            sound.choose()


    def set_menu_background(self,number = 0):
        if number == 0:
            self.background = pygame.image.load("images/Menu.png").convert()
        elif number == 1:
            self.background = pygame.image.load("images/Menu1.png").convert()
        elif number == 2:
            self.background = pygame.image.load("images/Menu2.png").convert()
        elif number == 3:
            self.background = pygame.image.load("images/Menu3.png").convert()
        elif number == 4:
            self.background = pygame.image.load("images/Menu4.png").convert()

    def set_record_menu(self):
        self.background = pygame.image.load("images/records.png").convert()
        self.print_background()
        self.background_number = 5

    def set_reference_menu(self):
        self.background = pygame.image.load("images/reference.png").convert()
        self.print_background()
        self.background_number = 6