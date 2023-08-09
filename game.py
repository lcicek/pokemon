# Example file showing a basic pygame "game loop"
import pygame
import os

from lock import MovementLock
from animator import Animator
from location import Location
from player import Player
from parameters import *
from controller import Controller
from utility import *
from movementHandler import handle_input
from renderer import Renderer

# Set position window will open up at:
os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN

# SETUP PYGAME:
pygame.init()
clock = pygame.time.Clock()
running = True

# SETUP SPRITES:
player = Player()
location = Location(LOCATION_SPRITE, LOCATION_FOREGROUND)

controller = Controller()
animator = Animator()
renderer = Renderer()

### INIT LOCKS ###
move_lock = MovementLock()

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
            scale = calculate_scale(renderer.screen.get_width())
            scale_location(location, player, scale)
            renderer.rescale(scale)

    handle_input(controller, player, location, move_lock)
    animator.animate_player(player, move_lock)
    renderer.render(player, location, animator, move_lock)

    # update display:
    pygame.display.flip()
    clock.tick(FPS)

    if frames == log_frame:
        log_time(start_time)
        frames = 0

pygame.quit()