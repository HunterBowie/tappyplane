import pygame
import windowgui
import constants, assets
from scrolling_image import ScrollingImage
from plane import Plane
from rock import Rock

pygame.init()
window = windowgui.Window((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tappy Plane")

assets.convert_images()

class Game:
    def __init__(self, window):
        self.window = window
        pygame.mouse.set_visible(False)
        self.background = ScrollingImage(assets.IMAGES["background"])
        self.plane = Plane()
        self.cursor_timer = windowgui.Timer()
        
        self.rocks = []
        for i in range(4):
            self.new_rock()
        
        
    def new_rock(self):
        finished = False
        counter = 0
        while not finished:
            new_rock = Rock()
            finished = True
            for rock in self.rocks:
                if rock.get_rect().colliderect(new_rock.get_rect()):
                    finished = False
            if finished:
                self.rocks.append(new_rock)
          
            counter += 1
            if counter > 20:
                raise Exception("rock cannot be added")
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            self.window.eventloop(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.plane.boost()
                self.cursor_timer.start()
        
        self.background.update()
        self.background.render(self.window.screen)

        remove_rocks = []
        for rock in self.rocks:
            rock.update()
            rock.render(self.window.screen)
            if rock.passed_screen:
                remove_rocks.append(rock)
        
        for rock in remove_rocks:
            self.rocks.remove(rock)
            self.new_rock()
        
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