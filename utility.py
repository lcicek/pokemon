from pygame import time
import psutil
import os
from psutil import cpu_percent
from constant.parameters import (
    VIEWPORT_WIDTH,
    MIN_SCALE, MAX_SCALE,
    TIME_PER_FRAME_MS, FRAMES_PER_SELECT,
    START, A, B
)

def handle_menu(controller, game_menu, outside_lock, arrow_lock):
    menu_was_opened = controller.action_keys[START]
    menu_was_closed = game_menu.can_be_closed() and (controller.action_keys[B] or controller.action_keys[START])

    if game_menu.is_open() and menu_was_closed:
        game_menu.close_menu(outside_lock)
        return
    
    if game_menu.is_closed() and menu_was_opened:
        game_menu.open_menu(outside_lock)
        return
    
    if game_menu.is_open():
        if arrow_lock.is_locked():
            arrow_lock.update()

        if arrow_lock.is_unlocked() and controller.has_movement_input():
            game_menu.move_arrow(controller.active_movement_key)
            arrow_lock.lock(FRAMES_PER_SELECT)
        elif arrow_lock.is_unlocked() and controller.action_keys[A]:
            game_menu.select(outside_lock)

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