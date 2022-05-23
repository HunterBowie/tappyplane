import assets

class Rock:
    def __init__(self):
        self.image = assets.IMAGES["rock-grass-up"]
        self.x = 600
        self.y = 200
    
    def update(self):
        self.x -= 1

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        