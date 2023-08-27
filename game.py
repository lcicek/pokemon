import os
import pygame

from constant.paths import LOCATION_SPRITE, LOCATION_FOREGROUND
from constant.parameters import *
from graphics.animator import Animator
from graphics.renderer import Renderer
from graphics.infoBox import GameMenu, DialogueBox

from logic.location import Location
from logic.player import Player
from controller import Controller
from logic.lock import Lock, MovementLock
from utility import *

import logic.movementHandler as movementHandler

os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOW_SPAWN # window starting position on screen

### SETUP ###
pygame.init()
pygame.display.set_caption(WINDOW_CAPTION)
clock = pygame.time.Clock()
running = True

game_state = OUTSIDE

player = Player()
location = Location(LOCATION_SPRITE, LOCATION_FOREGROUND)

controller = Controller(game_state)
animator = Animator()
renderer = Renderer(player)

game_menu = GameMenu()
dialogue_box = DialogueBox()

### LOCKS ###
move_lock = MovementLock()
outside_lock = Lock()
arrow_lock = MovementLock()
dialogue_lock = MovementLock()

### LOG ###
frames = 0
log_frame = FPS * 5

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
            game_menu.rescale(scale)
            dialogue_box.rescale(scale)

    controller.listen()

    current_state = update_game_state(controller, move_lock, outside_lock, player, location, game_menu, dialogue_box, dialogue_lock)
    
    if game_state != current_state:
        game_state = current_state
        controller.set_state(current_state)

    if game_state == OUTSIDE:
        movementHandler.handle_movement(controller, player, location, move_lock, outside_lock)
    elif game_state == GAME_MENU:
        handle_menu_navigation(controller, game_menu, outside_lock, arrow_lock, move_lock, player)
    elif game_state == DIALOGUE:
        handle_dialogue(controller, player, dialogue_box, move_lock, outside_lock, dialogue_lock)

    animator.animate(location, player, move_lock)
    renderer.render(player, location, animator, move_lock, game_state, game_menu, dialogue_box)

    clock.tick(FPS)

    if frames == log_frame:
        log(start_time)
        frames = 0

pygame.quit()