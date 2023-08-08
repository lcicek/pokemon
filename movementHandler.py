from parameters import (
    WALKING, STANDING, JUMPING, SPRINTING,
    LEFT, RIGHT, UP
)

def handle_input(controller, player, location, move_lock):
    controller.listen()

    if move_lock.is_unlocked():
        direction = controller.active_movement_key
        sprinting = controller.b
        executed_move = execute_movement(direction, player, location, sprinting=sprinting)
        
        if executed_move:
            move_lock.lock(player)
    else:
        unlocked = move_lock.try_unlock()

        if not unlocked and player.is_jumping():
            player.animation.next_keyframe(move_lock.frame_count(), player.get_move_state())

def execute_movement(input_direction, player, location, sprinting=False):
    if input_direction is None and player.is_standing(): # player stands and there is no new input:
        return False

    player_stopped_moving = input_direction is None and (player.is_walking() or player.is_jumping() or player.is_sprinting())
    direction_is_new = player.direction != input_direction

    if player_stopped_moving:
        stop(player)
        return False
    
    if direction_is_new and player.is_standing():
        turn(player, input_direction)
    elif next_square_is_jumpable(player, location, input_direction):
        jump(player, input_direction)
    elif next_square_is_walkable(player, location, input_direction) and sprinting:
        sprint(player, input_direction)
    elif next_square_is_walkable(player, location, input_direction) and not sprinting:
        walk(player, input_direction)
    else:
        bump(player, input_direction, action=SPRINTING if sprinting else WALKING)
    
    return True

def stop(player):
    player.update(action=STANDING)

def turn(player, direction):
    player.update(direction=direction)

def bump(player, direction, action):
    player.update(action=action, direction=direction)
    player.update_previous_position() # when bumping: previous position = current position
    
def jump(player, direction):
    player.update(action=JUMPING, direction=direction, move=True)

def walk(player, direction):
    player.update(action=WALKING, direction=direction, move=True)

def sprint(player, direction):
    player.update(action=SPRINTING, direction=direction, move=True)

def next_coordinates(player, direction):
        next_x = player.x
        next_y = player.y

        if direction == LEFT:
            next_x -= 1
        elif direction == RIGHT:
            next_x += 1
        elif direction == UP:
            next_y -= 1
        else:
            next_y += 1

        return next_x, next_y

def next_square_is_jumpable(player, location, direction):
    next_x, next_y = next_coordinates(player, direction)
    
    return location.square_is_jumping_ledge(next_y, next_x, direction)

def next_square_is_walkable(player, location, direction):
    next_x, next_y = next_coordinates(player, direction)
    next_blocks = location.square_is_solid(next_y, next_x, direction)
    
    return not (next_blocks or next_is_out_of_bounds(next_x, next_y, location))

def next_is_out_of_bounds(next_x, next_y, location):
    return not next_is_in_bounds(next_x, next_y, location)

def next_is_in_bounds(next_x, next_y, location):
    return next_x >= 0 and next_y >= 0 and next_x < location.width and next_y < location.height