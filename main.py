import arcade

SCREEN_WIDTH = 1856
SCREEN_HEIGHT = 928
SCREEN_TITLE = "Mushroomer"

CHARACTER_SCALING = 1
MAP_SCALING = 1
PLAYER_SPEED = 4
ENEMY_SPEED = 0


class StartGameView(arcade.View):

    def on_show_view(self):
        # Настраиваем окно
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        # Рисуем окно
        self.clear()
        arcade.draw_text("Start Game", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to start", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Нажатие мыши
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class WinGameView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.BLUE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("You Win!", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("You found all the mushrooms", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Click to Do it again", self.window.width / 2, self.window.height / 2 - 200,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class EndGameView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.FUCHSIA)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("End Game", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("You didn't find all the mushrooms", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Click to Try again", self.window.width / 2, self.window.height / 2 - 200,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/pers1.png")
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.enemy_sprite = None
        self.physics_engine = None
        # self.camera = None
        self.score = 0
        self.grib_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.shag_sound = arcade.load_sound("sounds/shagi-begom-po-lesu.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.csscolor.FOREST_GREEN)

    def setup(self):

        self.scene = arcade.Scene()
        # self.camera = arcade.Camera(self.width, self.height)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Beer")
        self.score = 0

        # Карта
        map_name = "maps/map1.json"
        layer_options = {
            "Trees": {
                "use_spatial_hash": True,
            },
            "Mushrooms": {
                "use_spatial_hash": True,
            },
        }
        self.tile_map = arcade.load_tilemap(map_name, MAP_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Игрок
        image_source = "images/player.png"
        self.player_sprite = arcade.Sprite(image_source,CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # медведь
        image_source = "images/bear.png"
        self.enemy_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.enemy_sprite.center_x = 600
        self.enemy_sprite.center_y = 600
        self.scene.add_sprite("Bear", self.enemy_sprite)

        # Физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            walls=self.scene["Trees"]
        )

    def on_draw(self):

        self.clear()
        self.scene.draw()

        # self.camera.use()
        '''def center_camera_to_player(self):
            screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
             screen_center_y = self.player_sprite.center_y - (
                    self.camera.viewport_height / 2
            )

            # Don't let camera travel past 0
            if screen_center_x < 0:
                screen_center_x = 0
            if screen_center_y < 0:
               screen_center_y = 0
            player_centered = screen_center_x, screen_center_y

            self.camera.move_to(player_centered)'''

        # Убрать!!!
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text,10,10,arcade.csscolor.WHITE,18,)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_SPEED
            arcade.play_sound(self.shag_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_SPEED
            arcade.play_sound(self.shag_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
            arcade.play_sound(self.shag_sound)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
            arcade.play_sound(self.shag_sound)
        if key == arcade.key.P:
            arcade.close_window()

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()
        # self.center_camera_to_player()

        grib_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Mushrooms"])
        for grib in grib_hit_list:
            grib.remove_from_sprite_lists()
            arcade.play_sound(self.grib_sound)
            self.score += 1

       # траектория медведя
        if self.enemy_sprite.center_x < 1600 and self.enemy_sprite.center_y == 600:
             self.enemy_sprite.center_x += ENEMY_SPEED + 4
        elif self.enemy_sprite.center_x == 1600 and self.enemy_sprite.center_y > 300:
            self.enemy_sprite.center_y += ENEMY_SPEED - 4
        elif self.enemy_sprite.center_y == 300 and self.enemy_sprite.center_x > 600:
            self.enemy_sprite.center_x += ENEMY_SPEED - 4
        elif self.enemy_sprite.center_x == 600 and self.enemy_sprite.center_y < 600:
            self.enemy_sprite.center_y += ENEMY_SPEED + 4

        death = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Bear"])
        if death:
            arcade.play_sound(self.game_over)
            view = GameOverView()
            self.window.show_view(view)

        #Условия победы
        if self.player_sprite.center_x >= 1856:
            arcade.play_sound(self.game_over)
            if self.score == 10:
                view = WinGameView()
                self.window.show_view(view)
            elif self.score < 10:
                view = EndGameView()
                self.window.show_view(view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartGameView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
