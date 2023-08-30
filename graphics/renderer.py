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

        # set shift value for smooth location movement:
        if move_lock.is_newly_locked():
            self.update_shift(player, move_lock)

        # move the location:
        if move_lock.is_locked():    
            self.shift_location(move_lock)
        else:
            # check for correctness of location (especially after shifting it):
            assert self.location_x == -(player.x - X_HALF)*self.unit_size and self.location_y == -(player.y - Y_HALF)*self.unit_size

        # render the location:
        self.render_graphic(location.graphic)

        # render potential grass animations:
        if len(animator.grass_animations) > 0:
            self.render_grass(animator, player, move_lock) # also handles rendering of player because we render grass animations as: background grass => player => foreground grass
        else:
            self.render_player(animator)

        ## foreground elements ##
        if location.square_is_grass(row=player.y, col=player.x):
            self.render_grass_bottom(location, animator, player, move_lock)

        self.render_graphic(location.foreground_graphic)
        
        ## menu/pop-up elements ##
        if game_state == GAME_MENU:
            self.render_game_menu(game_menu)
        elif game_state == DIALOGUE:
            self.render_dialogue_box(dialogue_box)

        pygame.display.flip()

    def render_grass(self, animator, player, move_lock):
        """
        Depending on the player movement direction, the grass animation has to be rendered
        either in the foreground (above the player) or in the background (below the player).
        
        For upwards movement: first grass animation (head) = background and rest (tail) = foreground.
        For downwards movement: first grass animation (head) = foreground and rest (tail) = background.
        For horizontal movement: render whole grass animation in foreground.
        """        
        if player.is_moving_down():
            self.render_grass_tail(animator, player, move_lock)
            self.render_player(animator)
            self.render_grass_head(animator, player, move_lock)
        elif player.is_moving_up():
            self.render_grass_head(animator, player, move_lock)
            self.render_player(animator)
            self.render_grass_tail(animator, player, move_lock)
        else: # left/right movement
            self.render_player(animator)
            self.render_grass_head(animator, player, move_lock)
            self.render_grass_tail(animator, player, move_lock)

    def render_grass_tail(self, animator, player, move_lock):
        for animation in animator.grass_animations[:-1]:
            x, y = animation[0]
            x, y = self.get_grass_position(x, y, player, move_lock)
            frame = animation[1].get_frame()

            self.screen.blit(frame, (x, y))

    def render_grass_head(self, animator, player, move_lock):
        x, y = animator.grass_animations[-1][0]
        x, y = self.get_grass_position(x, y, player, move_lock)
        frame = animator.grass_animations[-1][1].get_frame()

        self.screen.blit(frame, (x, y))

    def render_grass_bottom(self, location, animator, player, move_lock):
        """
        Renders the bottom of a grass square in the foreground (above the player), to give
        the illusion that the player is standing in the grass.
        """
        if location.square_is_grass(row=player.y, col=player.x) and not player.is_moving_up():
            frame = animator.grass_bottom.scaled_image
            x, y = (player.x, player.y)
            x, y = self.get_grass_position(x, y, player, move_lock)

            self.screen.blit(frame, (x, y))

    def get_grass_position(self, x, y, player, move_lock):
        """
        Given a map (x, y) (e.g. (25, 13)), transforms it into a viewport (x, y) (e.g. (500, 250))
        and shifts it accordingly if player is moving.
        """
        x, y = self.map_to_window_position(x, y, player)

        if player.is_moving():
            x, y = self.shift_grass_animation(x, y, move_lock)
        
        return x, y

    def render_player(self, animator):
        self.screen.blit(animator.get_active_player_frame(), (self.player_x, self.player_y))

    def render_graphic(self, graphic):
        self.screen.blit(graphic.scaled_image, (self.location_x, self.location_y))

    def render_dialogue_box(self, dialogue_box):
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

    def render_game_menu(self, game_menu):
        self.render_infobox(game_menu)
        self.render_infobox_arrow(game_menu)

    def shift_location(self, move_lock):
        self.location_x += self.shift_x
        self.location_y += self.shift_y

        # prevent rounding errors (e.g.: shift = 1/30 = 0.33333 and 30/30 = 0.9999999):
        if move_lock.will_be_unlocked():
            self.location_x = round(self.location_x)
            self.location_y = round(self.location_y)

    def shift_grass_animation(self, x, y, move_lock):
        x += self.shift_x * move_lock.frames_since_start
        y += self.shift_y * move_lock.frames_since_start

        return x, y

    def update_shift(self, player, move_lock):
        """
        To ensure smooth player movement, the location has to be shifted by a small increment every
        frame. This function takes the current move duration (which differs for walking, sprinting etc.),
        and divides it into increments ("shifts") of 1/duration that are added/subtracted to the location
        position depending on the direction of the movement.
        """
        step_x, step_y = player.get_delta()

        # shift values are inverted since player moving right means shifting the location to the left
        self.shift_x = -(step_x / move_lock.lock_duration) * self.unit_size
        self.shift_y = -(step_y / move_lock.lock_duration) * self.unit_size

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