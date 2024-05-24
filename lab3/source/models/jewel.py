import pygame
import random
from source.models.effect_type import EffectType
from source.models.grid_item import GridItem
from source.models.jewel_type import JewelType
import source.constants as constants


class Jewel(GridItem):
    def __init__(self, screen: pygame.Surface, row_num: int, col_num: int, jewel_type_tuple: tuple, jewel_effect_tuple: tuple, effect_weight_tuple: tuple):
        super().__init__(screen, row_num, col_num)

        self.jewel_type: JewelType = random.choice(jewel_type_tuple)
        self.effect: EffectType = random.choices(jewel_effect_tuple, weights=effect_weight_tuple)[0]
        if self.effect != EffectType.NONE:
            image_name: str = f"../resources/images/{self.effect.value}/{self.jewel_type.value + '_' + self.effect.value}.png"
        else:
            image_name: str = f"../resources/images/default/{self.jewel_type.value}.png"
        self.image: pygame.Surface = pygame.image.load(image_name)
        self.image: pygame.Surface = pygame.transform.smoothscale(self.image, constants.JEWEL_SIZE)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.left = self.col_num * constants.JEWEL_WIDTH
        self.rect.top = self.row_num * constants.JEWEL_HEIGHT

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def snap(self):
        self.snap_row()
        self.snap_col()

    def snap_row(self):
        self.rect.top = self.row_num * constants.JEWEL_HEIGHT

    def snap_col(self):
        self.rect.left = self.col_num * constants.JEWEL_WIDTH
