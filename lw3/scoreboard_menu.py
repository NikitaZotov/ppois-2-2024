from settings import *


class ScoreboardMenu:
    def __init__(self, game):
        self.main_surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_surface.fill('black')

        self.game = game

        self.scoreboard = self.game.load()
        self.scoreboard.sort(key=lambda a: a[1], reverse=True)

        self.places = []
        self.places_pos = []

        self.font = pygame.font.Font("fonts/emulogic.ttf", 20)

        self.instructions_text = self.font.render('PRESS ESC TO EXIT SCOREBOARD', False, (255, 255, 255))

        for i in range(5):
            text = self.font.render(f'{i + 1}. ', False, (255, 255, 255))
            self.places.append(text)
            self.places_pos.append((50, (i + 1) * 50))

    def update(self):
        self.game.display_surface.blit(self.main_surface, (0, 0))
        self.game.display_surface.blit(self.instructions_text, (50, 0))
        for i in range(5):
            self.game.display_surface.blit(self.places[i], self.places_pos[i])
            place = self.font.render(f'{self.scoreboard[i][0]} - {self.scoreboard[i][1]}', False, (255, 255, 255))
            self.game.display_surface.blit(place, (self.places_pos[i][0] + 40, self.places_pos[i][1]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game.state = 'MAIN MENU'
