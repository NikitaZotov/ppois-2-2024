import pygame


class Button:
    def __init__(self, width, height, screen: pygame.display = None):
        self.screen = screen
        self.width = width
        self.height = height
        self.inactive_clr = (200, 200, 200)
        self.active_clr = (255, 255, 255)
        self.btn_font = pygame.font.Font("freesansbold.ttf", 32)

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(5)
        if mouse[0]-self.width < x < mouse[0]+self.width and mouse[1]-self.height < y < mouse[1]+self.height:
            pygame.draw.rect(self.screen, self.active_clr, (x-8, y, self.width, self.height))
            if click and action is not None:
                action()

        else:
            pygame.draw.rect(self.screen, self.inactive_clr, (x-8, y, self.width, self.height))
        btn_text = self.btn_font.render(message, False, (0, 0, 0))
        self.screen.blit(btn_text, (x, y))