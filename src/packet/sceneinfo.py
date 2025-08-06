from kaitai import rm_v6
from .id import RemarkableId
from .packet import create_packet_backbone, SigCounter, create_header, create_sig_id, create_sig_u1, create_sig_len

class SceneInfoPacket(rm_v6.RmV6.SceneInfoPacket):
    kind = rm_v6.RmV6.PacketType.scene
    min_ver = 0
    ver = 1

    def __init__(self, parent):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        scene_cnt = SigCounter(1)
        subfields_cnt = SigCounter(1)

        self.current_layer = rm_v6.RmV6.SceneInfoCurrentLayer(None, self, self._root)
        self.current_layer.current_layer_sig = create_sig_len(self.current_layer, scene_cnt.next())
        self.current_layer.timestamp_sig = create_sig_id(self.current_layer, subfields_cnt.next())
        self.current_layer.timestamp = RemarkableId.zero().to_kaitai(self.current_layer)
        self.current_layer.value_sig = create_sig_id(self.current_layer, subfields_cnt.next())
        self.current_layer.value = RemarkableId.zero().to_kaitai(self.current_layer)
        self.current_layer.current_layer_length = self.current_layer.len - 5

        subfields_cnt.reset()
        self.background_visible = rm_v6.RmV6.SceneInfoBackgroundVisible(None, self, self._root)
        self.background_visible.background_visible_sig = create_sig_len(self.background_visible, scene_cnt.next())
        self.background_visible.timestamp_sig = create_sig_id(self.background_visible, subfields_cnt.next())
        self.background_visible.timestamp = RemarkableId.zero().to_kaitai(self.background_visible)
        self.background_visible.value_sig = create_sig_u1(self.background_visible, subfields_cnt.next())
        self.background_visible.value = 1
        self.background_visible.background_visible_length = self.background_visible.len - 5

        subfields_cnt.reset()
        self.root_document_visible = rm_v6.RmV6.SceneInfoRootDocumentVisible(None, self, self._root)
        self.root_document_visible.root_document_visible_sig = create_sig_len(self.root_document_visible, scene_cnt.next())
        self.root_document_visible.timestamp_sig = create_sig_id(self.root_document_visible, subfields_cnt.next())
        self.root_document_visible.timestamp = RemarkableId.zero().to_kaitai(self.root_document_visible)
        self.root_document_visible.value_sig = create_sig_u1(self.root_document_visible, subfields_cnt.next())
        self.root_document_visible.value = 1
        self.root_document_visible.root_document_visible_length = self.root_document_visible.len - 5
    
    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len,
            SceneInfoPacket.min_ver, SceneInfoPacket.ver, SceneInfoPacket.kind)
        return self.parent
    
