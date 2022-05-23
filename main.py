import pygame
import windowgui, constants, assets
from scrolling_image import ScrollingImage
from plane import Plane
from rock import Rock

pygame.init()
window = windowgui.Window((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tappy Plane")

assets.convert_images()

def main():
    window.start()

    bg = ScrollingImage(assets.IMAGES["background"])
    plane = Plane()
    rock = Rock()
    while window.running:

        for event in pygame.event.get():
            window.eventloop(event)
        bg.update()
        bg.render(window.screen)
        rock.update()
        rock.render(window.screen)
        plane.render(window.screen)
        window.update()
    

if __name__ == "__main__":
    main()