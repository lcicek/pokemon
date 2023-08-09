import pygame

from parameters import (
    DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT,
    X_HALF, Y_HALF, CENTER_X_RATIO, CENTER_Y_RATIO,
    UNIT_SIZE, DEFAULT_SCALE
)

class Renderer:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
        self.unit_size = UNIT_SIZE * DEFAULT_SCALE

    def render(self, player, location, animator, move_lock):
        self.screen.fill("black")

        x, y = self.calculate_location_position(player, move_lock)

        self.renderGraphic(location.graphic, x, y)
        self.renderPlayer(animator)
        self.renderGraphic(location.foreground_graphic, x, y)

    def renderPlayer(self, animator): # render player at center 
            render_x = self.screen.get_width() * CENTER_X_RATIO
            render_y = self.screen.get_height() * CENTER_Y_RATIO
            frame = animator.active_player_animation.get_frame()
            self.screen.blit(frame, (render_x, render_y))

    def renderGraphic(self, graphic, x, y): 
        self.screen.blit(graphic.scaled_image, (x, y))

    def calculate_location_position(self, player, move_lock):
        player_did_not_walk = move_lock.is_unlocked() or player.is_standing()

        if player_did_not_walk or player.bumped():
            x, y = self.target_render_position(player)
        else:
            delta_x, delta_y = player.get_previous_delta()

            step = move_lock.frames_since_start
            num_frames = move_lock.lock_duration
            x = self.intermediate_position(player.prev_x, step, delta_x, num_frames)
            y = self.intermediate_position(player.prev_y, step, delta_y, num_frames)
            x, y = self.position_to_render_position(x, y)

        return x, y

    def target_render_position(self, player):
        target_x = (-player.x + X_HALF) * self.unit_size
        target_y = (-player.y + Y_HALF) * self.unit_size

        return target_x, target_y

    def intermediate_position(self, start_position, step, direction, num_frames):
        distance_per_step = direction / num_frames
        intermediate_position = start_position + step * distance_per_step

        return intermediate_position

    def position_to_render_position(self, x, y):
        x = (-x + X_HALF) * self.unit_size
        y = (-y + Y_HALF) * self.unit_size

        return x, y

    def rescale(self, scale):
        self.screen = pygame.display.set_mode((VIEWPORT_WIDTH * scale, VIEWPORT_HEIGHT * scale), pygame.RESIZABLE)
        self.unit_size = UNIT_SIZE * scale

