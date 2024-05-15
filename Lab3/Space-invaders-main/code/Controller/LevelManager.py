from Model.LeaderBoard import Leaderboard
from game import Game
from Controller.ConfigurationManager import ConfigurationManager
from View.TextInputView import TextInputView
import settings as settings
import pygame

class LevelManager:
    def __init__(self,screen,LeaderBoard):
        self.screen=screen
        self.current_level_index = 0
        self.score_table = Leaderboard()
        self.JsonLoader = ConfigurationManager()
        self.levels = settings.waves_names
        self.run=True
        self.current_page = Game(self.screen,self.levels[0])
        self.score=0;
        self.LeaderBoard=LeaderBoard

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.run = False
                pygame.time.wait(300)
                return
        self.current_page.handle_event(event)

    def update(self):
        result = self.current_page.update()
        if result== "finish":
            if self.current_level_index >= len(self.levels):
                if self.LeaderBoard.is_higher_score(self.current_page.score):
                    self.score = self.current_page.score
                    self.current_page = TextInputView(self.screen)
                else:
                    self.run = False
            else:
                self.current_level_index += 1
                self.score = self.current_page.score
                self.current_page=Game(self.screen,self.levels[self.current_level_index],self.score)
        elif result == "loose":
            if self.LeaderBoard.is_higher_score( self.current_page.score):
                self.score=self.current_page.score
                self.current_page=TextInputView(self.screen)
            else:
                 self.run=False
        elif result == "LeaderName":
            self.LeaderBoard.add_record(self.current_page.text,self.score)
            self.run = False


