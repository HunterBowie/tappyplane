import constants, assets

class Plane:
    def __init__(self):
        self.image_frame = 1
        self.image = assets.IMAGES["plane-red-1"]
        self.x = 50
        self.y = constants.HEIGHT//2-self.image.get_height()//2
    
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
