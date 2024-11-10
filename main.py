import arcade

SCREEN_TITLE = "Mushroomer"

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

PLAYER_SPEED = 3
ENEMY_SPEED = 0

class StartGameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/start_game.jpg")
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class WinGameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/win_game.jpg")
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class EndGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/end_game.jpg")
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.draw_text("You didn't find all the mushrooms", self.window.width / 2, self.window.height / 2 - 100,
                         arcade.color.WHITE_SMOKE, font_size=28, anchor_x="center")
        arcade.draw_text("Click to Try again", self.window.width / 2, self.window.height / 2 - 160,
                         arcade.color.WHITE_SMOKE, font_size=16, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/game_over.jpg")
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        self.clear()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.draw_text("Click to Restart", self.window.width / 2, self.window.height / 2 - 120,
                         arcade.color.WHITE_SMOKE, font_size=16, anchor_x="center")

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
        self.camera = None
        self.score = 0

        self.leaves_sound = arcade.load_sound("sounds/leaves.wav")
        self.grib_sound = arcade.load_sound("sounds/es.mp3")
        self.bear_sound = arcade.load_sound("sounds/hrum.mp3")
        self.finish_sound = arcade.load_sound("sounds/finish.mp3")
        self.win_sound = arcade.load_sound("sounds/win.mp3")

        arcade.set_background_color(arcade.csscolor.FOREST_GREEN)

    def setup(self):

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Beer")
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.score = 0

        # Карта
        map_name = "maps/map1.json"
        layer_options = {"Trees": {"use_spatial_hash": True,},
                         "Mushrooms": {"use_spatial_hash": True,},
                         }
        self.tile_map = arcade.load_tilemap(map_name, 1, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Игрок
        self.player_sprite = arcade.Sprite("images/player.png", 1)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.scene.add_sprite("Player", self.player_sprite)

        # Медведь
        self.enemy_sprite = arcade.Sprite("images/bear.png", 1)
        self.enemy_sprite.center_x = 600
        self.enemy_sprite.center_y = 600
        self.scene.add_sprite("Bear", self.enemy_sprite)

        # Физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, walls=self.scene["Trees"])

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_SPEED
            arcade.play_sound(self.leaves_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_SPEED
            arcade.play_sound(self.leaves_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
            arcade.play_sound(self.leaves_sound)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
            arcade.play_sound(self.leaves_sound)
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

    def on_draw(self):

        self.clear()
        self.scene.draw()
        self.camera.use()

    def center_camera_to_player(self):

        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):

        self.physics_engine.update()
        self.center_camera_to_player()

        #собираем грибы
        grib_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Mushrooms"])
        for grib in grib_hit_list:
            grib.remove_from_sprite_lists()
            arcade.play_sound(self.grib_sound)
            self.score += 1

       #траектория медведя
        if self.enemy_sprite.center_x < 1600 and self.enemy_sprite.center_y == 600:
             self.enemy_sprite.center_x += ENEMY_SPEED + 4
        elif self.enemy_sprite.center_x == 1600 and self.enemy_sprite.center_y > 300:
            self.enemy_sprite.center_y += ENEMY_SPEED - 4
        elif self.enemy_sprite.center_y == 300 and self.enemy_sprite.center_x > 600:
            self.enemy_sprite.center_x += ENEMY_SPEED - 4
        elif self.enemy_sprite.center_x == 600 and self.enemy_sprite.center_y < 600:
            self.enemy_sprite.center_y += ENEMY_SPEED + 4

        #Условия поражения
        death = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Bear"])
        if death:
            arcade.play_sound(self.bear_sound)
            view = GameOverView()
            self.window.show_view(view)

        #Условия победы
        if self.player_sprite.center_x >= 1856:
            if self.score == 10:
                view = WinGameView()
                self.window.show_view(view)
                arcade.play_sound(self.win_sound)
            elif self.score < 10:
                view = EndGameView()
                self.window.show_view(view)
                arcade.play_sound(self.finish_sound)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartGameView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
