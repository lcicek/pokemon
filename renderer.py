import pygame

from constant.parameters import (
    DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT,
    X_HALF, Y_HALF, CENTER_X_RATIO, CENTER_Y_RATIO,
    UNIT_SIZE, DEFAULT_SCALE,
    GAME_MENU, DIALOGUE
)

class Renderer:
    def __init__(self, player) -> None:
        self.screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
        self.unit_size = UNIT_SIZE * DEFAULT_SCALE
        
        # render player at center:
        self.player_x = self.screen.get_width() * CENTER_X_RATIO
        self.player_y = self.screen.get_height() * CENTER_Y_RATIO

        self.location_x = -(player.x - X_HALF) * self.unit_size
        self.location_y = -(player.y - Y_HALF) * self.unit_size

    def render(self, player, location, animator, move_lock, game_state, game_menu, dialogue_box):
        self.screen.fill("black")

        self.update_shift(player, move_lock)
        self.shift_location()

        self.renderGraphic(location.graphic)
        self.renderPlayer(animator)
        self.renderGrass(animator, player, move_lock)
        self.renderGraphic(location.foreground_graphic)
        
        if game_state == GAME_MENU:
            self.renderGameMenu(game_menu)
        elif game_state == DIALOGUE:
            self.renderDialogueBox(dialogue_box)

        pygame.display.flip()

    def renderGrass(self, animator, player, move_lock):
        for i, anim in enumerate(animator.grass_animations):
            if len(animator.grass_animations) == 2:
                pass

            x, y = anim[0]
            x, y = self.map_to_window_position(x, y, player)

            if player.is_moving():
                x, y = self.shift_grass_animation(x, y, move_lock)
            
            frame = anim[1].get_frame()
            self.screen.blit(frame, (x, y))

    def renderPlayer(self, animator):
        self.screen.blit(animator.get_active_player_frame(), (self.player_x, self.player_y))

    def renderGraphic(self, graphic):
        self.screen.blit(graphic.scaled_image, (self.location_x, self.location_y))

    def renderDialogueBox(self, dialogue_box):
        x, y = self.render_infobox(dialogue_box)

        text_graphics, coordinates = dialogue_box.get_text_graphics()
        for i, graphic in enumerate(text_graphics):
            x_offset = coordinates[i][0] * self.unit_size
            y_offset = coordinates[i][1] * self.unit_size
            self.screen.blit(graphic, (x + x_offset, y + y_offset))

        if not dialogue_box.end_reached():
            self.render_infobox_arrow(dialogue_box)

    def render_infobox(self, infobox):
        x, y = infobox.get_position()
        x *= self.unit_size
        y *= self.unit_size
        self.screen.blit(infobox.get_graphic(), (x, y))

        return x, y

    def render_infobox_arrow(self, infobox):
        x, y = infobox.get_arrow_position()
        x *= self.unit_size
        y *= self.unit_size
        self.screen.blit(infobox.get_arrow_graphic(), (x, y))

    def renderGameMenu(self, game_menu):
        self.render_infobox(game_menu)
        self.render_infobox_arrow(game_menu)

    def shift_location(self):
        self.location_x += self.shift_x
        self.location_y += self.shift_y

    def shift_grass_animation(self, x, y, move_lock):
        x += self.shift_x * move_lock.frames_since_start
        y += self.shift_y * move_lock.frames_since_start

        return x, y

    def update_shift(self, player, move_lock):
        if player.is_standing() or player.bumped():
            assert self.location_x == -(player.x - X_HALF)*self.unit_size and self.location_y == -(player.y - Y_HALF)*self.unit_size
            self.shift_x = 0
            self.shift_y = 0
            return

        step_x, step_y = player.get_delta()
        total_steps = move_lock.lock_duration

        # shift values are inverted since player moving right means shifting the location to the left
        shift_x = -(step_x / total_steps)
        shift_y = -(step_y / total_steps)

        self.shift_x = shift_x * self.unit_size
        self.shift_y = shift_y * self.unit_size

    def map_to_window_position(self, x, y, player):
        """
        Transforms map position to window position. This is done by:
            1. Using the player position to calculate the viewport.
            2. Normalizing the viewport from (vp_x, vp_y) to (0, 0).
            3. Saving the difference tuple (-vp_x, -vp_y) and adding it to (x, y).
            4. Now each component in the viewport corresponds to a square on the window grid, where top-left=(0, 0) and bottom-right=(17, 13).
            5. Lastly, the viewport grid is multiplied by self.unit_size to account for unit length and window rescaling.
        """
        viewport_coordinate = player.get_viewport_coordinate()
        delta = player.get_delta()
        x -= viewport_coordinate[0] - delta[0]
        y -= viewport_coordinate[1] - delta[1]

        x *= self.unit_size
        y *= self.unit_size

        return x, y 

    def rescale(self, scale):
        self.screen = pygame.display.set_mode((VIEWPORT_WIDTH * scale, VIEWPORT_HEIGHT * scale), pygame.RESIZABLE)
        self.unit_size = UNIT_SIZE * scale

        self.player_x = self.screen.get_width() * CENTER_X_RATIO
        self.player_y = self.screen.get_height() * CENTER_Y_RATIO