import pygame
from View.Button import Button
class TextInputView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.text_color = (0, 0, 0)
        self.background_color = (255, 255, 255)
        self.text = ""
        self.rect = pygame.Rect( screen.get_width() // 4, screen.get_height() // 3, screen.get_width() // 2, screen.get_height() // 10)
        self.button = Button(screen, (screen.get_width() // 2 - 50,  screen.get_height() // 2 + 50), 100, 40, "OK", self.on_button_click)
        self.run=True
        self.mesage=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 15:
                 self.text += event.unicode
        self.button.handle_event(event)

    def update(self):
        if self.run==False:
            return "LeaderName"
        self.screen.fill((100, 100,100))
        max_length_text = self.font.render("Введите имя. Максимальная длинна 15 символов", True, (0, 0, 0))
        max_length_rect = max_length_text.get_rect(center=(self.rect.centerx, self.rect.top -50))
        self.screen.blit(max_length_text, max_length_rect)
        pygame.draw.rect(self.screen, self.background_color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        self.screen.blit(text_surface, text_rect)
        self.button.update()
        if self.mesage==True:
            max_length_text = self.font.render("Имя не должно быть пустым", True, (0, 0, 0))
            max_length_rect = max_length_text.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
            self.screen.blit(max_length_text, max_length_rect)

    def on_button_click(self):
        if len(self.text)>0:
            self.run=False
        else:
            self.mesage=True
