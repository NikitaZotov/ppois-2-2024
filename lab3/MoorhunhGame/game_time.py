import pygame
import constant

class Time:
    def __init__(self, time):
        self.start_time = time
        self.round_duration = constant.TIME

    def check_round_time(self, time, screen):
        elapsed_time = (time - self.start_time) // 1000
        font = pygame.font.Font("font/ofont.ru_Kardinal.ttf", 30)
        text_time = font.render(f"TIME: {self.round_duration - elapsed_time}", True, constant.WHITE)
        text_time_black = font.render(f"TIME: {self.round_duration - elapsed_time}", True, constant.BLACK)
        screen.blit(text_time_black, (9, 9))
        screen.blit(text_time_black, (9, 11))
        screen.blit(text_time_black, (11, 9))
        screen.blit(text_time_black, (11, 11))
        screen.blit(text_time, (10, 10))
        if elapsed_time > self.round_duration:
            return True
        else:
            return False