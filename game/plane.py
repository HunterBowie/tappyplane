import random, pygame
import game.constants as constants
import game.assets as assets
import windowgui

class Plane:
    IMAGE_STEM = "plane-"
    IMAGE_COLOR = "red"
    def __init__(self):
        self.image_name = self.IMAGE_STEM
        if self.IMAGE_COLOR == "random":
            self.image_name = self.image_name + random.choice(["red","green","blue","yellow"])
        else:
            self.image_name = self.image_name + self.IMAGE_COLOR
        self.image_frame = 1
        self.mask = pygame.mask.from_surface(self.get_image())
        self.x = 50
        self.vel_y = 0
        self.angle = 0
        self.angle_offset = (0, 0)
        self.angle_vel = -constants.PLANE_DOWN_ANGLE_VEL
        self.y = constants.HEIGHT//2-self.get_image().get_height()//2
        self.frame_timer = windowgui.Timer()
        self.frame_timer.start()
        self.angle_timer = windowgui.Timer()
    
    
    def get_static_rect(self):
        rect = self.mask.get_rect()
        rect.x, self.y = self.x, self.y
        return rect
    
    def get_image(self):
        return assets.IMAGES[self.image_name + "-" + str(self.image_frame)]
    
    def get_real_pos(self):
        return self.x+self.angle_offset[0], self.y+self.angle_offset[1]
    
    def colliderocks(self, rocks):
        for rock in rocks:
            x1, y1 = self.get_real_pos()
            x2, y2 = rock.x, rock.y
            if rock.mask.overlap(self.mask, (int(x1-x2), int(y1-y2))):
                return True
        return False
    
    def outside_screen(self):
        rect = self.get_static_rect()
        rect.x, rect.y = self.get_real_pos()
        if rect.colliderect(pygame.Rect(0,0,constants.WIDTH,constants.HEIGHT)):
            return False
        return True

    def boost(self):
        self.vel_y = constants.PLANE_BOOST_VEL
        self.angle_vel = constants.PLANE_UP_ANGLE_VEL
        self.angle_timer.start()
    
    def update(self):
        if self.frame_timer.passed(constants.PLANE_ANIMATION_DELAY):
            self.image_frame += 1
            self.frame_timer.start()
        
        if self.image_frame > 3:
            self.image_frame = 1
        
        self.vel_y += constants.PLANE_GRAVITY
        if self.vel_y > constants.PLANE_GRAVITY_LIMIT:
            self.vel_y = constants.PLANE_GRAVITY_LIMIT
        
        self.angle += self.angle_vel
        if self.angle > constants.PLANE_UP_ANGLE_LIMIT:
            if self.angle_timer.passed(constants.PLANE_KEEP_ANGLE_TIME):
                self.angle_vel = -constants.PLANE_DOWN_ANGLE_VEL
            else:
                self.angle = constants.PLANE_UP_ANGLE_LIMIT
        elif self.angle < -constants.PLANE_DOWN_ANGLE_LIMIT:
            self.angle = -constants.PLANE_DOWN_ANGLE_LIMIT
        self.y += self.vel_y
        self.mask = pygame.mask.from_surface(pygame.transform.rotate(self.get_image(), self.angle))

    
    def render(self, screen):
        image, self.angle_offset = windowgui.rotate_image(self.get_image(), self.get_static_rect(), self.angle)
        screen.blit(image, self.get_real_pos())
    
