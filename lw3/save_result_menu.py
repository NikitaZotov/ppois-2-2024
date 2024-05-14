import pygame

from settings import *
from text_input_box import TextInputBox


class SaveResultMenu:
    def __init__(self):
        self.main_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_surface.fill('black')

        self.font = pygame.font.Font("fonts/emulogic.ttf", 20)

        self.entry_text = self.font.render('YOUR RESULT IS NOW IN TOP-5\nWRITE YOUR NAME TO SAVE IT', False, (255, 255, 255))
        self.input_box = TextInputBox(50, 200, 215, self.font)
        self.group = pygame.sprite.Group(self.input_box)

        self.confirm_text = self.font.render('PRESS ENTER TO CONFIRM', False, (255, 255, 255))

    def update(self, game):
        game.display_surface.blit(self.main_surface, (0, 0))
        game.display_surface.blit(self.entry_text, (50, 50))
        game.display_surface.blit(self.confirm_text, (50, 300))

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.update_scoreboard(self.input_box.text)
                    pygame.quit()
                    sys.exit()

        self.group.update(event_list)
        self.main_surface.fill(0)
        self.group.draw(self.main_surface)
