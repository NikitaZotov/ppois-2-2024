import pygame
import constant

class Restart:
    def __init__(self, screen):
        self.screen = screen

    def print_restart(self, score):
        self.background = pygame.image.load("images/restart.png")
        pygame.mouse.set_visible(True)
        running = True
        while running:
            self.screen.blit(self.background, (250, 175))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if position[0] > 276 and position[0] < 334 and position[1] > 300 and position[1] < 358:
                            return True
                        if position[0] > 460 and position[0] < 518 and position[1] > 300 and position[1] < 358:
                            return False
            position = [283,185]
            self.print_score(score,position)
            pygame.display.update()

    def print_leader(self, score):
        self.background = pygame.image.load("images/restart_add.png")
        text = ''
        pygame.mouse.set_visible(True)
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        position = pygame.mouse.get_pos()
                        if position[0] > 279 and position[0] < 337 and position[1] > 362 and position[1] < 420:
                            return True
                        if position[0] > 463 and position[0] < 521 and position[1] > 362 and position[1] < 420:
                            return [False, None]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        return [False, text]
                    else:
                        text += event.unicode
            custom_font = pygame.font.Font('font/ofont.ru_Kardinal.ttf', 48)
            position = [283,150]
            self.print_score(score,position)
            text = text[:10]
            txt = custom_font.render(text, True, constant.WHITE)
            txt_black = custom_font.render(text,True,constant.BLACK)
            self.screen.blit(txt_black, (295, 267))
            self.screen.blit(txt_black, (297, 267))
            self.screen.blit(txt_black, (295, 269))
            self.screen.blit(txt_black, (297, 269))
            self.screen.blit(txt, (296, 269))
            # self.screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            # self.print_rect()
            pygame.display.update()

    def print_rect(self):
        pygame.draw.rect(self.screen,(0,0,255),(463,387,58,58))
        pygame.display.flip()
    def print_score(self, score, position):
        custom_font = pygame.font.Font('font/ofont.ru_Kardinal.ttf', 88)
        text = custom_font.render(f"{score}", True, constant.WHITE)
        text_black = custom_font.render(f"{score}", True, constant.BLACK)
        self.screen.blit(text_black, (position[0] - 1, position[1] - 1))
        self.screen.blit(text_black, (position[0] - 1, position[1] + 1))
        self.screen.blit(text_black, (position[0] + 1, position[1] - 1))
        self.screen.blit(text_black, (position[0] + 1, position[1] + 1))
        self.screen.blit(text, (position[0], position[1]))
