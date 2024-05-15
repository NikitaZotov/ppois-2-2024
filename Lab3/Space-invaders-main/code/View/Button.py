import pygame
from settings import font_path

class Button():
    def __init__(self,screen, pos, width, height, text, callback=None,motion_callback=None):
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text
        self.screen=screen
        self.callback = callback
        self.motion_callback=motion_callback
        self.font = pygame.font.Font(font_path, 20)
        self.clicked = False
        self.rect=pygame.Rect(pos[0],pos[1],width,height)

    def update(self):
        color = (150, 150, 150)
        if self.clicked:
            color = (120, 120, 120)
        pygame.draw.rect(self.screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
                    pygame.time.wait(300)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.clicked and self.rect.collidepoint(event.pos):
                    self.clicked = False
                    if self.callback:
                        self.callback()
        elif event.type == pygame.MOUSEMOTION:
            self.clicked = self.rect.collidepoint(event.pos)
            if self.clicked and self.motion_callback:
                self.motion_callback();

