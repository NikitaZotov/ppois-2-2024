import pygame.mixer
from pygame.mixer import Sound

from model import GameEngine
from event.event_manager import ev_manager
from event import InitializeEvent, TickEvent, EndRunEvent, StartRunEvent, EatenEvent, GhostStateEvent
from model.side import Side
from model.state import State


class SoundManager:
    def __init__(
            self,
            model: GameEngine
    ):
        self.model = model
        self.count = 0
        self.sound_counter = {}
        self.pacman_moving_sound: Sound | None = None
        self.pacman_death_sound: Sound | None = None
        self.pacman_powerup_sound: Sound | None = None
        self.ghost_fright_sound: Sound | None = None
        self.ghost_death_sound: Sound | None = None
        self.is_played = False

        ev_manager.add_handler(TickEvent, lambda e: self.__tick_event_handler(e))
        ev_manager.add_handler(InitializeEvent, lambda e: self.initialize(e))
        ev_manager.add_handler(EndRunEvent, self.__get_end_run_event_handler())
        ev_manager.add_handler(StartRunEvent, self.__get_start_run_event_handler())
        ev_manager.add_handler(EatenEvent, self.__get_eaten_event_handler())
        ev_manager.add_handler(GhostStateEvent, self.__get_fright_event_handler())

    def initialize(self, event: InitializeEvent):
        self.pacman_moving_sound = Sound(r"resource/waka.wav")
        self.pacman_death_sound = Sound(r"resource/death.wav")
        self.pacman_powerup_sound = Sound(r"resource/powerup.wav")
        self.ghost_fright_sound = Sound(r"resource/fright.wav")
        self.ghost_death_sound = Sound(r"resource/ghost_death.wav")
        self.pacman_moving_sound.set_volume(0.15)
        self.pacman_death_sound.set_volume(0.3)
        self.pacman_powerup_sound.set_volume(0.3)
        self.ghost_fright_sound.set_volume(0.2)
        self.ghost_death_sound.set_volume(0.5)
        pygame.mixer.music.load(r"resource/misery.wav")
        pygame.mixer.music.play(loops=-1)

    def __tick_event_handler(self, event):
        if self.model.state.peek() != State.game_play:
            return
        self.count += 1
        if self.model.map_.p_tracker.pacman.direction == Side.stop:
            self.pacman_moving_sound.stop()
            self.is_played = False
        elif not self.is_played:
            self.pacman_moving_sound.play(loops=-1)
            self.is_played = True

    def __get_end_run_event_handler(self):
        def handler(event: EndRunEvent):
            self.pacman_moving_sound.stop()
            self.is_played = False
            self.pacman_death_sound.play()

        return handler

    def __get_start_run_event_handler(self):
        def handler(event: StartRunEvent):
            self.pacman_death_sound.stop()

        return handler

    def __get_eaten_event_handler(self):
        from model.object import Haste, Powerup
        from model.object.ghosts import Ghost

        def handler(event: EatenEvent):
            if isinstance(event.game_object, Powerup | Haste):
                self.pacman_powerup_sound.play()
            elif isinstance(event.game_object, Ghost):
                self.ghost_death_sound.play()

        return handler

    def __get_fright_event_handler(self):
        from model.object.ghosts import FrightState

        def handler(event: GhostStateEvent):
            if event.ghost_state is FrightState:
                self.ghost_fright_sound.stop()
                self.ghost_fright_sound.play(maxtime=6000)

        return handler
