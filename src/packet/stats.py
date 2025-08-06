from kaitai import rm_v6
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_u4

class StatsPacket(rm_v6.RmV6.PageStatsPacket):
    kind = rm_v6.RmV6.PacketType.stats
    min_ver = 0
    ver = 1

    def __init__(self, parent, text_chars: int, text_lines: int):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.loads_sig = create_sig_u4(self, cnt.next())
        self.loads = 0
        self.merges_sig = create_sig_u4(self, cnt.next())
        self.merges = 0
        self.text_chars_sig = create_sig_u4(self, cnt.next())
        self.text_chars = text_chars
        self.text_lines_sig = create_sig_u4(self, cnt.next())
        self.text_lines = text_lines
        self.keyboard_count_sig = create_sig_u4(self, cnt.next())
        self.keyboard_count = 0
    
    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            StatsPacket.min_ver, StatsPacket.ver, StatsPacket.kind)
        return self.parent
    
