from parameters import VIEWPORT_WIDTH, UNIT_SIZE, X_HALF, Y_HALF, CENTER_X_RATIO, CENTER_Y_RATIO

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale

def outOfBounds(player, location, delta_x, delta_y):
    """ Returns true if the move would cause the player to be out of bounds."""
    next_x = player.x + delta_x
    next_y = player.y + delta_y

    return next_x < 0 or next_y < 0 or next_x == location.width or next_y == location.height

def renderPlayer(screen, player): # render player at center 
    render_x = screen.get_width() * CENTER_X_RATIO
    render_y = screen.get_height() * CENTER_Y_RATIO
    screen.blit(player.graphic.scaled_img, (render_x, render_y))

def renderGraphic(screen, graphic, player): 
    render_x = (-player.x + X_HALF) * UNIT_SIZE * player.graphic.scale 
    render_y = (-player.y + Y_HALF) * UNIT_SIZE * player.graphic.scale
    screen.blit(graphic.scaled_img, (render_x, render_y))

def direction(key):
    if key == 'w': # up
        delta = [0, -1]
    elif key == 's': # down
        delta = [0, 1]
    elif key == 'a': # left
        delta = [-1, 0]
    elif key == 'd': # right
        delta = [1, 0]
    else:
        delta = None

    return delta