import pygame

class Sound:
    def __init__(self):
        self.shot_sound = pygame.mixer.Sound("music/fire.wav")
        self.shot_reload = pygame.mixer.Sound("music/reload.wav")
        self.choose_sound = pygame.mixer.Sound("music/choose.wav")
    def start_game_music(self):
        pygame.mixer.music.load("music/game.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def stop_game_music(self):
        pygame.mixer.music.stop()

    def fire(self):
        self.shot_sound.play()

    def reload(self):
        self.shot_reload.play()

    def choose(self):
        self.choose_sound.play()

    def start_menu_music(self):
        pygame.mixer.music.load("music/menu.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def stop_menu_music(self):
        pygame.mixer.music.stop()