# Example file showing a basic pygame "game loop"
import pygame
from threading import Event

from parameters import viewport_width, viewport_height, screen_start
from controller import Controller

# pygame setup
pygame.init()
screen = pygame.display.set_mode((viewport_width, viewport_height))
clock = pygame.time.Clock()
running = True

move = Event()
controller = Controller(move)
image = pygame.image.load("SafariZone.png")
viewport = pygame.Rect(0, 0, viewport_width, viewport_height)

while running:
    # poll for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pygame.QUIT event means the user clicked X to close your window
            running = False
        
    # check for move event
    if move.is_set():
        viewport = viewport.move(controller.delta_x, controller.delta_y)
        move.clear()

    # clear surface:
    screen.fill("black")

    # render current viewport:
    screen.blit(image, screen_start, viewport)

    # update display:
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

controller.quit()
pygame.quit()