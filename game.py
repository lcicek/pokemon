# Example file showing a basic pygame "game loop"
import pygame
import os

from lock import Lock
from graphic import Graphic
from location import Location
from player import Player
from parameters import *
from controller import Controller
from utility import *
from movementHandler import handle_input
from renderHandler import handle_render

# Set position window will open up at:
os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN

# SETUP PYGAME:
pygame.init()
screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
unit_size = UNIT_SIZE * DEFAULT_SCALE

# SETUP SPRITES:
player = Player()
location = Location(LOCATION_SPRITE, LOCATION_FOREGROUND)

controller = Controller()

### INIT LOCKS ###
move_lock = Lock()

### LOG ###
frames = 0
log_frame = FPS * 2

while running:
    start_time = pygame.time.get_ticks()
    frames += 1

    # poll for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            scale = calculate_scale(screen.get_width())
            scale_graphics(location, player, scale)
            screen = get_scaled_screen(scale)
            unit_size = UNIT_SIZE * scale

    # clear surface:
    screen.fill("black")

    handle_input(controller, player, location, move_lock)
    handle_render(screen, player, location, unit_size, move_lock=move_lock)

    # update display:
    pygame.display.flip()
    clock.tick(FPS)

    if frames == log_frame:
        log_time(start_time)
        frames = 0

pygame.quit()