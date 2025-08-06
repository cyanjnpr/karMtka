from kaitai import rm_v6
from .id import RemarkableId
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_id, create_sig_len, create_sig_u4

class GroupItemPacket(rm_v6.RmV6.CrdtGroupItemPacket):
    kind = rm_v6.RmV6.PacketType.group_item
    min_ver = 1
    ver = 1

    def __init__(self, parent, parent_id: RemarkableId, node_id: RemarkableId):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.positioned_packet = rm_v6.RmV6.PositionedChildPacket(None, self, self._root)
        self.positioned_packet.parent_id_sig = create_sig_id(self.positioned_packet, cnt.next())
        self.positioned_packet.parent_id = parent_id.to_kaitai(self.positioned_packet)
        self.positioned_packet.child_packet = rm_v6.RmV6.PositionedPacket(None, self.positioned_packet, self.positioned_packet._root)
        self.positioned_packet.child_packet.id_sig = create_sig_id(self.positioned_packet.child_packet, cnt.next())
        self.positioned_packet.child_packet.id = RemarkableId(0).to_kaitai(self.positioned_packet.child_packet)
        self.positioned_packet.child_packet.left_sig = create_sig_id(self.positioned_packet.child_packet, cnt.next())
        self.positioned_packet.child_packet.left = RemarkableId.zero().to_kaitai(self.positioned_packet.child_packet)
        self.positioned_packet.child_packet.right_sig = create_sig_id(self.positioned_packet.child_packet, cnt.next())
        self.positioned_packet.child_packet.right = RemarkableId.zero().to_kaitai(self.positioned_packet.child_packet)
        self.positioned_packet.child_packet.deleted_length_sig = create_sig_u4(self.positioned_packet.child_packet, cnt.next())
        self.positioned_packet.child_packet.deleted_length = 0
        self.node = rm_v6.RmV6.CrdtGroupItemNode(None, self, self._root)
        self.node.node_id_length_sig = create_sig_len(self.node, cnt.next())
        cnt.reset()
        cnt.next()
        self.node.unknown_byte = 2
        self.node.node_id_sig = create_sig_id(self.node, cnt.next())
        self.node.node_id = node_id.to_kaitai(self.node)
        self.node.node_id_length = 2 + self.node.node_id.len
    
    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            GroupItemPacket.min_ver, GroupItemPacket.ver, GroupItemPacket.kind)
        return self.parent
    
