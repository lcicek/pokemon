# Example file showing a basic pygame "game loop"
import pygame
from pygame import display, RESIZABLE

from threading import Event

from view import View
from parameters import DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from controller import Controller
from renderer import Renderer
from location import Location
from utility import *

# INITIALIZE:
player = pygame.image.load("player.png")
location = Location("SafariZone.png", "safari_zone")
view = View(location.surface)
renderer = Renderer(location=location)
move = Event()
controller = Controller(move)

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

    # check for move event
    if move.is_set():
        view.updateViewport(controller.delta_x, controller.delta_y)
        move.clear()

    # clear surface:
    screen.fill("black")

    # render current viewport:
    renderer.renderViewport(screen, view.surface)
    renderer.renderPlayer(screen, player)

    # update display:
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

controller.quit()
pygame.quit()