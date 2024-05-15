import pygame
from random import randint

from View.Enemys.BaseEnemy import BaseEnemy
from View.obstacle import Block
from Controller.ConfigurationManager import ConfigurationManager
from View.Enemys.BallAlien import BallAlien
from View.Enemys.RandomBallAlien import RandomBallAlien
from View.Enemys.extra import Extra
from View.Enemys.Ram import Ram
from View.Enemys.Boss import Boss
from View.Enemys.Generator import Generator
from View.Enemys.Minion import Minion
import copy
from settings import screen_width,screen_height
import settings as settings

class CharacterGenerator:
    def __init__(self, aliens, blocks, events):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.aliens= aliens
        self.blocks= blocks
        self.events=events
        self.JsonLoader = ConfigurationManager()
        self.last_event_time = pygame.time.get_ticks()
        self.direction=1
        self.extra_spawn_time = 5
        self.miniom_timer= 5
        self.duration=None
        self.background_color = (0, 0, 0)

    def process_wave(self, wave_name):
        alien_matrix_y=100
        wave = settings.waves_dict[wave_name]
        for enemy_data in wave._enemy_dict:
            alien_type = enemy_data["type"]
            if alien_type=="Extra":
                self.create_extra()
                continue
            elif alien_type=="Generator":
                self.create_generator()
                continue
            if "generate_type" in enemy_data:
                generate_type = enemy_data["generate_type"]
                if generate_type == "matrix":
                    rows = enemy_data["rows"]
                    cols = enemy_data["columns"]
                    alien_matrix_y=self.alien_matrix(alien_type=alien_type,rows=rows, cols=cols,y_offset=alien_matrix_y)
                elif generate_type == "spawning":
                    interval =enemy_data["interval"]
                    self.create_alien_in_random_place(alien_type,interval)
                elif generate_type == "center_top":
                    self.create_alien_in_center_top(alien_type)
                    # self.create_alien_in_random_place(alien_type, 20000)
        if wave.obstacle[1]!=0:
            self.create_obstacles(wave.obstacle[0], wave.obstacle[1])
        if  wave.duration!=0:
            self.duration= wave.duration
        if wave.background_color!=None:
            self.background_color=wave.background_color

    def create_alien(self, alien_type, x, y):
        new_alien_data = copy.deepcopy(settings.alien_type_dict[alien_type])
        alien_classes = {
            "BallAlien": BallAlien,
            "RandomBallAlien": RandomBallAlien,
            "Extra": Extra,
            "Ram": Ram,
            "Boss": Boss,
            "Generator": Generator,
            "Minion":Minion
        }
        alien_class = alien_classes.get(alien_type, BaseEnemy)
        return alien_class(x, y, new_alien_data)

    def create_extra(self):
        def create_extra_event():
            self.extra_spawn_time -= 1
            if self.extra_spawn_time <= 0:
                self.aliens.add(self.create_alien("Extra", 0, 0))
                self.extra_spawn_time = randint(200, 400)
        self.events.append(create_extra_event)

    def create_generator(self):
        def create_generator():
            self.extra_spawn_time -= 1
            if self.extra_spawn_time <= 0:
                self.aliens.add(self.create_alien("Generator",randint(50, self.screen_width-50),randint(70, 170)))
                self.extra_spawn_time = randint(500, 800)

        def cretae_minions():
            self.miniom_timer-= 1
            if self.miniom_timer<=0:
                generator_sprites = [sprite for sprite in self.aliens.sprites() if isinstance(sprite, Generator)]
                if generator_sprites:
                    self.aliens.add(self.create_alien("Minion", randint(50, self.screen_width - 50), randint(70, 170)))
                    self.miniom_timer = randint(120, 160)

        self.events.append(create_generator)
        self.events.append(cretae_minions)


    def create_alien_in_random_place(self, alien_type, interval):
        def new_event():
            current_time = pygame.time.get_ticks()
            if current_time - self.last_event_time >= interval:
                new_alien = self.create_alien(alien_type, randint(100 ,self.screen_width-100), randint(50, 200))
                self.aliens.add(new_alien)
                self.last_event_time = current_time

        self.events.append(new_event)

    def create_alien_in_center_top(self, alien_type):
        alien_sprite = self.create_alien(alien_type, x=self.screen_width/2, y=150)
        self.aliens.add(alien_sprite)

    def alien_matrix(self, rows, cols, alien_type,x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x_pos = col_index * x_distance + x_offset
                y_pos = row_index * y_distance + y_offset
                alien_sprite= self.create_alien(alien_type,x=x_pos,y=y_pos)
                self.aliens.add(alien_sprite)
        last_alien_sprite = self.aliens.sprites()[-1]
        last_alien_rect = last_alien_sprite.rect
        self.events.append(self.alien_position_checker)

        return last_alien_rect.bottom +y_distance /5 # Возвращаем нижнюю координату y последнего инопланетянина

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= self.screen_width:
                self.direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def create_obstacle(self,shape, x_start, y_start, offset_x):
        for row_index, row in enumerate(shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacle(self, *offset, shape, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(shape,x_start, y_start, offset_x)

    def create_obstacles(self, shape,obstacle_amount):
        self.block_size = 6
        self.obstacle_amount = obstacle_amount
        self.obstacle_x_positions = [num * (self.screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacle(*self.obstacle_x_positions,shape= shape, x_start=self.screen_width / 15, y_start=480)