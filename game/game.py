import pygame, random, os
import constants, assets, windowgui
from scrolling_image import ScrollingImage
from plane import Plane
from rock import Rock

pygame.init()
window = windowgui.Window((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tappy Plane")

assets.convert_images()

windowgui.Text.default_style["font_file"] = os.path.join(windowgui.assets.FOUNTS_DIR, "rounded.ttf")

class Game:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.background = ScrollingImage(0, assets.IMAGES["background"])
        pygame.mouse.set_visible(False)
        
        self.plane = Plane()
        self.rocks = []
        self.last_spawned_rocks = []
        self.last_spawned_rock_num = 0
        self.theme = "snow"
        self.theme_timer = windowgui.Timer()
        self.theme_timer.start()
        self.difficulty = 1
        self.difficulty_timer = windowgui.Timer()
        self.difficulty_timer.start()
        self.cursor_timer = windowgui.Timer()
        self._generate_rocks()
        self.score = 0
    
    def config(self, plane_color=None):
        if plane_color:
            Plane.IMAGE_NAME = "plane-" + plane_color
        
    
    def _new_theme(self):
        changed = False
        prev_theme = self.theme
        while not changed:
            self.theme = random.choice(constants.THEMES)
            if self.theme != prev_theme:
                changed = True
        
   
    def _generate_rocks(self):
        self.last_spawned_rocks.clear()
        choices = [1,1,1,1,2,2,2,2,3,4,5]
        rand = random.choice(choices)
        while rand == self.last_spawned_rock_num:
            rand = random.choice(choices)
        rocks = []
        # small top, large bottom
        if rand == 1:
            rocks.append(Rock(self.theme, "small", "up", x_offset=(-100+self.difficulty)))
            rocks.append(Rock(self.theme, "large", "down", x_offset=(100-self.difficulty)))
        # large top, small bottom
        elif rand == 2:
            rocks.append(Rock(self.theme, "small", "down", x_offset=(-100+self.difficulty)))
            rocks.append(Rock(self.theme, "large", "up", x_offset=(100-self.difficulty)))
        # large bottom, 2 small bottom
        elif rand == 3:
            direction = random.choice(["down", "up"])
            rocks.append(Rock(self.theme, "large", direction, x_offset=0))
            rocks.append(Rock(self.theme, "small", direction, x_offset=-(75+20)))
            rocks.append(Rock(self.theme, "small", direction, x_offset=75))
        # large bottom, large top
        elif rand == 4:
            rocks.append(Rock(self.theme, "large", "down", x_offset=(-100+self.difficulty//2)))
            rocks.append(Rock(self.theme, "large", "up", x_offset=(100-self.difficulty//2)))
        # 3 large bottom
        elif rand == 5:
            first_direction = random.choice(["down", "up"])
            second_direction = "down"
            if first_direction == "down":
                second_direction = "up"
            rocks.append(Rock(self.theme, "small", first_direction, x_offset=random.randint(50, 100)))
            rocks.append(Rock(self.theme, "small", first_direction, x_offset=-random.randint(50, 100)))
            rocks.append(Rock(self.theme, "small", second_direction, x_offset=0))
        for rock in rocks:
            self.rocks.append(rock)
            self.last_spawned_rocks.append(rock)
        self.last_spawned_rock_num = rand

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.window.eventloop(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.plane.boost()
                self.cursor_timer.start()
        
        self.background.update()
        self.background.render(self.window.screen)

        if self.theme_timer.passed(20):
            self._new_theme()
            self.theme_timer.start()

        if self.difficulty_timer.passed(5):
            self.difficulty += 2 
            if self.difficulty > 80:
                self.difficulty = 80
            self.difficulty_timer.start()

        last_rocks_passed = [rock.passed_start for rock in self.last_spawned_rocks]
        if all(last_rocks_passed):
            self.score += 1
            self._generate_rocks()

        remove_rocks = []
        for rock in self.rocks:
            rock.update()
            rock.render(self.window.screen)
            if rock.passed_screen:
                remove_rocks.append(rock)
        
        for rock in remove_rocks:
            self.rocks.remove(rock)
                
        
        self.plane.update()
        if self.plane.colliderocks(self.rocks) or self.plane.outside_screen():
            self.running = False
            return None
        
        self.plane.render(self.window.screen)

        if pygame.mouse.get_focused():
            cursor_image = assets.IMAGES["cursor"]
            if not self.cursor_timer.passed(.1) and self.cursor_timer.started():
                
                cursor_image = assets.IMAGES["cursor-pressed"]
                
            cursor_pos = mouse_pos[0]-cursor_image.get_width()//2, mouse_pos[1]-cursor_image.get_height()//2
            self.window.screen.blit(cursor_image, cursor_pos)



        self.window.update()

    def run(self):
        self.running = True
        while self.window.running and self.running:
            self.update()
        pygame.mouse.set_visible(True)

if __name__ == "__main__":
    window.start()
    Game(window).run()
