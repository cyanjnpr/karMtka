from .packet import create_sig_len, SigCounter, create_kaitai_leb, create_sig_id, create_sig_u1, create_packet_backbone, create_sig_u4, create_header
from typing import List
from kaitai import rm_v6
from .id import RemarkableId
from enum import Enum

SIG_BOLD_START = 1
SIG_BOLD_END = 2
SIG_ITALIC_START = 3
SIG_ITALIC_END = 4

class FontWeight(Enum):
    NORMAL = 1
    BOLD = 2
    ITALIC = 3
    BOLD_ITALIC = 4

    def __len__(self):
        if (self == FontWeight.BOLD):
            return 2
        elif (self == FontWeight.ITALIC):
            return 2
        elif (self == FontWeight.BOLD_ITALIC):
            return 4
        elif(self == FontWeight.NORMAL):
            return 0
        return 0

def create_text(parent: rm_v6.ReadWriteKaitaiStruct, line: str, cnt: SigCounter = SigCounter(1)) -> rm_v6.RmV6.Text:
    text = rm_v6.RmV6.Text(None, parent, parent._root)
    text.text_length_sig = create_sig_len(text, cnt.next())
    text.unknown_byte = 1
    text.stripped_text_length = create_kaitai_leb(len(line.encode('utf-8')))
    text.text_length = text.stripped_text_length.len + len(line.encode('utf-8')) + 1
    text.text = line
    return text

def create_style(parent: rm_v6.ReadWriteKaitaiStruct, 
        key: RemarkableId, style_val: int) -> rm_v6.RmV6.TextStyle:
    style = rm_v6.RmV6.TextStyle(None, parent, parent._root)
    style.key = key.to_kaitai(style)
    style.timestamp_sig = create_sig_id(style, 1)
    style.timestamp = RemarkableId(1).to_kaitai(style)
    style.style_length_sig = create_sig_len(style, 2)
    style.style_length = 2 # constant size
    style.style_sig = create_sig_u1(style, 1)
    style.style = style_val
    return style

# find all nl charactercs and optionally translate positions by a certain num
# ignore direct repetitions of nl, there's no point in applying a style to an empty line
def new_line_positions(lines: List[str], translate_by: int = 0):
    pos = []
    i = max(translate_by, 0)
    for line in lines:
        previous_ch = ''
        for ch in line:
            if ch == '\n' and previous_ch != '\n':
                pos.append(i)
            i += 1
            previous_ch = ch
    return pos

class TextPosition(rm_v6.RmV6.TextPosition):

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, 
            width: float, y_pos: float):
        super().__init__(None, parent, parent._root)
        self.root_text_length_sig = create_sig_len(self, 2)
        self.styles_length_sig = create_sig_len(self, 1)
        self.styles : List[rm_v6.RmV6.TextStyle] = []
        self.num_styles = create_kaitai_leb(len(self.styles))
        self.styles_length = self.num_styles.len + sum(st.len for st in self.styles)
        self.root_text_length = self.styles_length + 5
        self.position_length_sig = create_sig_len(self, 3)
        self.position_length = 16
        self.text_width_sig = create_sig_u4(self, 4)
        self.text_width = float(width)
        self.x = float(-self.text_width / 2)
        self.y = float(y_pos)

    def recalculate_styles_len(self):
        self.num_styles = create_kaitai_leb(len(self.styles))
        self.styles_length = self.num_styles.len + sum(st.len for st in self.styles)
        self.root_text_length = self.styles_length + 5

    def with_style(self, style: rm_v6.RmV6.TextStyle):
        self.styles.append(style)
        self.recalculate_styles_len()


class TextItem(rm_v6.RmV6.TextItem):

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, line: str, weight: int = None,
            id: RemarkableId = RemarkableId.zero(), left: RemarkableId = RemarkableId.zero(), 
            right: RemarkableId = RemarkableId.zero()):
        super().__init__(None, parent, parent._root)
        cnt = SigCounter()
        self.text_item_length_sig = create_sig_len(self, cnt.next())
        cnt.next() # for some reason one sig is omitted
        self.positioned_packet = rm_v6.RmV6.PositionedPacket(None, self, self._root)
        self.positioned_packet.id_sig = create_sig_id(self.positioned_packet, cnt.next())
        self.id = id
        self.positioned_packet.id = self.id.to_kaitai(self.positioned_packet)
        self.positioned_packet.left_sig = create_sig_id(self.positioned_packet, cnt.next())
        self.positioned_packet.left = left.to_kaitai(self.positioned_packet)
        self.positioned_packet.right_sig = create_sig_id(self.positioned_packet, cnt.next())
        self.positioned_packet.right = right.to_kaitai(self.positioned_packet)
        self.positioned_packet.deleted_length_sig = create_sig_u4(self.positioned_packet, cnt.next())
        self.positioned_packet.deleted_length = 0
        self.text = create_text(self, line, cnt)
        if weight != None:
            cnt.reset()
            cnt.next()
            cnt.next()
            self.font_weight_sig = create_sig_u4(self, cnt.next())
            self.font_weight = weight
            self.text.text_length += 5
            self.text_item_length = self.positioned_packet.len + self.text.len + 5
        else:
            self.text_item_length = self.positioned_packet.len + self.text.len

    def translate_index(self, index: int):
        t: str = self.text.text
        if len(t) <= index:
            return RemarkableId.zero()
        return self.start_id() + index

    def start_id(self):
        return self.id

    def end_id(self):
        return RemarkableId(1, self.id.minor + self.text.stripped_text_length.value - 1)


class TextPacket(rm_v6.RmV6.TextPacket):
    kind = rm_v6.RmV6.PacketType.text_item
    min_ver = 1
    ver = 1

    def __init__(self, parent: rm_v6.ReadWriteKaitaiStruct, lines: List[str], styles: List[int], 
            weights: List[int], width: float = 936, y_pos: float = 234):
        self.parent = create_packet_backbone(parent)
        super().__init__(None, self.parent, self.parent._root)
        self.parent_id_sig = create_sig_id(self, 1)
        # only one text packet per file (i think?), parent_id always zero
        self.parent_id = RemarkableId.zero().to_kaitai(self)
        self.length_with_styles_sig = create_sig_len(self, 2)
        self.length_with_text_sig = create_sig_len(self, 1)
        self.length_with_text_inner_sig = create_sig_len(self, 1)
        self.items: List[TextItem] = []
        keys = new_line_positions(lines, RemarkableId.position()+1)
        self.create_items(lines)
        self.create_weights(weights)
        # set only after weights, since they are also items, unlike styles
        self.num_items = create_kaitai_leb(len(self.items))
        self.position = TextPosition(self, width, y_pos)
        self.create_styles(keys, styles)
        self.length_with_text_inner = 1 + sum(t.len for t in self.items)
        self.length_with_text = self.length_with_text_inner + 5
        self.length_with_styles = (self.length_with_text + 5 + sum(s.len for s in self.position.styles) +
            10 + self.position.num_styles.len)

    def create_items(self, lines: List[str]):
        for i, line in enumerate(lines):
            if i == 0:
                current = TextItem(self, line, id = RemarkableId(1))
            else:
                id = RemarkableId(1)
                current = TextItem(self, line, id=id, left=(id - 1))
            RemarkableId.move_counter(len(line)-1)
            self.items.append(current)

    def create_styles(self, keys: List[int], styles: List[int]):
        self.position.with_style(create_style(self.position, RemarkableId.zero(), styles[0]))
        for i, key in enumerate(keys):
            style = create_style(self.position, RemarkableId(1, key+1), styles[min(i+1, len(styles) - 1)])
            self.position.with_style(style)

    def create_weights(self, weights: List[int]):
        items_updated = []
        left = RemarkableId.zero()
        for i, item in enumerate(self.items):
            right = self.items[i+1].start_id() if i < len(self.items) - 1 else RemarkableId.zero()
            weight = FontWeight(weights[min(i, len(weights) - 1)])
            if (weight == FontWeight.BOLD):
                start = TextItem(self, "", SIG_BOLD_START, id=RemarkableId(1), 
                    left=left, right=item.start_id())
                end = TextItem(self, "", SIG_BOLD_END, id=RemarkableId(1), 
                    left=item.end_id(), right=right)
                items_updated.extend([start, item, end])
            elif (weight  == FontWeight.ITALIC):
                start = TextItem(self, "", SIG_ITALIC_START, id=RemarkableId(1), 
                    left=left, right=item.start_id())
                end = TextItem(self, "", SIG_ITALIC_END, id=RemarkableId(1), 
                    left=item.end_id(), right=right)
                items_updated.extend([start, item, end])
            elif (weight == FontWeight.BOLD_ITALIC):
                # for both styles to be applied, matching style ids must follow directly
                start_i_id = RemarkableId(1)
                end_i_id = RemarkableId(1)
                start_i = TextItem(self, "", SIG_ITALIC_START, id=start_i_id, 
                    left=left, right=item.start_id())
                start_b = TextItem(self, "", SIG_BOLD_START, id=RemarkableId(1), 
                    left=start_i_id, right=item.start_id())
                end_b = TextItem(self, "", SIG_BOLD_END, id=RemarkableId(1), 
                    left=item.end_id(), right=RemarkableId.zero())
                end_i = TextItem(self, "", SIG_ITALIC_END, id=end_i_id, 
                    left=item.end_id(), right=right)
                end_b.positioned_packet.right = end_i_id.to_kaitai(end_b.positioned_packet)
                items_updated.extend([start_i, start_b, item, end_b, end_i])
            elif (weight == FontWeight.NORMAL):
                items_updated.append(item)
            left = item.end_id()
            
        self.items = items_updated

    def pack(self) -> rm_v6.RmV6.Packet:
        self.parent.packet_body = self
        self.parent.packet_header = create_header(self.parent, self.len + sum(i.len for i in self.items) +
            sum(s.len for s in self.position.styles),
            TextPacket.min_ver, TextPacket.ver, TextPacket.kind)
        return self.parent
    
