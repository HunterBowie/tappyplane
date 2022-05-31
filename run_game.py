import os
import game, windowgui


class MainMenu:
    def __init__(self, window):
        self.window = window
        self._init_ui()
        self.hide_text = False
        self.title = windowgui.Text(0, 30, "Tappy Plane", style={"size": 45})
        self.title.x, self.title.y = windowgui.root_rect(self.window.screen.get_size(), self.title.get_rect(),
        center_x=True)
        self.highscore = self.get_highscore()
        self.highscore_label = windowgui.Text(-30, 90, "Top Score: ")
        self.highscore_label.x, self.highscore_label.y = windowgui.root_rect(self.window.screen.get_size(),
         self.highscore_label.get_rect(), center_x=True)
        
    
    def get_highscore(self):
        with open(os.path.join(game.assets.CURRENT_DIR, "highscore.txt"), "r") as file:
            data = int(file.read())
        return data
    
    def save_highscore(self, score):
        with open(os.path.join(game.assets.CURRENT_DIR, "highscore.txt"), "w") as file:
            file.write(str(score))

    def _init_ui(self):
        red_plane_button = windowgui.Button("red", 60, -30, 100, 100, hide_button=False, top_img=game.assets.IMAGES["plane-red-1"])
        blue_plane_button = windowgui.Button("blue", -60, -30, 100, 100, hide_button=False, top_img=game.assets.IMAGES["plane-blue-1"])
        green_plane_button = windowgui.Button("green", -180, -30, 100, 100, hide_button=False, top_img=game.assets.IMAGES["plane-green-1"])
        yellow_plane_button = windowgui.Button("yellow", 180, -30, 100, 100, hide_button=False, top_img=game.assets.IMAGES["plane-yellow-1"])
        self.button_group = windowgui.TogglableButtonGroup(
         [red_plane_button, blue_plane_button, green_plane_button, yellow_plane_button]   
        )
        play_button = windowgui.Button("play", 0, 80, 250, 50, top_img=windowgui.Text(0,0,"Play").surface)
        windowgui.root_rects(self.window.screen.get_size(), [play_button.rect, red_plane_button.rect, blue_plane_button.rect, green_plane_button.rect, yellow_plane_button.rect],
         center_x=True, center_y=True)
        self.window.ui.add([
            play_button, self.button_group
        ])
    
    def display_game_over(self):
        timer = windowgui.Timer()
        timer.start()
        
        self.window.screen.fill(windowgui.Colors.WHITE)
        image = game.assets.IMAGES["game-over"]
        self.window.screen.blit(image, (game.constants.WIDTH//2-image.get_width()//2,
         game.constants.HEIGHT//2-image.get_height()//2))
        while not timer.passed(10):
            pass

    
    def eventloop(self, event):
        if event.type == windowgui.UIEvent.BUTTON_CLICKED:
            if event.ui_id == "play" and self.button_group.selected:
                self.window.ui.clear()
                self.hide_text = True
                new_game = game.Game(self.window)
                new_game.config(plane_color=self.button_group.selected.id)
                new_game.run()
                if new_game.score > self.get_highscore():
                    self.save_highscore(new_game.score)
                    self.highscore = new_game.score
                self.hide_text = False
                self._init_ui()
    
    def update(self):
        if not self.hide_text:
            self.title.render(self.window.screen)
            self.window.screen.blit(game.get_number_image(self.highscore, scale=0.5), (455, 87))
            self.highscore_label.render(self.window.screen)
game.window.set_manager(MainMenu)
game.window.start(auto_cycle=True)
