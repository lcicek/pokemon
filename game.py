# Example file showing a basic pygame "game loop"
import pygame
from pygame import display, RESIZABLE
import os

from lock import Lock
from graphic import Graphic
from player import Player
from parameters import *
from controller import Controller
from utility import *

# Set position window will open up at:
os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN

# SETUP PYGAME:
pygame.init()
screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# SETUP SPRITES:
player = Player()
location = Graphic(LOCATION_SPRITE)

controller = Controller()

### INIT LOCKS ###
move_lock = Lock()

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

    # Check for more "events":

    # clear surface:
    screen.fill("black")

    handle_input(controller, player, move_lock)
    handle_render(screen, player, location, move_lock=move_lock)

    #renderGraphic(screen, location, player)
    #renderPlayer(screen, player)
    # update display:
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()