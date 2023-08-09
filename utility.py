from pygame import time
from psutil import cpu_percent
from parameters import VIEWPORT_WIDTH, MAX_SCALE, TIME_PER_FRAME_MS

def scale_location(location, scale):
    location.graphic.rescale(scale)
    location.foreground_graphic.rescale(scale)

def calculate_scale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    scale = min(scale, MAX_SCALE)
    return scale

def log_time(start_time):
    print(f"Time: (target={TIME_PER_FRAME_MS}ms, actual={(time.get_ticks() - start_time)}ms). CPU: {cpu_percent()}%")