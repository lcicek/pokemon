from pygame import time

from parameters import (
    VIEWPORT_WIDTH, UNIT_SIZE,
    X_HALF, Y_HALF,
    CENTER_X_RATIO, CENTER_Y_RATIO,
    WALKING, STANDING,
    FRAMES_PER_WALK, FRAMES_PER_STANDING_TURN
)

def handle_render(screen, player, location, move_lock):
    if move_lock.is_unlocked() or player.is_standing():
        x, y = target_render_position(player, location)
        renderGraphic(screen, location, x, y)
    else:
        x_diff = player.x - player.prev_x
        y_diff = player.y - player.prev_y

        x_increment = x_diff / FRAMES_PER_WALK
        y_increment = y_diff / FRAMES_PER_WALK

        current_x_increment = x_increment * move_lock.get_frame_number()
        current_y_increment = y_increment * move_lock.get_frame_number()

        x = player.prev_x + current_x_increment
        y = player.prev_y + current_y_increment

        x, y = current_render_position(x, y, location)

        print(x, y)
        renderGraphic(screen, location, x, y)

    renderPlayer(screen, player)

def renderPlayer(screen, player): # render player at center 
        render_x = screen.get_width() * CENTER_X_RATIO
        render_y = screen.get_height() * CENTER_Y_RATIO
        frame = player.animation.active_frame
        screen.blit(frame, (render_x, render_y))

def renderGraphic(screen, graphic, x, y): 
    screen.blit(graphic.scaled_image, (x, y))

def position_increment(graphic):
    return (UNIT_SIZE * graphic.scale) / FRAMES_PER_WALK

def current_render_position(x, y, graphic):
    current_x = (-x + X_HALF) * UNIT_SIZE * graphic.scale
    current_y = (-y + Y_HALF) * UNIT_SIZE * graphic.scale

    return current_x, current_y

def target_render_position(player, graphic):
    target_x = (-player.x + X_HALF) * UNIT_SIZE * graphic.scale
    target_y = (-player.y + Y_HALF) * UNIT_SIZE * graphic.scale

    return target_x, target_y

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale

def stop(player):
    player.update_action(STANDING)
    player.update_animation()

def turn(player, direction):
    player.update_direction(direction)
    player.update_animation()

    if player.is_walking():
        player.update_position(direction)

def walk(player, direction):
    print(player.move_frame)
    player.update_action(WALKING)
    player.update_direction(direction)
    player.update_animation()
    player.update_position(direction)

def update_movement_lock(executed_move, move_lock):
    if executed_move:
        move_lock.lock()

def execute_movement(input_direction, player):
    if input_direction is None and player.is_standing():
        return False

    player_stopped_moving = input_direction is None and player.is_walking()
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
        move_lock.try_unlock(player.is_standing())

        # move:
        #if player.isInBounds(location, controller.delta_x, controller.delta_y):
        #    player.updatePosition(controller.delta_x, controller.delta_y)
        #    walking_event.set()