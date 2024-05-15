import os.path
import random

import pygame

from tools.loader import SINGLE, BACK, putLargeNum
from tools.utils import rounded_rect


def showScreen(win, sel):
    win.fill((0, 0, 0))

    rounded_rect(win, (255, 255, 255), (70, 5, 340, 60), 15, 4)
    win.blit(SINGLE.HEAD, (100, 7))
    win.blit(BACK, (460, 0))

    rounded_rect(win, (255, 255, 255), (10, 70, 480, 180), 12, 4)
    for cnt, i in enumerate(SINGLE.PARA1):
        y = 75 + cnt * 17
        win.blit(i, (20, y))
    win.blit(SINGLE.CHOOSE, (90, 160))
    win.blit(SINGLE.SELECT, (200, 150))
    pygame.draw.rect(win, (50, 100, 150), (200 + sel * 50, 150, 50, 50), 3)

    rounded_rect(win, (255, 255, 255), (170, 210, 140, 30), 7, 3)
    win.blit(SINGLE.START, (170, 210))


def main(win):
    sel = 0
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)
        showScreen(win, sel)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50:
                    return 1

                if 160 < y < 210 and 200 < x < 350:
                    sel = (x // 50) - 4

                if 380 < y < 410:
                    for i in range(9):
                        if 110 + i * 35 < x < 135 + i * 35:
                            lvl = i + 1

                if 170 < x < 310 and 220 < y < 250:
                    if sel == 2:
                        return True, random.randint(0, 1)
                    else:
                        return True, sel

        pygame.display.update()
