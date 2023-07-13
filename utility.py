from parameters import SCREEN_POS, ASPECT_RATIO, BASE, X

def renderViewport(screen, image, viewport, pos=SCREEN_POS):
    screen.blit(image, pos, viewport)

def renderPlayer(screen, image, pos):
    screen.blit(image, pos)

def roundToBase(x): # rounds x to the closest multiple of base
    x = BASE * round(x / BASE)

    if x == 0:
        return BASE
    else:
        return x

def newUnit(size):
    unit = round(size[0] / X)
    unit = roundToBase(unit)

    return unit