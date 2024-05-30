import sys
import pygame
from Model.ball import Ball
from Model.player import Player
import random
from Model.table import Table


class Game:
    def __init__(self, width, height, screen: pygame.display, speed=7):
        self.screen_width = width
        self.screen_height = height
        self.screen = screen
        self.speed = speed
        self.opponent_score = 0
        self.player_score = 0
        self.game()
        table = Table()
        if table.get_first()[1] < self.player_score and self.player_score > self.opponent_score:
            self.new_record(table)
            return
        else:
            self.winner_end()
            return

    def game(self):
        pygame.display.set_caption("Pong")
        clock = pygame.time.Clock()
        ball = Ball(self.screen_width/2-15, self.screen_height/2-15, width=30, height=30, speed=self.speed)
        player = Player(10, self.screen_height / 2 - 10, 10, 140)
        opponent = Player(self.screen_width - 20, self.screen_height / 2 - 10, 10, 140)
        game_font = pygame.font.Font("freesansbold.ttf", 64)
        light_grey = (200, 200, 200)
        while True:
            # triggers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        player.speed += self.speed
                    if event.key == pygame.K_UP:
                        player.speed -= self.speed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player.speed -= self.speed
                    if event.key == pygame.K_UP:
                        player.speed += self.speed
            ball.ball_animation(self.screen_height)
            self.ball_restart(ball)
            if ball.colliderect(player) or ball.colliderect(opponent):
                ball.speed_x *= -1
                pygame.mixer.Sound.play(ball.sound)
            opponent.opponent_ai(ball, self.speed)
            player.player_animation(self.screen_height)
            # Visuals update, create
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, light_grey, player)
            pygame.draw.rect(self.screen, light_grey, opponent)
            pygame.draw.ellipse(self.screen, light_grey, ball)
            pygame.draw.aaline(self.screen, light_grey, (self.screen_width / 2, 0),
                               (self.screen_width / 2, self.screen_height))
            player_text = game_font.render(f"{self.opponent_score}", False, light_grey)
            self.screen.blit(player_text, (self.screen_width / 2 + 10, self.screen_height / 2))
            opponent_text = game_font.render(f"{self.player_score}", False, light_grey)
            self.screen.blit(opponent_text, (self.screen_width / 2 - 45, self.screen_height / 2))
            score_time = 120 - int(pygame.time.get_ticks() / 1200)
            time_text = game_font.render(f"{score_time}", False, light_grey)
            self.screen.blit(time_text, (self.screen_width / 2, 0))
            if score_time == 0:
                return
            # update screen
            pygame.display.flip()
            clock.tick(30)

    def winner_end(self):
        clock = pygame.time.Clock()
        game_font = pygame.font.Font("freesansbold.ttf", 48)
        light_grey = (200, 200, 200)
        if self.player_score > self.opponent_score:
            screen_text = "Player win"
        else:
            screen_text = "Bot win"
        while True:
            if self.player_score > self.opponent_score:
                screen_text = "Player win"
            else:
                screen_text = "Bot win"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.screen.fill((0, 0, 0))

            screen_text = game_font.render(screen_text, False, light_grey)
            self.screen.blit(screen_text, (self.screen_width / 2 - 100, self.screen_height / 2))
            pygame.display.flip()
            clock.tick(30)

    def new_record(self, table: Table):
        clock = pygame.time.Clock()
        game_font = pygame.font.Font("freesansbold.ttf", 48)
        light_grey = (200, 200, 200)
        input_text = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(input_text) > 0:
                        table.add_record([str(input_text), self.player_score])
                        return
                    elif event.key == pygame.K_ESCAPE and len(input_text) > 0:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            self.screen.fill((0, 0, 0))
            light_grey = (200, 200, 200)
            screen_text = "New record"
            ent = "Enter"
            screen_text = game_font.render(screen_text, False, light_grey)
            self.screen.blit(screen_text, (self.screen_width / 2 - 100, 100))
            ent = game_font.render(ent, False, light_grey)
            self.screen.blit(ent, (100, 400))
            inp = game_font.render(input_text, False, light_grey)
            self.screen.blit(inp, (400, 400))
            pygame.display.flip()
            clock.tick(30)

    def ball_restart(self, ball: Ball):
        score_sound = pygame.mixer.Sound("D:/lab1/ppois3/Model/sounds/score.ogg")
        if ball.left <= 0 or ball.right >= self.screen_width:
            if ball.left <= 0:
                self.opponent_score += 1
                ball.center = (self.screen_width / 2, self.screen_height / 2)
                ball.speed_x *= random.choice((-1, 1))
                ball.speed_y *= random.choice((-1, 1))
            else:
                self.player_score += 1
                ball.center = (self.screen_width / 2, self.screen_height / 2)
                ball.speed_x *= random.choice((-1, 1))
                ball.speed_y *= random.choice((-1, 1))
            score_sound.play()