# Example file showing a basic pygame "game loop"
import pygame
from pygame import display, RESIZABLE
import os

from graphic import Graphic
from threading import Event
from parameters import *
from controller import Controller
from utility import *

# Set position window will open up at:
os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN

# EVENTS:
key_press_event = Event()

# SETUP SPRITES:
player = Graphic(PLAYER_SPRITE, DEFAULT_PLAYER_X, DEFAULT_PLAYER_Y)
location = Graphic(LOCATION_SPRITE, DEFAULT_SCREEN_X, DEFAULT_SCREEN_Y)

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
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.VIDEORESIZE:
            scale = calculateScale(screen.get_width()) # screen.get_width() = event.dict['size][0]
            player.updateScale(scale)
            location.updateScale(scale)
            screen = display.set_mode((VIEWPORT_WIDTH * scale, VIEWPORT_HEIGHT * scale), RESIZABLE)

    # clear surface:
    screen.fill("black")

    # check for move event
    if key_press_event.is_set():
        delta_x = controller.delta_x * UNIT_SIZE * location.scale
        delta_y = controller.delta_y * UNIT_SIZE * location.scale
        out_of_bounds = outOfBounds(player, location, delta_x, delta_y)
        if not out_of_bounds:
            location.updatePos(delta_x, delta_y)
        key_press_event.clear()

    renderGraphic(screen, location)
    renderGraphic(screen, player)

    # update display:
    pygame.display.flip()

    clock.tick(20)  # limits FPS to 60

controller.quit()
pygame.quit()