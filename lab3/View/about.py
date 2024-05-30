import pygame
import sys


class About:
    def __init__(self, width, height, screen: pygame.display):
        self.screen = screen
        self.width = width
        self.height = height
        self.about_text = ["Pong is one of the earliest arcade video games and a seminal piece of the gaming industry.",
        "It was created by Atari and released in 1972. Pong is a simple two-dimensional tennis game that has been",
        "widely regarded as the game that launched the arcade video game industry and helped establish video games",
         "as a mainstream entertainment medium.",
        "Gameplay",
    "Pong simulates a table tennis game where the player controls an in-game paddle by moving it vertically across",
    "the left or right side of the screen. The objective is to use the paddle to hit a ball back and forth across",
    "the screen, trying to score points by getting the ball past the opponent's paddle.",
    "The game can be played against another human player or a computer-controlled opponent.",
    
    "Game Mechanics",
    "Controls: The game is controlled using simple up and down buttons to move the paddle vertically.",
    "Scoring: Points are scored when the opponent fails to return the ball. The first player to reach a predetermined",
     "number of points wins the game.",
    "Physics: The ball bounces off the top and bottom edges of the screen, and the angle of the ball's bounce is",
     "influenced by where it hits the paddle.",
    "For exit from every new display use ESC button."]
        self.draw()
        return

    def draw(self):
        pygame.display.set_caption("Table Record")
        clock = pygame.time.Clock()
        text_font = pygame.font.SysFont("freesansbold.ttf", 32)
        title_font = pygame.font.SysFont("freesansbold.ttf", 64)
        light_grey = (200, 200, 200)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.screen.fill((0, 0, 0))
            title_text = title_font.render("About the game", False, light_grey)
            self.print_text(text_font)
            self.screen.blit(title_text, (self.width/2-200, 0))
            pygame.display.flip()
            clock.tick(30)

    def print_text(self, text_font):
        count = 0
        for line in self.about_text:
            about_label = text_font.render(line, True, (255, 255, 255))
            self.screen.blit(about_label, (100, 100 + count*35))
            count += 1

