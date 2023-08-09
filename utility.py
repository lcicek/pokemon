from pygame import time
import psutil
import os
from psutil import cpu_percent, virtual_memory
from constant.parameters import VIEWPORT_WIDTH, MIN_SCALE, MAX_SCALE, TIME_PER_FRAME_MS

def scale_location(location, scale):
    location.graphic.rescale(scale)
    location.foreground_graphic.rescale(scale)

def calculate_scale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    scale = min(scale, MAX_SCALE)
    scale = max(scale, MIN_SCALE)

    return scale

def log(start_time):
    time_info = f"Time: (target={TIME_PER_FRAME_MS}ms, actual={(time.get_ticks() - start_time)}ms). "
    cpu_info = f"CPU: {cpu_percent()}%. "
    memory_rss_info = f"RSS: {psutil.Process(os.getpid()).memory_info()[0] >> 20}MB. "
    memory_vms_info = f"VMS: {psutil.Process(os.getpid()).memory_info()[1] >> 20}MB. "

    print(time_info + cpu_info + memory_rss_info + memory_vms_info)