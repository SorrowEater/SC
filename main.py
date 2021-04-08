import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Suchli Crad!"
MOVEMENT_SPEED = 5
PLAYER_SCALE = 0.35
VIEWPORT_MARGIN = 40


class SCO(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        self.background = arcade.load_texture('images/background.bmp')
        self.right_pressed = None
        self.left_pressed = None
        self.down_pressed = None
        self.up_pressed = None
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.AMAZON)
        self.player_sprite = None
        self.player_sprite = arcade.Sprite('images/PlayerUp.bmp', PLAYER_SCALE)
        self.player_sprite.append_texture(arcade.load_texture('images/PlayerDown.bmp'))
        self.player_sprite.append_texture(arcade.load_texture('images/PlayerLeft.bmp'))
        self.player_sprite.append_texture(arcade.load_texture('images/PlayerRight.bmp'))
        self.player_sprite.append_texture(arcade.load_texture('images/PlayerUp.bmp'))
        self.set_fullscreen(True)
        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.view_left = 0
        self.view_bottom = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        if self.left_pressed and not self.up_pressed and not self.down_pressed:
            self.player_sprite.set_texture(2)
        if self.right_pressed and not self.up_pressed and not self.down_pressed:
            self.player_sprite.set_texture(3)
        if self.up_pressed and not self.right_pressed and not self.left_pressed:
            self.player_sprite.set_texture(4)
        if self.down_pressed and not self.left_pressed and not self.right_pressed:
            self.player_sprite.set_texture(1)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, 2048, 1200, self.background)
        self.player_sprite.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_sprite.update()
        # --- Manage Scrolling ---
        # Keep track of if we changed the boundary. We don't want to call the
        # set_viewport command if we didn't change the view port.
        changed = False

        if self.player_sprite.center_x >= 51:
            # Scroll left
            left_boundary = self.view_left + VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.player_sprite.left
                changed = True

        if self.player_sprite.center_x <= 1999:
            # Scroll right
            right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT +
                                self.view_bottom)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        if not self.right_pressed and self.up_pressed:
            self.player_sprite.set_texture(4)
        if not self.right_pressed and self.down_pressed:
            self.player_sprite.set_texture(1)
        if not self.left_pressed and self.down_pressed:
            self.player_sprite.set_texture(1)
        if not self.left_pressed and self.up_pressed:
            self.player_sprite.set_texture(4)
        if not self.up_pressed and self.left_pressed:
            self.player_sprite.set_texture(2)
        if not self.up_pressed and self.right_pressed:
            self.player_sprite.set_texture(3)
        if not self.down_pressed and self.left_pressed:
            self.player_sprite.set_texture(2)
        if not self.down_pressed and self.right_pressed:
            self.player_sprite.set_texture(3)


def main():
    """ Main method """
    SCO()
    arcade.run()


if __name__ == "__main__":
    main()
