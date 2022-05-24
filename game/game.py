import pygame, random
import windowgui
import constants, assets
from scrolling_image import ScrollingImage
from ground import Ground
from plane import Plane
from rock import Rock

pygame.init()
window = windowgui.Window((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tappy Plane")

assets.convert_images()

class Game:
    def __init__(self, window):
        self.window = window
        self.background = ScrollingImage(0, assets.IMAGES["background"])
        self.ground = Ground("snow")
        pygame.mouse.set_visible(False)
        
        self.plane = Plane()
        self.rocks = []
        self.theme = "snow"
        self.theme_timer = windowgui.Timer()
        self.theme_timer.start()
        self.difficulty = 1
        self.difficulty_timer = windowgui.Timer()
        self.difficulty_timer.start()
        

        self.rock_timer = windowgui.Timer()
        self.rock_timer.start()
        self.cursor_timer = windowgui.Timer()

        self._generate_rock_pair()
    
    def _new_theme(self):
        changed = False
        prev_theme = self.theme
        while not changed:
            self.theme = random.choice(constants.THEMES)
            if self.theme != prev_theme:
                changed = True
        
        self.ground.change_theme(self.theme)
   
    def _generate_rock_pair(self):
        top_rock = Rock(self.theme, "small", "up", x_offset=(-100+self.difficulty))
        bottom_rock = Rock(self.theme, "large", "down", x_offset=(100-self.difficulty))
        if random.randint(0, 1):
            top_rock = Rock(self.theme, "small", "down", x_offset=(-100+self.difficulty))
            bottom_rock = Rock(self.theme, "large", "up", x_offset=(100-self.difficulty))
        
        self.rocks.append(top_rock)
        self.rocks.append(bottom_rock)
        
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.window.eventloop(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.plane.boost()
                self.cursor_timer.start()
        
        self.background.update()
        self.background.render(self.window.screen)

        if self.theme_timer.passed(10):
            self._new_theme()
            self.theme_timer.start()

        if self.difficulty_timer.passed(10):
            self.difficulty += 4
            self.difficulty_timer.start()


        if self.rock_timer.passed(2):
            self._generate_rock_pair()
            self.rock_timer.start()

        remove_rocks = []
        for rock in self.rocks:
            rock.update()
            rock.render(self.window.screen)
            if rock.passed_screen:
                remove_rocks.append(rock)
        
        for rock in remove_rocks:
            self.rocks.remove(rock)
        
        self.ground.update()
        self.ground.render(self.window.screen)
        
        
        self.plane.update()
        if self.plane.colliderocks(self.rocks):
            self.window.running = False
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
        while self.window.running:
            self.update()

if __name__ == "__main__":
    window.start()
    Game(window).run()