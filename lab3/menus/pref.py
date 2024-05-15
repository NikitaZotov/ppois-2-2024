import os.path
import json
import pygame
from tools.loader import PREF, BACK
from tools.utils import rounded_rect

KEYS = ["sounds", "flip", "show_moves", "allow_undo", "show_clock"]

DEFAULTPREFS = {
    "sounds": True,
    "flip": True,
    "show_moves": True,
    "allow_undo": True,
    "show_clock": False
}


def save(load):
    with open(os.path.join("res", "preferences.json"), "w") as f:
        json.dump(load, f)


def load():
    path = os.path.join("res", "preferences.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(DEFAULTPREFS, f)

    with open(path, "r") as f:
        mydict = json.load(f)
        for key in KEYS:
            if key not in mydict:
                mydict[key] = DEFAULTPREFS[key]
        return mydict


def prompt(win):
    rounded_rect(win, (255, 255, 255), (110, 160, 280, 130), 4, 4)

    win.blit(PREF.PROMPT[0], (130, 165))
    win.blit(PREF.PROMPT[1], (130, 190))

    win.blit(PREF.YES, (145, 240))
    win.blit(PREF.NO, (305, 240))
    pygame.draw.rect(win, (255, 255, 255), (140, 240, 60, 28), 2)
    pygame.draw.rect(win, (255, 255, 255), (300, 240, 45, 28), 2)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 240 < event.pos[1] < 270:
                    if 140 < event.pos[0] < 200:
                        return True
                    elif 300 < event.pos[0] < 350:
                        return False


def showScreen(win, prefs):
    win.fill((0, 0, 0))

    rounded_rect(win, (255, 255, 255), (70, 10, 350, 70), 20, 4)
    rounded_rect(win, (255, 255, 255), (10, 85, 480, 360), 12, 4)

    win.blit(BACK, (460, 0))
    win.blit(PREF.HEAD, (110, 15))

    win.blit(PREF.SOUNDS, (90, 90))
    win.blit(PREF.FLIP, (25, 150))
    win.blit(PREF.MOVE, (100, 210))
    win.blit(PREF.UNDO, (25, 270))
    win.blit(PREF.CLOCK, (25, 330))

    for i in range(5):
        win.blit(PREF.COLON, (225, 90 + (i * 60)))
        if prefs[KEYS[i]]:
            rounded_rect(
                win, (255, 255, 255), (249, 92 + (60 * i), 80, 40), 8, 2)
        else:
            rounded_rect(
                win, (255, 255, 255), (359, 92 + (60 * i), 90, 40), 8, 2)
        win.blit(PREF.TRUE, (250, 90 + (i * 60)))
        win.blit(PREF.FALSE, (360, 90 + (i * 60)))

    rounded_rect(win, (255, 255, 255), (350, 452, 85, 40), 10, 2)
    win.blit(PREF.BSAVE, (350, 450))


def main(win):
    prefs = load()
    clock = pygame.time.Clock()
    while True:
        clock.tick(24)
        showScreen(win, prefs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT and prompt(win):
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 460 < x < 500 and 0 < y < 50 and prompt(win):
                    return 1

                if 350 < x < 425 and 450 < y < 490:
                    save(prefs)
                    return 1

                for i in range(6):
                    if 90 + i * 60 < y < 130 + i * 60:
                        if 250 < x < 330:
                            prefs[KEYS[i]] = True
                        if 360 < x < 430:
                            prefs[KEYS[i]] = False
        pygame.display.update()
