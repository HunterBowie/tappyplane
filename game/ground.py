import random, pygame
import assets, constants
from scrolling_image import ScrollingImage

class Ground:
    IMAGES = {
        "snow": [
            "ground-snow",
            "ground-rock"
        ],
        "grass": [
            "ground-grass",
            "ground-rock"
        ],
        "ice": [
            "ground-ice"
        ]
    }
    def __init__(self, theme):
        self.theme = theme
        self._init()
    
    def change_theme(self, theme):
        self.theme = theme
        self._init()
    
    def _init(self):
        image = assets.IMAGES[random.choice(self.IMAGES[self.theme])]
        self.y = constants.HEIGHT-image.get_height()+10
        self.scrolling_image = ScrollingImage(self.y, image)
        self.mask = pygame.mask.from_surface(image)
    
    def collideplane(self, plane):
        pos1 = self.scrolling_image.x1, self.y
        pos2 = self.scrolling_image.x2, self.y
        plane_pos = plane.get_real_pos()
        if self.mask.overlap(plane.mask, (pos1[0]-plane_pos[0], pos1[1]-plane_pos[1])):
            return True
        if self.mask.overlap(plane.mask, (pos2[0]-plane_pos[0], pos2[1]-plane_pos[1])):
            return True
        return False


    def update(self):
        self.scrolling_image.update()

    def render(self, screen):
        self.scrolling_image.render(screen)