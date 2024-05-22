import pygame
import constant


class Cursor:
    def __init__(self):
        # pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load("images/scope_1.png").convert_alpha()
        self.offset = 15
        self.cursor_number = 1

    def collision_detected(self, screen, position, chickens_group):
        score = 0
        width = 0
        height = 0
        shift = 0
        if self.offset > 100:
            if position[0] > 640:
                shift = 160 - (800 - position[0])
            elif position[0] < 160:
                shift = -1 * (160 - position[0])
        square = 15
        if self.cursor_number == 1:
            width = position[0] - self.offset - shift + 8
            height = position[1] - self.offset + 8
            square_rect = pygame.Rect(width, height, square,
                                      square)
        else:
            width = position[0] - self.offset - shift + 995
            height = position[1] - self.offset + 998
            square = 10
            square_rect = pygame.Rect(width, height, square,
                                      square)
        pygame.draw.rect(screen, constant.WHITE, square_rect)

        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = square_rect

        collided_sprites = pygame.sprite.spritecollide(temp_sprite, chickens_group, False)

        flag = False
        for sprite in collided_sprites:
            score += sprite.score
            sprite.kill()
            flag = True
        if self.cursor_number != 1:
            score *= 2
        result = [flag, score, width, height]
        return result


    def print_cursor(self, screen, position):
        shift = 0
        if self.offset > 100:
            if position[0] > 640:
                shift = 160 - (800 - position[0])
            elif position[0] < 160:
                shift = -1 * (160 - position[0])
        # print(f"Shift: {shift}")
        screen.blit(self.cursor_img, (position[0] - self.offset - shift, position[1] - self.offset))

    def set_cursor(self, num=1):
        if num == 1:
            self.cursor_number = 1
            self.cursor_img = pygame.image.load("images/scope_1.png").convert_alpha()
            self.offset = 15
        else:
            self.cursor_number = 2
            self.cursor_img = pygame.image.load("images/scope_2.png").convert_alpha()
            self.offset = 1000

    def hide_cursor(self,screen):
        print("hide cursor")
        screen.blit(self.cursor_img, (900,900))