# Example file showing a basic pygame "game loop"
import pygame
from pygame import display, RESIZABLE

from threading import Event
from parameters import *
from controller import Controller
from renderer import Renderer
from location import Location
from utility import *

# EVENTS:
key_press_event = Event()

# INITIALIZE:
player = pygame.image.load("player.png")
location = Location("SafariZone.png", "safari_zone")
renderer = Renderer(location=location)
controller = Controller(key_press_event)
screen_x = SCREEN_POS[0]
screen_y = SCREEN_POS[1]

# SETUP PYGAME:
pygame.init()
screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

while running:
    # poll for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.VIDEORESIZE:
            scale = calculateScale(screen.get_width()) # screen.get_width() = event.dict['size][0]
            renderer.updateScale(scale)
            screen = display.set_mode((VIEWPORT_WIDTH * scale, VIEWPORT_HEIGHT * scale), RESIZABLE)

    # clear surface:
    screen.fill("black")

    # check for move event
    if key_press_event.is_set():
        delta_x = controller.delta_x * UNIT_SIZE * renderer.scale
        delta_y = controller.delta_y * UNIT_SIZE * renderer.scale

        screen_x -= delta_x
        screen_y -= delta_y

        key_press_event.clear()

    renderer.renderLocation(screen, location.surface, (screen_x, screen_y))
    renderer.renderPlayer(screen, player)

    # update display:
    pygame.display.flip()

    clock.tick(20)  # limits FPS to 60

controller.quit()
pygame.quit()