import pygame


class PlayerBigLaser(pygame.sprite.Sprite):
    def __init__(self, pos, speed,screen_height, interval):
        super().__init__()
        self.interval=interval
        self.height_y_constraint = screen_height
        self.image = pygame.Surface((7,30))
        self.image.fill('red')
        self.speed=speed
        self.rect = self.image.get_rect(center=pos)

    def collision_with_enemy(self, enemy_group, player_laser_collision_with_enemy):
        aliens_hit = pygame.sprite.spritecollide(self, enemy_group, False)
        for alien in aliens_hit:
            player_laser_collision_with_enemy(alien)
        # self.explosion_sound.play()

    def destroy(self):
        if self.rect.y <= -50-self.height_y_constraint or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def collision_with_blocks(self, blocks_group):
        # Возвращает список блоков, с которыми лазер столкнулся
        collided_blocks = pygame.sprite.spritecollide(self, blocks_group, True)
        # Если есть столкновения, уничтожаем лазер


    def update(self, blocks_group, enemy_group, player_laser_collision_with_enemy):
        self.rect.y+=self.speed
        self.collision_with_blocks(blocks_group)
        self.collision_with_enemy(enemy_group, player_laser_collision_with_enemy)
        self.destroy()
