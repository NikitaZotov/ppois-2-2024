import pygame
import source.constants as constants
from source.models.grid_item import GridItem


class Block(GridItem):
    def __init__(self, screen: pygame.Surface, row_num: int, col_num: int):
        super().__init__(screen, row_num, col_num)
        self.image: pygame.Surface = pygame.image.load("../resources/images/block.jpg")

        self.image: pygame.Surface = pygame.transform.smoothscale(self.image, constants.JEWEL_SIZE)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.left = self.col_num * constants.JEWEL_WIDTH
        self.rect.top = self.row_num * constants.JEWEL_HEIGHT

    def draw(self):
        self.screen.blit(self.image, self.rect)
