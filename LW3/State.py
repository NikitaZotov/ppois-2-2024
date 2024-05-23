import random
from typing import List

import pygame

from Player import Player
from Shoot import Shoot
from WaveManager import WaveManager
from Weapon import Pistol, AK47, Deagle, Uzi

WIDTH = 800
HEIGHT = 600


class State:
    def __init__(self):
        self.player = Player(WIDTH / 2, HEIGHT / 2)
        self.is_alive = True

        self.is_menu_open = True
        self.is_leaderboard_open = False
        self.is_help_menu_open = False
        self.is_new_record = False

        self.running = True

        self.enemies = []
        self.dead_enemies = []
        self.dead_enemies_max_number = 5
        self.life_time = 0
        self.current_wave_index = 0
        self.wave_list = WaveManager.load_waves_from_file("waves.json")
        self.current_wave = self.wave_list[0]
        self.score = 0
        self.weapon_sound = pygame.mixer.Sound("sounds/pistol_sound.mp3")
        self.music = pygame.mixer.Sound("sounds/menu_sound.mp3")
        self.weapon_sound.set_volume(0.5)
        self.all_weapon = [Pistol(), AK47(), Deagle(), Uzi()]
        self.laying_weapon = []
        self.shoots: List[Shoot] = []

        # events
        self.time_event = pygame.USEREVENT + 1
        self.wave_event = pygame.USEREVENT + 2
        self.weapon_event = pygame.USEREVENT + 3

        # spawn events

        self.bat_spawn_event = pygame.USEREVENT + 4
        self.skeleton_spawn_event = pygame.USEREVENT + 5
        self.ghost_spawn_event = pygame.USEREVENT + 6
        self.werewolf_spawn_event = pygame.USEREVENT + 7
        self.zombie_spawn_event = pygame.USEREVENT + 8

        # ativate user events
        pygame.time.set_timer(self.time_event, 1000)
        pygame.time.set_timer(self.weapon_event, 7000)
        pygame.time.set_timer(self.wave_event, 30000)

        self.change_the_spawning_time(self.current_wave)

    def reset_game(self):
        self.player = Player(WIDTH / 2, HEIGHT / 2)
        self.is_alive = True
        self.enemies = []
        self.life_time = 0
        self.current_wave_index = 0
        self.current_wave = self.wave_list[0]
        self.shoots = []
        self.laying_weapon = []
        self.score = 0
        self.weapon_sound = pygame.mixer.Sound("sounds/pistol_sound.mp3")
        self.dead_enemies = []
        self.change_the_spawning_time(self.current_wave)

    def update_life_time(self, time):
        self.life_time = time

    def update_wave(self):
        if self.current_wave_index < 20:
            self.current_wave_index += 1
            self.current_wave = self.wave_list[self.current_wave_index]
            self.change_the_spawning_time(self.current_wave)

    def change_the_spawning_time(self, current_wave):
        pygame.time.set_timer(self.bat_spawn_event, current_wave.bat_spawn_time)
        pygame.time.set_timer(self.skeleton_spawn_event, current_wave.skeleton_spawn_time)
        pygame.time.set_timer(self.ghost_spawn_event, current_wave.ghost_spawn_time)
        pygame.time.set_timer(self.werewolf_spawn_event, current_wave.werewolf_spawn_time)
        pygame.time.set_timer(self.zombie_spawn_event, current_wave.zombie_spawn_time)

    def spawn_weapon(self, x, y):
        random_weapon_index = random.randrange(0, 4, 1)
        self.laying_weapon.append((self.all_weapon[random_weapon_index], x, y))

    def remove_shoot(self, shoot):
        self.shoots.remove(shoot)

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
