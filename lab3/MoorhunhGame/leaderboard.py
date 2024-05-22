import pygame
import json
import constant


class Leaderboard:
    def __init__(self, screen):
        self.screen = screen

    def print_leaderboard(self):
        with open('leaderboard.json', 'r') as file:
            self.players_data = json.load(file)
        self.players_data = sorted(self.players_data, key=lambda player: player['score'], reverse=True)
        # print(self.players_data)
        x_pos = 130
        x_pos_score = 530
        y_pos = 157
        # custom_font = pygame.font.Font('font/Deledda Closed Black.ttf', 28)
        custom_font = pygame.font.Font('font/ofont.ru_Kardinal.ttf', 28)
        for i in range(len(self.players_data)):
            text = custom_font.render(f"{self.players_data[i]['name']}", True, constant.WHITE)
            text_score = custom_font.render(f"{self.players_data[i]['score']}", True, constant.WHITE)
            text_black = custom_font.render(f"{self.players_data[i]['name']}", True, constant.BLACK)
            text_score_black = custom_font.render(f"{self.players_data[i]['score']}", True, constant.BLACK)
            self.screen.blit(text_black, (x_pos - 1, y_pos - 1))
            self.screen.blit(text_black, (x_pos - 1, y_pos + 1))
            self.screen.blit(text_black, (x_pos + 1, y_pos - 1))
            self.screen.blit(text_black, (x_pos + 1, y_pos + 1))
            self.screen.blit(text_score_black, (x_pos_score - 1, y_pos - 1))
            self.screen.blit(text_score_black, (x_pos_score - 1, y_pos + 1))
            self.screen.blit(text_score_black, (x_pos_score + 1, y_pos - 1))
            self.screen.blit(text_score_black, (x_pos_score + 1, y_pos + 1))
            self.screen.blit(text, (x_pos, y_pos))
            self.screen.blit(text_score, (x_pos_score, y_pos))
            y_pos += 37

    def get_lower_result(self):
        with open('leaderboard.json', 'r') as file:
            self.players_data = json.load(file)
        self.players_data = sorted(self.players_data, key=lambda player: player['score'], reverse=True)
        if len(self.players_data) < 10:
            print(f"score {0}")
            return 0
        else:
            print(f"score: {self.players_data[9]['score']}")
            return int(self.players_data[9]['score'])

    def add_result(self,score,name = "Player"):
        if name == None or name == "":
            name = "Player"
        with open('leaderboard.json', 'r') as file:
            self.players_data = json.load(file)
        self.players_data = sorted(self.players_data, key=lambda player: player['score'], reverse=True)
        if len(self.players_data) == 10:
            self.players_data.pop()
        new_entry = {"name": name, "score": score}
        self.players_data.append(new_entry)
        with open('leaderboard.json', 'w') as file:
            json.dump(self.players_data, file, indent=4)