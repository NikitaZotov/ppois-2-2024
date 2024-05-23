import random

from core.ball import Ball
from core.bullet import Bullet
from core.double_ball import DoubleBall
from core.game_consts import *
from core.meteor import Meteor


class Modifiers:
    @staticmethod
    def add_game_modifier(balls, paddle, all_sprites, collision):
        if collision.bricks_destroyed >= 5:
            choice = random.randint(1, 5)
            match choice:
                case 1:
                    new_ball = Ball()
                    new_ball.rect.center = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT // 2)
                    all_sprites.add(new_ball)
                    balls.append(new_ball)  # Добавляем новый мяч в список мячей
                case 2:
                    collision.bricks_destroyed = 0
                    paddle.rect.width += 15  # Increase the paddle width by 15 pixels
                    paddle.image = pygame.Surface([paddle.rect.width, PADDLE_HEIGHT])  # Update the paddle image
                    paddle.image.fill(GREEN)
                    paddle.update()
                case 3:
                    pink_ball = DoubleBall()  # Create a new pink ball
                    pink_ball.rect.center = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT // 2)
                    all_sprites.add(pink_ball)
                case 4:
                    meteorite = Meteor()
                    all_sprites.add(meteorite)
                case 5:  # Handle the bullet shooting modifier
                    bullet = Bullet(paddle)
                    all_sprites.add(bullet)

            collision.bricks_destroyed = 0