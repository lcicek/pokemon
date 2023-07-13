# Example file showing a basic pygame "game loop"
import pygame
from threading import Event

from view import View
from parameters import SCREEN_POS, X, Y
from controller import Controller
from utility import *

BASE = 8
UNIT = BASE * 2

# init view
view = View(X, Y, UNIT)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((view.width, view.height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

move = Event()
controller = Controller(move)
image = pygame.image.load("SafariZone.png")
viewport = pygame.Rect(0, 0, view.width, view.height)

player = pygame.image.load("player.png")

while running:
    # poll for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.VIDEORESIZE:
            unit = newUnit(event.dict['size'])
            view.setUnit(unit) # updates width and height internally

            # screen = pygame.transform.scale(screen, (w, h))
            screen = pygame.display.set_mode((view.width, view.height), pygame.RESIZABLE)

    # check for move event
    if move.is_set():
        viewport = viewport.move(controller.delta_x * UNIT, controller.delta_y * UNIT)
        move.clear()

    # clear surface:
    screen.fill("black")

    # render current viewport:
    renderViewport(screen, image, viewport)
    renderPlayer(screen, player, (view.center_width, view.center_height))

    # update display:
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

controller.quit()
pygame.quit()