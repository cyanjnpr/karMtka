from PIL import Image, ImageFile
from .conversion import ImageConversion
from potrace import Bitmap, Path
from typing import Tuple, List
import math

 # Point class is private inside potracer
class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

class SketchImage():
    image_path: str
    shades: int
    conversion_method: str
    image_file: ImageFile.ImageFile
    current_x: int
    current_y: int
    left_to_right: bool
    previous_shade: int
    EOF: bool
    saved_pixel: Tuple[Tuple[int, int], float]
    potrace_path: Path
    saved_segment: List
    is_saved_segment_last: bool
    saved_segment_start: Point

    def __init__(self, path: str, shades: int, conversion_method: str):
        self.image_path = path
        self.shades = shades
        self.conversion_method = conversion_method
        self.left_to_right = True
        self.current_x = 0
        self.current_y = 0
        self.previous_shade = -1
        self.saved_segment = []
        self.is_saved_segment_last = False
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
            if (self.conversion_method == ImageConversion.POTRACE.name):
                potrace_bitmap = Bitmap(self.image_file, self.shades / 255.0)
                potrace_bitmap.invert()
                self.potrace_path = potrace_bitmap.trace()
                if len(self.potrace_path.curves) == 0:
                    self.EOF = True
                else:
                    self.saved_segment_start = self.potrace_path.curves[0].start_point
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

    def infer_bezier_steps(self, a, u, w, b) -> int:
        au = math.ceil(math.sqrt(math.pow(a.x-u.x, 2) + pow(a.y-u.y, 2)))
        uw = math.ceil(math.sqrt(math.pow(u.x-w.x, 2) + pow(u.y-w.y, 2)))
        wb = math.ceil(math.sqrt(math.pow(w.x-b.x, 2) + pow(w.y-b.y, 2)))
        ab = math.ceil(math.sqrt(math.pow(a.x-b.x, 2) + pow(a.y-b.y, 2)))
        return math.ceil(math.sqrt(au + uw + wb - ab)) * 2 + 1

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
    
    def next_segment(self):
        seg = self.potrace_path.curves[0].segments.pop(0)
        self.is_saved_segment_last = False
        if (len(self.potrace_path.curves[0].segments) == 0):
            self.is_saved_segment_last = True
            self.potrace_path.curves.pop(0)
            if (len(self.potrace_path.curves) == 0):
                self.EOF = True
            # else:
            #     self.saved_segment_start = self.potrace_path.curves[0].start_point
        if seg.is_corner:
            self.saved_segment = [seg.c]
        else:
            steps = self.infer_bezier_steps(self.saved_segment_start, seg.c1, seg.c2, seg.end_point)
            self.saved_segment = []
            for i in range(steps):
                t = i / steps
                bx = (math.pow(1 - t, 3) * self.saved_segment_start.x + 
                        3 * math.pow(1 - t, 2) * t * seg.c1.x +
                        3 * (1 - t) * math.pow(t, 2) * seg.c2.x +
                        math.pow(t, 3) * seg.end_point.x)
                by = (math.pow(1 - t, 3) * self.saved_segment_start.y + 
                        3 * math.pow(1 - t, 2) * t * seg.c1.y +
                        3 * (1 - t) * math.pow(t, 2) * seg.c2.y +
                        math.pow(t, 3) * seg.end_point.y)
                self.saved_segment.append(Point(bx, by))
        self.saved_segment.append(seg.end_point)

    def next_point(self, translate_x: int = 0, translate_y: int = 0) -> Tuple[
            float, float, float, float, float, float, bool]:
        if (self.conversion_method == ImageConversion.NAIVE.name):
            pixel = self.saved_pixel
            self.saved_pixel = self.next_pixel()
            if (pixel == None): return None
            (x,y), val = pixel
            shade = self.value_to_shade(val)
            width = 0 if shade == self.shades - 1 else 1
            pressure = 1 - shade / self.shades
            return x+translate_x, y+translate_y, 1, width, 0, pressure, False
        elif (self.conversion_method == ImageConversion.POTRACE.name):
            if len(self.saved_segment) == 0:
                self.next_segment()
            if len(self.saved_segment) == 1:
                if self.is_saved_segment_last:
                    self.saved_segment_start = self.potrace_path.curves[0].start_point
                    point = self.saved_segment.pop(0)
                    return point.x+translate_x, point.y+translate_y, 1, 2, 0, 1, self.is_saved_segment_last
                self.saved_segment_start = self.saved_segment.pop(0)
                return self.saved_segment_start.x+translate_x, self.saved_segment_start.y+translate_y, 1, 2, 0, 1, False
            point = self.saved_segment.pop(0)
            return point.x+translate_x, point.y+translate_y, 1, 2, 0, 1, False
    