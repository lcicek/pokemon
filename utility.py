from parameters import VIEWPORT_WIDTH, VIEWPORT_HEIGHT

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale

def outOfBounds(center_x, center_y, screen_x, screen_y, image_width, image_height, scale, player_width, player_height):
    "checks if moving the screen would cause the center square to be outside of image"

    max_width = image_width * scale - center_x - player_width
    max_height = image_height * scale - center_y - player_height

    if screen_x > center_x:
        return True
    elif screen_y > center_y:
        return True
    elif -screen_x > max_width:
        return True
    elif -screen_y > max_height:
        return True
    else:
        return False

def renderLocation(screen, location, pos):
    screen.blit(location.scaled_img, pos)

def renderPlayer(screen, player):
    screen.blit(player.scaled_img, (player.x, player.y))