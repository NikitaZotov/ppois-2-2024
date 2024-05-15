import pygame, sys
from View.MainMenu import Menu
from Controller.ConfigurationManager import ConfigurationManager
import settings as settings

if __name__ == "__main__":
	pygame.init()
	screen_info = pygame.display.Info()
	screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
	pygame.display.set_caption("Space invaders")
	clock = pygame.time.Clock()
	ConfigurationManager=ConfigurationManager()

	settings.alien_type_dict=ConfigurationManager.process_characters_in_folder()
	settings.waves_dict = ConfigurationManager.process_wave_in_folder()
	settings.waves_names = ConfigurationManager.sort_list(settings.waves_dict.keys())

	menu = Menu(screen)
	running = True
	while True:
		for event in pygame.event.get():
			menu.handle_event(event)
		menu.update()
		pygame.display.flip()
		clock.tick(60)

    



	

