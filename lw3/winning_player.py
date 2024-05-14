from settings import *
from sprites import Sprite


class WinningPlayer(Sprite):
    def __init__(self, level, pos, frames, groups, z, speed, animation_speed=ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        self.state = 'end'
        super().__init__(pos, frames[self.state][self.frame_index], groups, z)
        self.animation_speed = animation_speed
        self.level = level

        # movement
        self.on_flag = True
        self.speed = speed
        self.direction = vector(0, 1)
        self.gravity = 500
        self.on_floor = False
        self.move_right = False
        self.reached_end = False

    def get_state(self):
        if self.on_flag:
            self.state = 'end'
        if self.direction == vector(1, 1) or self.direction == vector(1, 0):
            self.state = 'movement'
        if self.direction == vector():
            self.state = 'idle'

    def check_contact(self):
        if self.on_flag:
            if int(self.rect.bottom) == 352:
                self.on_flag = False
            else:
                return

        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        collide_rects = [sprite.rect for sprite in self.level.collision_sprites]
        self.on_floor = True if floor_rect.collidelist(collide_rects) >= 0 else False

        right_rect = pygame.Rect((self.rect.topright[0] + 2, self.rect.topright[1]), (2, self.rect.height))
        self.move_right = False if right_rect.collidelist(collide_rects) >= 0 else True

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

    def update(self, delta_time):
        self.get_state()
        self.animate(delta_time)
        self.rect.topleft += self.direction * self.speed * delta_time
        self.check_contact()
        self.direction.x = 1 if self.move_right else 0
        self.direction.y = 1 if not self.on_floor else 0
        if self.state == 'idle':
            # print(123)
            self.level.game_win_timer.activate()

