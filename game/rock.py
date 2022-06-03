import random, pygame
import game.constants as constants
import game.assets as assets
import windowgui

class Rock:
    IMAGES = {
        "snow": {
            "up": [
                "rock-up",
                "rock-snow-up",
            ],
            "down":[
                "rock-down",
                "rock-snow-down"
            ]
        },
        "grass": {
            "up": [
                "rock-up",
                "rock-grass-up",
            ],
            "down": [
                "rock-down",
                "rock-grass-down",
            ]
        },
        "ice": {
            "up": [
                "rock-ice-up"
            ],
            "down": [
                "rock-ice-down"
            ]
        }
        
        
    }
    def __init__(self, theme, size, direction, x_offset=0):
        self.direction = direction
        self.size = size
        self.theme = theme
        self.x = constants.WIDTH+constants.ROCK_X_DIST+x_offset
        self.passed_screen = False
        self.passed_start = False
        self._init_image()
        self.mask = pygame.mask.from_surface(self.image)
    
    def _init_image(self):
        image_name = random.choice(self.IMAGES[self.theme][self.direction])
        self.image = assets.IMAGES[image_name]
        if self.direction == "up":
            if self.size == "small":
                self.y = constants.HEIGHT-self.image.get_height()//2
            else:
                self.y = constants.HEIGHT-self.image.get_height()+5
        else:
            if self.size == "small":
                self.y = -self.image.get_height()//2
            else:
                self.y = -5
    
    def get_rect(self):
        rect = self.mask.get_rect()
        rect.x, rect.y = self.x, self.y
        return rect
    
    def colllidepoint(self, pos):
        pos = pos[0]-self.x, pos[1]-self.y
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] > self.mask.get_size()[0] or pos[1] > self.mask.get_size()[1]:
            return False
        return self.mask.get_at(pos)

    
    def update(self):
        self.x -= constants.SCROLL_SPEED
        if self.x+self.image.get_width() < 0:
            self.passed_screen = True
        elif self.x+self.image.get_width() < constants.WIDTH:
            self.passed_start = True

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        