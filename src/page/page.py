from kaitai import rm_v6
import uuid
from typing import List
from .resolution import DeviceResolution
from packet import *
from config import C_SKETCH_IMPLEMENTATION
if (C_SKETCH_IMPLEMENTATION):
    from sketch import CSketch
else:
    from sketch import Sketch

class Page(rm_v6.RmV6):

    def __init__(self, uid: uuid.UUID, device: DeviceResolution, margin: int):
        super().__init__()
        self.device_type = device
        self.margin = margin
        self.header = "reMarkable .lines file, version=6          "
        self.layer_ids: List[RemarkableId] = []
        self.moves: List[TreeMovePacket] = []
        self.nodes: List[TreeNodePacket] = []
        self.groups: List[GroupItemPacket] = []
        self.packets: List[rm_v6.RmV6.Packet] = [
            UuidPacket(self, uid).pack(),
            MigrationPacket(self).pack()
        ]
        self.raw = bytearray()

    def build_append_stats(self, lines: List[str]):
        line_count = 1 + sum([line.count("\n") for line in lines])
        char_count = sum([len(line) for line in lines])
        self.packets.append(StatsPacket(self, char_count, line_count).pack())

    def build_tree(self, layers = 1):
        root_id = RemarkableId(0)
        self.nodes.append(TreeNodePacket(self, "", root_id))
        # to match files from the device
        RemarkableId.move_counter(9)
        for layer in range(1, layers+1):
            layer_id = RemarkableId(0)
            layer_timestamp = RemarkableId(0)
            self.layer_ids.append(layer_id)
            self.nodes.append(TreeNodePacket(self, "Layer {}".format(layer), layer_id, layer_timestamp))
            self.moves.append(TreeMovePacket(self, root_id, layer_id))
            self.groups.append(GroupItemPacket(self, root_id, layer_id))

    def build_append_lines(self, images: List[str], quality: int):
        for layer, image_path in enumerate(images):
            if (C_SKETCH_IMPLEMENTATION):
                s = CSketch(self.device_type.value)
                self.raw.extend(s.convert(
                    image_path, self.layer_ids[layer].minor, RemarkableId.internal_counter, quality))
            else:
                if (len(self.layer_ids) <= layer): return
                s = Sketch(self, self.layer_ids[layer])
                s.draw_image(image_path, quality, self.device_type.value)
                for l in s.lines: self.packets.append(l.pack())

    def build(self, lines: List[str], styles: List[int], weights: List[int], images: List[str], quality: int):
        self.build_append_stats(lines)
        self.build_tree(1 + len(images))
        self.packets.append(SceneInfoPacket(self, self.layer_ids[len(self.layer_ids) - 1]).pack())
        self.packets.extend([move.pack() for move in self.moves])
        t = TextPacket(self, lines, styles, weights, 
            self.device_type.value.with_margin(self.margin).w(), self.margin)
        self.packets.append(t.pack())
        self.packets.extend([node.pack() for node in self.nodes])
        self.packets.extend([group.pack() for group in self.groups])
        self.build_append_lines(images, quality)

