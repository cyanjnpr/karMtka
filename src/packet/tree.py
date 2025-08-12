from kaitai import rm_v6
from .id import RemarkableId
from .text import create_text
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_id, create_sig_u1, create_sig_len

class TreeMovePacket(rm_v6.RmV6.SceneTreeMovePacket):
    kind = rm_v6.RmV6.PacketType.tree_move
    min_ver = 1
    ver = 1

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, parent_id: RemarkableId = RemarkableId.zero(), 
        id: RemarkableId = RemarkableId.zero(), node: RemarkableId = RemarkableId.zero()):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.id_sig = create_sig_id(self, cnt.next())
        self.id = id.to_kaitai(self)
        self.node_sig = create_sig_id(self, cnt.next())
        self.node = node.to_kaitai(self)
        self.item_sig = create_sig_u1(self, cnt.next())
        self.item = 1
        self.parent_length_sig = create_sig_len(self, cnt.next())
        cnt.reset()
        self.parent_sig = create_sig_id(self, cnt.next())
        self.parent_id = parent_id.to_kaitai(self)
        self.parent_length = self.parent_id.len + 1
    
    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            TreeMovePacket.min_ver, TreeMovePacket.ver, TreeMovePacket.kind)
        return self.parent
    
    
class TreeNodePacket(rm_v6.RmV6.SceneTreeNodePacket):
    kind = rm_v6.RmV6.PacketType.tree_node
    min_ver = 1
    ver = 2

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, label: str = "", 
        id: RemarkableId = RemarkableId.zero(), timestamp: RemarkableId = RemarkableId.zero(),
        nod: RemarkableId = RemarkableId.zero()):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        cnt = SigCounter(1)
        self.id_sig = create_sig_id(self, cnt.next())
        self.id = id.to_kaitai(self)
        self.name_length_sig = create_sig_len(self, cnt.next())
        cnt.reset()
        self.timestamp_sig = create_sig_id(self, cnt.next())
        self.timestamp = timestamp.to_kaitai(self)
        self.name = create_text(self, label, cnt)
        self.name_length = 1 + self.name.len + self.timestamp.len
        self.node_length_sig = create_sig_len(self, cnt.next())
        cnt.reset()
        self.node_sig = create_sig_id(self, cnt.next())
        self.node = nod.to_kaitai(self)
        self.node_value_sig = create_sig_u1(self, cnt.next())
        self.node_value = 1
        self.node_length = 3 + self.node.len

    def rename_label(self, label: str):
        self.name = label
        self.name_length = 1 + self.name.len + self.timestamp.len

    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            TreeNodePacket.min_ver, TreeNodePacket.ver, TreeNodePacket.kind)
        return self.parent