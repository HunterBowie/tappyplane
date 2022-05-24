import random, pygame
import windowgui
import assets, constants

class Rock:
    IMAGES = [
        "rock-grass-up",
        "rock-grass-down",
        "rock-up",
        "rock-down",
        "rock-ice-up",
        "rock-ice-down",
        "rock-snow-up",
        "rock-snow-down"
    ]
    def __init__(self):
        self.x = random.randint(constants.WIDTH, constants.WIDTH+constants.ROCK_X_DIST)
        self.passed_screen = False
        self._init_image()
        self.mask = pygame.mask.from_surface(self.image)
    
    def _init_image(self):
        image_name = random.choice(self.IMAGES)
        self.image = assets.IMAGES[image_name]
        self.spike_size = random.choice(["low", "tall"])
        if image_name[-2:] == "up":
            if self.spike_size == "low":
                self.y = constants.HEIGHT-self.image.get_height()//2
            else:
                self.y = constants.HEIGHT-self.image.get_height()+5
        else:
            if self.spike_size == "low":
                self.y = -self.image.get_height()//2
            else:
                self.y = -5
    
    def get_rect(self):
        rect = self.mask.get_rect()
        rect.x, rect.y = self.x, self.y
        return rect
    
    def update(self):
        self.x -= constants.SCROLL_SPEED
        if self.x+self.image.get_width() < 0:
            self.passed_screen = True

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        