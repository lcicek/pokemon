from parameters import UNIT_SIZE, X_HALF, Y_HALF, CENTER_X_RATIO, CENTER_Y_RATIO

class Renderer:
    def __init__(self) -> None:
        pass

    def renderPlayer(screen, player): # render player at center 
        render_x = screen.get_width() * CENTER_X_RATIO
        render_y = screen.get_height() * CENTER_Y_RATIO
        screen.blit(player.graphic.scaled_img, (render_x, render_y))

    def renderGraphic(screen, graphic, player): 
        render_x = (-player.x + X_HALF) * UNIT_SIZE * player.graphic.scale 
        render_y = (-player.y + Y_HALF) * UNIT_SIZE * player.graphic.scale
        screen.blit(graphic.scaled_img, (render_x, render_y))