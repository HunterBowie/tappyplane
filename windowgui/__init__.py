"""
A package that provides a simplified and organized struture for designing UIs in pygame
"""

from .util import Colors, RealTimer, GameTimer, Text, root_rect, root_rects, load_image, get_surf, get_text_size
from .constants import UIColorStyle, UIEvent, Colors
from .assets import IMAGES_DIR, SOUNDS_DIR, FOUNTS_DIR

from .window import Window

from .flash import Flash
from .ui import Button, Slider, TextBox, CheckBox


