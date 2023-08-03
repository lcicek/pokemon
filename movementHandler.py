from parameters import WALKING, STANDING

def handle_input(controller, player, location, move_lock):
    input_direction = controller.listen()

    if move_lock.is_unlocked():
        executed_move = execute_movement(input_direction, player, location)
        
        if executed_move:
            move_lock.lock()
    else:
        move_lock.try_unlock(player.is_walking())

def execute_movement(input_direction, player, location):
    # case: player stands and there is no new input
    if input_direction is None and player.is_standing():
        return False

    player_stopped_moving = input_direction is None and player.is_walking()
    direction_is_new = player.direction != input_direction

    if player_stopped_moving:
        stop(player)
        return False
    
    if direction_is_new and player.is_standing():
        turn(player, input_direction)
    else:
        # move:
        if player.next_is_out_of_bounds(location, input_direction):
            bump(player, input_direction)
        else:
            walk(player, input_direction)
    
    return True

def stop(player):
    player.update_action(STANDING)
    player.update_animation()

def turn(player, direction):
    player.update_direction(direction)
    player.update_animation()

def bump(player, direction):
    player.update_action(WALKING)
    player.update_direction(direction)
    player.update_animation()
    player.update_previous_position()
    player.next_move_frame()
    

def walk(player, direction):
    player.update_action(WALKING)
    player.update_direction(direction)
    player.update_animation()
    player.update_position(direction)