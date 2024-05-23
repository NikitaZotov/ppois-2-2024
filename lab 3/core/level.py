import random

from brick import Brick
from core.wall import Wall
from game_consts import *


class LevelHandler:
    XML_FILE_PATH = "../static/levels.xml"

    current_level_index = None

    @staticmethod
    def read_levels_from_xml(file_path):
        levels = []
        tree = ET.parse(file_path)
        root = tree.getroot()
        for level in root.findall('level'):
            rows = [row.text for row in level.findall('row')]
            levels.append(rows)
        return levels

    @staticmethod
    def create_level(level_id=None):
        levels = LevelHandler.read_levels_from_xml(LevelHandler.XML_FILE_PATH)
        if level_id is None:
            chosen_level = random.choice(levels)
            LevelHandler.current_level_index = levels.index(chosen_level) + 1  # Adding 1 to make it 1-indexed
        else:
            chosen_level = levels[level_id]
            LevelHandler.current_level_index = level_id  # If a specific level is provided, use that

        bricks = pygame.sprite.Group()
        walls = pygame.sprite.Group()
        y = 0
        for row in chosen_level:  # Using chosen_level instead of level
            x = 0
            for brick in row:
                if brick == "B":
                    new_brick = Brick()
                    new_brick.rect.x = x * BRICK_WIDTH
                    new_brick.rect.y = y * BRICK_HEIGHT
                    bricks.add(new_brick)
                elif brick == "W":
                    new_wall = Wall(BRICK_WIDTH, BRICK_HEIGHT)
                    new_wall.rect.x = x * BRICK_WIDTH
                    new_wall.rect.y = y * BRICK_HEIGHT
                    walls.add(new_wall)
                x += 1
            y += 1
        return bricks, walls
