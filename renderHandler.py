from parameters import (
    UNIT_SIZE,
    X_HALF, Y_HALF, CENTER_X_RATIO, CENTER_Y_RATIO,
    FRAMES_PER_WALK,
)

def handle_render(screen, player, location, move_lock):
    x, y = calculate_location_position(player, location, move_lock)
    renderGraphic(screen, location, x, y)
    renderPlayer(screen, player)

def renderPlayer(screen, player): # render player at center 
        render_x = screen.get_width() * CENTER_X_RATIO
        render_y = screen.get_height() * CENTER_Y_RATIO
        frame = player.animation.active_frame
        screen.blit(frame, (render_x, render_y))

def renderGraphic(screen, graphic, x, y): 
    screen.blit(graphic.scaled_image, (x, y))

def calculate_location_position(player, location, move_lock):
    player_did_not_walk = move_lock.is_unlocked() or player.is_standing()

    if player_did_not_walk or player.bumped():
        x, y = target_render_position(player, location)
    else:
        delta_x, delta_y = player.get_previous_delta()

        x = intermediate_position(player.prev_x, move_lock.frame_count(), delta_x)
        y = intermediate_position(player.prev_y, move_lock.frame_count(), delta_y)
        x, y = position_to_render_position(x, y, location)

    return x, y

def target_render_position(player, graphic):
    target_x = (-player.x + X_HALF) * UNIT_SIZE * graphic.scale
    target_y = (-player.y + Y_HALF) * UNIT_SIZE * graphic.scale

    return target_x, target_y

def intermediate_position(start_position, step_number, direction):
    distance_per_step = direction / FRAMES_PER_WALK
    intermediate_position = start_position + step_number * distance_per_step

    return intermediate_position

def position_to_render_position(x, y, graphic):
    x = (-x + X_HALF) * UNIT_SIZE * graphic.scale
    y = (-y + Y_HALF) * UNIT_SIZE * graphic.scale

    return x, y
