from pygame import display, RESIZABLE
from pygame import time
from parameters import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, MAX_SCALE, TIME_PER_FRAME_MS

def scale_graphics(location, player, scale):
    player.animation.rescale(scale)
    player.update_animation()

    location.graphic.rescale(scale)
    location.foreground_graphic.rescale(scale)
    
def get_scaled_screen(scale):
    return display.set_mode((VIEWPORT_WIDTH * scale, VIEWPORT_HEIGHT * scale), RESIZABLE)

def calculate_scale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    scale = min(scale, MAX_SCALE)
    return scale

def log_time(start_time):
    print(f"Time: (target={TIME_PER_FRAME_MS}ms, actual={(time.get_ticks() - start_time)}ms)")