import pygame
import sys
from View.WaveMenu import WaveMenu
from Model.LeaderBoard import Leaderboard
from View.LeaderBoardView import LeaderBoardView
from Controller.LevelManager import LevelManager
from View.Button import Button
from View.HelperView import HelperView
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = [
            ("начать игру", (lambda: setattr(self, 'current_page', LevelManager(self.screen, self.leaderboard)))),
            ("выбрать уровень", (lambda: setattr(self, 'current_page', WaveMenu(self.screen)))),
            ("таблица рекордов", (lambda: setattr(self, 'current_page', LeaderBoardView(self.screen, self.leaderboard)))),
            ("справка", (lambda: setattr(self, 'current_page', HelperView(self.screen)))),
            ("выход", lambda: (self.leaderboard.save(),pygame.quit(), sys.exit()))
        ]
        self.current_page = None
        self.leaderboard = Leaderboard()
        self.leaderboard.load()
        self.Buttons = []
        self.create_menu()

    def create_menu(self):
        button_width, button_height = 350, 80
        for index, (option_text, option_action) in enumerate(self.options):
            self.Buttons.append(
                Button(self.screen, (50, 50 + index * 90), button_width, button_height, option_text, option_action))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.leaderboard.save()
            pygame.quit()
            sys.exit
        if self.current_page is None:
            for button in self.Buttons:
                button.handle_event(event)
        else:
            self.current_page.handle_event(event)

    def update(self):
        if self.current_page is None:
            self.screen.fill((250, 250, 230))
            pygame.display.set_caption("Space invaders")
            for button in self.Buttons:
                button.update()
        else:
            self.current_page.update()
            if not self.current_page.run:
                self.current_page = None
