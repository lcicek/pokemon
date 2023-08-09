import os
import pygame

from lock import MovementLock
from animator import Animator
from location import Location
from player import Player
from constant.paths import LOCATION_SPRITE, LOCATION_FOREGROUND
from constant.parameters import *
from controller import Controller
from utility import *
from movementHandler import handle_input
from renderer import Renderer

os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN # window starting position on screen

### SETUP ###
pygame.init()
pygame.display.set_caption(WINDOW_CAPTION)
clock = pygame.time.Clock()
running = True

player = Player()
location = Location(LOCATION_SPRITE, LOCATION_FOREGROUND)

controller = Controller()
animator = Animator()
renderer = Renderer()

### LOCKS ###
move_lock = MovementLock()

### LOG ###
frames = 0
log_frame = FPS * 10

while running:
    start_time = pygame.time.get_ticks()
    frames += 1

    # poll for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            scale = calculate_scale(renderer.screen.get_width())
            animator.rescale(scale)
            scale_location(location, scale)
            renderer.rescale(scale)

    handle_input(controller, player, location, move_lock)
    animator.animate_player(player, move_lock)
    renderer.render(player, location, animator, move_lock)

    clock.tick(FPS)

    if frames == log_frame:
        log(start_time)
        frames = 0

pygame.quit()