from parameters import unit

def move(key): # returns delta_x, delta_y
    delta = [0, 0] # delta_x, delta_y

    if key == 'w': # up
        delta[1] += -1
    elif key == 's': # down
        delta[1] += 1
    elif key == 'a': # left
        delta[0] += -1
    elif key == 'd': # right
        delta[0] += 1

    delta[0] *= unit
    delta[1] *= unit

    return delta[0], delta[1]