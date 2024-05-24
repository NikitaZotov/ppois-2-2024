import random

import pygame
from pygame.locals import *
import source.constants as constants
from source.models.jewel import Jewel
from source.models.direction import Direction
from source.windows.result_window import ResultWindow
from source.models.block import Block
from source.models.effect_type import EffectType
import source.helpers.helper as helper
from source.controllers.json_manager import JSONManager


class GameWindow:
    def __init__(self, time: int = None, points: int = None):
        self.json_manager: JSONManager = JSONManager()
        self.swap_sound: pygame.mixer.Sound = pygame.mixer.Sound("../resources/sounds/swap_sound.mp3")
        self.disappear_sound: pygame.mixer.Sound = pygame.mixer.Sound("../resources/sounds/disappear_sound.mp3")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.frame_count: int = 0
        self.time: int = time
        self.points: int = points
        self.current_time: int = 0
        self.clicked_jewel: Jewel | None = None
        self.swapped_jewel: Jewel | None = None
        self.coord_x: int | None = None
        self.coord_y: int | None = None
        self.screen: pygame.Surface = pygame.display.set_mode(constants.WINDOW_SIZE)
        self.board: list = self.json_manager.get_board()
        self.score: int = 0
        self.moves: int = 0

        pygame.display.set_caption("Jewel Quest")

        for row_num in range(constants.HEIGHT // constants.JEWEL_HEIGHT):
            for col_num in range(constants.WIDTH // constants.JEWEL_WIDTH):
                if self.board[row_num][col_num] == 0:
                    jewel_types: list = list(constants.JEWEL_NAMES)
                    jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types), constants.EFFECT_NAMES,
                                         constants.EFFECT_WEIGHTS)
                    while not self.match_three_start_check(jewel):
                        jewel_types.remove(jewel.jewel_type)
                        jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types), constants.EFFECT_NAMES,
                                             constants.EFFECT_WEIGHTS)
                    self.board[row_num][col_num] = jewel
                    print(self.match_three_start_check(jewel), row_num, col_num)
                else:
                    block: Block = Block(self.screen, row_num, col_num)
                    self.board[row_num][col_num] = block

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, 0, constants.WIDTH, constants.HEIGHT + constants.SCOREBOARD_HEIGHT))
        for row_num in range(constants.HEIGHT // constants.JEWEL_HEIGHT):
            for col_num in range(constants.WIDTH // constants.JEWEL_WIDTH):
                self.board[row_num][col_num].draw()

        font: pygame.font.Font = pygame.font.SysFont("monoface", 18)
        score_text: pygame.Surface = font.render(f"Score: {self.score}", 1, (0, 0, 0))
        score_text_rect: pygame.Rect = score_text.get_rect(
            center=(constants.WIDTH / 4, constants.HEIGHT + constants.SCOREBOARD_HEIGHT / 2))
        self.screen.blit(score_text, score_text_rect)

        moves_text: pygame.Surface = font.render(f"Moves: {self.moves}", 1, (0, 0, 0))
        moves_text_rect: pygame.Rect = moves_text.get_rect(
            center=(constants.WIDTH * 3 / 4, constants.HEIGHT + constants.SCOREBOARD_HEIGHT / 2))
        self.screen.blit(moves_text, moves_text_rect)

        if self.frame_count % 60 == 0:
            self.current_time += 1
        time_text: pygame.Surface = font.render(
            f"Time: {str(self.current_time // 60).zfill(2)}:{str(self.current_time % 60).zfill(2)}",
            1, (0, 0, 0))
        time_text_rect: pygame.Rect = time_text.get_rect(
            center=(constants.WIDTH / 2, constants.HEIGHT + constants.SCOREBOARD_HEIGHT / 2))
        self.screen.blit(time_text, time_text_rect)

    def swap(self, first_jewel: Jewel, second_jewel: Jewel):
        temp_row: int = first_jewel.row_num
        temp_col: int = first_jewel.col_num

        first_jewel.row_num = second_jewel.row_num
        first_jewel.col_num = second_jewel.col_num

        second_jewel.row_num = temp_row
        second_jewel.col_num = temp_col

        self.board[first_jewel.row_num][first_jewel.col_num] = first_jewel
        self.board[second_jewel.row_num][second_jewel.col_num] = second_jewel

        first_jewel.snap()
        second_jewel.snap()

    def match_three_check(self, jewel: Jewel):
        if jewel.row_num >= 2:
            if isinstance(self.board[jewel.row_num - 1][jewel.col_num], Jewel) and isinstance(
                    self.board[jewel.row_num - 2][jewel.col_num], Jewel):
                if (self.board[jewel.row_num - 1][jewel.col_num].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num - 2][jewel.col_num].jewel_type == jewel.jewel_type):
                    return False
        if jewel.col_num >= 2:
            if isinstance(self.board[jewel.row_num][jewel.col_num - 1], Jewel) and isinstance(
                    self.board[jewel.row_num][jewel.col_num - 2], Jewel):
                if (self.board[jewel.row_num][jewel.col_num - 1].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num][jewel.col_num - 2].jewel_type == jewel.jewel_type):
                    return False
        if jewel.row_num < constants.HEIGHT / constants.JEWEL_HEIGHT - 2:
            if isinstance(self.board[jewel.row_num + 1][jewel.col_num], Jewel) and isinstance(
                    self.board[jewel.row_num + 2][jewel.col_num], Jewel):
                if (self.board[jewel.row_num + 1][jewel.col_num].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num + 2][jewel.col_num].jewel_type == jewel.jewel_type):
                    return False
        if jewel.col_num < constants.WIDTH / constants.JEWEL_WIDTH - 2:
            if isinstance(self.board[jewel.row_num][jewel.col_num + 1], Jewel) and isinstance(
                    self.board[jewel.row_num][jewel.col_num + 2], Jewel):
                if (self.board[jewel.row_num][jewel.col_num + 1].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num][jewel.col_num + 2].jewel_type == jewel.jewel_type):
                    return False

        if 0 < jewel.row_num < constants.HEIGHT / constants.JEWEL_HEIGHT - 1:
            if isinstance(self.board[jewel.row_num - 1][jewel.col_num], Jewel) and isinstance(
                    self.board[jewel.row_num + 1][jewel.col_num], Jewel):
                if (self.board[jewel.row_num - 1][jewel.col_num].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num + 1][jewel.col_num].jewel_type == jewel.jewel_type):
                    return False

        if 0 < jewel.col_num < constants.WIDTH / constants.JEWEL_WIDTH - 1:
            if isinstance(self.board[jewel.row_num][jewel.col_num - 1], Jewel) and isinstance(
                    self.board[jewel.row_num][jewel.col_num + 1], Jewel):
                if (self.board[jewel.row_num][jewel.col_num - 1].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num][jewel.col_num + 1].jewel_type == jewel.jewel_type):
                    return False
        return True

    def match_three_start_check(self, jewel: Jewel):
        if jewel.row_num >= 2:
            if isinstance(self.board[jewel.row_num - 1][jewel.col_num], Jewel) and isinstance(
                    self.board[jewel.row_num - 2][jewel.col_num], Jewel):
                if (self.board[jewel.row_num - 1][jewel.col_num].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num - 2][jewel.col_num].jewel_type == jewel.jewel_type):
                    return False
        if jewel.col_num >= 2:
            if isinstance(self.board[jewel.row_num][jewel.col_num - 1], Jewel) and isinstance(
                    self.board[jewel.row_num][jewel.col_num - 2], Jewel):
                if (self.board[jewel.row_num][jewel.col_num - 1].jewel_type == jewel.jewel_type and
                        self.board[jewel.row_num][jewel.col_num - 2].jewel_type == jewel.jewel_type):
                    return False
        return True

    def find_matches(self, jewel: Jewel, matches: set, directions: list, direction: Direction = Direction.START):

        matches.add(jewel)
        directions.append(direction)

        if jewel.row_num > 0:
            neighbor: Jewel = self.board[jewel.row_num - 1][jewel.col_num]
            if isinstance(neighbor, Jewel):
                if jewel.jewel_type == neighbor.jewel_type and neighbor not in matches:
                    result: dict = self.find_matches(neighbor, matches, directions, Direction.UP)
                    matches.update(result["matches"])

        if jewel.row_num < constants.HEIGHT / constants.JEWEL_HEIGHT - 1:
            neighbor = self.board[jewel.row_num + 1][jewel.col_num]
            if isinstance(neighbor, Jewel):
                if jewel.jewel_type == neighbor.jewel_type and neighbor not in matches:
                    result: dict = self.find_matches(neighbor, matches, directions, Direction.DOWN)
                    matches.update(result["matches"])

        if jewel.col_num > 0:
            neighbor = self.board[jewel.row_num][jewel.col_num - 1]
            if isinstance(neighbor, Jewel):
                if jewel.jewel_type == neighbor.jewel_type and neighbor not in matches:
                    result: dict = self.find_matches(neighbor, matches, directions, Direction.LEFT)
                    matches.update(result["matches"])

        if jewel.col_num < constants.WIDTH / constants.JEWEL_WIDTH - 1:
            neighbor = self.board[jewel.row_num][jewel.col_num + 1]
            if isinstance(neighbor, Jewel):
                if jewel.jewel_type == neighbor.jewel_type and neighbor not in matches:
                    result: dict = self.find_matches(neighbor, matches, directions, Direction.RIGHT)
                    matches.update(result["matches"])

        if direction != Direction.START:
            directions.append(Direction.STEP_BACK)
        return {"matches": matches, "directions": directions}

    def match_three(self, jewel: Jewel):
        matches: set = self.find_matches(jewel, set(), list())["matches"]
        directions: list = self.find_matches(jewel, set(), list())["directions"]
        exceptions = [[Direction.START, Direction.DOWN, Direction.RIGHT, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.UP, Direction.STEP_BACK, Direction.RIGHT, Direction.STEP_BACK],
                      [Direction.START, Direction.LEFT, Direction.UP, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.DOWN, Direction.LEFT, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.UP, Direction.STEP_BACK, Direction.LEFT, Direction.STEP_BACK],
                      [Direction.START, Direction.RIGHT, Direction.UP, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.LEFT, Direction.DOWN, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.DOWN, Direction.STEP_BACK, Direction.RIGHT, Direction.STEP_BACK],
                      [Direction.START, Direction.UP, Direction.RIGHT, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.RIGHT, Direction.DOWN, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.DOWN, Direction.STEP_BACK, Direction.LEFT, Direction.STEP_BACK],
                      [Direction.START, Direction.UP, Direction.LEFT, Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.DOWN, Direction.RIGHT, Direction.UP, Direction.STEP_BACK,
                       Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.DOWN, Direction.LEFT, Direction.UP, Direction.STEP_BACK,
                       Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.UP, Direction.LEFT, Direction.DOWN, Direction.STEP_BACK,
                       Direction.STEP_BACK, Direction.STEP_BACK],
                      [Direction.START, Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.STEP_BACK,
                       Direction.STEP_BACK, Direction.STEP_BACK]]
        print(directions)
        if len(matches) >= 3:
            if directions in exceptions:
                return set()
            return matches
        else:
            return set()

    def bomb_jewel_activate(self, jewel: Jewel):
        deleted_jewels: set = {jewel, }
        for offset in ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)):
            new_row_num: int = jewel.row_num + offset[0]
            new_col_num: int = jewel.col_num + offset[1]
            if (0 <= new_row_num < constants.HEIGHT // constants.JEWEL_HEIGHT and
                    0 <= new_col_num < constants.WIDTH // constants.JEWEL_WIDTH and
                    not isinstance(self.board[new_row_num][new_col_num], Block)):
                deleted_jewels.add(self.board[new_row_num][new_col_num])

        return deleted_jewels

    def lightning_jewel_activate(self, jewel: Jewel):
        deleted_jewels: set = {jewel, }
        i = 1
        while jewel.row_num + i < constants.HEIGHT // constants.JEWEL_HEIGHT:
            if isinstance(self.board[jewel.row_num + i][jewel.col_num], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num + i][jewel.col_num])
            i += 1
        i = 1
        while jewel.row_num - i >= 0:
            if isinstance(self.board[jewel.row_num - i][jewel.col_num], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num - i][jewel.col_num])
            i += 1

        i = 1
        while jewel.col_num + i < constants.WIDTH // constants.JEWEL_WIDTH:
            if isinstance(self.board[jewel.row_num][jewel.col_num + i], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num][jewel.col_num + i])
            i += 1

        i = 1
        while jewel.col_num - i >= 0:
            if isinstance(self.board[jewel.row_num][jewel.col_num - i], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num][jewel.col_num - i])
            i += 1

        return deleted_jewels

    def flame_jewel_activate(self, jewel: Jewel):
        deleted_jewels: set = {jewel, }
        i = 1
        while (jewel.row_num + i < constants.HEIGHT // constants.JEWEL_HEIGHT and
               jewel.col_num + i < constants.WIDTH // constants.JEWEL_WIDTH):
            if isinstance(self.board[jewel.row_num + i][jewel.col_num + i], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num + i][jewel.col_num + i])
            i += 1

        i = 1
        while jewel.row_num - i >= 0 and jewel.col_num - i >= 0:
            if isinstance(self.board[jewel.row_num - i][jewel.col_num - i], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num - i][jewel.col_num - i])
            i += 1

        i = 1
        while jewel.col_num + i < constants.WIDTH // constants.JEWEL_WIDTH and jewel.row_num - i >= 0:
            if isinstance(self.board[jewel.row_num - i][jewel.col_num + i], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num - i][jewel.col_num + i])
            i += 1

        i = 1
        while jewel.col_num - i >= 0 and jewel.row_num + i < constants.HEIGHT // constants.JEWEL_HEIGHT:
            if isinstance(self.board[jewel.row_num + i][jewel.col_num - i], Block):
                break
            deleted_jewels.add(self.board[jewel.row_num + i][jewel.col_num - i])
            i += 1

        return deleted_jewels

    def run(self):
        effects_position: list = []
        running: bool = True
        pygame.mixer.music.load("../resources/sounds/game_music.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.6)
        while running:
            if self.time is not None and self.current_time >= self.time:
                pygame.mixer.music.stop()
                result_window: ResultWindow = ResultWindow(self.score, self.moves, self.current_time)
                result_window.run()
                pygame.display.update()
                running: bool = False

            if self.points is not None and self.score >= self.points:
                pygame.mixer.music.stop()
                result_window: ResultWindow = ResultWindow(self.score, self.moves, self.current_time)
                result_window.run()
                pygame.display.update()
                running: bool = False

            matches: set = set()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running: bool = False

                if self.clicked_jewel is None and event.type == MOUSEBUTTONDOWN:

                    for row in self.board:
                        for jewel in row:
                            if jewel.rect.collidepoint(event.pos):
                                self.clicked_jewel: Jewel = jewel

                                self.coord_x: int = event.pos[0]
                                self.coord_y: int = event.pos[1]

                if self.clicked_jewel is not None and event.type == MOUSEMOTION:

                    distance_x: int = abs(self.coord_x - event.pos[0])
                    distance_y: int = abs(self.coord_y - event.pos[1])

                    if self.swapped_jewel is not None:
                        self.swapped_jewel.snap()

                    if distance_x > distance_y and self.coord_x > event.pos[0]:
                        direction: Direction = Direction.LEFT
                    elif distance_x > distance_y and self.coord_x < event.pos[0]:
                        direction: Direction = Direction.RIGHT
                    elif distance_x < distance_y and self.coord_y > event.pos[1]:
                        direction: Direction = Direction.UP
                    else:
                        direction: Direction = Direction.DOWN

                    if direction in [Direction.LEFT, Direction.RIGHT]:
                        self.clicked_jewel.snap_row()
                    else:
                        self.clicked_jewel.snap_col()

                    if direction == Direction.LEFT and self.clicked_jewel.col_num > 0:

                        self.swapped_jewel: Jewel | None = self.board[self.clicked_jewel.row_num][
                            self.clicked_jewel.col_num - 1]
                        if isinstance(self.swapped_jewel, Block):
                            self.swapped_jewel: Jewel | None = None
                            continue

                        self.clicked_jewel.rect.left = self.clicked_jewel.col_num * constants.JEWEL_WIDTH - distance_x
                        self.swapped_jewel.rect.left = self.swapped_jewel.col_num * constants.JEWEL_WIDTH + distance_x

                        if self.clicked_jewel.rect.left <= self.swapped_jewel.col_num * constants.JEWEL_WIDTH + constants.JEWEL_WIDTH / 4:
                            self.swap(self.clicked_jewel, self.swapped_jewel)
                            matches.update(self.match_three(self.clicked_jewel))
                            matches.update(self.match_three(self.swapped_jewel))
                            self.swap_sound.play()
                            self.moves += 1
                            self.clicked_jewel: Jewel | None = None
                            self.swapped_jewel: Jewel | None = None

                    if direction == Direction.RIGHT and self.clicked_jewel.col_num < constants.WIDTH / constants.JEWEL_WIDTH - 1:

                        self.swapped_jewel: Jewel | None = self.board[self.clicked_jewel.row_num][
                            self.clicked_jewel.col_num + 1]
                        if isinstance(self.swapped_jewel, Block):
                            self.swapped_jewel = None
                            continue

                        self.clicked_jewel.rect.left = self.clicked_jewel.col_num * constants.JEWEL_WIDTH + distance_x
                        self.swapped_jewel.rect.left = self.swapped_jewel.col_num * constants.JEWEL_WIDTH - distance_x

                        if self.clicked_jewel.rect.left >= self.swapped_jewel.col_num * constants.JEWEL_WIDTH - constants.JEWEL_WIDTH / 4:
                            self.swap(self.clicked_jewel, self.swapped_jewel)
                            matches.update(self.match_three(self.clicked_jewel))
                            matches.update(self.match_three(self.swapped_jewel))
                            self.swap_sound.play()
                            self.moves += 1
                            self.clicked_jewel: Jewel | None = None
                            self.swapped_jewel: Jewel | None = None

                    if direction == Direction.UP and self.clicked_jewel.row_num > 0:

                        self.swapped_jewel = self.board[self.clicked_jewel.row_num - 1][self.clicked_jewel.col_num]
                        if isinstance(self.swapped_jewel, Block):
                            self.swapped_jewel: Jewel | None = None
                            continue

                        self.clicked_jewel.rect.top = self.clicked_jewel.row_num * constants.JEWEL_HEIGHT - distance_y
                        self.swapped_jewel.rect.top = self.swapped_jewel.row_num * constants.JEWEL_HEIGHT + distance_y

                        if self.clicked_jewel.rect.top <= self.swapped_jewel.row_num * constants.JEWEL_HEIGHT + constants.JEWEL_WIDTH / 4:
                            self.swap(self.clicked_jewel, self.swapped_jewel)
                            matches.update(self.match_three(self.clicked_jewel))
                            matches.update(self.match_three(self.swapped_jewel))
                            self.swap_sound.play()
                            self.moves += 1
                            self.clicked_jewel: Jewel | None = None
                            self.swapped_jewel: Jewel | None = None

                    if direction == Direction.DOWN and self.clicked_jewel.row_num < constants.HEIGHT / constants.JEWEL_HEIGHT - 1:

                        self.swapped_jewel: Jewel | None = self.board[self.clicked_jewel.row_num + 1][
                            self.clicked_jewel.col_num]
                        if isinstance(self.swapped_jewel, Block):
                            self.swapped_jewel = None
                            continue

                        self.clicked_jewel.rect.top = self.clicked_jewel.row_num * constants.JEWEL_HEIGHT + distance_y
                        self.swapped_jewel.rect.top = self.swapped_jewel.row_num * constants.JEWEL_HEIGHT - distance_y

                        if self.clicked_jewel.rect.top >= self.swapped_jewel.row_num * constants.JEWEL_HEIGHT - constants.JEWEL_WIDTH / 4:
                            self.swap(self.clicked_jewel, self.swapped_jewel)
                            matches.update(self.match_three(self.clicked_jewel))
                            matches.update(self.match_three(self.swapped_jewel))
                            self.swap_sound.play()
                            self.moves += 1
                            self.clicked_jewel: Jewel | None = None
                            self.swapped_jewel: Jewel | None = None

                if self.clicked_jewel is not None and event.type == MOUSEBUTTONUP:
                    self.swap_sound.play()

                    self.clicked_jewel.snap()
                    self.clicked_jewel: Jewel | None = None
                    if self.swapped_jewel is not None:
                        self.swapped_jewel.snap()
                        self.swapped_jewel: Jewel | None = None

            self.draw()
            pygame.display.update()

            if len(matches) >= 3:

                self.score += len(matches)
                self.disappear_sound.play()

                while len(matches) > 0:
                    self.clock.tick(100)

                    for jewel in matches:
                        helper.decrease_jewel_size(jewel)

                    for row_num in range(len(self.board)):
                        for col_num in range(len(self.board[row_num])):
                            jewel: Jewel = self.board[row_num][col_num]
                            if jewel.image.get_width() <= 0 or jewel.image.get_height() <= 0:
                                if jewel.effect.value != EffectType.NONE.value:
                                    effects_position.append((jewel.effect, row_num, col_num))
                                matches.remove(jewel)

                                jewel_types: list = list(constants.JEWEL_NAMES)
                                jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types), constants.EFFECT_NAMES,
                                                     constants.EFFECT_WEIGHTS)
                                while not self.match_three_check(jewel):
                                    jewel_types.remove(jewel.jewel_type)
                                    jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                         constants.EFFECT_NAMES,
                                                         constants.EFFECT_WEIGHTS)
                                self.board[row_num][col_num] = jewel

                    self.draw()
                    pygame.display.update()

                print(effects_position)
                for effect in effects_position:
                    if effect[0].value == EffectType.BOMB.value:
                        deleted_jewels: set = self.bomb_jewel_activate(self.board[effect[1]][effect[2]])
                        self.score += len(deleted_jewels)
                        while len(deleted_jewels) > 0:
                            self.clock.tick(100)

                            for jewel in deleted_jewels:
                                helper.decrease_jewel_size(jewel)

                            for row_num in range(len(self.board)):
                                for col_num in range(len(self.board[row_num])):
                                    jewel: Jewel = self.board[row_num][col_num]
                                    if jewel.image.get_width() <= 0 or jewel.image.get_height() <= 0:
                                        deleted_jewels.remove(jewel)

                                        jewel_types: list = list(constants.JEWEL_NAMES)
                                        jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                             constants.EFFECT_NAMES, constants.EFFECT_WEIGHTS)
                                        while not self.match_three_check(jewel):
                                            jewel_types.remove(jewel.jewel_type)
                                            jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                                 constants.EFFECT_NAMES,
                                                                 constants.EFFECT_WEIGHTS)
                                        self.board[row_num][col_num] = jewel

                            self.draw()
                            pygame.display.update()

                    if effect[0].value == EffectType.FLAME.value:
                        deleted_jewels = self.flame_jewel_activate(self.board[effect[1]][effect[2]])
                        self.score += len(deleted_jewels)
                        while len(deleted_jewels) > 0:
                            self.clock.tick(100)

                            for jewel in deleted_jewels:
                                helper.decrease_jewel_size(jewel)

                            for row_num in range(len(self.board)):
                                for col_num in range(len(self.board[row_num])):
                                    jewel = self.board[row_num][col_num]
                                    if jewel.image.get_width() <= 0 or jewel.image.get_height() <= 0:
                                        deleted_jewels.remove(jewel)

                                        jewel_types: list = list(constants.JEWEL_NAMES)
                                        jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                             constants.EFFECT_NAMES, constants.EFFECT_WEIGHTS)
                                        while not self.match_three_check(jewel):
                                            jewel_types.remove(jewel.jewel_type)
                                            jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                                 constants.EFFECT_NAMES,
                                                                 constants.EFFECT_WEIGHTS)
                                        self.board[row_num][col_num] = jewel

                            self.draw()
                            pygame.display.update()

                    if effect[0].value == EffectType.LIGHTNING.value:
                        deleted_jewels = self.lightning_jewel_activate(self.board[effect[1]][effect[2]])
                        self.score += len(deleted_jewels)
                        while len(deleted_jewels) > 0:
                            self.clock.tick(100)

                            for jewel in deleted_jewels:
                                helper.decrease_jewel_size(jewel)

                            for row_num in range(len(self.board)):
                                for col_num in range(len(self.board[row_num])):
                                    jewel: Jewel = self.board[row_num][col_num]
                                    if jewel.image.get_width() <= 0 or jewel.image.get_height() <= 0:
                                        deleted_jewels.remove(jewel)

                                        jewel_types: list = list(constants.JEWEL_NAMES)
                                        jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                             constants.EFFECT_NAMES, constants.EFFECT_WEIGHTS)
                                        while not self.match_three_check(jewel):
                                            jewel_types.remove(jewel.jewel_type)
                                            jewel: Jewel = Jewel(self.screen, row_num, col_num, tuple(jewel_types),
                                                                 constants.EFFECT_NAMES,
                                                                 constants.EFFECT_WEIGHTS)
                                        self.board[row_num][col_num] = jewel

                            self.draw()
                            pygame.display.update()
                effects_position.clear()
            self.frame_count += 1

        pygame.quit()
