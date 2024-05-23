import random
import time

import pygame.mixer

from core.ball import Ball
from core.bullet import Bullet
from core.double_ball import DoubleBall
from core.game_status import GameStatus
from core.meteor import Meteor
from core.music_handler import MusicHandler
from game_consts import *

pygame.mixer.init()

barabara_sound = pygame.mixer.Sound('../static/sounds/barabara.mp3')
sad_sound = pygame.mixer.Sound('../static/sounds/sad.mp3')


class Collision:
    def __init__(self):
        self.last_brick_destroyed_time = time.time()  # Инициализация времени последнего разрушения кирпича
        self.bricks_destroyed = 0

    @staticmethod
    def check_bullet_collision(walls, bricks, all_sprites):
        bullets = [sprite for sprite in all_sprites if isinstance(sprite, Bullet)]
        for bullet in bullets:
            for brick in bricks:
                if pygame.sprite.collide_rect(bullet, brick):
                    brick.kill()
            for wall in walls:
                if pygame.sprite.collide_rect(bullet, wall):
                    if wall.can_brake:
                        wall.kill()
                    else:
                        wall.set_break_true()
                        wall.image.fill(RED)
                        bullet.kill()

    @staticmethod
    def check_extra_ball_collision(balls, paddle, all_sprites):
        extra_balls = [sprite for sprite in all_sprites if isinstance(sprite, DoubleBall)]
        for extra_ball in extra_balls:
            if pygame.sprite.collide_rect(extra_ball, paddle):
                current_ball_count = len(balls)
                new_ball_count = current_ball_count * 2
                for _ in range(new_ball_count):
                    new_ball = Ball()
                    new_ball.rect.center = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT // 2)
                    all_sprites.add(new_ball)
                    balls.append(new_ball)

                extra_ball.kill()

    @staticmethod
    def check_meteor_collision(paddle, all_sprites):
        meteors = [sprite for sprite in all_sprites if isinstance(sprite, Meteor)]
        for meteor in meteors:
            if pygame.sprite.collide_rect(meteor, paddle):
                GameStatus.set_pause()

    def check_collision(self, balls, bricks, walls, paddle, all_sprites):

        self.check_extra_ball_collision(balls, paddle, all_sprites)
        self.check_meteor_collision(paddle, all_sprites)
        self.check_bullet_collision(walls, bricks, all_sprites)

        current_time = time.time()
        for ball in balls:
            if ball.rect.left <= BALL_SPEED:
                ball.rect.left = 1
                ball.speed_x = BALL_SPEED

            if ball.rect.right >= SCREEN_WIDTH - BALL_SPEED:
                ball.rect.right = SCREEN_WIDTH - 1
                ball.speed_x = -1 * BALL_SPEED

            if ball.rect.top <= BALL_SPEED:
                ball.rect.top = 1
                ball.speed_y = BALL_SPEED

            if pygame.sprite.spritecollide(ball, bricks, False):
                pygame.mixer.stop()  # Остановка всех звуков
                self.last_brick_destroyed_time = time.time()

                brick_hit = pygame.sprite.spritecollide(ball, bricks, True)[0]
                MusicHandler.play_barabara_music()
                self.bricks_destroyed += 1

                brick_left_edge = brick_hit.rect.left
                brick_right_edge = brick_hit.rect.right
                brick_top_edge = brick_hit.rect.top
                brick_bottom_edge = brick_hit.rect.bottom

                if ball.rect.bottom <= brick_top_edge + BALL_SPEED or ball.rect.top >= brick_bottom_edge - BALL_SPEED:
                    # if brick_top_edge < ball.rect.bottom:
                    #     ball.rect.top = brick_bottom_edge + 1
                    # else:
                    #     ball.rect.bottom = brick_top_edge - 1

                    ball.speed_y *= -1
                # Проверяем столкновение с боковой стеной
                elif ball.rect.right >= brick_left_edge - BALL_SPEED and ball.rect.left <= brick_right_edge + BALL_SPEED:
                    #
                    # if brick_left_edge < ball.rect.right:
                    #     ball.rect.right = brick_left_edge - 1
                    # else:
                    #     ball.rect.left = brick_right_edge + 1

                    if ball.speed_x > 0:
                        ball.speed_x = BALL_SPEED * -1
                        # ball.rect.right = brick_left_edge - 1
                        # print("teleport to left")
                    else:
                        ball.speed_x = BALL_SPEED
                        # ball.rect.left = brick_right_edge + 1
                        # print("teleport to right")

            if pygame.sprite.collide_rect(ball, paddle):
                wall_left_edge = paddle.rect.left
                wall_right_edge = paddle.rect.right
                wall_top_edge = paddle.rect.top
                wall_bottom_edge = paddle.rect.bottom

                if (ball.rect.bottom <= wall_top_edge + BALL_SPEED or
                        ball.rect.top >= wall_bottom_edge - BALL_SPEED):
                    ball.speed_y *= -1
                    distance_from_center = ball.rect.centerx - paddle.rect.centerx
                    h = abs(paddle.rect.left - paddle.rect.centerx)

                    ball.speed_x = BALL_SPEED * distance_from_center / h
                elif (ball.rect.right >= wall_left_edge - BALL_SPEED and
                      ball.rect.left <= wall_right_edge + BALL_SPEED):
                    ball.speed_y = BALL_SPEED * -1
                    # ball.speed_x *= -1
                    if ball.rect.centerx > paddle.rect.centerx:
                        ball.rect.left = paddle.rect.right + PADDLE_SPEED + BALL_SPEED
                        ball.rect.bottom = paddle.rect.top + 1
                        ball.speed_x = BALL_SPEED
                    else:
                        ball.rect.centerx = paddle.rect.left - PADDLE_SPEED - BALL_SPEED
                        ball.rect.bottom = paddle.rect.top + 1
                        ball.speed_x = -1 * BALL_SPEED

                    # if ball.speed_x > 0:
                    #     ball.speed_x = -1 * BALL_SPEED
                    # else:
                    #     ball.speed_x = BALL_SPEED

            if pygame.sprite.spritecollide(ball, walls, False):
                wall_hit = pygame.sprite.spritecollide(ball, walls, False)[0]
                if wall_hit.can_brake:
                    wall_hit.kill()
                wall_left_edge = wall_hit.rect.left
                wall_right_edge = wall_hit.rect.right
                wall_top_edge = wall_hit.rect.top
                wall_bottom_edge = wall_hit.rect.bottom

                if ball.rect.bottom <= wall_top_edge + BALL_SPEED or ball.rect.top >= wall_bottom_edge - BALL_SPEED:
                    if wall_top_edge < ball.rect.bottom:
                        ball.rect.top = wall_bottom_edge + 1
                    else:
                        ball.rect.bottom = wall_top_edge - 1
                    ball.speed_y *= -1
                # Проверяем столкновение с боковой стеной
                elif ball.rect.right >= wall_left_edge - BALL_SPEED and ball.rect.left <= wall_right_edge + BALL_SPEED:
                    # if wall_left_edge < ball.rect.right:
                    #     ball.rect.right = wall_left_edge - 1
                    # else:
                    #     ball.rect.left = wall_right_edge + 1

                    if ball.speed_x > 0:
                        ball.rect.right = wall_left_edge - 1
                        ball.speed_x = BALL_SPEED * -1
                    else:
                        ball.rect.left = wall_right_edge + 1
                        ball.speed_x = BALL_SPEED

            if ball.rect.top > SCREEN_HEIGHT:  # Если мяч вышел за нижнюю границу экрана
                balls.remove(ball)
            if current_time - self.last_brick_destroyed_time > 3:
                MusicHandler.play_sad_music()
