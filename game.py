# Example file showing a basic pygame "game loop"
import pygame
from pygame import display, RESIZABLE
import os

from player import Player
from threading import Event
from parameters import *
from controller import Controller
from location import Location
from utility import *

# WINDOW-POSITION:
os.environ['SDL_VIDEO_WINDOW_POS'] = "5, 35"

# EVENTS:
key_press_event = Event()

# INITIALIZE:
player = Player("player.png", "player")
location = Location("SafariZone.png", "safari_zone")
controller = Controller(key_press_event)
screen_x = SCREEN_POS[0]
screen_y = SCREEN_POS[1]

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

        screen_x -= delta_x
        screen_y -= delta_y

        key_press_event.clear()

    print(outOfBounds(player.x, player.y, screen_x, screen_y, location.width, location.height, player.scale, player.width, player.height))

    #print((screen_x, screen_y))
    renderLocation(screen, location, (screen_x, screen_y))
    renderPlayer(screen, player)

    # update display:
    pygame.display.flip()

    clock.tick(20)  # limits FPS to 60

controller.quit()
pygame.quit()