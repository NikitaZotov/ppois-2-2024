import pygame


class VolumeController:
    @staticmethod
    def set_volume(value):
        value /= 100
        pygame.mixer.music.set_volume(value)

    @staticmethod
    def increase_volume(step=0.1):
        pygame.mixer.music.set_volume(min(1.0, pygame.mixer.music.get_volume() + step))

    @staticmethod
    def decrease_volume(step=0.1):
        pygame.mixer.music.set_volume(max(0.0, pygame.mixer.music.get_volume() - step))
