from core.records_manager import RecordsManager
from game_consts import *

import pygame
import sys

pygame.init()


def show_select_level():
    levels = list(range(0, 10))
    selected_level_index = 0  # Default to the first level
    selected_level = levels[selected_level_index]
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font('../static/font.ttf', 28)
        title_text = font.render("Select Level", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        level_text = [font.render(f"Level {i+1}", True, WHITE) for i in levels]
        level_positions = [(SCREEN_WIDTH // 2, 100 + i * 50) for i in range(len(levels))]

        for i, item in enumerate(level_text):
            if i == selected_level_index:  # Highlight the selected level in red
                item = font.render(f"Level {i + 1}", True, RED)
            screen.blit(item, level_positions[i])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, pos in enumerate(level_positions):
                    if level_text[i].get_rect(center=pos).collidepoint(mouse_pos):
                        selected_level_index = i
                        selected_level = levels[selected_level_index]
                        return selected_level
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return selected_level  # Return the selected level
                elif event.key == pygame.K_UP:
                    selected_level_index = (selected_level_index - 1) % len(levels)
                    selected_level = levels[selected_level_index]
                elif event.key == pygame.K_DOWN:
                    selected_level_index = (selected_level_index + 1) % len(levels)
                    selected_level = levels[selected_level_index]
                elif event.key == pygame.K_RETURN:
                    return selected_level


def show_level_completed_screen(level, time):
    screen.fill(BLACK)

    font = pygame.font.Font('../static/font.ttf', 36)
    title_text = font.render("Level Completed!", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    time_text = font.render(f"Your time: {time} seconds", True, WHITE)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(time_text, time_rect)

    continue_text = font.render("Press any key to continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    screen.blit(continue_text, continue_rect)

    pygame.display.flip()

    # Ожидание нажатия любой клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return


def show_save_record_screen(level, time):
    screen.fill(BLACK)

    font = pygame.font.Font('../static/font.ttf', 36)
    title_text = font.render("New High Score!", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    time_text = font.render(f"Your time: {time} seconds", True, WHITE)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    screen.blit(time_text, time_rect)

    nickname_text = font.render("Enter your nickname:", True, WHITE)
    nickname_rect = nickname_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    screen.blit(nickname_text, nickname_rect)

    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 350, 400, 50)
    input_text = ""
    active = True
    records = RecordsManager()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Возврат к предыдущему экрану
                elif active:
                    if event.key == pygame.K_RETURN:
                        # Сохранить рекорд и вернуться к предыдущему экрану
                        records.add_record(level, input_text, time)
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        # Удаление последнего символа из строки ввода
                        input_text = input_text[:-1]
                    elif event.key in (
                            pygame.KMOD_CTRL | pygame.K_v, pygame.KMOD_CTRL | pygame.K_c, pygame.KMOD_CTRL | pygame.K_x):
                        pass
                        # Отключаем комбинации Ctrl+C, Ctrl+V, Ctrl+X
                    else:
                        input_text += event.unicode

        # Отрисовка поля ввода
        pygame.draw.rect(screen, BLACK, input_box)  # Очистка предыдущего текста
        pygame.draw.rect(screen, WHITE, input_box, 2)
        font_input = pygame.font.Font(None, 36)
        input_surface = font_input.render(input_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()


def show_help_screen():
    screen.fill(BLACK)

    font = pygame.font.Font('../static/font.ttf', 24)
    title_text = font.render("Arkanoid Help", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    rules_text = [
        "Welcome to Arkanoid!",
        "Rules:",
        "- Use the paddle to bounce the ball and break all the bricks.",
        "- If the ball falls below the paddle, you lose.",
        "- Break all the bricks to win the level.",
        "",
        "Controls:",
        "- Use the left and right arrow keys to move the paddle.",
        "",
        "Modifiers:",
        "- After destroying a certain number of bricks, there's a chance of getting an modifier to the game.",
        "- Extra Ball"
        "- Paddle Size Increase"
        "- Ball that multiply your balls by 2"
        "- Meteorite, that can brake your paddle"
        "- Bullet Shot, that can break whole column of bricks or damage the wall"
        "",
        "Press any key to return to the main menu."
    ]

    y_position = 100
    for line in rules_text:
        text_surface = font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        screen.blit(text_surface, text_rect)
        y_position += 30

    pygame.display.flip()

    # Ожидание нажатия любой клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return


def show_records_screen(records_manager):
    screen.fill(BLACK)

    font = pygame.font.Font('../static/font.ttf', 36)
    title_text = font.render("High Score Table", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    records_text = records_manager.get_records_table()
    records_lines = records_text.split('\n')
    for i, line in enumerate(records_lines):
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 40))
        screen.blit(text, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Возврат к предыдущему экрану

        pygame.display.flip()


def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu")

    font = pygame.font.Font('../static/font.ttf', 30)

    # Отображение каждого пункта меню
    menu_items = ["1. Start game", "2. High score table", "3. Help", "0. Exit"]
    item_positions = [(SCREEN_WIDTH // 2, 200 + i * 50) for i in range(len(menu_items))]

    rendered_items = [font.render(item, True, WHITE) for item in menu_items]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, pos in enumerate(item_positions):
                    if rendered_items[i].get_rect(center=pos).collidepoint(mouse_pos):
                        return i  # Возвращает индекс выбранного пункта меню
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 2
                elif event.key == pygame.K_0:
                    return 3

        for i, item in enumerate(rendered_items):
            screen.blit(item, item_positions[i])  # Отображение пунктов меню на экране

        pygame.display.flip()


def show_game_over_text():
    font = pygame.font.Font('../static/font.ttf', 72)  # Загружаем шрифт
    text = font.render("Game Over :(", True, RED)  # Создаем текст
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Выравниваем текст по центру экрана
    screen.blit(text, text_rect)  # Отображаем текст на экране
    pygame.display.flip()  # Обновляем экран
    pygame.time.wait(2000)  # Подождать 2 секунды перед выходом
    return

