import game.constants as constants

class ScrollingImage:
    def __init__(self, y, image):
        self.y = y
        self.x1 = 0
        self.x2 = image.get_width()
        self.image = image
    
    def update(self):
        self.x1 -= constants.SCROLL_SPEED
        self.x2 -= constants.SCROLL_SPEED
        if self.x1+self.image.get_width() < 0:
            self.x1 = self.x2+self.image.get_width()
            self.x1, self.x2, = self.x2, self.x1
    
    def render(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))