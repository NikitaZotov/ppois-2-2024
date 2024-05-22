import pygame
import constant


class Score:
    def __init__(self):
        self.score = 0

    def hit(self, score):
        self.score += score

    def print_score(self, screen):
        # self.score += 1
        font = pygame.font.Font("font/ofont.ru_Kardinal.ttf", 30)
        text_score = font.render(f"SCORE: {self.score}", True, constant.WHITE)
        text_score_black = font.render(f"SCORE: {self.score}", True, constant.BLACK)
        screen.blit(text_score_black, (609, 9))
        screen.blit(text_score_black, (609, 11))
        screen.blit(text_score_black, (611, 9))
        screen.blit(text_score_black, (611, 11))
        screen.blit(text_score, (610, 10))

    def print_score_after_death(self, score, coord_x, coord_y, screen, num):
        if num > 54:
            num = 54
        font = pygame.font.Font("font/ofont.ru_Kardinal.ttf", num)
        text_score = font.render(f"{score}", True, constant.WHITE)
        text_score_black = font.render(f"{score}", True, constant.BLACK)
        screen.blit(text_score_black, (coord_x - 1, coord_y - 1))
        screen.blit(text_score_black, (coord_x - 1, coord_y + 1))
        screen.blit(text_score_black, (coord_x + 1, coord_y - 1))
        screen.blit(text_score_black, (coord_x + 1, coord_y + 1))
        screen.blit(text_score, (coord_x,coord_y))