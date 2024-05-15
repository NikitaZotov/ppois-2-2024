import pygame
from settings import font_path
class HelperView():
    def __init__(self, screen,):
        self.font = pygame.font.Font(None, 36)
        self.screen = screen
        self.run = True
        self.font = pygame.font.Font(font_path, 20)

    def read_text_file(self,filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def update(self):
        self.screen.fill((255, 255, 255))
        helper_text =self.read_text_file("../configurations/helper.txt")
        self.blit_text(helper_text,(20,20))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.run = False
                pygame.time.wait(300)
                return

    def blit_text(self, text, pos, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = self.screen.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.