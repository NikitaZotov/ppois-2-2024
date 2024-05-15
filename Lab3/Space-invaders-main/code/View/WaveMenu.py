import pygame
from game import Game
from View.Button import Button
import settings as settings

class WaveMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('../font/Pixeled.ttf', 20)
        self.font_min=pygame.font.Font('../font/Pixeled.ttf', 9)
        self.selected_wave = None
        self.buttons = []
        self.run = True
        self.current_page=None
        self.wave_files=None
        self.wave_files = settings.waves_names
        self.page = 1
        self.waves_per_page = 7
        self.description = ""
        self.draw_waves_buttons()


    def show_wave_info(self,wave_name):
        self.description = settings.waves_dict[wave_name].description


    def draw_waves_buttons(self):
        self.buttons=[]
        button_width, button_height = 100, 50
        self.buttons.append(Button(self.screen, (50, 500), button_width, button_height, "Prev", self.prev_page))
        self.buttons.append(Button(self.screen, (250, 500), button_width, button_height, "Next", self.next_page))
        start_index = (self.page - 1) * self.waves_per_page
        end_index = start_index + self.waves_per_page
        page_waves = self.wave_files[start_index:end_index]
        button_width, button_height = 300, 45
        for index, option_text in enumerate(page_waves):
            wave_name = option_text
            select_wave_func = lambda wave_name=wave_name: setattr(self, 'current_page', Game(self.screen, wave_name))
            show_wave_info_func = lambda wave_name=wave_name: self.show_wave_info(wave_name)
            y=70 + index * 50
            self.buttons.append(
                Button(self.screen, (30,y), button_width, button_height, option_text, select_wave_func, show_wave_info_func))

    def handle_event(self,event):
        if self.current_page is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.run = False
                    pygame.time.wait(300)
                    return
            for button in self.buttons:
                button.handle_event(event)
        else:
            self.current_page.handle_event(event)

    def update(self):
        if self.current_page is None:
            self.screen.fill((255, 255, 255))
            title_text = self.font.render("Выберети волну", True, (0, 0, 0))
            self.screen.blit(title_text, (50, 20))
            if self.description != "":
                description_text = self.font_min.render(self.description, True, (0, 0, 0))
                self.screen.blit(description_text, (10, 450))
            for button in self.buttons:
                button.update()
        else:
            self.current_page.update()
            if self.current_page.error== True:
                self.current_page = None
            elif self.current_page.run == False:
                self.current_page = None

    def prev_page(self):
        self.description = ""
        self.page = max(1, self.page - 1)
        self.draw_waves_buttons()


    def next_page(self):
        self.description = ""
        max_pages = len(self.wave_files) // self.waves_per_page+1
        self.page = min(max_pages, self.page + 1)
        self.draw_waves_buttons()








