from os import path
import windowgui

CURRENT_DIR = path.dirname(__file__)
IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")

IMAGES = {
    "background": windowgui.load_image("background", IMAGES_DIR, convert=False),
    "plane-red-1": windowgui.load_image("Planes/planeRed1", IMAGES_DIR, convert=False),
    "plane-red-2": windowgui.load_image("Planes/planeRed2", IMAGES_DIR, convert=False),
    "plane-red-3": windowgui.load_image("Planes/planeRed3", IMAGES_DIR, convert=False),
    "rock-grass-up": windowgui.load_image("rockGrass", IMAGES_DIR, convert=False),

}

def convert_images():
    """coverting of images must be called after the initalization of pygame display"""
    for name,img in IMAGES.items():
        IMAGES[name] = img.convert_alpha()