from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite
from player import Player
from groups import AllSprites
from tube import Tube
from flag import Flag, FlagPillar
from timer import Timer
from goomba import Goomba
from winning_player import WinningPlayer
from ui import GameUI

import json
import random


class Level:
    def __init__(self, game, tmx_map, level_frames):
        # player
        self.player = None
        self.reached_points = {}
        self.player_death_timer = Timer(2500)
        self.player_is_dead = False
        self.player_after_win = None
        self.game_win_timer = Timer(200)

        # mobs
        self.mobs_locations = {}
        self.mobs = []
        self.mobs_setup()
        self.dead_mobs = {}

        # objects
        self.tubes = []
        self.flag = []
        self.breaking_image = self.extract_breaking_img(tmx_map)

        # general
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.tmx_map = tmx_map
        self.game = game

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.breakable_sprites = pygame.sprite.Group()

        # coins
        self.coins = []
        self.existing_coins = []
        self.coin_timers = {}

        # mushrooms
        self.mushrooms_lvl1 = []
        self.mushrooms_lvl2 = []

        self.level_frames = level_frames
        self.game_ui = GameUI()
        self.setup(self.tmx_map)

    def setup(self, tmx_map):
        layer_num = 0
        for layer in tmx_map.visible_layers:
            for x, y, surf in tmx_map.get_layer_by_name(layer.name).tiles():
                groups = [self.all_sprites]
                layer_key = 'bg' if layer.name == 'Background' else 'fg'
                tile_id = tmx_map.get_tile_gid(x, y, layer_num)
                if layer.name == 'Foreground':
                    groups.append(self.collision_sprites)

                z = LAYERS[layer_key]
                sprite = Sprite((x * TALE_SIZE, y * TALE_SIZE), surf, groups, z)
                if layer.name == 'Foreground' and tile_id == 22:
                    self.coins.append(sprite)
            layer_num += 1

        # 22 - bonus and coind, 23 - brick

        # player
        self.player = Player((300, 352), self, self.level_frames['player'])

        with open("worlds/1-1/W11.json") as json_file:
            json_data = json.loads(json_file.read())

        # tubes
        groups = [self.all_sprites, self.collision_sprites]
        for tube in json_data['tubes']:
            self.tubes.append(Tube(tube['x'], tube['y'], groups))

        # flag
        self.flag.append(Flag(json_data['flag']['x'] - 25, json_data['flag']['y'] + 15, self.all_sprites))
        self.flag.append(FlagPillar(json_data['flag']['x'], json_data['flag']['y'], self.all_sprites))

    def mobs_setup(self):
        with open("worlds/1-1/W11.json") as json_file:
            json_data = json.loads(json_file.read())
        for i in json_data['mobs']:
            locations = []
            for j in i['pos']:
                locations.append((j['x'], j['y']))
            self.mobs_locations[i['player_x_pos']] = locations
            self.reached_points[i['player_x_pos']] = False

    @staticmethod
    def extract_breaking_img(tmx_map):
        img = None
        layer_num = 0
        for layer in tmx_map.visible_layers:
            for x, y, surf in tmx_map.get_layer_by_name(layer.name).tiles():
                if layer.name == 'Foreground' and x == 2 and y == 15:
                    img = tmx_map.get_tile_image(x, y, layer_num)
            layer_num += 1
        return img

    def top_collision(self, sprite, level_frames):
        self.all_sprites.remove(sprite)
        self.collision_sprites.remove(sprite)
        surf = self.breaking_image if sprite in self.coins else sprite.image
        MovingSprite(sprite.rect.topleft, surf, self.all_sprites, LAYERS['semi bg'], 125,
                     'y')
        if sprite not in self.coins:
            self.game.sound_manager.play('brick_break', 0, 0.5)
            return
        chance = random.random()
        if chance <= 0.2:
            self.game.sound_manager.play('mushroom_appear', 0, 0.5)
            mushroom_lvl2 = Sprite((sprite.rect.x, sprite.rect.y - 32),
                                   pygame.image.load('images/mushroom/mushroom2.png'), self.all_sprites,
                                   LAYERS['semi bg'])
            self.mushrooms_lvl2.append(mushroom_lvl2)
        elif chance <= 0.5:
            self.game.sound_manager.play('mushroom_appear', 0, 0.5)
            mushroom_lvl1 = Sprite((sprite.rect.x, sprite.rect.y - 32),
                                   pygame.image.load('images/mushroom/mushroom.png'), self.all_sprites,
                                   LAYERS['semi bg'])
            self.mushrooms_lvl1.append(mushroom_lvl1)
        else:
            self.game.sound_manager.play('coin', 0, 0.5)
            coin = AnimatedSprite((sprite.rect.x + 10, sprite.rect.y - 28), level_frames['coin'], self.all_sprites,
                                  LAYERS['bg'])
            self.coin_timers[coin] = Timer(750)
            self.coin_timers[coin].activate()
            self.existing_coins.append(coin)
            self.game.player_score += 100
            self.game.player_coins += 1

    def mob_update(self):
        for x, reached in self.reached_points.items():
            if self.player.rect.x >= x and not reached:
                self.reached_points[x] = True
                self.mob_spawn(x)

    def mob_spawn(self, x):
        for pos in self.mobs_locations[x]:
            self.mobs.append(Goomba(pos, self.level_frames['goomba'], self, LAYERS['fg'], 100))

    def mob_death(self, mob):
        self.game.sound_manager.play('kill_mob', 0, 0.5)
        self.dead_mobs[mob] = Timer(200)
        self.dead_mobs[mob].activate()
        self.game.player_score += 100
        mob.killed()

    def mushroom_lvl1_collision(self, mushroom):
        self.game.sound_manager.play('mushroom_eat', 0, 0.5)
        self.game.player_score += 300
        self.all_sprites.remove(mushroom)
        self.mushrooms_lvl1.remove(mushroom)
        if self.player.lvl >= 1:
            return
        self.player.level_change(1, (self.level_frames['player1'], self.level_frames['player2']))

    def mushroom_lvl2_collision(self, mushroom):
        self.game.sound_manager.play('mushroom_eat', 0, 0.5)
        self.game.player_score += 500
        self.all_sprites.remove(mushroom)
        self.mushrooms_lvl2.remove(mushroom)
        if self.player.lvl == 2:
            return
        self.player.level_change(2, (self.level_frames['player1'], self.level_frames['player2']))

    def player_death(self):
        if self.game.player_lives == 1:
            self.game.game_over()
            return
        self.game.sound_manager.play('overworld', 9999999, 0.5)
        self.game.player_lives -= 1
        self.game.player_score = 0
        self.game.player_coins = 0
        self.__init__(self.game, self.tmx_map, self.level_frames)

    def player_becomes_dead(self):
        self.player.level_change(1, (self.level_frames['player'],))
        self.player.death_jump_active = True
        if not self.player_is_dead:
            self.game.sound_manager.stop('overworld')
            self.game.sound_manager.play('death', 0, 0.5)
            self.player_is_dead = True
            self.player_death_timer.activate()
            for mob in self.mobs:
                mob.ability_to_move = False

    def flag_moving(self):
        self.game.sound_manager.stop('overworld')
        self.game.sound_manager.play('level_end', 0, 0.5)
        self.flag[0].game_end = True
        self.game.game_end = True
        self.all_sprites.remove(self.player)
        self.collision_sprites.remove(self.player)
        self.player_after_win = WinningPlayer(self, self.player.rect.topleft + vector(10, 0),
                                              self.level_frames['player'],
                                              self.all_sprites, LAYERS['fg'], 100)

    def timers_update(self):
        # coin timers
        for timer in self.coin_timers.values():
            timer.update()
        for coin, timer in self.coin_timers.items():
            if not timer.active and coin in self.existing_coins:
                self.existing_coins.remove(coin)
                self.all_sprites.remove(coin)

        # mob timers
        for timer in self.dead_mobs.values():
            timer.update()
        for mob, timer in self.dead_mobs.items():
            if not timer.active:
                self.all_sprites.remove(mob)
                self.collision_sprites.remove(mob)

        # player death timer
        self.player_death_timer.update()
        if not self.player_death_timer.active and self.player_is_dead:
            self.player_death()

        # game win timer
        self.game_win_timer.update()
        if (self.player_after_win is not None and self.player_after_win.state == 'idle'
                and not self.game_win_timer.active):
            self.game.game_win()
            return

    def run(self, delta_time):
        self.all_sprites.update(delta_time)
        with open("worlds/1-1/W11.json") as json_file:
            json_data = json.loads(json_file.read())
        self.display_surface.fill(json_data['sky_color'])
        self.all_sprites.draw(self.player.rect.center)
        self.timers_update()
        self.mob_update()
        self.game_ui.update(self.game)
