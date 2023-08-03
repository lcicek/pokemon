from pygame import time

from parameters import (
    VIEWPORT_WIDTH, UNIT_SIZE,
    X_HALF, Y_HALF,
    CENTER_X_RATIO, CENTER_Y_RATIO,
    WALKING, STANDING, LEFT
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

def update_player(player, action, direction):
    player.update_action(action)
    player.update_direction(direction)
    player.update_position(direction)
    player.update_animation()

def stop(player):
    player.update_action(STANDING)
    player.update_animation()

def turn(player, direction):
    update_player(player, STANDING, direction)

def walk(player, direction):
    update_player(player, WALKING, direction)

def update_movement_lock(executed_move, move_lock):
    if executed_move:
        start_time = time.get_ticks()
        move_lock.lock(start_time)

def execute_movement(input_direction, player):
    if input_direction is None and player.is_standing():
        return False

    player_stopped_moving = input_direction is None and not player.is_standing()
    direction_is_new = player.direction != input_direction

    if player_stopped_moving:
        stop(player)
    elif direction_is_new:
        turn(player, input_direction)
    else:
        walk(player, input_direction)
    
    return True

def handle_input(controller, player, move_lock):
    input_direction = controller.listen()

    if move_lock.is_unlocked():
        executed_move = execute_movement(input_direction, player)
        update_movement_lock(executed_move, move_lock)
    else:
        move_lock.try_unlock()

        # move:
        #if player.isInBounds(location, controller.delta_x, controller.delta_y):
        #    player.updatePosition(controller.delta_x, controller.delta_y)
        #    walking_event.set()