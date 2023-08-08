from parameters import (
    X_HALF, Y_HALF, CENTER_X_RATIO, CENTER_Y_RATIO,
    FRAMES_PER_WALK, FRAMES_PER_JUMP, FRAMES_PER_SPRINT
)

def handle_render(screen, player, location, unit_size, move_lock):
    x, y = calculate_location_position(player, unit_size, move_lock)
    renderGraphic(screen, location.graphic, x, y)
    renderPlayer(screen, player)
    renderGraphic(screen, location.foreground_graphic, x, y)

def renderPlayer(screen, player): # render player at center 
        render_x = screen.get_width() * CENTER_X_RATIO
        render_y = screen.get_height() * CENTER_Y_RATIO
        frame = player.animation.active_frame
        screen.blit(frame, (render_x, render_y))

def renderGraphic(screen, graphic, x, y): 
    screen.blit(graphic.scaled_image, (x, y))

def calculate_location_position(player, scale, move_lock):
    player_did_not_walk = move_lock.is_unlocked() or player.is_standing()

    if player_did_not_walk or player.bumped():
        x, y = target_render_position(player, scale)
    else:
        delta_x, delta_y = player.get_previous_delta()

        num_frames = get_num_frames(player)
        current_step = move_lock.frame_count()

        x = intermediate_position(player.prev_x, current_step, delta_x, num_frames)
        y = intermediate_position(player.prev_y, current_step, delta_y, num_frames)
        x, y = position_to_render_position(x, y, scale)

    return x, y

def get_num_frames(player):
    if player.is_walking():
        return FRAMES_PER_WALK
    elif player.is_sprinting():
        return FRAMES_PER_SPRINT
    else:
        return FRAMES_PER_JUMP

def target_render_position(player, unit_size):
    target_x = (-player.x + X_HALF) * unit_size
    target_y = (-player.y + Y_HALF) * unit_size

    return target_x, target_y

def intermediate_position(start_position, step_number, direction, num_frames):
    distance_per_step = direction / num_frames
    intermediate_position = start_position + step_number * distance_per_step

    return intermediate_position

def position_to_render_position(x, y, unit_size):
    x = (-x + X_HALF) * unit_size
    y = (-y + Y_HALF) * unit_size

    return x, y
