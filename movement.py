def move(key):
    pos_delta = (0, 0) # x, y

    if key == 'w': # up
        pos_delta[1] += 1
    elif key == 's': # down
        pos_delta[1] += -1
    elif key == 'a': # left
        pos_delta[0] += -1
    elif key == 'd': # right
        pos_delta[0] += 1

    
    