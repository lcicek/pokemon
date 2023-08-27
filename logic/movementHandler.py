from constant.parameters import (
    WALKING, STANDING, JUMPING, SPRINTING,
    LEFT, RIGHT, UP,
    FRAMES_PER_TURN, FRAMES_PER_WALK, FRAMES_PER_SPRINT, FRAMES_PER_JUMP, 
    B
)

def handle_movement(controller, player, location, move_lock, outside_lock):
    if outside_lock.is_unlocked() and move_lock.is_unlocked():
        direction = controller.active_movement_key
        sprinting = controller.b_toggled
        movement_duration = execute_movement(direction, player, location, sprinting=sprinting)
        
        if movement_duration > 0:
            move_lock.lock(movement_duration)

def execute_movement(input_direction, player, location, sprinting=False):
    if input_direction is None and player.is_standing(): # player stands and there is no new input:
        return 0

    player_stopped_moving = input_direction is None and player.is_moving()
    direction_is_new = player.direction != input_direction

    if player_stopped_moving:
        stop(player)
        return 0
    
    if direction_is_new and player.is_standing():
        turn(player, input_direction)
        return FRAMES_PER_TURN
    elif next_square_is_jumpable(player, location, input_direction):
        jump(player, input_direction)
        return FRAMES_PER_JUMP
    elif next_square_is_walkable(player, location, input_direction) and sprinting:
        sprint(player, input_direction)
        return FRAMES_PER_SPRINT
    elif next_square_is_walkable(player, location, input_direction) and not sprinting:
        walk(player, input_direction)
        return FRAMES_PER_WALK
    else:
        action = SPRINTING if sprinting else WALKING
        bump(player, input_direction, action=action)
        return FRAMES_PER_SPRINT if action == SPRINTING else FRAMES_PER_WALK

def stop(player):
    player.update(action=STANDING)

def turn(player, direction):
    player.update(direction=direction)
    player.update_previous_position()

def bump(player, direction, action):
    player.update(action=action, direction=direction)
    player.update_previous_position() # when bumping: previous position = current position
    
def jump(player, direction):
    player.update(action=JUMPING, direction=direction, move=True)

def walk(player, direction):
    player.update(action=WALKING, direction=direction, move=True)

def sprint(player, direction):
    player.update(action=SPRINTING, direction=direction, move=True)

def next_square_is_jumpable(player, location, direction):
    next_x, next_y = player.next_coordinates(direction)
    
    return location.square_is_jumping_ledge(next_y, next_x, direction)

def next_square_is_walkable(player, location, direction):
    next_x, next_y = player.next_coordinates(direction)
    next_blocks = location.square_is_solid(next_y, next_x, direction)
    
    return not (next_blocks or next_is_out_of_bounds(next_x, next_y, location))

def next_is_out_of_bounds(next_x, next_y, location):
    return not next_is_in_bounds(next_x, next_y, location)

def next_is_in_bounds(next_x, next_y, location):
    return next_x >= 0 and next_y >= 0 and next_x < location.width and next_y < location.height