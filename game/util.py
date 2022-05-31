import pygame
import game.assets as assets

def get_number_image(value, scale=1):
    images = [
        assets.IMAGES["num-0"],
        assets.IMAGES["num-1"],
        assets.IMAGES["num-2"],
        assets.IMAGES["num-3"],
        assets.IMAGES["num-4"],
        assets.IMAGES["num-5"],
        assets.IMAGES["num-6"],
        assets.IMAGES["num-7"],
        assets.IMAGES["num-8"],
        assets.IMAGES["num-9"]
    ]
    image_size = images[0].get_size()
    for i in range(len(images)):
        images[i] = pygame.transform.scale(images[i], (int(image_size[0]*scale), int(image_size[1]*scale)))
    
    final_images = []
    value = str(value)
    for digit in value:
        final_images.append(images[int(digit)])
    surf = pygame.Surface((images[0].get_width()*len(final_images), images[0].get_height()), pygame.SRCALPHA)
    pos = 0, 0
    for image in final_images:
        surf.blit(image, pos)
        pos = pos[0]+images[0].get_width(), pos[1]
    return surf

