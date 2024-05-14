from settings import *
from sprites import MovingSprite


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, level, level_frames):
        # general
        self.level = level
        super().__init__(self.level.all_sprites)

        # image
        self.frames, self.frame_index = level_frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]

        # rects
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = LAYERS['fg']

        # movement
        self.direction = vector()
        self.speed = 250
        self.gravity = 500
        self.jump = False
        self.jump_height = 430

        # mobs
        self.killed_mob = False
        self.mob_kill_jump_height = 150

        # collision
        self.on_floor = False

        # death
        self.death_jump_active = False
        self.death_jump = 300

        # game assets
        self.lvl = 0

        # win
        self.on_flag = False
        self.to_castle_moving = False

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if self.level.player_is_dead:
            self.direction.x = 0
            return

        if self.on_flag:
            self.direction.y += 1
            return

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
            self.facing_right = True
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
            self.facing_right = False
        if keys[pygame.K_UP]:
            self.jump = True

        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def move(self, delta_time):
        # horizontal
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        # vertical
        self.direction.y += self.gravity / 2 * delta_time
        self.rect.y += self.direction.y * delta_time
        self.direction.y += self.gravity / 2 * delta_time
        self.collision('vertical')

        # death
        if self.death_jump_active:
            self.direction.y = -self.death_jump
            self.death_jump_active = False
            return

        # jumping
        if self.killed_mob:
            self.direction.y = -self.mob_kill_jump_height
            self.killed_mob = False
        else:
            if self.jump:
                if self.on_floor:
                    if self.lvl == 1:
                        self.level.game.sound_manager.play('big_mario_jump', 0, 0.2)
                    else:
                        self.level.game.sound_manager.play('small_mario_jump', 0, 0.5)
                    self.direction.y = -self.jump_height
                self.jump = False

    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.level.collision_sprites]

        # collision
        self.on_floor = True if floor_rect.collidelist(collide_rects) >= 0 else False

    def collision(self, axis):
        for sprite in self.level.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.rect.right = sprite.rect.left
                    if sprite in self.level.mobs and not sprite.dead:
                        if self.lvl == 2:
                            self.level.mob_death(sprite)
                        else:
                            self.level.player_becomes_dead()
                else:  # vertical
                    # top
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                        self.level.top_collision(sprite, self.level.level_frames)
                    # bottom
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                        if sprite in self.level.mobs:
                            self.level.mob_death(sprite)
                            self.killed_mob = True
                    self.direction.y = 0

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

    def get_state(self):
        if self.level.player_is_dead:
            self.state = 'death'
            return
        if self.on_flag:
            self.state = 'end'
            return
        if self.on_floor:
            self.state = 'idle' if self.direction.x == 0 else 'movement'
        else:
            self.state = 'jumping'

    def map_boarder_check(self):
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y = 0
        if self.rect.bottom >= 445:
            self.level.player_becomes_dead()
            self.level_change(1, (self.level.level_frames['player'],))
            self.death_jump_active = True

    def mushroom_collision_check(self):
        for sprite in self.level.mushrooms_lvl1:
            if sprite.rect.colliderect(self.rect):
                self.level.mushroom_lvl1_collision(sprite)

        for sprite in self.level.mushrooms_lvl2:
            if sprite.rect.colliderect(self.rect):
                self.level.mushroom_lvl2_collision(sprite)

    def flag_collision_check(self):
        if self.level.flag[1].rect.colliderect(self.rect):
            self.flag_touch()

    def level_change(self, lvl, frames_tuple):
        self.lvl = lvl
        self.frames = frames_tuple[self.lvl - 1]
        self.rect = (self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])].
                     get_frect(topleft=self.rect.topleft))

    def flag_touch(self):
        self.level_change(1, (self.level.level_frames['player'], ))
        self.on_flag = True
        self.level.flag_moving()

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.input()
        self.animate(delta_time)
        self.move(delta_time)
        self.map_boarder_check()
        self.mushroom_collision_check()
        self.flag_collision_check()
        self.check_contact()
        self.get_state()
