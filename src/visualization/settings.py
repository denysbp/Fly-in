from os import path


class Color:
    """
    Custom color class
    """
    def __init__(self) -> None:
        """
        Color base class
        """
        self.WHITE = (255, 255, 255)
        self.RED = (235, 64, 52)
        self.BLUE = (15, 73, 219)
        self.BLACK = (0, 0, 0)
        self.GREEN = (23, 252, 3)
        self.PURPLE = (111, 3, 252)
        self.BROWN = (71, 50, 25)
        self.MAROON = (107, 64, 13)
        self.GOLD = (211, 175, 55)
        self.DARKRED = (61, 2, 2)
        self.CRIMSON = (220, 20, 60)
        self.CYAN = (0, 255, 255)
        self.ORANGE = (255, 165, 0)


WIDTH = 1260
HEIGHT = 1840
FPS = 60
TURN_DURATION_MS = 1000
ZOOM_STEP = 1.12
MIN_ZOOM = 0.35
MAX_ZOOM = 3.0
DEFAULT_ZOOM = 1.3
FIT_MARGIN = 360
FIT_SCALE_FACTOR = 0.78


img_dir = path.join(path.dirname(__file__), 'img')
damage_dir = path.join(path.dirname(__file__), 'Damage')
drone_1 = path.join(img_dir, "drone1.png")
drone_2 = path.join(img_dir, "drone2.png")
drone_3 = path.join(img_dir, "drone2.png")
drone_4 = path.join(img_dir, "drone3.png")
drone_5 = path.join(img_dir, "drone4.png")
drone_6 = path.join(img_dir, "drone5.png")
drone_7 = path.join(img_dir, "drone7.png")
drone_8 = path.join(img_dir, "drone8.png")
back_ground = path.join(img_dir, "background.jpg")
