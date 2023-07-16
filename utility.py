from parameters import VIEWPORT_WIDTH, UNIT_SIZE

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale

def outOfBounds(player, location, delta_x, delta_y):
    """ Returns true if the move would cause the player to be out of bounds."""
    min_x = player.x
    min_y = player.y + player.scaled_width # only because width = height / 2

    # note: location.x and location.y are inverted (more details in function direction(key) (see below))
    max_x = -(location.scaled_width - player.x - player.scaled_width)
    max_y = -(location.scaled_height - player.y - player.scaled_height) # having width here is not a mistake

    if (location.x + delta_x > min_x or #  left
        location.x + delta_x < max_x or # right; to compare to max_x we have to invert location.x again
        location.y + delta_y > min_y or #  top
        location.y + delta_y < max_y): #  bottom; to compare to max_y we have to invert location.y again
        return True
    else:
        return False

def renderGraphic(screen, graphic):
    screen.blit(graphic.scaled_img, (graphic.x, graphic.y))


def direction(key):
    """ If key is in 'wasd', returns INVERTED direction, i.e. going left is not delta_x=-1 but delta_x = 1.
        That is because we move the image by shifting it across the screen (i.e. like moving a frame across an image).
        If the player goes left, he wants to discover more squares on the left. To reveal those squares,
        we move the image to the right: the previously right-most squares will now be hidden, the previously left-most
        squares will be at position 1, and the new squares will be at the new left-most position 0."""

    if key == 'w': # up
        delta = [0, 1]
    elif key == 's': # down
        delta = [0, -1]
    elif key == 'a': # left
        delta = [1, 0]
    elif key == 'd': # right
        delta = [-1, 0]
    else:
        delta = None

    return delta