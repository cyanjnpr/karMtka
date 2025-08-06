from kaitai import rm_v6
from .id import RemarkableId
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_id, create_sig_u1

class MigrationPacket(rm_v6.RmV6.MigrationInfoPacket):
    kind = rm_v6.RmV6.PacketType.migration
    min_ver = 1
    ver = 1

    def __init__(self, parent):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.migration_id_sig = create_sig_id(self, cnt.next())
        self.migration_id = RemarkableId.one().to_kaitai(self)
        self.device_sig = create_sig_u1(self, cnt.next())
        self.device = 1
        self.v3_sig = create_sig_u1(self, cnt.next())
        self.v3 = 0
    
    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            MigrationPacket.min_ver, MigrationPacket.ver, MigrationPacket.kind)
        return self.parent
    
