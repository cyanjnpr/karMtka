from PIL import Image, ImageFile
from typing import Tuple
import math

class SketchImage():
    image_path: str
    shades: int
    image_file: ImageFile.ImageFile
    current_x: int
    current_y: int
    left_to_right: bool
    previous_shade: int
    EOF: bool
    saved_pixel: Tuple[Tuple[int, int], float]

    def __init__(self, path: str, shades: int):
        self.image_path = path
        self.shades = shades
        self.left_to_right = True
        self.current_x = 0
        self.current_y = 0
        self.previous_shade = -1
        self.EOF = False

    def __enter__(self):
        self.left_to_right = True
        self.current_x = 0
        self.current_y = 0
        self.previous_shade = -1
        self.EOF = False
        self.image_file = None
        try:
            self.image_file = Image.open(self.image_path).convert('LA')
            self.saved_pixel = self.next_pixel()
        except:
            self.EOF = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.EOF = True
        if (self.image_file != None): self.image_file.close()

    def fit(self, screen_width: int, screen_height: int):
        if (float(self.image_file.width) / float(self.image_file.height) > 
                float(screen_width) / float(screen_height)):
            if (self.image_file.width > screen_width):
                self.image_file = self.image_file.resize((
                    screen_width, 
                    int(self.image_file.height * screen_width / float(self.image_file.width))))
        else:
            if (self.image_file.height > screen_height):
                self.image_file = self.image_file.resize((
                    int(self.image_file.width * screen_height / float(self.image_file.height)), 
                    screen_height))

    def value_to_shade(self, val: float) -> int:
        return math.floor(val / 256 * self.shades)
    
    def following_pixel_shade(self, x: int) -> int:
        following_x: int
        if (self.left_to_right):
            following_x = x + 1
        else:
            following_x = x - 1
        if (following_x < 0  or following_x == self.image_file.width): return -1
        return self.value_to_shade(self.getpixel((following_x, self.current_y)))

    def getpixel(self, xy: Tuple[int, int]) -> int:
        val, alpha = self.image_file.getpixel(xy)
        if (alpha == 255):
            return val 
        elif (alpha == 0):
            return 255
        return val + ((255 - val) * (1 - (alpha / 255)))

    def next_pixel(self) -> Tuple[Tuple[int, int], float]:
        for y in range(self.current_y, self.image_file.height):
            self.current_y = y
            if (self.left_to_right):
                for x in range(self.current_x, self.image_file.width):
                    val = self.getpixel((x, y))
                    shade = self.value_to_shade(val)
                    if (self.previous_shade != shade or self.following_pixel_shade(x) != shade):
                        self.current_x = x + 1
                        self.previous_shade = shade
                        return ((x, y), val)
            else:
                for x in range(self.current_x, -1, -1):
                    val = self.getpixel((x, y))
                    shade = self.value_to_shade(val)
                    if (self.previous_shade != shade or self.following_pixel_shade(x) != shade):
                        self.current_x = x - 1
                        self.previous_shade = shade
                        return ((x, y), val)
            self.previous_shade = -1
            self.left_to_right = not self.left_to_right
            self.current_x = 0 if self.left_to_right else self.image_file.width - 1
        self.EOF = True
        return None

    def next_point(self, translate_x: int = 0, translate_y: int = 0) -> Tuple[
            float, float, float, float, float, float]:
        pixel = self.saved_pixel
        self.saved_pixel = self.next_pixel()
        if (pixel == None): return None
        (x,y), val = pixel
        shade = self.value_to_shade(val)
        width = 0 if shade == self.shades - 1 else 1
        pressure = 1 - shade / self.shades
        return x+translate_x, y+translate_y, 1, width, 0, pressure
    