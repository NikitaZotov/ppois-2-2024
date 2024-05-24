from source.models.jewel_type import JewelType
from source.models.effect_type import EffectType

# set game window parameters
WIDTH = 400
HEIGHT = 400
SCOREBOARD_HEIGHT = 25
WINDOW_SIZE = (WIDTH, HEIGHT + SCOREBOARD_HEIGHT)

# jewel size
JEWEL_WIDTH = 40
JEWEL_HEIGHT = 40
JEWEL_SIZE = (JEWEL_WIDTH, JEWEL_HEIGHT)

RULES_TEXT = ('Welcome to the game ‘Jewels Quest’. In it you will have to collect identical gems in combinations. In the game there are 7 types of common stones: red, green, blue, yellow, purple, dark and turquoise. The combination requires at least 3 identical stones in a row, all adjacent stones will be included in the combination.'
              'Also, regular stones can have certain effects: bomb, lightning and fire.'
              '- Bomb: when a combination with a bomb is collected, the stone itself and all surrounding stones disappear.'
              '- Lightning: when combining with Lightning, the stone itself and all stones horizontally and vertically disappear.'
              '- Fire: when you collect a combination with fire, the stone itself and all the stones along the diagonals disappear.'
              'There are 2 modes in the game:'
              '- By time: the game ends when a certain time expires.'
              '- On points: the game ends when the player reaches a certain number of points.'
              'The game also has 3 different levels.')

# set jewel colors
JEWEL_NAMES = (
    JewelType.RED_STONE, JewelType.GREEN_STONE, JewelType.BLUE_STONE, JewelType.YELLOW_STONE, JewelType.PURPLE_STONE,
    JewelType.DARK_STONE, JewelType.CYAN_STONE)
EFFECT_NAMES = (EffectType.NONE, EffectType.BOMB, EffectType.FLAME, EffectType.LIGHTNING)
EFFECT_WEIGHTS = (0.9, 0.1 / 3, 0.1 / 3, 0.1 / 3)
LEVEL_NAMES = ("level1", "level2", "level3")
