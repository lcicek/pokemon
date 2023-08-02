from time import perf_counter_ns
from pygame.time import delay

from parameters import (
    VIEWPORT_WIDTH, UNIT_SIZE,
    X_HALF, Y_HALF,
    CENTER_X_RATIO, CENTER_Y_RATIO,
    TURN_DURATION, NS_TO_MS_RATIO, MOVE_DURATION,
    WALKING, STANDING
)

def handle_render(screen, player):
    renderPlayer(screen, player)

def renderPlayer(screen, player): # render player at center 
        render_x = screen.get_width() * CENTER_X_RATIO
        render_y = screen.get_height() * CENTER_Y_RATIO
        frame = player.animation.active_frame
        screen.blit(frame, (render_x, render_y))

def renderGraphic(screen, graphic, player): 
    render_x = (-player.x + X_HALF) * UNIT_SIZE * player.idle_graphic.scale 
    render_y = (-player.y + Y_HALF) * UNIT_SIZE * player.idle_graphic.scale
    screen.blit(graphic.scaled_img, (render_x, render_y))

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale

def relative_delay(start_time):
    elapsed_time_ns = perf_counter_ns() - start_time
    elapsed_time_ms = elapsed_time_ns / NS_TO_MS_RATIO
    remaining_time_ms = TURN_DURATION - elapsed_time_ms

    if remaining_time_ms > 0:
        delay(int(remaining_time_ms)) # temporarily decreases fps because MOVE_DURATION / TIME_PER_FRAME frames are skipped

def update_player(player, state, direction):
    player.update_action(state)
    player.update_direction(direction)
    player.update_position(direction)
    player.update_animation()

def handle_movement(key_press_event, controller, player):
    key_is_pressed = key_press_event.is_set()

    if not key_is_pressed and player.is_standing(): # player did nothing
        return
    
    if key_is_pressed and player.is_standing() and player.turns(controller.direction):
        # allow small interval to enable player to turn without moving (via quick press and release of key)
        relative_delay(controller.press_start_time)
        update_player(player, STANDING, controller.direction)
    elif key_is_pressed: # player moves
        #if player.is_in_bounds(location, controller.delta_x, controller.delta_y):
        delay(MOVE_DURATION)
        update_player(player, WALKING, controller.direction)
    else: # player stopped moving
        update_player(player, STANDING, controller.direction)

        # move:
        #if player.isInBounds(location, controller.delta_x, controller.delta_y):
        #    player.updatePosition(controller.delta_x, controller.delta_y)
        #    walking_event.set()