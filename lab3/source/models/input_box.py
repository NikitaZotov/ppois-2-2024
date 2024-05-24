import pygame


class TextInputBox:
    def __init__(self, x, y, width, height, font, color=(255, 255, 255), max_characters=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = ''
        self.font = font
        self.max_characters = max_characters
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                print(self.text)
            else:
                if (self.max_characters is None or
                        len(self.text) < self.max_characters):
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4))
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
