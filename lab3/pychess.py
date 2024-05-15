import sys
import pygame

import chess
import menus
from tools.loader import MAIN
from tools import sound

sys.stdout.flush()

pygame.init()
clock = pygame.time.Clock()

if pygame.version.vernum[0] >= 2:
    win = pygame.display.set_mode((500, 500), pygame.SCALED)
else:
    win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("PyChess")
pygame.display.set_icon(MAIN.ICON)

sngl = (260, 140, 220, 40)
mult = (280, 200, 200, 40)
load = (280, 260, 120, 40)
pref = (265, 320, 210, 40)
rules = (380, 380, 120, 40)


def showMain(prefs):
    global cnt, img

    win.blit(MAIN.BG, (0, 0))
    win.blit(MAIN.SINGLE, sngl[:2])
    win.blit(MAIN.MULTI, mult[:2])
    win.blit(MAIN.LOAD, load[:2])
    win.blit(MAIN.PREF, pref[:2])
    win.blit(MAIN.RULES, rules[:2])


cnt = 0
img = 0
run = True

prefs = menus.pref.load()

music = sound.Music()
music.play(prefs)
while run:
    clock.tick(30)
    showMain(prefs)

    x, y = pygame.mouse.get_pos()

    if sngl[0] < x < sum(sngl[::2]) and sngl[1] < y < sum(sngl[1::2]):
        win.blit(MAIN.SINGLE_H, sngl[:2])

    if mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
        win.blit(MAIN.MULTI_H, mult[:2])

    if load[0] < x < sum(load[::2]) and load[1] < y < sum(load[1::2]):
        win.blit(MAIN.LOAD_H, load[:2])

    if pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
        win.blit(MAIN.PREF_H, pref[:2])

    if rules[0] < x < sum(rules[::2]) and rules[1] < y < sum(rules[1::2]):
        win.blit(MAIN.RULES_H, rules[:2])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if sngl[0] < x < sum(sngl[::2]) and sngl[1] < y < sum(sngl[1::2]):
                sound.play_click(prefs)
                ret = menus.splayermenu(win)
                if ret == 0:
                    run = False
                elif ret != 1:
                    if ret[0]:
                        run = chess.singleplayer(win, ret[1], prefs)

            elif mult[0] < x < sum(mult[::2]) and mult[1] < y < sum(mult[1::2]):
                sound.play_click(prefs)
                ret = menus.timermenu(win, prefs)
                if ret == 0:
                    run = False
                elif ret != 1:
                    run = chess.multiplayer(win, ret[0], ret[1], prefs)

            elif load[0] < x < sum(load[::2]) and load[1] < y < sum(load[1::2]):
                sound.play_click(prefs)
                ret = menus.loadgamemenu(win)
                if ret == 0:
                    run = False

                elif ret != 1:
                    if ret[0] == "multi":
                        run = chess.multiplayer(win, *ret[1:3], prefs, ret[3])
                    elif ret[0] == "mysingle":
                        run = chess.singleplayer(win, ret[1], prefs, ret[2])

            elif pref[0] < x < sum(pref[::2]) and pref[1] < y < sum(pref[1::2]):
                sound.play_click(prefs)
                run = menus.prefmenu(win)

                prefs = menus.pref.load()
                if music.is_playing():
                    if not prefs["sounds"]:
                        music.stop()
                else:
                    music.play(prefs)

            elif rules[0] < x < sum(rules[::2]) and rules[1] < y < sum(rules[1::2]):
                sound.play_click(prefs)
                run = menus.rules(win)

    pygame.display.flip()

music.stop()
pygame.quit()
