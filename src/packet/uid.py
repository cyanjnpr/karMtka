from kaitai import rm_v6
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_len
import uuid

class UuidItem(rm_v6.RmV6.UuidItem):

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, cnt: SigCounter, uid: uuid.UUID):
        super().__init__(None, parent, parent._root)
        self.uuid_length_sig = create_sig_len(self, cnt.next())
        u_hex = uid.hex
        self.uuid = [int(u_hex[i:i+2], 16) for i in range(0, len(u_hex), 2)]
        self.second = 1
        self.unknown_byte_2 = 0
        self.uuid_length = len(self.uuid)
        self.uuid_packet_length = self.uuid_length + 3


class UuidPacket(rm_v6.RmV6.UuidPacket):
    kind = rm_v6.RmV6.PacketType.uuid 
    min_ver = 1
    ver = 1

    def __init__(self, parent, uid: uuid.UUID):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.uuids = [
            UuidItem(self, cnt, uid)
        ]
        self.num_uuids = len(self.uuids)
    
    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            UuidPacket.min_ver, UuidPacket.ver, UuidPacket.kind)
        return self.parent
    
