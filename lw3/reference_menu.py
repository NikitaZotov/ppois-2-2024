from settings import *


class ReferenceMenu:
    def __init__(self):
        self.main_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_surface.fill('black')

        self.font = pygame.font.Font("fonts/emulogic.ttf", 15)

        reference = ('SUPER MARIO BROS IS A PIXEL PLATFORMER.\n'
                     'DURING THE GAME PLAYER HAVE TO COMPLETE THE LEVEl\n'
                     'OVERCOMING OBSTACLES, AND GO TO THE CASTLE.\n'
                     'CONTROL IS IMPLEMENTED USING ARROW KEYS.\n'
                     'THERE ARE 1 MOB TYPE AND 2 TYPES OF PICK UP BONUSES.\n'
                     'IF AFTER COMPLETING THE GAME YOUR RESULT IS INTO\n'
                     'THE TOP-5 BEST, IT WOULD BE SAVED BY GAME.\n'
                     'HAVE A GOOD GAME!')

        self.instructions_text = self.font.render('PRESS ESC TO EXIT REFERENCE', False, (255, 255, 255))

        self.text = self.font.render(reference, False, (255, 255, 255))

    def update(self, game):
        game.display_surface.blit(self.main_surface, (0, 0))
        game.display_surface.blit(self.instructions_text, (50, 50))
        game.display_surface.blit(self.text, (50, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game.state = 'MAIN MENU'
