from time import perf_counter_ns
from pygame.time import delay

from parameters import (
    VIEWPORT_WIDTH, UNIT_SIZE,
    X_HALF, Y_HALF,
    CENTER_X_RATIO, CENTER_Y_RATIO,
    TURN_TIME, NS_TO_MS_RATIO
)

def renderPlayer(screen, player): # render player at center 
        render_x = screen.get_width() * CENTER_X_RATIO
        render_y = screen.get_height() * CENTER_Y_RATIO
        screen.blit(player.idle_graphic.scaled_img, (render_x, render_y))

def renderGraphic(screen, graphic, player): 
    render_x = (-player.x + X_HALF) * UNIT_SIZE * player.idle_graphic.scale 
    render_y = (-player.y + Y_HALF) * UNIT_SIZE * player.idle_graphic.scale
    screen.blit(graphic.scaled_img, (render_x, render_y))

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale

def delay_movement(start_time):
    elapsed_time_ns = perf_counter_ns() - start_time
    elapsed_time_ms = elapsed_time_ns / NS_TO_MS_RATIO
    remaining_time_ms = TURN_TIME - elapsed_time_ms

    if remaining_time_ms > 0:
        delay(int(remaining_time_ms))
    
def handle_movement(key_press_event, controller):
    if key_press_event.is_set():
        delay_movement(controller.press_start_time)

        if not key_press_event.is_set(): # if key was released quickly
            print("turn occured")
            pass

        # move:
        #if player.isInBounds(location, controller.delta_x, controller.delta_y):
        #    player.updatePosition(controller.delta_x, controller.delta_y)
        #    walking_event.set()