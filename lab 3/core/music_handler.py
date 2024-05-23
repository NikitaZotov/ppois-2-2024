import pygame

pygame.mixer.init()

class MusicHandler:
    barabara_sound = pygame.mixer.Sound('../static/sounds/barabara.mp3')
    sad_sound = pygame.mixer.Sound('../static/sounds/sad.mp3')

    current_sound_playing = None

    @staticmethod
    def play_sad_music():
        if not MusicHandler.current_sound_playing == MusicHandler.sad_sound:
            pygame.mixer.stop()
            MusicHandler.current_sound_playing = MusicHandler.sad_sound
            MusicHandler.sad_sound.play()

    @staticmethod
    def play_barabara_music():
        pygame.mixer.stop()
        MusicHandler.current_sound_playing = MusicHandler.barabara_sound
        MusicHandler.barabara_sound.play()
