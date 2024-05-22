import math
import random

import pygame
import constant
from background import Background
from sound import Sound
from bullet import Bullet
from score import Score
from game_time import Time
from cursor import Cursor
from bird import Bird
from leaderboard import Leaderboard
from restart import Restart

class Game:
    def __init__(self, screen):
        self.scale = 1.0
        self.screen = screen
        self.background = None
        self.sound = Sound()
        self.bullet = Bullet()
        self.score = Score()
        self.time = None
        self.cursor = Cursor()
        self.chickens_group = pygame.sprite.Group()
        self.speed = None
        self.repeat = 0
        self.result = [False,0]
        self.leaderboard = Leaderboard(self.screen)
        self.restart = Restart(self.screen)
        print("I am a game")

    def start_game(self, x=0, y=0):
        self.background = Background(self.screen,x,y)
        self.background.set_game_background()
        self.sound.start_game_music()
        self.time = Time(pygame.time.get_ticks())
        running = True
        flag4 = True
        flag5 = False
        flag_stop = False
        while running:
            self.bullet.time_reload += 2
            self.init_chicken()
            self.speed = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.bullet.fire(self.cursor):
                            print("Fire pliii")
                            self.result = self.cursor.collision_detected(self.screen, pygame.mouse.get_pos(), self.chickens_group)
                            self.score.score += self.result[1]
                            print(self.result[1])
                    if event.button == 3:
                        self.bullet.reload()
                    if event.button == 4 and flag4:
                        flag4 = False
                        flag5 = True
                        self.cursor.set_cursor(2)
                        self.set_scale_of_background(event.button)
                        self.get_start_pos_of_scale()
                        pos_xy = pygame.mouse.get_pos()
                        if pos_xy[0] > 640:
                            pygame.mouse.set_pos(400 + pos_xy[0], pos_xy[1])
                        elif pos_xy[0] < 160:
                            pygame.mouse.set_pos(400 - pos_xy[0], pos_xy[1])
                        else:
                            pygame.mouse.set_pos(400, pos_xy[1])
                        for sprite in self.chickens_group:
                            sprite.scale_images(1.25)
                    if event.button == 5 and flag5:
                        flag4 = True
                        flag5 = False
                        self.cursor.set_cursor(1)
                        self.set_scale_of_background(event.button)
                        self.get_start_pos_background()
                        self.background.y_pos = 0
                        pygame.mouse.set_pos(400, 300)
                        for sprite in self.chickens_group:
                            sprite.scale_images(1)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        self.sound.stop_game_music()
                        running = False
                        return self.score
            self.get_coords_of_shift()
            self.background.print_background(self.background.x_pos,self.background.y_pos)
            self.chickens_group.update(self.speed,self.cursor.cursor_number)
            self.chickens_group.draw(self.screen)
            if not flag_stop:
                self.cursor.print_cursor(self.screen, pygame.mouse.get_pos())
            self.bullet.print_bullet(self.bullet.bullets,self.screen)
            self.score.print_score(self.screen)
            if flag_stop:
                if self.leaderboard.get_lower_result() > 10 or 10 == 0:
                    return self.restart.print_restart(self.score.score)
                    # return self.leaderboard.add_result(self.score.score)  #fsdsds
                else:
                    result = self.restart.print_leader(self.score.score)
                    self.leaderboard.add_result(self.score.score,result[1])
                    return result[0]
                running = False
            if self.time.check_round_time(pygame.time.get_ticks(),self.screen):
                self.sound.stop_game_music()
                self.cursor.hide_cursor(self.screen)
                flag_stop = True
            self.print_score_after_death()
            pygame.display.update()

    def print_score_after_death(self):
        if self.result[0] and self.repeat < 120:
            self.repeat += 1
            self.score.print_score_after_death(self.result[1],self.result[2],self.result[3],self.screen,self.repeat)
        else:
            self.repeat = 0
            self.result[0] = False
    def init_chicken(self):
        value = random.randint(0,1000)
        if value < 2:
            for _ in range(1):
                self.chicken = Bird()
                self.chickens_group.add(self.chicken)
    def set_scale_of_background(self,button):
        if button == 4:
            self.scale = 1.2
        if button == 5:
            self.scale = 1
        self.background.create_scale_background(self.scale)

    def get_start_pos_background(self):
        mouse_pos = pygame.mouse.get_pos()
        offset = 400 - mouse_pos[0]
        self.background.x_pos = int((self.background.x_pos + offset) / 1.4 + 16)
        if self.background.x_pos < -400:
            self.background.x_pos = -400
        if self.background.x_pos > 0:
            self.background.x_pos = 0
    def get_start_pos_of_scale(self):
        mouse_pos = pygame.mouse.get_pos()
        offset = 400 - mouse_pos[0]
        self.background.x_pos = int((self.background.x_pos+offset)*1.4 - 16)
        if self.background.x_pos < -640:
            self.background.x_pos = -640
        if self.background.x_pos > 0:
            self.background.x_pos = 0
        shift = int(mouse_pos[1] / 150)
        self.background.y_pos = -30 * shift
        print(f"mouse: {mouse_pos[0]}  back: {self.background.x_pos}")

    def get_coords_of_shift(self):
        if self.scale > 1:
            left_border = -640
        else:
            left_border = -400
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > 780:
            if self.background.x_pos > left_border:
                x = self.background.x_pos - 0.5
                self.background.x_pos = x
                self.speed = 0.2
            else:
                x = left_border
        elif mouse_pos[0] < 20:
            if self.background.x_pos < 0:
                x = self.background.x_pos + 0.5
                self.background.x_pos = x
                self.speed = -0.2
            else:
                x = 0
        else:
            x = self.background.x_pos
        self.background.x_pos = x