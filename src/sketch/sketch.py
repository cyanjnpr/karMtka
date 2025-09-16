from packet import RemarkableId, LinePacket
from typing import List
from kaitai import rm_v6
from .image import SketchImage

# xochitl won't render a line consisting of more points
MAX_POINTS = 30_000
POINTS_CAP = int(MAX_POINTS * 0.7)

class Sketch():
    parent: rm_v6.ReadWriteKaitaiStruct
    lines: List[LinePacket]

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, layer_id: RemarkableId, device_type):
        self.device_type = device_type
        self.layer = layer_id
        self.parent = parent
        self.lines = [
            LinePacket(self.parent, self.layer)
        ]

    def current_line(self) -> LinePacket:
        return self.lines[len(self.lines) - 1]

    def draw_point(self, x: float ,y: float, 
        speed: float, width: float, direction: float, pressure: float, is_last: bool = False):
        self.current_line().new_point(x, y, speed, width, direction, pressure)
        if self.current_line().num_points() > POINTS_CAP or is_last:
            self.lines.append(LinePacket(self.parent, self.layer))

    # for testing parameters and how they change displayed line
    def rectangle(self, start_x, start_y, width, height):
        value, speed, pressure, direction = 1, 1, 1, 0
        for y in range(start_y, start_y + height, 2):
            pressure = (y - start_y) / height
            self.draw_point(start_x, y, speed, value, direction, pressure)
            self.draw_point(start_x + width, y, speed, value, direction, pressure)
            self.draw_point(start_x + width, y+1, speed, value, direction, pressure)
            self.draw_point(start_x, y+1, speed, value, direction, pressure)

    def draw_image(self, image_path: str, quality: int, conversion_method: str):
        screen_height = self.device_type.h()
        with SketchImage(image_path, quality, conversion_method, self.device_type.w(), self.device_type.h()) as img:
            if (img.EOF): return
            origin_x = -img.image_file.width / 2.0
            origin_y = self.device_type.margin + (screen_height - img.image_file.height) / 2.0
            p = img.next_point(origin_x, origin_y)
            while (not img.EOF):
                self.draw_point(*p)
                p = img.next_point(origin_x, origin_y)
                
