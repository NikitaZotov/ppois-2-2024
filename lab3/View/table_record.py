import pygame
import sys
from Model.table import Table


class TableRecord:
    def __init__(self, width, height, screen: pygame.display):
        self.table = Table()
        self.screen = screen
        self.width = width
        self.height = height
        self.draw()
        return

    def draw(self):
        pygame.display.set_caption("Table Record")
        clock = pygame.time.Clock()
        text_font = pygame.font.SysFont("freesansbold.ttf", 32)
        title_font = pygame.font.SysFont("freesansbold.ttf", 64)
        light_grey = (200, 200, 200)
        records = self.table.get_five_first()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.screen.fill((0, 0, 0))
            title_text = title_font.render("Records", False, light_grey)
            self.screen.blit(title_text, (self.width/2-64, 0))
            name_text = text_font.render("Name", False, light_grey)
            number_text = text_font.render("Number goals", False, light_grey)
            self.screen.blit(name_text, (self.width/2-200, 100))
            self.screen.blit(number_text, (self.width/2+200, 100))
            for i in range(len(records)):
                name_text = text_font.render(f"{records[i][0]}", False, light_grey)
                number_text = text_font.render(f"{records[i][1]}", False, light_grey)
                self.screen.blit(name_text, (self.width/2-200, 160+50*i))
                self.screen.blit(number_text, (self.width/2+200, 160+50*i))
            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    f = TableRecord(1280,   720,   screen)
