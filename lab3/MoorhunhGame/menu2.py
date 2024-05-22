import pygame


class Game:
    def __init__(self):
        self.FPS = 144
        self.WHITE = (255, 255, 255)
        self.width = 800
        self.height = 600
        pygame.init()
        self.clock = pygame.time.Clock()
        self.backPosX = 0
        self.backPosY = 0
        self.flagRightBG = True
        self.flagLeftBG = False
        self.scale = 1
        self.num = 6
        self.SCORE = 0

    def start_game(self):
        pygame.display.set_caption("Moorhunh")
        pygame.display.set_icon(pygame.image.load("images/icon.bmp"))
        screen = pygame.display.set_mode((self.width, self.height))
        background = pygame.image.load("images/village.bmp")
        start_time = pygame.time.get_ticks()
        custom_event = pygame.USEREVENT + 1
        pygame.time.set_timer(custom_event, 3)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__scaleBackGround(event.button, background, screen)
                    if event.button == 1:
                        self.remove_bullets(bullets, screen)
                        self.num -= 1
                        self.fire_in_aim()
                    if event.button == 3:
                        self.num = 6
                elif event.type == custom_event:
                    self.__scaleBackGround(3, background, screen)
            if self.scale == 1:
                self.__shiftBackGround()
                screen.blit(background, (self.backPosX, self.backPosY))
            bullets = self.load_bullets(screen, self.num)
            self.score_result(screen)
            self.time_round(start_time, screen)
            pygame.display.update()

            self.clock.tick(self.FPS)
    def time_round(self, start_time, screen):
        duration = 2 * 60 * 1000
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        remaining_time = max(duration - elapsed_time, 0)
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        font = pygame.font.Font("font/ofont.ru_Kardinal.ttf", 36)
        text_time = font.render(f"Time: {minutes:02}:{seconds:02}", True, self.WHITE)
        text_time_outline = font.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
        screen.blit(text_time_outline, (9, 9))
        screen.blit(text_time_outline, (9, 11))
        screen.blit(text_time_outline, (11, 9))
        screen.blit(text_time_outline, (11, 11))
        screen.blit(text_time, (10, 10))
        if elapsed_time >= duration:
            print("Время вышло!")
            pass

    def score_result(self, screen):
        font = pygame.font.Font("font/ofont.ru_Kardinal.ttf", 36)
        text_score_outline = font.render(f"SCORE: {self.SCORE}", True, (0, 0, 0))
        text_score = font.render(f"SCORE: {self.SCORE}", True, self.WHITE)
        screen.blit(text_score_outline, (550, 7))
        screen.blit(text_score_outline, (552, 7))
        screen.blit(text_score_outline, (550, 9))
        screen.blit(text_score_outline, (552, 9))
        screen.blit(text_score, (551, 8))

    def fire_in_aim(self):
        if self.num < 0:
            print("bullets are finished")
        else:
            self.SCORE += 25

    def remove_bullets(self, bullets, screen):
        bullet = pygame.image.load("images/bullet.png")
        for bullet_rect in bullets:
            screen.blit(bullet, bullet_rect)

    def load_bullets(self, screen, num):
        bullet = pygame.image.load("images/bullet.png")
        bullet_rect = bullet.get_rect()
        bullets = []
        for i in range(num):
            bullet_rect.topleft = (720 - ((i - 1) * 40), 510)
            screen.blit(bullet, bullet_rect)
            bullets.append(bullet_rect)
        return bullets

    def __scaleBackGround(self, event_button, background, screen):
        if event_button == 4:
            if round(self.scale, 3) != 1.331:
                self.scale *= 1.1
        elif event_button == 5:
            if self.scale != 1:
                self.scale /= 1.1
        print(self.scale)
        original_width, original_height = background.get_size()
        new_width = int(original_width * self.scale)
        new_height = int(original_height * self.scale)
        scaled_background = pygame.transform.scale(background, (new_width, new_height))
        mouseX, mouseY = pygame.mouse.get_pos()
        x = (self.backPosX + 400 - mouseX) * self.scale
        y = (self.backPosY + 300 - mouseY) * self.scale
        x, y = self.__check_correct_value(x, y, new_width, new_height)
        print(f"pos x: {x}  pos y: {y}")
        screen.blit(scaled_background, (x, y))

    def __check_correct_value(self, x, y, newWidth, newHeight):
        print(newWidth)
        print(newHeight)
        if y > 0:
            y = 0
        if y < 600 - newHeight:
            y = 600 - newWidth
        if x > 0:
            x = 0
        if x < 800 - newWidth:
            x = 800 - newWidth
        if y == -720:
            y = -120
        if abs(800 - newWidth - x) > 50:
            x -= 50
        if x >= - 50:
            x = 0
        return x, y

    def __shiftBackGround(self):
        if self.flagRightBG:
            self.__shiftBackGroundRight()
        elif self.flagLeftBG:
            self.__shiftBackGroundLeft()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > 780:
            self.flagRightBG = True
            self.flagLeftBG = False
        elif mouse_pos[0] < 20:
            self.flagRightBG = False
            self.flagLeftBG = True
        else:
            self.flagLeftBG = self.flagRightBG = False

    def __shiftBackGroundRight(self):
        if self.backPosX > -400:
            self.backPosX -= 3

    def __shiftBackGroundLeft(self):
        if self.backPosX < 0:
            self.backPosX += 3
