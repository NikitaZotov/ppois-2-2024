import pygame


class GridItem:
    def __init__(self, screen: pygame.Surface, row_num: int, col_num: int):
        self.screen: pygame.Surface = screen
        self.row_num: int = row_num
        self.col_num: int = col_num
