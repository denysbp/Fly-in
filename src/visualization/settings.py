from os import path

class Color:
    def __init__(self):
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


WIDTH = 760
HEIGHT = 920
FPS = 60

img_dir = path.join(path.dirname(__file__), 'img')
drone_1 = path.join(img_dir, "drone1.jpeg")
drone_2 = path.join(img_dir, "drone2.jpeg")
drone_3 = path.join(img_dir, "drone3.jpeg")
drone_4 = path.join(img_dir, "drone4.jpeg")
rainbow = path.join(img_dir, "rainbow.jpg")