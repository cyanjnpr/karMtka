from kaitai import rm_v6
from .id import RemarkableId
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_id, create_sig_dbl, create_sig_len, create_sig_u4
import math
from enum import Enum

class SketchTools(Enum):
    PAINTBRUSH = 12 # doesn't show at all, unusable
    MECHANICAL = 13 # looks fine
    PENCIL = 14 # looks fine
    BALLPOINT = 15 # very sensitive to pressure, fully filled at around 25% of max pressure
    MARKER = 16 # doesn't show at all, unusable
    FINELINER = 17 # no pressure detection, unusable
    HIGHLIGHTER = 18 # ends up as blob, unusable
    CALIGRAPHY = 21 # no pressure detection, unusable

class SketchColors(Enum):
    BLACK = 0

class Point(rm_v6.RmV6.Point):

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, x: float, y: float, 
                 speed: float, width: float, direction: float, pressure: float):
        super().__init__(None, parent, parent._root)
        self.x = x
        self.y = y
        self.speed = int(min(2**14, speed) * 4)
        self.width = int(min(2**14, width) * 4)
        self.direction = int(min(direction, 1) / (2 * math.pi) * 255)
        self.pressure = int(min(pressure, 1) * 255)

    def translate_by(self, x: float, y: float):
        self.x += x
        self.y += y
        return self
        
    def __len__(self):
        return 14
    
    @staticmethod
    def len():
        return 14
     

class LinePoints(rm_v6.RmV6.CrdtLineItemPoints):

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, cnt: SigCounter):
        super().__init__(None, parent, parent._root)
        self.length_sig = create_sig_len(self, cnt.next())
        self.unknown_byte = 3
        cnt.reset()
        self.tool_sig = create_sig_u4(self, cnt.next())
        self.tool = SketchTools.MECHANICAL.value
        self.color_sig = create_sig_u4(self, cnt.next())
        self.color = SketchColors.BLACK.value
        self.thickness_scale_sig =  create_sig_dbl(self, cnt.next())
        self.thickness_scale = 1.0
        self.starting_length_sig = create_sig_u4(self, cnt.next())
        self.starting_length = 0
        self.points_length_sig = create_sig_len(self, cnt.next())
        cnt.reset()
        for _ in range(5): cnt.next()
        self.ts_sig = create_sig_id(self, cnt.next())
        self.ts = RemarkableId(0, 1).to_kaitai(self)
        self.points = []
        self.recalculate_lengths()

    def recalculate_lengths(self):
        self.points_length = len(self.points) * Point.len()
        self.length = self.points_length + 31 + self.ts.len

    def append_point(self, point: Point):
        self.points.append(point)
        self.recalculate_lengths()


class LinePacket(rm_v6.RmV6.CrdtLineItemPacket):
    kind = rm_v6.RmV6.PacketType.line_item
    min_ver = 2
    ver = 2

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, parent_id: RemarkableId):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.positioned_packet = rm_v6.RmV6.PositionedChildPacket(None, self, self._root)
        self.positioned_packet.parent_id_sig = create_sig_id(self, cnt.next())
        self.positioned_packet.parent_id = parent_id.to_kaitai(self.positioned_packet)
        self.positioned_packet.child_packet = rm_v6.RmV6.PositionedPacket(None, self.positioned_packet, self.positioned_packet._root)
        self.positioned_packet.child_packet.id_sig = create_sig_id(self, cnt.next())
        self.positioned_packet.child_packet.id = RemarkableId(1).to_kaitai(self.positioned_packet.child_packet)
        self.positioned_packet.child_packet.left_sig = create_sig_id(self, cnt.next())
        self.positioned_packet.child_packet.left = RemarkableId.zero().to_kaitai(self.positioned_packet.child_packet)
        self.positioned_packet.child_packet.right_sig = create_sig_id(self, cnt.next())
        self.positioned_packet.child_packet.right = RemarkableId.zero().to_kaitai(self.positioned_packet.child_packet)
        self.positioned_packet.child_packet.deleted_length_sig = create_sig_u4(self, cnt.next())
        self.positioned_packet.child_packet.deleted_length = 0
        self.points = LinePoints(self, cnt)

    def append_point(self, point: Point):
        self.points.append_point(point)

    def new_point(self, x: float, y: float, 
        speed: float, width: float, direction: float, pressure: float):
        self.points.append_point(Point(self.points, x, y,
            speed, width, direction, pressure))
        
    def num_points(self) -> int:
        return len(self.points.points)

    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len + sum(len(p) for p in self.points.points),
            LinePacket.min_ver, LinePacket.ver, LinePacket.kind)
        return self.parent
    
