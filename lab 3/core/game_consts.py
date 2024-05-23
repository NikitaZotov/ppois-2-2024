import pygame
import xml.etree.ElementTree as ET

tree = ET.parse('../static/game_consts.xml')
root = tree.getroot()

SCREEN_WIDTH = int(root.find('SCREEN_WIDTH').text)
SCREEN_HEIGHT = int(root.find('SCREEN_HEIGHT').text)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BRICK_WIDTH = int(root.find('BRICK_WIDTH').text)
BRICK_HEIGHT = int(root.find('BRICK_HEIGHT').text)

PADDLE_WIDTH = int(root.find('PADDLE_WIDTH').text)
PADDLE_HEIGHT = int(root.find('PADDLE_HEIGHT').text)
PADDLE_SPEED = int(root.find('PADDLE_SPEED').text)

WHITE = tuple(map(int, root.find('WHITE').text.split(',')))
RED = tuple(map(int, root.find('RED').text.split(',')))
PINK = tuple(map(int, root.find('PINK').text.split(',')))
GREEN = tuple(map(int, root.find('GREEN').text.split(',')))
BLUE = tuple(map(int, root.find('BLUE').text.split(',')))
BLACK = tuple(map(int, root.find('BLACK').text.split(',')))
GRAY = tuple(map(int, root.find('GRAY').text.split(',')))

BALL_RADIUS = int(root.find('BALL_RADIUS').text)
BALL_SPEED = int(root.find('BALL_SPEED').text)

