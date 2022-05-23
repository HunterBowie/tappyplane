class ScrollingImage:
    def __init__(self, image):
        self.x1 = 0
        self.x2 = image.get_width()
        self.image = image
    
    def update(self):
        self.x1 -= 1
        self.x2 -= 1
        if self.x1+self.image.get_width() < 0:
            self.x1 = self.x2+self.image.get_width()
            self.x1, self.x2, = self.x2, self.x1
    
    def render(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))