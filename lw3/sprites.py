from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = z


class MovingSprite(Sprite):
    def __init__(self, pos, surf, groups, z, speed, move_dir):
        super().__init__(pos, surf, groups, z)

        # movement
        self.speed = speed
        self.move_dir = move_dir
        self.direction = vector(1, 0) if self.move_dir == 'x' else vector(0, 1)

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * delta_time


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z, animation_speed=ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self, delta_time):
        self.animate(delta_time)
