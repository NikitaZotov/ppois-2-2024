import pygame

import model
from controller import controller
from model import state_machine
from model.ghost_manager import GhostManager
from ui import GeneralViewManager
from model.map_loader import MapLoader
from controller.sound_manager import SoundManager


def run():
    pygame.mixer.init()
    state = state_machine.StateMachine()
    game_model = model.GameEngine(
        state,
        MapLoader()
    )
    sound = SoundManager(game_model)
    ctrl = controller.Controller(game_model)
    graphics = GeneralViewManager(game_model)
    game_model.ghost_manager = GhostManager(game_model)
    game_model.run()


if __name__ == '__main__':
    run()
