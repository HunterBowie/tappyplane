import pygame, random, os
import game.constants as constants
import game.assets as assets
import windowgui
from game.scrolling_image import ScrollingImage
from game.plane import Plane
from game.rock import Rock
from game.util import get_number_image

pygame.init()
window = windowgui.Window((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tappy Plane")

assets.convert_images()

pygame.display.set_icon(pygame.transform.scale(assets.IMAGES["plane-red-1"], (44, 35)))

windowgui.Text.default_style["font_file"] = os.path.join(windowgui.assets.FOUNTS_DIR, "rounded.ttf")

class Game:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.background = ScrollingImage(0, assets.IMAGES["background"])
        pygame.mouse.set_visible(False)
        
        self.planes = []
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
        
        self.score = 0        
        
    
    def config(self, plane_color="red", display_score=True, managed=False,
     num_planes=1, terrain_simple=False):
        if plane_color:
            Plane.IMAGE_COLOR = plane_color
        self.managed = managed
        self.display_score = display_score
        self.num_planes = num_planes
        self.planes.clear()
        for i in range(self.num_planes):
            self.planes.append(Plane())
        self.terrain_simple = terrain_simple
        self._generate_rocks()
    
    def reset(self):
        pass
    
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
        if self.terrain_simple:
            choices = [1, 2]
        rand = random.choice(choices)
        if not self.terrain_simple:
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

            if not self.managed:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for plane in self.planes:
                        plane.boost()
                    self.cursor_timer.start()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for plane in self.planes:
                            plane.boost()
        
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
                
        
        for plane in self.planes:
            plane.update()
            if plane.colliderocks(self.rocks) or plane.outside_screen():
                if self.managed:
                    self.planes.remove(plane)
                    if len(self.planes) == 0:
                        self.running = False
                else:
                    self.running = False
                    return None
        
        for plane in self.planes:
            plane.render(self.window.screen)
         
        if self.display_score:
            number_surf = get_number_image(self.score)
            x = constants.WIDTH//2-number_surf.get_width()//2
            y = 30
            self.window.screen.blit(number_surf, (x, y))

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
        self.end()
        
    def end(self):
        pygame.mouse.set_visible(True)
