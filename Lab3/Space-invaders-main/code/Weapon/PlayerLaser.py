import pygame


class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height,weapon_type):
        super().__init__()
        self.speed = speed
        self.height_y_constraint = screen_height

        if weapon_type=="laser":
            self.image = pygame.Surface((4, 20))
            self.image.fill('white')
            self.rect = self.image.get_rect(center=pos)
        elif weapon_type=="rocket":
            self.speed = speed*2
            self.image = pygame.image.load("../graphics/weapon/rocket/rocket1.png").convert_alpha()
            self.rect = self.image.get_rect(center=pos)
            self.scale_image(3)

    def scale_image(self, scale_factor):
        width = int(self.image.get_width() * scale_factor*2)
        height = int(self.image.get_height() * scale_factor)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(center=self.rect.center)

    def collision_with_enemy(self, enemy_group,player_laser_collision_with_enemy):
        aliens_hit = pygame.sprite.spritecollide(self, enemy_group, False )
        for alien in aliens_hit:
            player_laser_collision_with_enemy( alien)
            self.kill()
        # self.explosion_sound.play()

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def collision_with_blocks(self, blocks_group):
        # Возвращает список блоков, с которыми лазер столкнулся
        collided_blocks = pygame.sprite.spritecollide(self, blocks_group, True)
        # Если есть столкновения, уничтожаем лазер
        if collided_blocks:
            self.kill()

    def update(self, blocks_group, enemy_group,player_laser_collision_with_enemy):
        self.rect.y += self.speed
        self.collision_with_blocks(blocks_group)
        self.collision_with_enemy(enemy_group,player_laser_collision_with_enemy)
        self.destroy()
