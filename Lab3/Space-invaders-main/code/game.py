import random

import pygame
from player import Player
from View.Enemys.extra import Extra
from random import choice
from Weapon.EnemyLaser import EnemyLaser
from Controller.CharacterGenerator import CharacterGenerator
from View.Explosion import Explosion
from View.Enemys.Ram import Ram
from View.Enemys.Boss import Boss

class Game:
    def __init__(self, screen, wave_name, score=0):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen =screen
        self.wave_name=wave_name

        self.run = True
        self.pause = False


        self.lives = 1
        player_sprite = Player(( self.screen_width / 2,  self.screen_width),  self.screen_width, 5, self.lives)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.live_surf = pygame.image.load('../graphics/life.png').convert_alpha()
        self.live_x_start_pos = self.screen_width - (self.live_surf.get_size()[0]  + 20)*self.lives
        self.score = 0
        self.font = pygame.font.Font('../font/Pixeled.ttf', 20)

        self.score=score

        self.blocks = pygame.sprite.Group()

        self.events=[]

        self.background_color=(0,0,0)
        self.duration=None
        self.start_level_time = pygame.time.get_ticks()
        self.aliens = pygame.sprite.Group()
        self.CharacterGenerator = CharacterGenerator(self.aliens,self.blocks,self.events )

        self.generation_function=None

        self.error=False

        self.CharacterGenerator.process_wave(self.wave_name)

        self.duration = self.CharacterGenerator.duration
        self.background_color = self.CharacterGenerator.background_color
        self.alien_lasers = pygame.sprite.Group()

        self.alien_shoot_timer = pygame.time.get_ticks()
        self.alien_shoot_delay = 1000


        self.music = pygame.mixer.Sound('../audio/music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

        self.explosions= pygame.sprite.Group()

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        current_time = pygame.time.get_ticks()
        # Проверяем, прошло ли достаточно времени с момента последнего выстрела пришельцев
        if current_time - self.alien_shoot_timer >= self.alien_shoot_delay:
            if self.aliens.sprites():
                random_alien = choice(self.aliens.sprites())
                if  not isinstance(random_alien,Ram) :
                    laser_sprite = EnemyLaser(random_alien.rect.center, 6, self.screen_height)
                    self.alien_lasers.add(laser_sprite)
                    self.laser_sound.play()
            self.alien_shoot_timer = current_time



    def collision_checks(self):
        self.player.sprite.lasers.update(self.blocks,self.aliens,self.player_laser_collision_with_enemy )

        self.player.update()
        self.alien_lasers.update(self.blocks, self.player)

        self.aliens.update(direction=self.CharacterGenerator.direction)

        for alien in self.aliens:
            pygame.sprite.spritecollide(alien, self.blocks, True)

        collided_aliens = pygame.sprite.spritecollide(self.player.sprite, self.aliens, True)
        for alien in collided_aliens:
                alien.kill()
                self.player.sprite.lives -= 1

        self.lives =self.player.sprite.lives

    def display_lives(self):
        if self.lives==0:
            self.game_over()
            return
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            self.screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        self.screen.blit(score_surf, score_rect)

    def player_laser_collision_with_enemy(self, enemy):
        self.score+=enemy.enemy_data.score
        if isinstance(enemy,Boss):
            enemy.breaking()
        else:
            enemy.enemy_data.lives-=1
        if isinstance(enemy, Extra):
            self.player.sprite.weapon_type=choice(["rocket","BigLaser"])

        if enemy.enemy_data.lives <= 0:
            self.aliens.remove(enemy)
            new_explosion=Explosion(self.screen,enemy.rect.x,enemy.rect.y)
            self.explosions.add(new_explosion)
            new_explosion.play_sound()
            del enemy

    def level_timer_redraw(self,left_time):
        left_time=left_time//1000
        time_surf = self.font.render(f'time: {left_time}', False, 'white')
        timr_rect = time_surf.get_rect(topleft=(10, 40))
        self.screen.blit(time_surf, timr_rect)

    def finish_level(self,time_is_up):
        if not self.aliens.sprites() or time_is_up :
            image = pygame.image.load("../graphics/win.jpg").convert_alpha()
            image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
            self.screen.blit(image, (0, 0))
            pygame.display.flip()
            pygame.time.wait(2000)
            self.run=False
            self.music.stop()
            return "finish"

    def game_over(self):
        image = pygame.image.load("../graphics/game_over.jpg").convert_alpha()
        image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
        self.screen.blit(image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(1000)
        self.run = False
        self.music.stop()
        return "loose"


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE:
                self.pause= not self.pause
                pygame.time.wait(300)
                return
            elif event.key == pygame.K_BACKSPACE:
                self.run= False
                pygame.time.wait(300)
                return

    def update(self):
        if self.error is True:
            return

        if self.pause==True:
                return

        self.screen.fill(self.background_color)
        current_time = pygame.time.get_ticks()
        if self.duration is not None:
            left_time=current_time - self.start_level_time
            if left_time>= self.duration:
                return self.finish_level(True)
            else:
                self.level_timer_redraw(self.duration-left_time)

        if self.lives<=0:
            return self.game_over()
        self.explosions.update()

        self.collision_checks()
        self.alien_shoot()

        if len(self.events)!=0:
            for generated_event in self.events:
                generated_event()

        self.player.sprite.lasers.draw(self.screen)
        self.player.draw(self.screen)
        self.blocks.draw(self.screen)
        self.aliens.draw(self.screen)
        self.alien_lasers.draw(self.screen)
        self.display_lives()
        self.display_score()
        if self.duration is None:
            return self.finish_level(False)

