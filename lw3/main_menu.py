import sys

import pygame

from settings import *


class MainMenu:
    def __init__(self):
        self.main_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_surface.fill('black')

        # menu options
        self.font = pygame.font.Font("fonts/emulogic.ttf", 20)

        self.play_text = self.font.render('PLAY', False, (255, 255, 255))

        self.scoreboard_text = self.font.render('SCOREBOARD', False, (255, 255, 255))

        self.reference_text = self.font.render('REFERENCE', False, (255, 255, 255))

        self.exit_text = self.font.render('EXIT', False, (255, 255, 255))

        self.choice_rect = pygame.surface.Surface((20, 20))
        self.choice_rect.fill('white')
        self.choice_rect_pos_index = 0
        self.choice_rect_pos = {
            0: (50, 55),
            1: (50, 155),
            2: (50, 255),
            3: (50, 355)
        }

    def update(self, game):
        game.display_surface.blit(self.main_surface, (0, 0))
        game.display_surface.blit(self.play_text, (100, 50))
        game.display_surface.blit(self.scoreboard_text, (100, 150))
        game.display_surface.blit(self.reference_text, (100, 250))
        game.display_surface.blit(self.exit_text, (100, 350))
        game.display_surface.blit(self.choice_rect, self.choice_rect_pos[self.choice_rect_pos_index])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.choice_rect_pos_index = max(self.choice_rect_pos_index - 1, 0)
                if keys[pygame.K_DOWN]:
                    print(self.choice_rect_pos_index)
                    self.choice_rect_pos_index = min(self.choice_rect_pos_index + 1, 3)
                if keys[pygame.K_RETURN]:
                    match self.choice_rect_pos_index:
                        case 0:
                            game.state = 'LOADING GAME'
                        case 1:
                            game.state = 'SCOREBOARD'
                        case 2:
                            game.state = 'REFERENCE'
                        case 3:
                            pygame.quit()
                            sys.exit()

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     self.choice_rect_pos_index = max(self.choice_rect_pos_index - 1, 0)
        # if keys[pygame.K_DOWN]:
        #     print(self.choice_rect_pos_index)
        #     self.choice_rect_pos_index = min(self.choice_rect_pos_index + 1, 3)
        # if keys[pygame.K_RETURN]:
        #     match self.choice_rect_pos_index:
        #         case 0:
        #             game.state = 'LOADING GAME'
        #         case 1:
        #             game.state = 'SCOREBOARD'
        #         case 2:
        #             game.state = 'REFERENCE'
        #         case 3:
        #             pygame.quit()
        #             sys.exit()
