import pygame
from source.models.jewel import Jewel
import source.constants as constants


def decrease_jewel_size(jewel: Jewel):
    new_width: int = jewel.image.get_width() - 1
    new_height: int = jewel.image.get_height() - 1
    new_size: tuple = (new_width, new_height)
    jewel.image = pygame.transform.smoothscale(jewel.image, new_size)
    jewel.rect.left = jewel.col_num * constants.JEWEL_WIDTH + (
            constants.JEWEL_WIDTH - new_width) / 2
    jewel.rect.top = jewel.row_num * constants.JEWEL_HEIGHT + (
            constants.JEWEL_HEIGHT - new_height) / 2


def render_text_with_word_wrap(text, font, max_width):
    words = text.split(' ')
    rendered_lines = []
    rendered_line = ''
    for word in words:
        test_line = rendered_line + word + ' '
        test_render = font.render(test_line, True, (255, 255, 255))
        if test_render.get_width() <= max_width:
            rendered_line = test_line
        else:
            rendered_lines.append(rendered_line)
            rendered_line = word + ' '
    rendered_lines.append(rendered_line)

    rendered_surface = pygame.Surface((max_width, sum([font.size(line)[1] for line in rendered_lines])),
                                      pygame.SRCALPHA)
    y = 0
    for line in rendered_lines:
        rendered_text = font.render(line, True, (255, 255, 255))
        rendered_surface.blit(rendered_text, (0, y))
        y += font.size(line)[1]

    return rendered_surface

