from pygame import time
import psutil
import os
from interactor import Interactor
from psutil import cpu_percent
from movementHandler import stop
from constant.parameters import (
    VIEWPORT_WIDTH,
    MIN_SCALE, MAX_SCALE,
    TIME_PER_FRAME_MS, FRAMES_PER_SELECT,
    START, A, B,
    OUTSIDE, GAME_MENU, DIALOGUE
)

# similar to handle_menu_navigation:
def handle_dialogue(controller, player, dialogue_box, move_lock, outside_lock, dialogue_lock):
    if move_lock.is_locked(): # wait for movement to finish before enabling menu actions
        return

    if not player.is_standing(): # set player state to standing while game menu is open
        stop(player)

    dialogue_will_be_closed = dialogue_box.is_active() and dialogue_box.end_reached() and (controller.action_keys[A] or controller.action_keys[B])

    if dialogue_will_be_closed:
        dialogue_box.close()
        outside_lock.unlock()
        return

    if dialogue_lock.is_locked():
        dialogue_lock.update()

    if dialogue_lock.is_unlocked() and (controller.action_keys[A] or controller.action_keys[B]):
        dialogue_box.next()
        dialogue_lock.lock(FRAMES_PER_SELECT)

def try_to_open_game_menu(controller, outside_lock, player, game_menu):
    if controller.action_keys[START]: # start was pressed = game menu was opened
        game_menu.open()
        outside_lock.lock()
        controller.action_keys[START] = False

def try_to_open_dialogue(controller, outside_lock, player, location, dialogue_box):
    if controller.action_keys[A]:
        next_x, next_y = player.next_coordinates()
        interactor = location.map[next_x][next_y]

        if isinstance(interactor, Interactor):
            dialogue_box.open(interactor.text)
            outside_lock.lock()
            controller.action_keys[A] = False

def update_game_state(controller, move_lock, outside_lock, player, location, game_menu, dialogue_box):
    if move_lock.is_locked():
        move_lock.update()

    if outside_lock.is_unlocked() and game_menu.is_inactive(): # if game menu is closed and no other state has locked outside
        try_to_open_game_menu(controller, outside_lock, player, game_menu)

    if game_menu.is_active():
        return GAME_MENU

    if outside_lock.is_unlocked() and dialogue_box.is_inactive():
        try_to_open_dialogue(controller, outside_lock, player, location, dialogue_box)

    if dialogue_box.is_active():
        return DIALOGUE

    # ... check for other states here
    
    return OUTSIDE

def handle_menu_navigation(controller, game_menu, outside_lock, arrow_lock, move_lock, player):
    if move_lock.is_locked(): # wait for movement to finish before enabling menu actions
        return

    if not player.is_standing(): # set player state to standing while game menu is open
        stop(player)

    game_menu_will_be_closed = game_menu.is_active() and (controller.action_keys[B] or controller.action_keys[START] or (controller.action_keys[A] and game_menu.arrow_at_exit()))

    if game_menu_will_be_closed:
        game_menu.close()
        outside_lock.unlock()
        return

    if arrow_lock.is_locked():
        arrow_lock.update()

    if arrow_lock.is_unlocked() and controller.has_movement_input():
        game_menu.move_arrow(controller.active_movement_key)
        arrow_lock.lock(FRAMES_PER_SELECT)

def scale_location(location, scale):
    location.graphic.rescale(scale)
    location.foreground_graphic.rescale(scale)

def calculate_scale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    scale = min(scale, MAX_SCALE)
    scale = max(scale, MIN_SCALE)

    return scale

def log(start_time):
    time_info = f"Time: (target={TIME_PER_FRAME_MS}ms, actual={(time.get_ticks() - start_time)}ms). "
    cpu_info = f"CPU: {cpu_percent()}%. "
    memory_rss_info = f"RSS: {psutil.Process(os.getpid()).memory_info()[0] >> 20}MB. "
    memory_vms_info = f"VMS: {psutil.Process(os.getpid()).memory_info()[1] >> 20}MB. "

    print(time_info + cpu_info + memory_rss_info + memory_vms_info)