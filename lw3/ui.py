from settings import *


class GameUI:

    def __init__(self):
        self.font = pygame.font.Font("fonts/emulogic.ttf", 20)
        self.text = "SCORE COINS WORLD TIME LIVES"

        self.game_end = False

    def update(self, game):
        if self.game_end:
            return
        x = 10
        for word in self.text.split(' '):
            rect = self.font.render(word, False, (255, 255, 255))
            game.display_surface.blit(rect, (x, 0))
            x += 168

        text = self.font.render(str(game.player_score), False, (255, 255, 255))  # player score
        rect = text.get_rect(center=(60, 35))
        game.display_surface.blit(text, rect)

        text = self.font.render(str(game.player_coins), False, (255, 255, 255))  # player coins
        rect = text.get_rect(center=(230, 35))
        game.display_surface.blit(text, rect)

        text = self.font.render(game.world, False, (255, 255, 255))  # world name
        rect = text.get_rect(center=(395, 35))
        game.display_surface.blit(text, rect)

        text = self.font.render(str(400 - int(int(game.world_timer.current_time) / 1000)), False, (255, 255, 255))  # time
        rect = text.get_rect(center=(557, 35))
        game.display_surface.blit(text, rect)

        text = self.font.render(str(game.player_lives), False, (255, 255, 255))  # num of lives
        rect = text.get_rect(center=(730, 35))
        game.display_surface.blit(text, rect)
