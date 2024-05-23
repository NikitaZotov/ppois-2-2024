import random

import pygame
import math

from Enemy import Bat, Skeleton, Ghost, Werewolf, Zombie
from LeaderboardManager import LeaderboardManager
from Player import Player
from State import State
from Util import Util

WIDTH = 800
HEIGHT = 600


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.alpha = 255
        self.leaderboard_manager = LeaderboardManager()
        self.leaderboard_manager.read_leaderboard_from_file("leaderboard.json")
        self.name = ""

    def start_game(self):
        pygame.init()
        pygame.mixer.init()
        menu_sound = pygame.mixer.Sound("sounds/menu_sound.mp3")
        game_sound = pygame.mixer.Sound("sounds/game_sound.mp3")
        pygame.display.set_caption("Crimsonland")
        self.font = pygame.font.Font(None, 36)

        background_image = pygame.image.load("sprites/background.png").convert()
        self.state = State()
        while self.state.running:
            pygame.display.update()
            self.clock.tick(60)
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False
            if self.state.is_menu_open:
                self.display_menu()
                self.set_music(menu_sound)
                continue
            self.set_music(game_sound)
            x, y = pygame.mouse.get_pos()
            self.state.player.update_angle(x, y)
            # self.resolve_game_actions()
            # for event in pygame.event.get():
            #     if event.type == pygame.MOUSEMOTION:
            #         x, y = event.pos
            #         self.state.player.update_angle(x, y)
            #         self.state.player.update_angle(x, y)

            # x, y = pygame.mouse.get_pos()
            # print(x, y)
            # self.state.player.update_angle(x, y)
            if self.state.is_alive:
                self.resolve_game_actions()
                self.resolve_player_actions()
            # elif self.state.is_new_record:
            #     self.resolve_new_record_actions()

            self.resolve_shots_actions()
            self.state.player.decrement_cooldown()
            self.resolve_enemies_movement()

            self.screen.fill((0, 0, 0))
            self.screen.blit(background_image, (0, 0))
            if self.state.is_new_record:
                self.resolve_new_record_actions()
            self.rotate_and_draw_for_player()
            self.draw_laying_weapons()
            self.draw_shoots()
            self.draw_wave_start_message(self.state.current_wave_index)
            self.draw_player_health()
            self.draw_score(self.state.score)
            self.rotate_and_draw_for_enemies()
            self.draw_dead_enemies()

            self.resolve_enemy_engagement()
            self.resolve_weapon_raising()

        pygame.quit()

    def resolve_player_actions(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            shoot = self.state.player.try_shoot()
            if shoot is not None:
                self.state.shoots.append(shoot)
                self.state.weapon_sound.play()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.state.player.move_left()
        if keys[pygame.K_d]:
            self.state.player.move_right()
        if keys[pygame.K_w]:
            self.state.player.move_up()
        if keys[pygame.K_s]:
            self.state.player.move_down()

    def rotate_and_draw_for_player(self):
        rotated_entity_image = pygame.transform.rotate(self.state.player.sprite,
                                                       -self.state.player.turn_angle * 180 / math.pi)
        entity_rect = rotated_entity_image.get_rect(
            center=self.state.player.sprite.get_rect(center=(self.state.player.x, self.state.player.y)).center)
        self.screen.blit(rotated_entity_image, entity_rect)

    def display_menu(self):
        self.screen.blit(pygame.image.load("sprites/main_page_survivor.jpg").convert(), (0, 0))
        self.react_to_menu_events()
        self.choose_what_to_draw()

    def react_to_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state.is_help_menu_open or self.state.is_leaderboard_open:
                        self.state.is_leaderboard_open = False
                        self.state.is_help_menu_open = False
                    else:
                        self.state.running = False
                        self.state.is_menu_open = False
                elif event.key == pygame.K_SPACE:
                    self.state.is_menu_open = False
                    self.state.is_help_menu_open = False
                    self.state.is_leaderboard_open = False
                elif event.key == pygame.K_TAB:
                    self.state.is_leaderboard_open = True
                    self.state.is_help_menu_open = False
                elif event.key == pygame.K_h:
                    self.state.is_help_menu_open = True
                    self.state.is_leaderboard_open = False

    def choose_what_to_draw(self):
        if self.state.is_help_menu_open:
            self.draw_help_menu()
        elif self.state.is_leaderboard_open:
            self.draw_leaderbord_menu()
        else:
            self.draw_menu()

    def draw_help_menu(self):
        # Очищаем экран
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.image.load("sprites/help_menu.png").convert(), (0, 0))
        # Настройки текста
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        line_spacing = 40

        # Информация о игре
        help_text = [
            "Добро пожаловать в игру!",
            "",
            "Описание игры:",
            "Цель игры - достичь победы!",
            "Управление:",
            "WASD - движение персонажа",
            "ЛКМ - стрельба",
            "ESC - выход из игры",
            "TAB - открыть таблицу лидеров",
            "H - открыть меню помощи",
            "",
            "Нажмите ESC, чтобы вернуться в меню"
        ]

        # Отрисовка текста на экране
        y = 100
        for line in help_text:
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += line_spacing

        # Обновление экрана
        pygame.display.flip()

    def draw_leaderbord_menu(self):
        self.leaderboard_manager = LeaderboardManager()
        self.leaderboard_manager.read_leaderboard_from_file("leaderboard.json")
        # Очищаем экран
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.image.load("sprites/help_menu.png").convert(), (0, 0))
        # Настройки текста
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        line_spacing = 40

        # Заголовок
        title_text = "Leaderboard"
        title_surface = font.render(title_text, True, text_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Отрисовка данных лидерборда
        y = 100
        for index, record in enumerate(self.leaderboard_manager.leaderboard, start=1):
            name = record["name"]
            score = record["score"]
            line_text = f"{index}. {name}: {score}"
            line_surface = font.render(line_text, True, text_color)
            line_rect = line_surface.get_rect(center=(self.screen.get_width() // 2, y))
            self.screen.blit(line_surface, line_rect)
            y += line_spacing

        # Обновление экрана
        pygame.display.flip()

    def draw_menu(self):
        # Очищаем экран
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.image.load("sprites/main_page_survivor.jpg").convert(), (0, 0))
        # Настройки текста
        font = pygame.font.Font(None, 36)
        text_color = (208, 128, 4)

        # Пункты меню
        menu_items = ["Начать игру(Space)", "Таблица лидеров(Tab)", "Помощь(H)", "Выход(Ess)"]
        x = 100  # Начальная координата X
        y = 200
        for item in menu_items:
            item_surface = font.render(item, True, text_color)
            item_rect = item_surface.get_rect(topleft=(x, y))
            self.screen.blit(item_surface, item_rect)
            y += 50

        # Обновление экрана
        pygame.display.flip()

    def resolve_game_actions(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state.is_menu_open = True
                self.state.reset_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.state.reset_game()
                continue
            elif self.state.is_alive:
                if event.type == self.state.time_event:
                    self.state.update_life_time(self.state.life_time + 1)
                elif event.type == self.state.wave_event:
                    self.alpha = 255
                    self.state.update_wave()
                elif event.type == self.state.weapon_event:
                    if self.state.laying_weapon:
                        self.state.laying_weapon = []
                    x = random.randrange(WIDTH)
                    y = random.randrange(HEIGHT)
                    self.state.spawn_weapon(x, y)
                else:
                    self.enemy_actions(event)

    def enemy_actions(self, event):
        x, y = Util.get_spawn_coordinates(WIDTH, HEIGHT)
        if event.type == self.state.bat_spawn_event:
            self.state.add_enemy(Bat(x, y))
        elif event.type == self.state.skeleton_spawn_event:
            self.state.add_enemy(Skeleton(x, y))
        elif event.type == self.state.ghost_spawn_event:
            self.state.add_enemy(Ghost(x, y))
        elif event.type == self.state.werewolf_spawn_event:
            self.state.add_enemy(Werewolf(x, y))
        elif event.type == self.state.zombie_spawn_event:
            self.state.add_enemy(Zombie(x, y))

    def draw_laying_weapons(self):
        for weapon_info in self.state.laying_weapon:
            weapon, x, y = weapon_info  # weapon - объект оружия, x и y - координаты
            # laying_weapon_sprite = pygame.image.load(weapon.laying_sprite)
            # resized_weapon_image = pygame.transform.scale(laying_weapon_sprite, (
            #     20, 20)).convert_alpha()  # Изменяем размер изображения
            self.screen.blit(weapon.laying_sprite, (x, y))  # Отрисовка изображения оружия по указанным координатам

    def resolve_shots_actions(self):
        for shoot in self.state.shoots.copy():
            delta_x = shoot.speed * math.cos(shoot.turn_angle)
            delta_y = shoot.speed * math.sin(shoot.turn_angle)
            shoot.set_coordinates(shoot.x + delta_x, shoot.y + delta_y)
            if shoot.x < 0 or shoot.y < 0 or shoot.x > WIDTH or shoot.y > HEIGHT:
                self.state.remove_shoot(shoot)

    def draw_shoots(self):
        for shoot in self.state.shoots:
            shoot_image = pygame.image.load(shoot.sprite).convert_alpha()
            rotated_entity_image = pygame.transform.rotate(shoot_image, -shoot.turn_angle * 180 / math.pi)
            entity_rect = rotated_entity_image.get_rect(
                center=shoot_image.get_rect(center=(shoot.x, shoot.y)).center)
            self.screen.blit(rotated_entity_image, entity_rect)  # Отрисовка изображения оружия по указанным координатам

    def resolve_enemies_movement(self):
        for enemy in self.state.enemies:
            enemy.update_angle(self.state.player.x, self.state.player.y)
            delta_x, delta_y = enemy.get_shifted_coordinates()
            enemy.update_coordinates(enemy.x + delta_x, enemy.y + delta_y)

    def rotate_and_draw_for_enemies(self):
        for enemy in self.state.enemies:
            # enemy_image = pygame.image.load(enemy.sprite)
            # resized_enemy_image = pygame.transform.scale(enemy_image, (
            #     34, 34)).convert_alpha()
            rotated_enemy_image = pygame.transform.rotate(enemy.sprite,
                                                          -enemy.turn_angle * 180 / math.pi)
            enemy_rect = rotated_enemy_image.get_rect(
                center=self.state.player.sprite.get_rect(center=(enemy.x, enemy.y)).center)
            self.screen.blit(rotated_enemy_image, enemy_rect)

    def resolve_enemy_engagement(self):
        for enemy in self.state.enemies.copy():
            if Util.if_the_enemy_is_near(self.state.player, enemy) and self.state.is_alive:
                self.state.player.current_health -= 1
                if self.state.player.current_health <= 29:
                    self.state.is_alive = False

                    if self.leaderboard_manager.leaderboard[0]["score"] < self.state.score:
                        self.state.is_new_record = True
                    else:
                        self.state.is_menu_open = True
                        self.state.reset_game()

            for shoot in self.state.shoots.copy():
                if Util.is_point_in_square(shoot.x, shoot.y, enemy):
                    enemy.take_the_damage(shoot.damage)
                    if enemy.current_health < 0:
                        self.state.enemies.remove(enemy)
                        self.state.score += 100
                        if len(self.state.dead_enemies) == self.state.dead_enemies_max_number:
                            self.state.dead_enemies.remove(self.state.dead_enemies[0])
                        self.state.dead_enemies.append(enemy)
                    else:
                        self.state.shoots.remove(shoot)

    def resolve_weapon_raising(self):
        for weapon in self.state.laying_weapon:
            if Util.is_point_in_square(weapon[1], weapon[2], self.state.player):
                self.state.player.current_weapon = weapon[0]
                self.state.weapon_sound = pygame.mixer.Sound(self.state.player.current_weapon.sound)
                self.state.weapon_sound.set_volume(0.5)
                # self.state.player.sprite = pygame.image.load(self.state.player.current_weapon.sprite)
                # self.state.player.sprite = pygame.transform.scale(self.state.player.sprite, (
                #     35, 35)).convert_alpha()

                self.state.player.sprite = self.state.player.current_weapon.sprite
                self.state.laying_weapon = []

    def draw_wave_start_message(self, wave_number):
        message = f"Wave: {wave_number + 1}"  # Форматируем сообщение о номере волны
        text_surface = self.font.render(message, True, (255, 255, 255))  # Создаем поверхность текста
        text_rect = text_surface.get_rect(topright=(780, 20))  # Получаем прямоугольник для позиционирования текста
        self.screen.blit(text_surface, text_rect)  # Отрисовываем текст на экране

    def draw_player_health(self):
        health_message = f"HP: {int(self.state.player.current_health / 30)}"  # Форматируем сообщение о здоровье игрока
        health_surface = self.font.render(health_message, True, (255, 255, 255))  # Создаем поверхность текста
        health_rect = health_surface.get_rect(topleft=(600, 20))  # Получаем прямоугольник для позиционирования текста
        self.screen.blit(health_surface, health_rect)  # Отрисовываем текст на экране

    def draw_score(self, score):
        score_message = f"Score: {score}"  # Формируем сообщение о текущем счете
        score_surface = self.font.render(score_message, True, (255, 255, 255))  # Создаем поверхность текста
        score_rect = score_surface.get_rect(
            topright=(500, 20))  # Получаем прямоугольник для позиционирования текста
        self.screen.blit(score_surface, score_rect)  # Отрисовываем текст на экране

    def resolve_new_record_actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.leaderboard_manager.add_record_to_leaderboard(self.name, self.state.score)
                    self.leaderboard_manager.write_leaderboard_to_file("leaderboard.json")
                    self.state.is_menu_open = True
                    self.state.is_new_record = False
                    self.state.reset_game()
                    self.name = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    if len(self.name) < 24:
                        self.name += event.unicode
        self.display_new_record_message(self.name)

    def display_new_record_message(self, input_text):
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        new_record_text = "Новый рекорд!!!"
        nickname_text = f"Введите ник: {input_text}"
        new_record_surface = font.render(new_record_text, True, text_color)
        nickname_surface = font.render(nickname_text, True, text_color)
        new_record_rect = new_record_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        nickname_rect = nickname_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(new_record_surface, new_record_rect)
        self.screen.blit(nickname_surface, nickname_rect)

    def draw_dead_enemies(self):
        for enemy in self.state.dead_enemies:
            # enemy_sprite = pygame.image.load(enemy.dead_sprite)
            # resized_enemy_image = pygame.transform.scale(enemy_sprite, (
            #     34, 34)).convert_alpha()  # Изменяем размер изображения
            self.screen.blit(enemy.dead_sprite, (enemy.x, enemy.y))

    def set_music(self, music):
        if self.state.music != music:
            self.state.music.stop()
            self.state.music = music
            self.state.music.play()


if __name__ == "__main__":
    game = Game()
    game.start_game()
