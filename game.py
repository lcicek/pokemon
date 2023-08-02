# Example file showing a basic pygame "game loop"
import pygame
from pygame import display, RESIZABLE
import os

from graphic import Graphic
from player import Player
from threading import Event
from parameters import *
from controller import Controller
from utility import *

# Set position window will open up at:
os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN

# EVENTS:
key_press_event = Event()
walking_event = Event()

# SETUP SPRITES:
player = Player()
#location = Graphic(LOCATION_SPRITE)

# INITIALIZE CONTROLLER:
controller = Controller(key_press_event)

# SETUP PYGAME:
pygame.init()
screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

while running:
    # poll for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.VIDEORESIZE:
        #    scale = calculateScale(screen.get_width()) # screen.get_width() = event.dict['size][0]
        #    player.graphic.updateScale(scale)
        #    location.updateScale(scale)
        #    screen = display.set_mode((VIEWPORT_WIDTH * scale, VIEWPORT_HEIGHT * scale), RESIZABLE)

    # clear surface:
    screen.fill("black")

    handle_movement(key_press_event, controller, player)
    handle_render(screen, player)

    #renderGraphic(screen, location, player)
    #renderPlayer(screen, player)
    # update display:
    pygame.display.flip()
    clock.tick(20)  # limits FPS to 20

controller.quit()
pygame.quit()