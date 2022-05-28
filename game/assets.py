from os import path
import windowgui

CURRENT_DIR = path.dirname(__file__)
IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")

IMAGES = {
    "background": windowgui.load_image("background", IMAGES_DIR),
    "plane-red-1": windowgui.load_image("Planes/planeRed1", IMAGES_DIR),
    "plane-red-2": windowgui.load_image("Planes/planeRed2", IMAGES_DIR),
    "plane-red-3": windowgui.load_image("Planes/planeRed3", IMAGES_DIR),
    "plane-green-1": windowgui.load_image("Planes/planeGreen1", IMAGES_DIR),
    "plane-green-2": windowgui.load_image("Planes/planeGreen2", IMAGES_DIR),
    "plane-green-3": windowgui.load_image("Planes/planeGreen3", IMAGES_DIR),
    "plane-blue-1": windowgui.load_image("Planes/planeBlue1", IMAGES_DIR),
    "plane-blue-2": windowgui.load_image("Planes/planeBlue2", IMAGES_DIR),
    "plane-blue-3": windowgui.load_image("Planes/planeBlue3", IMAGES_DIR),
    "plane-yellow-1": windowgui.load_image("Planes/planeYellow1", IMAGES_DIR),
    "plane-yellow-2": windowgui.load_image("Planes/planeYellow2", IMAGES_DIR),
    "plane-yellow-3": windowgui.load_image("Planes/planeYellow3", IMAGES_DIR),
    "rock-grass-up": windowgui.load_image("rockGrass", IMAGES_DIR),
    "rock-grass-down": windowgui.load_image("rockGrassDown", IMAGES_DIR),
    "rock-up": windowgui.load_image("rock", IMAGES_DIR),
    "rock-down": windowgui.load_image("rockDown", IMAGES_DIR),
    "rock-ice-up": windowgui.load_image("rockIce", IMAGES_DIR),
    "rock-ice-down": windowgui.load_image("rockIceDown", IMAGES_DIR),
    "rock-snow-up": windowgui.load_image("rockSnow", IMAGES_DIR),
    "rock-snow-down": windowgui.load_image("rockSnowDown", IMAGES_DIR),
    "cursor": windowgui.load_image("UI/tap", IMAGES_DIR),
    "cursor-pressed": windowgui.load_image("UI/tapTick", IMAGES_DIR),
    "ground-rock": windowgui.load_image("groundDirt", IMAGES_DIR),
    "ground-snow": windowgui.load_image("groundSnow", IMAGES_DIR),
    "ground-grass": windowgui.load_image("groundGrass", IMAGES_DIR),
    "ground-ice": windowgui.load_image("groundIce", IMAGES_DIR),
    "game-over": windowgui.load_image("UI/textGameOver", IMAGES_DIR),
    "num-0": windowgui.load_image("Numbers/number0", IMAGES_DIR),
    "num-1": windowgui.load_image("Numbers/number1", IMAGES_DIR),
    "num-2": windowgui.load_image("Numbers/number2", IMAGES_DIR),
    "num-3": windowgui.load_image("Numbers/number3", IMAGES_DIR),
    "num-4": windowgui.load_image("Numbers/number4", IMAGES_DIR),
    "num-5": windowgui.load_image("Numbers/number5", IMAGES_DIR),
    "num-6": windowgui.load_image("Numbers/number6", IMAGES_DIR),
    "num-7": windowgui.load_image("Numbers/number7", IMAGES_DIR),
    "num-8": windowgui.load_image("Numbers/number8", IMAGES_DIR),
    "num-9": windowgui.load_image("Numbers/number9", IMAGES_DIR),



}

def convert_images():
    """coverting of images must be called after the initalization of pygame display"""
    for name,img in IMAGES.items():
        IMAGES[name] = img.convert_alpha()