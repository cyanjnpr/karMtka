# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

from . import kaitai_leb128 as leb128
class RmV6(ReadWriteKaitaiStruct):

    class PacketType(IntEnum):
        migration = 0
        tree_move = 1
        tree_node = 2
        glyph_item = 3
        group_item = 4
        line_item = 5
        text_item = 7
        uuid = 9
        stats = 10
        scene = 13
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.header = (self._io.read_bytes(43)).decode("ASCII")
        self.packets = []
        i = 0
        while not self._io.is_eof():
            _t_packets = RmV6.Packet(self._io, self, self._root)
            _t_packets._read()
            self.packets.append(_t_packets)
            i += 1



    def _fetch_instances(self):
        pass
        for i in range(len(self.packets)):
            pass
            self.packets[i]._fetch_instances()



    def _write__seq(self, io=None):
        super(RmV6, self)._write__seq(io)
        self._io.write_bytes((self.header).encode(u"ASCII"))
        for i in range(len(self.packets)):
            pass
            if self._io.is_eof():
                raise kaitaistruct.ConsistencyError(u"packets", self._io.size() - self._io.pos(), 0)
            self.packets[i]._write__seq(self._io)

        if not self._io.is_eof():
            raise kaitaistruct.ConsistencyError(u"packets", self._io.size() - self._io.pos(), 0)


    def _check(self):
        pass
        if (len((self.header).encode(u"ASCII")) != 43):
            raise kaitaistruct.ConsistencyError(u"header", len((self.header).encode(u"ASCII")), 43)
        for i in range(len(self.packets)):
            pass
            if self.packets[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"packets", self.packets[i]._root, self._root)
            if self.packets[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"packets", self.packets[i]._parent, self)


    class CrdtGlyphItemValue(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.length_sig = RmV6.SigLen(self._io, self, self._root)
            self.length_sig._read()
            self.length = self._io.read_u4le()
            self.unknown_byte_1 = self._io.read_u1()
            self.color_sig = RmV6.SigU4(self._io, self, self._root)
            self.color_sig._read()
            self.color = self._io.read_u4le()
            self.text = RmV6.Text(self._io, self, self._root)
            self.text._read()
            self.rect = RmV6.GlyphRect(self._io, self, self._root)
            self.rect._read()
            self.first_sig = RmV6.SigId(self._io, self, self._root)
            self.first_sig._read()
            self.first = RmV6.IdField(self._io, self, self._root)
            self.first._read()
            self.last_sig = RmV6.SigId(self._io, self, self._root)
            self.last_sig._read()
            self.unknown_byte_2 = self._io.read_u1()
            self.last = RmV6.IdField(self._io, self, self._root)
            self.last._read()
            self.include_last_id_sig = RmV6.SigU1(self._io, self, self._root)
            self.include_last_id_sig._read()
            self.unknown_byte_3 = self._io.read_u1()
            self.include_last_id = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.length_sig._fetch_instances()
            self.color_sig._fetch_instances()
            self.text._fetch_instances()
            self.rect._fetch_instances()
            self.first_sig._fetch_instances()
            self.first._fetch_instances()
            self.last_sig._fetch_instances()
            self.last._fetch_instances()
            self.include_last_id_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.CrdtGlyphItemValue, self)._write__seq(io)
            self.length_sig._write__seq(self._io)
            self._io.write_u4le(self.length)
            self._io.write_u1(self.unknown_byte_1)
            self.color_sig._write__seq(self._io)
            self._io.write_u4le(self.color)
            self.text._write__seq(self._io)
            self.rect._write__seq(self._io)
            self.first_sig._write__seq(self._io)
            self.first._write__seq(self._io)
            self.last_sig._write__seq(self._io)
            self._io.write_u1(self.unknown_byte_2)
            self.last._write__seq(self._io)
            self.include_last_id_sig._write__seq(self._io)
            self._io.write_u1(self.unknown_byte_3)
            self._io.write_u1(self.include_last_id)


        def _check(self):
            pass
            if self.length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"length_sig", self.length_sig._root, self._root)
            if self.length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"length_sig", self.length_sig._parent, self)
            if self.color_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"color_sig", self.color_sig._root, self._root)
            if self.color_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"color_sig", self.color_sig._parent, self)
            if self.text._root != self._root:
                raise kaitaistruct.ConsistencyError(u"text", self.text._root, self._root)
            if self.text._parent != self:
                raise kaitaistruct.ConsistencyError(u"text", self.text._parent, self)
            if self.rect._root != self._root:
                raise kaitaistruct.ConsistencyError(u"rect", self.rect._root, self._root)
            if self.rect._parent != self:
                raise kaitaistruct.ConsistencyError(u"rect", self.rect._parent, self)
            if self.first_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"first_sig", self.first_sig._root, self._root)
            if self.first_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"first_sig", self.first_sig._parent, self)
            if self.first._root != self._root:
                raise kaitaistruct.ConsistencyError(u"first", self.first._root, self._root)
            if self.first._parent != self:
                raise kaitaistruct.ConsistencyError(u"first", self.first._parent, self)
            if self.last_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"last_sig", self.last_sig._root, self._root)
            if self.last_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"last_sig", self.last_sig._parent, self)
            if self.last._root != self._root:
                raise kaitaistruct.ConsistencyError(u"last", self.last._root, self._root)
            if self.last._parent != self:
                raise kaitaistruct.ConsistencyError(u"last", self.last._parent, self)
            if self.include_last_id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"include_last_id_sig", self.include_last_id_sig._root, self._root)
            if self.include_last_id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"include_last_id_sig", self.include_last_id_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((((17 + self.text.len) + self.rect.len) + self.first.len) + self.last.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SceneTreeNodePacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.id_sig = RmV6.SigId(self._io, self, self._root)
            self.id_sig._read()
            self.id = RmV6.IdField(self._io, self, self._root)
            self.id._read()
            self.name_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.name_length_sig._read()
            self.name_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.name = RmV6.Text(self._io, self, self._root)
            self.name._read()
            self.node_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.node_length_sig._read()
            self.node_length = self._io.read_u4le()
            self.node_sig = RmV6.SigId(self._io, self, self._root)
            self.node_sig._read()
            self.node = RmV6.IdField(self._io, self, self._root)
            self.node._read()
            self.node_value_sig = RmV6.SigU1(self._io, self, self._root)
            self.node_value_sig._read()
            self.node_value = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.id_sig._fetch_instances()
            self.id._fetch_instances()
            self.name_length_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.name._fetch_instances()
            self.node_length_sig._fetch_instances()
            self.node_sig._fetch_instances()
            self.node._fetch_instances()
            self.node_value_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneTreeNodePacket, self)._write__seq(io)
            self.id_sig._write__seq(self._io)
            self.id._write__seq(self._io)
            self.name_length_sig._write__seq(self._io)
            self._io.write_u4le(self.name_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.name._write__seq(self._io)
            self.node_length_sig._write__seq(self._io)
            self._io.write_u4le(self.node_length)
            self.node_sig._write__seq(self._io)
            self.node._write__seq(self._io)
            self.node_value_sig._write__seq(self._io)
            self._io.write_u1(self.node_value)


        def _check(self):
            pass
            if self.id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id_sig", self.id_sig._root, self._root)
            if self.id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"id_sig", self.id_sig._parent, self)
            if self.id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id", self.id._root, self._root)
            if self.id._parent != self:
                raise kaitaistruct.ConsistencyError(u"id", self.id._parent, self)
            if self.name_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"name_length_sig", self.name_length_sig._root, self._root)
            if self.name_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"name_length_sig", self.name_length_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.name._root != self._root:
                raise kaitaistruct.ConsistencyError(u"name", self.name._root, self._root)
            if self.name._parent != self:
                raise kaitaistruct.ConsistencyError(u"name", self.name._parent, self)
            if self.node_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_length_sig", self.node_length_sig._root, self._root)
            if self.node_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_length_sig", self.node_length_sig._parent, self)
            if self.node_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_sig", self.node_sig._root, self._root)
            if self.node_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_sig", self.node_sig._parent, self)
            if self.node._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node", self.node._root, self._root)
            if self.node._parent != self:
                raise kaitaistruct.ConsistencyError(u"node", self.node._parent, self)
            if self.node_value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_value_sig", self.node_value_sig._root, self._root)
            if self.node_value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_value_sig", self.node_value_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((((15 + self.id.len) + self.timestamp.len) + self.name.len) + self.node.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SigU4(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.sig = self._io.read_u1()
            _ = self.sig
            if not ((_ & 15) == 4):
                raise kaitaistruct.ValidationExprError(self.sig, self._io, u"/types/sig_u4/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.SigU4, self)._write__seq(io)
            self._io.write_u1(self.sig)


        def _check(self):
            pass
            _ = self.sig
            if not ((_ & 15) == 4):
                raise kaitaistruct.ValidationExprError(self.sig, None, u"/types/sig_u4/seq/0")


    class Point(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.speed = self._io.read_u2le()
            self.width = self._io.read_u2le()
            self.direction = self._io.read_u1()
            self.pressure = self._io.read_u1()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.Point, self)._write__seq(io)
            self._io.write_f4le(self.x)
            self._io.write_f4le(self.y)
            self._io.write_u2le(self.speed)
            self._io.write_u2le(self.width)
            self._io.write_u1(self.direction)
            self._io.write_u1(self.pressure)


        def _check(self):
            pass

        @property
        def direction_value(self):
            if hasattr(self, '_m_direction_value'):
                return self._m_direction_value

            self._m_direction_value = (((self.direction * 2) * 3.14) / 255.0)
            return getattr(self, '_m_direction_value', None)

        def _invalidate_direction_value(self):
            del self._m_direction_value
        @property
        def pressure_value(self):
            if hasattr(self, '_m_pressure_value'):
                return self._m_pressure_value

            self._m_pressure_value = (self.pressure / 255.0)
            return getattr(self, '_m_pressure_value', None)

        def _invalidate_pressure_value(self):
            del self._m_pressure_value
        @property
        def speed_value(self):
            if hasattr(self, '_m_speed_value'):
                return self._m_speed_value

            self._m_speed_value = (self.speed / 4.0)
            return getattr(self, '_m_speed_value', None)

        def _invalidate_speed_value(self):
            del self._m_speed_value
        @property
        def width_value(self):
            if hasattr(self, '_m_width_value'):
                return self._m_width_value

            self._m_width_value = (self.width / 4.0)
            return getattr(self, '_m_width_value', None)

        def _invalidate_width_value(self):
            del self._m_width_value
        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = 14
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class PositionedPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.id_sig = RmV6.SigId(self._io, self, self._root)
            self.id_sig._read()
            self.id = RmV6.IdField(self._io, self, self._root)
            self.id._read()
            self.left_sig = RmV6.SigId(self._io, self, self._root)
            self.left_sig._read()
            self.left = RmV6.IdField(self._io, self, self._root)
            self.left._read()
            self.right_sig = RmV6.SigId(self._io, self, self._root)
            self.right_sig._read()
            self.right = RmV6.IdField(self._io, self, self._root)
            self.right._read()
            self.deleted_length_sig = RmV6.SigU4(self._io, self, self._root)
            self.deleted_length_sig._read()
            self.deleted_length = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            self.id_sig._fetch_instances()
            self.id._fetch_instances()
            self.left_sig._fetch_instances()
            self.left._fetch_instances()
            self.right_sig._fetch_instances()
            self.right._fetch_instances()
            self.deleted_length_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.PositionedPacket, self)._write__seq(io)
            self.id_sig._write__seq(self._io)
            self.id._write__seq(self._io)
            self.left_sig._write__seq(self._io)
            self.left._write__seq(self._io)
            self.right_sig._write__seq(self._io)
            self.right._write__seq(self._io)
            self.deleted_length_sig._write__seq(self._io)
            self._io.write_u4le(self.deleted_length)


        def _check(self):
            pass
            if self.id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id_sig", self.id_sig._root, self._root)
            if self.id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"id_sig", self.id_sig._parent, self)
            if self.id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id", self.id._root, self._root)
            if self.id._parent != self:
                raise kaitaistruct.ConsistencyError(u"id", self.id._parent, self)
            if self.left_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"left_sig", self.left_sig._root, self._root)
            if self.left_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"left_sig", self.left_sig._parent, self)
            if self.left._root != self._root:
                raise kaitaistruct.ConsistencyError(u"left", self.left._root, self._root)
            if self.left._parent != self:
                raise kaitaistruct.ConsistencyError(u"left", self.left._parent, self)
            if self.right_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"right_sig", self.right_sig._root, self._root)
            if self.right_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"right_sig", self.right_sig._parent, self)
            if self.right._root != self._root:
                raise kaitaistruct.ConsistencyError(u"right", self.right._root, self._root)
            if self.right._parent != self:
                raise kaitaistruct.ConsistencyError(u"right", self.right._parent, self)
            if self.deleted_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"deleted_length_sig", self.deleted_length_sig._root, self._root)
            if self.deleted_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"deleted_length_sig", self.deleted_length_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (((8 + self.id.len) + self.left.len) + self.right.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class TextStyle(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.key = RmV6.IdField(self._io, self, self._root)
            self.key._read()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.style_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.style_length_sig._read()
            self.style_length = self._io.read_u4le()
            self.style_sig = RmV6.SigU1(self._io, self, self._root)
            self.style_sig._read()
            self.style = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.key._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.style_length_sig._fetch_instances()
            self.style_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.TextStyle, self)._write__seq(io)
            self.key._write__seq(self._io)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.style_length_sig._write__seq(self._io)
            self._io.write_u4le(self.style_length)
            self.style_sig._write__seq(self._io)
            self._io.write_u1(self.style)


        def _check(self):
            pass
            if self.key._root != self._root:
                raise kaitaistruct.ConsistencyError(u"key", self.key._root, self._root)
            if self.key._parent != self:
                raise kaitaistruct.ConsistencyError(u"key", self.key._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.style_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"style_length_sig", self.style_length_sig._root, self._root)
            if self.style_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"style_length_sig", self.style_length_sig._parent, self)
            if self.style_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"style_sig", self.style_sig._root, self._root)
            if self.style_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"style_sig", self.style_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((8 + self.key.len) + self.timestamp.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class PositionedChildPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.parent_id_sig = RmV6.SigId(self._io, self, self._root)
            self.parent_id_sig._read()
            self.parent_id = RmV6.IdField(self._io, self, self._root)
            self.parent_id._read()
            self.child_packet = RmV6.PositionedPacket(self._io, self, self._root)
            self.child_packet._read()


        def _fetch_instances(self):
            pass
            self.parent_id_sig._fetch_instances()
            self.parent_id._fetch_instances()
            self.child_packet._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.PositionedChildPacket, self)._write__seq(io)
            self.parent_id_sig._write__seq(self._io)
            self.parent_id._write__seq(self._io)
            self.child_packet._write__seq(self._io)


        def _check(self):
            pass
            if self.parent_id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_id_sig", self.parent_id_sig._root, self._root)
            if self.parent_id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_id_sig", self.parent_id_sig._parent, self)
            if self.parent_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_id", self.parent_id._root, self._root)
            if self.parent_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_id", self.parent_id._parent, self)
            if self.child_packet._root != self._root:
                raise kaitaistruct.ConsistencyError(u"child_packet", self.child_packet._root, self._root)
            if self.child_packet._parent != self:
                raise kaitaistruct.ConsistencyError(u"child_packet", self.child_packet._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((1 + self.parent_id.len) + self.child_packet.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class AnchorThresholdId(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.anchor_threshold_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.anchor_threshold_length_sig._read()
            self.uknown_byte = self._io.read_u1()
            self.anchor_threshold_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigU4(self._io, self, self._root)
            self.value_sig._read()
            self.value = self._io.read_f4le()


        def _fetch_instances(self):
            pass
            self.anchor_threshold_length_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.AnchorThresholdId, self)._write__seq(io)
            self.anchor_threshold_length_sig._write__seq(self._io)
            self._io.write_u1(self.uknown_byte)
            self._io.write_u4le(self.anchor_threshold_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self._io.write_f4le(self.value)


        def _check(self):
            pass
            if self.anchor_threshold_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"anchor_threshold_length_sig", self.anchor_threshold_length_sig._root, self._root)
            if self.anchor_threshold_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"anchor_threshold_length_sig", self.anchor_threshold_length_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (12 + self.timestamp.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class AnchorId(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.anchor_id_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.anchor_id_length_sig._read()
            self.anchor_id_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigId(self._io, self, self._root)
            self.value_sig._read()
            self.value = RmV6.IdField(self._io, self, self._root)
            self.value._read()


        def _fetch_instances(self):
            pass
            self.anchor_id_length_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()
            self.value._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.AnchorId, self)._write__seq(io)
            self.anchor_id_length_sig._write__seq(self._io)
            self._io.write_u4le(self.anchor_id_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self.value._write__seq(self._io)


        def _check(self):
            pass
            if self.anchor_id_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"anchor_id_length_sig", self.anchor_id_length_sig._root, self._root)
            if self.anchor_id_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"anchor_id_length_sig", self.anchor_id_length_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)
            if self.value._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
            if self.value._parent != self:
                raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((6 + self.timestamp.len) + self.value.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class Text(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.text_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.text_length_sig._read()
            self.text_length = self._io.read_u4le()
            self.stripped_text_length = leb128.Leb128(self._io)
            self.stripped_text_length._read()
            self.unknown_byte = self._io.read_u1()
            self.text = (self._io.read_bytes(self.stripped_text_length.value)).decode("UTF-8")


        def _fetch_instances(self):
            pass
            self.text_length_sig._fetch_instances()
            self.stripped_text_length._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.Text, self)._write__seq(io)
            self.text_length_sig._write__seq(self._io)
            self._io.write_u4le(self.text_length)
            self.stripped_text_length._write__seq(self._io)
            self._io.write_u1(self.unknown_byte)
            self._io.write_bytes((self.text).encode(u"UTF-8"))


        def _check(self):
            pass
            if self.text_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"text_length_sig", self.text_length_sig._root, self._root)
            if self.text_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"text_length_sig", self.text_length_sig._parent, self)
            if (len((self.text).encode(u"UTF-8")) != self.stripped_text_length.value):
                raise kaitaistruct.ConsistencyError(u"text", len((self.text).encode(u"UTF-8")), self.stripped_text_length.value)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((6 + self.stripped_text_length.value) + self.stripped_text_length.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class TextPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.parent_id_sig = RmV6.SigId(self._io, self, self._root)
            self.parent_id_sig._read()
            self.parent_id = RmV6.IdField(self._io, self, self._root)
            self.parent_id._read()
            self.length_with_styles_sig = RmV6.SigLen(self._io, self, self._root)
            self.length_with_styles_sig._read()
            self.length_with_styles = self._io.read_u4le()
            self.length_with_text_sig = RmV6.SigLen(self._io, self, self._root)
            self.length_with_text_sig._read()
            self.length_with_text = self._io.read_u4le()
            self.length_with_text_inner_sig = RmV6.SigLen(self._io, self, self._root)
            self.length_with_text_inner_sig._read()
            self.length_with_text_inner = self._io.read_u4le()
            self.num_items = leb128.Leb128(self._io)
            self.num_items._read()
            self.items = []
            for i in range(self.num_items.value):
                _t_items = RmV6.TextItem(self._io, self, self._root)
                _t_items._read()
                self.items.append(_t_items)

            self.position = RmV6.TextPosition(self._io, self, self._root)
            self.position._read()


        def _fetch_instances(self):
            pass
            self.parent_id_sig._fetch_instances()
            self.parent_id._fetch_instances()
            self.length_with_styles_sig._fetch_instances()
            self.length_with_text_sig._fetch_instances()
            self.length_with_text_inner_sig._fetch_instances()
            self.num_items._fetch_instances()
            for i in range(len(self.items)):
                pass
                self.items[i]._fetch_instances()

            self.position._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.TextPacket, self)._write__seq(io)
            self.parent_id_sig._write__seq(self._io)
            self.parent_id._write__seq(self._io)
            self.length_with_styles_sig._write__seq(self._io)
            self._io.write_u4le(self.length_with_styles)
            self.length_with_text_sig._write__seq(self._io)
            self._io.write_u4le(self.length_with_text)
            self.length_with_text_inner_sig._write__seq(self._io)
            self._io.write_u4le(self.length_with_text_inner)
            self.num_items._write__seq(self._io)
            for i in range(len(self.items)):
                pass
                self.items[i]._write__seq(self._io)

            self.position._write__seq(self._io)


        def _check(self):
            pass
            if self.parent_id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_id_sig", self.parent_id_sig._root, self._root)
            if self.parent_id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_id_sig", self.parent_id_sig._parent, self)
            if self.parent_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_id", self.parent_id._root, self._root)
            if self.parent_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_id", self.parent_id._parent, self)
            if self.length_with_styles_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"length_with_styles_sig", self.length_with_styles_sig._root, self._root)
            if self.length_with_styles_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"length_with_styles_sig", self.length_with_styles_sig._parent, self)
            if self.length_with_text_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"length_with_text_sig", self.length_with_text_sig._root, self._root)
            if self.length_with_text_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"length_with_text_sig", self.length_with_text_sig._parent, self)
            if self.length_with_text_inner_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"length_with_text_inner_sig", self.length_with_text_inner_sig._root, self._root)
            if self.length_with_text_inner_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"length_with_text_inner_sig", self.length_with_text_inner_sig._parent, self)
            if (len(self.items) != self.num_items.value):
                raise kaitaistruct.ConsistencyError(u"items", len(self.items), self.num_items.value)
            for i in range(len(self.items)):
                pass
                if self.items[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"items", self.items[i]._root, self._root)
                if self.items[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"items", self.items[i]._parent, self)

            if self.position._root != self._root:
                raise kaitaistruct.ConsistencyError(u"position", self.position._root, self._root)
            if self.position._parent != self:
                raise kaitaistruct.ConsistencyError(u"position", self.position._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (((16 + self.parent_id.len) + self.num_items.len) + self.position.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SigU1(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.sig = self._io.read_u1()
            _ = self.sig
            if not ((_ & 15) == 1):
                raise kaitaistruct.ValidationExprError(self.sig, self._io, u"/types/sig_u1/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.SigU1, self)._write__seq(io)
            self._io.write_u1(self.sig)


        def _check(self):
            pass
            _ = self.sig
            if not ((_ & 15) == 1):
                raise kaitaistruct.ValidationExprError(self.sig, None, u"/types/sig_u1/seq/0")


    class SigDbl(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.sig = self._io.read_u1()
            _ = self.sig
            if not ((_ & 15) == 8):
                raise kaitaistruct.ValidationExprError(self.sig, self._io, u"/types/sig_dbl/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.SigDbl, self)._write__seq(io)
            self._io.write_u1(self.sig)


        def _check(self):
            pass
            _ = self.sig
            if not ((_ & 15) == 8):
                raise kaitaistruct.ValidationExprError(self.sig, None, u"/types/sig_dbl/seq/0")


    class SigId(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.sig = self._io.read_u1()
            _ = self.sig
            if not ((_ & 15) == 15):
                raise kaitaistruct.ValidationExprError(self.sig, self._io, u"/types/sig_id/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.SigId, self)._write__seq(io)
            self._io.write_u1(self.sig)


        def _check(self):
            pass
            _ = self.sig
            if not ((_ & 15) == 15):
                raise kaitaistruct.ValidationExprError(self.sig, None, u"/types/sig_id/seq/0")


    class TextItem(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.text_item_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.text_item_length_sig._read()
            self.text_item_length = self._io.read_u4le()
            self.positioned_packet = RmV6.PositionedPacket(self._io, self, self._root)
            self.positioned_packet._read()
            if (self.positioned_packet.deleted_length == 0):
                pass
                self.text = RmV6.Text(self._io, self, self._root)
                self.text._read()

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass
                self.font_weight_sig = RmV6.SigU4(self._io, self, self._root)
                self.font_weight_sig._read()

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass
                self.font_weight = self._io.read_u4le()



        def _fetch_instances(self):
            pass
            self.text_item_length_sig._fetch_instances()
            self.positioned_packet._fetch_instances()
            if (self.positioned_packet.deleted_length == 0):
                pass
                self.text._fetch_instances()

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass
                self.font_weight_sig._fetch_instances()

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass



        def _write__seq(self, io=None):
            super(RmV6.TextItem, self)._write__seq(io)
            self.text_item_length_sig._write__seq(self._io)
            self._io.write_u4le(self.text_item_length)
            self.positioned_packet._write__seq(self._io)
            if (self.positioned_packet.deleted_length == 0):
                pass
                self.text._write__seq(self._io)

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass
                self.font_weight_sig._write__seq(self._io)

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass
                self._io.write_u4le(self.font_weight)



        def _check(self):
            pass
            if self.text_item_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"text_item_length_sig", self.text_item_length_sig._root, self._root)
            if self.text_item_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"text_item_length_sig", self.text_item_length_sig._parent, self)
            if self.positioned_packet._root != self._root:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._root, self._root)
            if self.positioned_packet._parent != self:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._parent, self)
            if (self.positioned_packet.deleted_length == 0):
                pass
                if self.text._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"text", self.text._root, self._root)
                if self.text._parent != self:
                    raise kaitaistruct.ConsistencyError(u"text", self.text._parent, self)

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass
                if self.font_weight_sig._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"font_weight_sig", self.font_weight_sig._root, self._root)
                if self.font_weight_sig._parent != self:
                    raise kaitaistruct.ConsistencyError(u"font_weight_sig", self.font_weight_sig._parent, self)

            if  (((self.positioned_packet.deleted_length == 0)) and ((self.text_item_length > (self.text.len + self.positioned_packet.len)))) :
                pass


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (5 + self.text_item_length)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class CrdtLineItemPoints(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.length_sig = RmV6.SigLen(self._io, self, self._root)
            self.length_sig._read()
            self.length = self._io.read_u4le()
            self.unknown_byte = self._io.read_u1()
            self.tool_sig = RmV6.SigU4(self._io, self, self._root)
            self.tool_sig._read()
            self.tool = self._io.read_u4le()
            self.color_sig = RmV6.SigU4(self._io, self, self._root)
            self.color_sig._read()
            self.color = self._io.read_u4le()
            self.thickness_scale_sig = RmV6.SigDbl(self._io, self, self._root)
            self.thickness_scale_sig._read()
            self.thickness_scale = self._io.read_f8le()
            self.starting_length_sig = RmV6.SigU4(self._io, self, self._root)
            self.starting_length_sig._read()
            self.starting_length = self._io.read_u4le()
            self.points_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.points_length_sig._read()
            self.points_length = self._io.read_u4le()
            self.points = []
            for i in range(self.points_length // 14):
                _t_points = RmV6.Point(self._io, self, self._root)
                _t_points._read()
                self.points.append(_t_points)

            self.ts_sig = RmV6.SigId(self._io, self, self._root)
            self.ts_sig._read()
            self.ts = RmV6.IdField(self._io, self, self._root)
            self.ts._read()
            if (((self.length - self.points_length) - 33) > 0):
                pass
                self.move_id_sig = RmV6.SigId(self._io, self, self._root)
                self.move_id_sig._read()

            if (((self.length - self.points_length) - 33) > 0):
                pass
                self.move_id = RmV6.IdField(self._io, self, self._root)
                self.move_id._read()



        def _fetch_instances(self):
            pass
            self.length_sig._fetch_instances()
            self.tool_sig._fetch_instances()
            self.color_sig._fetch_instances()
            self.thickness_scale_sig._fetch_instances()
            self.starting_length_sig._fetch_instances()
            self.points_length_sig._fetch_instances()
            for i in range(len(self.points)):
                pass
                self.points[i]._fetch_instances()

            self.ts_sig._fetch_instances()
            self.ts._fetch_instances()
            if (((self.length - self.points_length) - 33) > 0):
                pass
                self.move_id_sig._fetch_instances()

            if (((self.length - self.points_length) - 33) > 0):
                pass
                self.move_id._fetch_instances()



        def _write__seq(self, io=None):
            super(RmV6.CrdtLineItemPoints, self)._write__seq(io)
            self.length_sig._write__seq(self._io)
            self._io.write_u4le(self.length)
            self._io.write_u1(self.unknown_byte)
            self.tool_sig._write__seq(self._io)
            self._io.write_u4le(self.tool)
            self.color_sig._write__seq(self._io)
            self._io.write_u4le(self.color)
            self.thickness_scale_sig._write__seq(self._io)
            self._io.write_f8le(self.thickness_scale)
            self.starting_length_sig._write__seq(self._io)
            self._io.write_u4le(self.starting_length)
            self.points_length_sig._write__seq(self._io)
            self._io.write_u4le(self.points_length)
            for i in range(len(self.points)):
                pass
                self.points[i]._write__seq(self._io)

            self.ts_sig._write__seq(self._io)
            self.ts._write__seq(self._io)
            if (((self.length - self.points_length) - 33) > 0):
                pass
                self.move_id_sig._write__seq(self._io)

            if (((self.length - self.points_length) - 33) > 0):
                pass
                self.move_id._write__seq(self._io)



        def _check(self):
            pass
            if self.length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"length_sig", self.length_sig._root, self._root)
            if self.length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"length_sig", self.length_sig._parent, self)
            if self.tool_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"tool_sig", self.tool_sig._root, self._root)
            if self.tool_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"tool_sig", self.tool_sig._parent, self)
            if self.color_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"color_sig", self.color_sig._root, self._root)
            if self.color_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"color_sig", self.color_sig._parent, self)
            if self.thickness_scale_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"thickness_scale_sig", self.thickness_scale_sig._root, self._root)
            if self.thickness_scale_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"thickness_scale_sig", self.thickness_scale_sig._parent, self)
            if self.starting_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"starting_length_sig", self.starting_length_sig._root, self._root)
            if self.starting_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"starting_length_sig", self.starting_length_sig._parent, self)
            if self.points_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"points_length_sig", self.points_length_sig._root, self._root)
            if self.points_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"points_length_sig", self.points_length_sig._parent, self)
            if (len(self.points) != self.points_length // 14):
                raise kaitaistruct.ConsistencyError(u"points", len(self.points), self.points_length // 14)
            for i in range(len(self.points)):
                pass
                if self.points[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"points", self.points[i]._root, self._root)
                if self.points[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"points", self.points[i]._parent, self)

            if self.ts_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"ts_sig", self.ts_sig._root, self._root)
            if self.ts_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"ts_sig", self.ts_sig._parent, self)
            if self.ts._root != self._root:
                raise kaitaistruct.ConsistencyError(u"ts", self.ts._root, self._root)
            if self.ts._parent != self:
                raise kaitaistruct.ConsistencyError(u"ts", self.ts._parent, self)
            if (((self.length - self.points_length) - 33) > 0):
                pass
                if self.move_id_sig._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"move_id_sig", self.move_id_sig._root, self._root)
                if self.move_id_sig._parent != self:
                    raise kaitaistruct.ConsistencyError(u"move_id_sig", self.move_id_sig._parent, self)

            if (((self.length - self.points_length) - 33) > 0):
                pass
                if self.move_id._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"move_id", self.move_id._root, self._root)
                if self.move_id._parent != self:
                    raise kaitaistruct.ConsistencyError(u"move_id", self.move_id._parent, self)


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (((37 + self.ts.len) + self.move_id.len) if (((self.length - self.points_length) - 33) > 0) else (36 + self.ts.len))
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class AnchorMode(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.anchor_mode_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.anchor_mode_length_sig._read()
            self.unknown_byte = self._io.read_u1()
            self.anchor_mode_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigU1(self._io, self, self._root)
            self.value_sig._read()
            self.value = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.anchor_mode_length_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.AnchorMode, self)._write__seq(io)
            self.anchor_mode_length_sig._write__seq(self._io)
            self._io.write_u1(self.unknown_byte)
            self._io.write_u4le(self.anchor_mode_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self._io.write_u1(self.value)


        def _check(self):
            pass
            if self.anchor_mode_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"anchor_mode_length_sig", self.anchor_mode_length_sig._root, self._root)
            if self.anchor_mode_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"anchor_mode_length_sig", self.anchor_mode_length_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (9 + self.timestamp.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SceneInfoRootDocumentVisible(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.root_document_visible_sig = RmV6.SigLen(self._io, self, self._root)
            self.root_document_visible_sig._read()
            self.root_document_visible_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigU1(self._io, self, self._root)
            self.value_sig._read()
            self.value = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.root_document_visible_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneInfoRootDocumentVisible, self)._write__seq(io)
            self.root_document_visible_sig._write__seq(self._io)
            self._io.write_u4le(self.root_document_visible_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self._io.write_u1(self.value)


        def _check(self):
            pass
            if self.root_document_visible_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"root_document_visible_sig", self.root_document_visible_sig._root, self._root)
            if self.root_document_visible_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"root_document_visible_sig", self.root_document_visible_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (8 + self.timestamp.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class UuidPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.unknown_byte_1 = self._io.read_u1()
            self.uuid_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.uuid_length_sig._read()
            self.uuid_packet_length = self._io.read_u4le()
            self.uuid_length = self._io.read_u1()
            self.uuid = []
            for i in range(16):
                self.uuid.append(self._io.read_u1())

            self.second = self._io.read_u1()
            self.unknown_byte_2 = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.uuid_length_sig._fetch_instances()
            for i in range(len(self.uuid)):
                pass



        def _write__seq(self, io=None):
            super(RmV6.UuidPacket, self)._write__seq(io)
            self._io.write_u1(self.unknown_byte_1)
            self.uuid_length_sig._write__seq(self._io)
            self._io.write_u4le(self.uuid_packet_length)
            self._io.write_u1(self.uuid_length)
            for i in range(len(self.uuid)):
                pass
                self._io.write_u1(self.uuid[i])

            self._io.write_u1(self.second)
            self._io.write_u1(self.unknown_byte_2)


        def _check(self):
            pass
            if self.uuid_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"uuid_length_sig", self.uuid_length_sig._root, self._root)
            if self.uuid_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"uuid_length_sig", self.uuid_length_sig._parent, self)
            if (len(self.uuid) != 16):
                raise kaitaistruct.ConsistencyError(u"uuid", len(self.uuid), 16)
            for i in range(len(self.uuid)):
                pass


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = 25
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class CrdtLineItemPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.positioned_packet = RmV6.PositionedChildPacket(self._io, self, self._root)
            self.positioned_packet._read()
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.points = RmV6.CrdtLineItemPoints(self._io, self, self._root)
                self.points._read()



        def _fetch_instances(self):
            pass
            self.positioned_packet._fetch_instances()
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.points._fetch_instances()



        def _write__seq(self, io=None):
            super(RmV6.CrdtLineItemPacket, self)._write__seq(io)
            self.positioned_packet._write__seq(self._io)
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.points._write__seq(self._io)



        def _check(self):
            pass
            if self.positioned_packet._root != self._root:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._root, self._root)
            if self.positioned_packet._parent != self:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._parent, self)
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                if self.points._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"points", self.points._root, self._root)
                if self.points._parent != self:
                    raise kaitaistruct.ConsistencyError(u"points", self.points._parent, self)


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((self.positioned_packet.len + self.points.len) if (self.positioned_packet.child_packet.deleted_length == 0) else self.positioned_packet.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class PageStatsPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.loads_sig = RmV6.SigU4(self._io, self, self._root)
            self.loads_sig._read()
            self.loads = self._io.read_u4le()
            self.merges_sig = RmV6.SigU4(self._io, self, self._root)
            self.merges_sig._read()
            self.merges = self._io.read_u4le()
            self.text_chars_sig = RmV6.SigU4(self._io, self, self._root)
            self.text_chars_sig._read()
            self.text_chars = self._io.read_u4le()
            self.text_lines_sig = RmV6.SigU4(self._io, self, self._root)
            self.text_lines_sig._read()
            self.text_lines = self._io.read_u4le()
            self.keyboard_count_sig = RmV6.SigU4(self._io, self, self._root)
            self.keyboard_count_sig._read()
            self.keyboard_count = self._io.read_u4le()


        def _fetch_instances(self):
            pass
            self.loads_sig._fetch_instances()
            self.merges_sig._fetch_instances()
            self.text_chars_sig._fetch_instances()
            self.text_lines_sig._fetch_instances()
            self.keyboard_count_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.PageStatsPacket, self)._write__seq(io)
            self.loads_sig._write__seq(self._io)
            self._io.write_u4le(self.loads)
            self.merges_sig._write__seq(self._io)
            self._io.write_u4le(self.merges)
            self.text_chars_sig._write__seq(self._io)
            self._io.write_u4le(self.text_chars)
            self.text_lines_sig._write__seq(self._io)
            self._io.write_u4le(self.text_lines)
            self.keyboard_count_sig._write__seq(self._io)
            self._io.write_u4le(self.keyboard_count)


        def _check(self):
            pass
            if self.loads_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"loads_sig", self.loads_sig._root, self._root)
            if self.loads_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"loads_sig", self.loads_sig._parent, self)
            if self.merges_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"merges_sig", self.merges_sig._root, self._root)
            if self.merges_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"merges_sig", self.merges_sig._parent, self)
            if self.text_chars_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"text_chars_sig", self.text_chars_sig._root, self._root)
            if self.text_chars_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"text_chars_sig", self.text_chars_sig._parent, self)
            if self.text_lines_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"text_lines_sig", self.text_lines_sig._root, self._root)
            if self.text_lines_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"text_lines_sig", self.text_lines_sig._parent, self)
            if self.keyboard_count_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"keyboard_count_sig", self.keyboard_count_sig._root, self._root)
            if self.keyboard_count_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"keyboard_count_sig", self.keyboard_count_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = 25
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class TextPosition(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.root_text_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.root_text_length_sig._read()
            self.root_text_length = self._io.read_u4le()
            self.styles_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.styles_length_sig._read()
            self.styles_length = self._io.read_u4le()
            self.num_styles = leb128.Leb128(self._io)
            self.num_styles._read()
            self.styles = []
            for i in range(self.num_styles.value):
                _t_styles = RmV6.TextStyle(self._io, self, self._root)
                _t_styles._read()
                self.styles.append(_t_styles)

            self.position_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.position_length_sig._read()
            self.position_length = self._io.read_u4le()
            self.x = self._io.read_f8le()
            self.y = self._io.read_f8le()
            self.text_width_sig = RmV6.SigU4(self._io, self, self._root)
            self.text_width_sig._read()
            self.text_width = self._io.read_f4le()


        def _fetch_instances(self):
            pass
            self.root_text_length_sig._fetch_instances()
            self.styles_length_sig._fetch_instances()
            self.num_styles._fetch_instances()
            for i in range(len(self.styles)):
                pass
                self.styles[i]._fetch_instances()

            self.position_length_sig._fetch_instances()
            self.text_width_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.TextPosition, self)._write__seq(io)
            self.root_text_length_sig._write__seq(self._io)
            self._io.write_u4le(self.root_text_length)
            self.styles_length_sig._write__seq(self._io)
            self._io.write_u4le(self.styles_length)
            self.num_styles._write__seq(self._io)
            for i in range(len(self.styles)):
                pass
                self.styles[i]._write__seq(self._io)

            self.position_length_sig._write__seq(self._io)
            self._io.write_u4le(self.position_length)
            self._io.write_f8le(self.x)
            self._io.write_f8le(self.y)
            self.text_width_sig._write__seq(self._io)
            self._io.write_f4le(self.text_width)


        def _check(self):
            pass
            if self.root_text_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"root_text_length_sig", self.root_text_length_sig._root, self._root)
            if self.root_text_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"root_text_length_sig", self.root_text_length_sig._parent, self)
            if self.styles_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"styles_length_sig", self.styles_length_sig._root, self._root)
            if self.styles_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"styles_length_sig", self.styles_length_sig._parent, self)
            if (len(self.styles) != self.num_styles.value):
                raise kaitaistruct.ConsistencyError(u"styles", len(self.styles), self.num_styles.value)
            for i in range(len(self.styles)):
                pass
                if self.styles[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"styles", self.styles[i]._root, self._root)
                if self.styles[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"styles", self.styles[i]._parent, self)

            if self.position_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"position_length_sig", self.position_length_sig._root, self._root)
            if self.position_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"position_length_sig", self.position_length_sig._parent, self)
            if self.text_width_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"text_width_sig", self.text_width_sig._root, self._root)
            if self.text_width_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"text_width_sig", self.text_width_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (36 + self.num_styles.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SceneTreeNodeAnchor(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.id = RmV6.AnchorId(self._io, self, self._root)
            self.id._read()
            self.mode = RmV6.AnchorMode(self._io, self, self._root)
            self.mode._read()
            self.threshold = RmV6.AnchorThresholdId(self._io, self, self._root)
            self.threshold._read()
            self.origin = RmV6.AnchorInitialOriginX(self._io, self, self._root)
            self.origin._read()


        def _fetch_instances(self):
            pass
            self.id._fetch_instances()
            self.mode._fetch_instances()
            self.threshold._fetch_instances()
            self.origin._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneTreeNodeAnchor, self)._write__seq(io)
            self.id._write__seq(self._io)
            self.mode._write__seq(self._io)
            self.threshold._write__seq(self._io)
            self.origin._write__seq(self._io)


        def _check(self):
            pass
            if self.id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id", self.id._root, self._root)
            if self.id._parent != self:
                raise kaitaistruct.ConsistencyError(u"id", self.id._parent, self)
            if self.mode._root != self._root:
                raise kaitaistruct.ConsistencyError(u"mode", self.mode._root, self._root)
            if self.mode._parent != self:
                raise kaitaistruct.ConsistencyError(u"mode", self.mode._parent, self)
            if self.threshold._root != self._root:
                raise kaitaistruct.ConsistencyError(u"threshold", self.threshold._root, self._root)
            if self.threshold._parent != self:
                raise kaitaistruct.ConsistencyError(u"threshold", self.threshold._parent, self)
            if self.origin._root != self._root:
                raise kaitaistruct.ConsistencyError(u"origin", self.origin._root, self._root)
            if self.origin._parent != self:
                raise kaitaistruct.ConsistencyError(u"origin", self.origin._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (((self.id.len + self.mode.len) + self.threshold.len) + self.origin.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class PacketHeader(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.length = self._io.read_u4le()
            self.first_version = self._io.read_u1()
            self.minimal_version = self._io.read_u1()
            self.version = self._io.read_u1()
            self.header_type = KaitaiStream.resolve_enum(RmV6.PacketType, self._io.read_u1())


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.PacketHeader, self)._write__seq(io)
            self._io.write_u4le(self.length)
            self._io.write_u1(self.first_version)
            self._io.write_u1(self.minimal_version)
            self._io.write_u1(self.version)
            self._io.write_u1(int(self.header_type))


        def _check(self):
            pass

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = 8
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SceneInfoPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.current_layer = RmV6.SceneInfoCurrentLayer(self._io, self, self._root)
            self.current_layer._read()
            self.background_visible = RmV6.SceneInfoBackgroundVisible(self._io, self, self._root)
            self.background_visible._read()
            self.root_document_visible = RmV6.SceneInfoRootDocumentVisible(self._io, self, self._root)
            self.root_document_visible._read()


        def _fetch_instances(self):
            pass
            self.current_layer._fetch_instances()
            self.background_visible._fetch_instances()
            self.root_document_visible._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneInfoPacket, self)._write__seq(io)
            self.current_layer._write__seq(self._io)
            self.background_visible._write__seq(self._io)
            self.root_document_visible._write__seq(self._io)


        def _check(self):
            pass
            if self.current_layer._root != self._root:
                raise kaitaistruct.ConsistencyError(u"current_layer", self.current_layer._root, self._root)
            if self.current_layer._parent != self:
                raise kaitaistruct.ConsistencyError(u"current_layer", self.current_layer._parent, self)
            if self.background_visible._root != self._root:
                raise kaitaistruct.ConsistencyError(u"background_visible", self.background_visible._root, self._root)
            if self.background_visible._parent != self:
                raise kaitaistruct.ConsistencyError(u"background_visible", self.background_visible._parent, self)
            if self.root_document_visible._root != self._root:
                raise kaitaistruct.ConsistencyError(u"root_document_visible", self.root_document_visible._root, self._root)
            if self.root_document_visible._parent != self:
                raise kaitaistruct.ConsistencyError(u"root_document_visible", self.root_document_visible._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((self.current_layer.len + self.background_visible.len) + self.root_document_visible.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SigU2(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.sig = self._io.read_u1()
            _ = self.sig
            if not ((_ & 15) == 2):
                raise kaitaistruct.ValidationExprError(self.sig, self._io, u"/types/sig_u2/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.SigU2, self)._write__seq(io)
            self._io.write_u1(self.sig)


        def _check(self):
            pass
            _ = self.sig
            if not ((_ & 15) == 2):
                raise kaitaistruct.ValidationExprError(self.sig, None, u"/types/sig_u2/seq/0")


    class IdField(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.major = leb128.Leb128(self._io)
            self.major._read()
            self.minor = leb128.Leb128(self._io)
            self.minor._read()


        def _fetch_instances(self):
            pass
            self.major._fetch_instances()
            self.minor._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.IdField, self)._write__seq(io)
            self.major._write__seq(self._io)
            self.minor._write__seq(self._io)


        def _check(self):
            pass

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (self.major.len + self.minor.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class MigrationInfoPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.migration_id_sig = RmV6.SigId(self._io, self, self._root)
            self.migration_id_sig._read()
            self.migration_id = RmV6.IdField(self._io, self, self._root)
            self.migration_id._read()
            self.device_sig = RmV6.SigU1(self._io, self, self._root)
            self.device_sig._read()
            self.device = self._io.read_u1()
            self.v3_sig = RmV6.SigU1(self._io, self, self._root)
            self.v3_sig._read()
            self.v3 = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.migration_id_sig._fetch_instances()
            self.migration_id._fetch_instances()
            self.device_sig._fetch_instances()
            self.v3_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.MigrationInfoPacket, self)._write__seq(io)
            self.migration_id_sig._write__seq(self._io)
            self.migration_id._write__seq(self._io)
            self.device_sig._write__seq(self._io)
            self._io.write_u1(self.device)
            self.v3_sig._write__seq(self._io)
            self._io.write_u1(self.v3)


        def _check(self):
            pass
            if self.migration_id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"migration_id_sig", self.migration_id_sig._root, self._root)
            if self.migration_id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"migration_id_sig", self.migration_id_sig._parent, self)
            if self.migration_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"migration_id", self.migration_id._root, self._root)
            if self.migration_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"migration_id", self.migration_id._parent, self)
            if self.device_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"device_sig", self.device_sig._root, self._root)
            if self.device_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"device_sig", self.device_sig._parent, self)
            if self.v3_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"v3_sig", self.v3_sig._root, self._root)
            if self.v3_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"v3_sig", self.v3_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (5 + self.migration_id.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class CrdtGlyphItemPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.positioned_packet = RmV6.PositionedChildPacket(self._io, self, self._root)
            self.positioned_packet._read()
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.value = RmV6.CrdtGlyphItemValue(self._io, self, self._root)
                self.value._read()



        def _fetch_instances(self):
            pass
            self.positioned_packet._fetch_instances()
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.value._fetch_instances()



        def _write__seq(self, io=None):
            super(RmV6.CrdtGlyphItemPacket, self)._write__seq(io)
            self.positioned_packet._write__seq(self._io)
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.value._write__seq(self._io)



        def _check(self):
            pass
            if self.positioned_packet._root != self._root:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._root, self._root)
            if self.positioned_packet._parent != self:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._parent, self)
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                if self.value._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
                if self.value._parent != self:
                    raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((self.positioned_packet.len + self.value.len) if (self.positioned_packet.child_packet.deleted_length == 0) else self.positioned_packet.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SigLen(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.sig = self._io.read_u1()
            _ = self.sig
            if not ((_ & 15) == 12):
                raise kaitaistruct.ValidationExprError(self.sig, self._io, u"/types/sig_len/seq/0")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(RmV6.SigLen, self)._write__seq(io)
            self._io.write_u1(self.sig)


        def _check(self):
            pass
            _ = self.sig
            if not ((_ & 15) == 12):
                raise kaitaistruct.ValidationExprError(self.sig, None, u"/types/sig_len/seq/0")


    class SceneInfoCurrentLayer(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.current_layer_sig = RmV6.SigLen(self._io, self, self._root)
            self.current_layer_sig._read()
            self.current_layer_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigId(self._io, self, self._root)
            self.value_sig._read()
            self.value = RmV6.IdField(self._io, self, self._root)
            self.value._read()


        def _fetch_instances(self):
            pass
            self.current_layer_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()
            self.value._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneInfoCurrentLayer, self)._write__seq(io)
            self.current_layer_sig._write__seq(self._io)
            self._io.write_u4le(self.current_layer_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self.value._write__seq(self._io)


        def _check(self):
            pass
            if self.current_layer_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"current_layer_sig", self.current_layer_sig._root, self._root)
            if self.current_layer_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"current_layer_sig", self.current_layer_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)
            if self.value._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
            if self.value._parent != self:
                raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((7 + self.timestamp.len) + self.value.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class AnchorInitialOriginX(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.anchor_initial_origin_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.anchor_initial_origin_length_sig._read()
            self.unknown_byte = self._io.read_u1()
            self.anchor_initial_origin_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigU4(self._io, self, self._root)
            self.value_sig._read()
            self.value = self._io.read_f4le()


        def _fetch_instances(self):
            pass
            self.anchor_initial_origin_length_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.AnchorInitialOriginX, self)._write__seq(io)
            self.anchor_initial_origin_length_sig._write__seq(self._io)
            self._io.write_u1(self.unknown_byte)
            self._io.write_u4le(self.anchor_initial_origin_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self._io.write_f4le(self.value)


        def _check(self):
            pass
            if self.anchor_initial_origin_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"anchor_initial_origin_length_sig", self.anchor_initial_origin_length_sig._root, self._root)
            if self.anchor_initial_origin_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"anchor_initial_origin_length_sig", self.anchor_initial_origin_length_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (12 + self.timestamp.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class CrdtGroupItemNode(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.node_id_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.node_id_length_sig._read()
            self.node_id_length = self._io.read_u4le()
            self.unknown_byte = self._io.read_u1()
            self.node_id_sig = RmV6.SigId(self._io, self, self._root)
            self.node_id_sig._read()
            self.node_id = RmV6.IdField(self._io, self, self._root)
            self.node_id._read()


        def _fetch_instances(self):
            pass
            self.node_id_length_sig._fetch_instances()
            self.node_id_sig._fetch_instances()
            self.node_id._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.CrdtGroupItemNode, self)._write__seq(io)
            self.node_id_length_sig._write__seq(self._io)
            self._io.write_u4le(self.node_id_length)
            self._io.write_u1(self.unknown_byte)
            self.node_id_sig._write__seq(self._io)
            self.node_id._write__seq(self._io)


        def _check(self):
            pass
            if self.node_id_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_id_length_sig", self.node_id_length_sig._root, self._root)
            if self.node_id_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_id_length_sig", self.node_id_length_sig._parent, self)
            if self.node_id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_id_sig", self.node_id_sig._root, self._root)
            if self.node_id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_id_sig", self.node_id_sig._parent, self)
            if self.node_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_id", self.node_id._root, self._root)
            if self.node_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_id", self.node_id._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (7 + self.node_id.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class CrdtGroupItemPacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.positioned_packet = RmV6.PositionedChildPacket(self._io, self, self._root)
            self.positioned_packet._read()
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.node = RmV6.CrdtGroupItemNode(self._io, self, self._root)
                self.node._read()



        def _fetch_instances(self):
            pass
            self.positioned_packet._fetch_instances()
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.node._fetch_instances()



        def _write__seq(self, io=None):
            super(RmV6.CrdtGroupItemPacket, self)._write__seq(io)
            self.positioned_packet._write__seq(self._io)
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                self.node._write__seq(self._io)



        def _check(self):
            pass
            if self.positioned_packet._root != self._root:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._root, self._root)
            if self.positioned_packet._parent != self:
                raise kaitaistruct.ConsistencyError(u"positioned_packet", self.positioned_packet._parent, self)
            if (self.positioned_packet.child_packet.deleted_length == 0):
                pass
                if self.node._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"node", self.node._root, self._root)
                if self.node._parent != self:
                    raise kaitaistruct.ConsistencyError(u"node", self.node._parent, self)


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = ((self.positioned_packet.len + self.node.len) if (self.positioned_packet.child_packet.deleted_length == 0) else self.positioned_packet.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class Packet(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.packet_header = RmV6.PacketHeader(self._io, self, self._root)
            self.packet_header._read()
            _on = self.packet_header.header_type
            if _on == RmV6.PacketType.stats:
                pass
                self.packet_body = RmV6.PageStatsPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.tree_node:
                pass
                self.packet_body = RmV6.SceneTreeNodePacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.glyph_item:
                pass
                self.packet_body = RmV6.CrdtGlyphItemPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.uuid:
                pass
                self.packet_body = RmV6.UuidPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.tree_move:
                pass
                self.packet_body = RmV6.SceneTreeMovePacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.scene:
                pass
                self.packet_body = RmV6.SceneInfoPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.text_item:
                pass
                self.packet_body = RmV6.TextPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.group_item:
                pass
                self.packet_body = RmV6.CrdtGroupItemPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.line_item:
                pass
                self.packet_body = RmV6.CrdtLineItemPacket(self._io, self, self._root)
                self.packet_body._read()
            elif _on == RmV6.PacketType.migration:
                pass
                self.packet_body = RmV6.MigrationInfoPacket(self._io, self, self._root)
                self.packet_body._read()
            if  (((self.packet_header.header_type == RmV6.PacketType.tree_node)) and ((self.packet_body.len < self.packet_header.length))) :
                pass
                self.scene_tree_node_anchor = RmV6.SceneTreeNodeAnchor(self._io, self, self._root)
                self.scene_tree_node_anchor._read()



        def _fetch_instances(self):
            pass
            self.packet_header._fetch_instances()
            _on = self.packet_header.header_type
            if _on == RmV6.PacketType.stats:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.tree_node:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.glyph_item:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.uuid:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.tree_move:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.scene:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.text_item:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.group_item:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.line_item:
                pass
                self.packet_body._fetch_instances()
            elif _on == RmV6.PacketType.migration:
                pass
                self.packet_body._fetch_instances()
            if  (((self.packet_header.header_type == RmV6.PacketType.tree_node)) and ((self.packet_body.len < self.packet_header.length))) :
                pass
                self.scene_tree_node_anchor._fetch_instances()



        def _write__seq(self, io=None):
            super(RmV6.Packet, self)._write__seq(io)
            self.packet_header._write__seq(self._io)
            _on = self.packet_header.header_type
            if _on == RmV6.PacketType.stats:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.tree_node:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.glyph_item:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.uuid:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.tree_move:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.scene:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.text_item:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.group_item:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.line_item:
                pass
                self.packet_body._write__seq(self._io)
            elif _on == RmV6.PacketType.migration:
                pass
                self.packet_body._write__seq(self._io)
            if  (((self.packet_header.header_type == RmV6.PacketType.tree_node)) and ((self.packet_body.len < self.packet_header.length))) :
                pass
                self.scene_tree_node_anchor._write__seq(self._io)



        def _check(self):
            pass
            if self.packet_header._root != self._root:
                raise kaitaistruct.ConsistencyError(u"packet_header", self.packet_header._root, self._root)
            if self.packet_header._parent != self:
                raise kaitaistruct.ConsistencyError(u"packet_header", self.packet_header._parent, self)
            _on = self.packet_header.header_type
            if _on == RmV6.PacketType.stats:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.tree_node:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.glyph_item:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.uuid:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.tree_move:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.scene:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.text_item:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.group_item:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.line_item:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            elif _on == RmV6.PacketType.migration:
                pass
                if self.packet_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._root, self._root)
                if self.packet_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"packet_body", self.packet_body._parent, self)
            if  (((self.packet_header.header_type == RmV6.PacketType.tree_node)) and ((self.packet_body.len < self.packet_header.length))) :
                pass
                if self.scene_tree_node_anchor._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"scene_tree_node_anchor", self.scene_tree_node_anchor._root, self._root)
                if self.scene_tree_node_anchor._parent != self:
                    raise kaitaistruct.ConsistencyError(u"scene_tree_node_anchor", self.scene_tree_node_anchor._parent, self)


        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (self.packet_header.length + self.packet_header.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class GlyphRect(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.rect_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.rect_length_sig._read()
            self.rect_length = self._io.read_u4le()
            self.unknown_byte = self._io.read_u1()
            self.x = self._io.read_f8le()
            self.y = self._io.read_f8le()
            self.width = self._io.read_f8le()
            self.height = self._io.read_f8le()


        def _fetch_instances(self):
            pass
            self.rect_length_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.GlyphRect, self)._write__seq(io)
            self.rect_length_sig._write__seq(self._io)
            self._io.write_u4le(self.rect_length)
            self._io.write_u1(self.unknown_byte)
            self._io.write_f8le(self.x)
            self._io.write_f8le(self.y)
            self._io.write_f8le(self.width)
            self._io.write_f8le(self.height)


        def _check(self):
            pass
            if self.rect_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"rect_length_sig", self.rect_length_sig._root, self._root)
            if self.rect_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"rect_length_sig", self.rect_length_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = 38
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SceneTreeMovePacket(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.id_sig = RmV6.SigId(self._io, self, self._root)
            self.id_sig._read()
            self.id = RmV6.IdField(self._io, self, self._root)
            self.id._read()
            self.node_sig = RmV6.SigId(self._io, self, self._root)
            self.node_sig._read()
            self.node = RmV6.IdField(self._io, self, self._root)
            self.node._read()
            self.item_sig = RmV6.SigU1(self._io, self, self._root)
            self.item_sig._read()
            self.item = self._io.read_u1()
            self.parent_length_sig = RmV6.SigLen(self._io, self, self._root)
            self.parent_length_sig._read()
            self.parent_length = self._io.read_u4le()
            self.parent_sig = RmV6.SigId(self._io, self, self._root)
            self.parent_sig._read()
            self.parent_id = RmV6.IdField(self._io, self, self._root)
            self.parent_id._read()


        def _fetch_instances(self):
            pass
            self.id_sig._fetch_instances()
            self.id._fetch_instances()
            self.node_sig._fetch_instances()
            self.node._fetch_instances()
            self.item_sig._fetch_instances()
            self.parent_length_sig._fetch_instances()
            self.parent_sig._fetch_instances()
            self.parent_id._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneTreeMovePacket, self)._write__seq(io)
            self.id_sig._write__seq(self._io)
            self.id._write__seq(self._io)
            self.node_sig._write__seq(self._io)
            self.node._write__seq(self._io)
            self.item_sig._write__seq(self._io)
            self._io.write_u1(self.item)
            self.parent_length_sig._write__seq(self._io)
            self._io.write_u4le(self.parent_length)
            self.parent_sig._write__seq(self._io)
            self.parent_id._write__seq(self._io)


        def _check(self):
            pass
            if self.id_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id_sig", self.id_sig._root, self._root)
            if self.id_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"id_sig", self.id_sig._parent, self)
            if self.id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"id", self.id._root, self._root)
            if self.id._parent != self:
                raise kaitaistruct.ConsistencyError(u"id", self.id._parent, self)
            if self.node_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node_sig", self.node_sig._root, self._root)
            if self.node_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"node_sig", self.node_sig._parent, self)
            if self.node._root != self._root:
                raise kaitaistruct.ConsistencyError(u"node", self.node._root, self._root)
            if self.node._parent != self:
                raise kaitaistruct.ConsistencyError(u"node", self.node._parent, self)
            if self.item_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"item_sig", self.item_sig._root, self._root)
            if self.item_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"item_sig", self.item_sig._parent, self)
            if self.parent_length_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_length_sig", self.parent_length_sig._root, self._root)
            if self.parent_length_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_length_sig", self.parent_length_sig._parent, self)
            if self.parent_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_sig", self.parent_sig._root, self._root)
            if self.parent_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_sig", self.parent_sig._parent, self)
            if self.parent_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"parent_id", self.parent_id._root, self._root)
            if self.parent_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"parent_id", self.parent_id._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (((10 + self.id.len) + self.node.len) + self.parent_id.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len

    class SceneInfoBackgroundVisible(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.background_visible_sig = RmV6.SigLen(self._io, self, self._root)
            self.background_visible_sig._read()
            self.background_visible_length = self._io.read_u4le()
            self.timestamp_sig = RmV6.SigId(self._io, self, self._root)
            self.timestamp_sig._read()
            self.timestamp = RmV6.IdField(self._io, self, self._root)
            self.timestamp._read()
            self.value_sig = RmV6.SigU1(self._io, self, self._root)
            self.value_sig._read()
            self.value = self._io.read_u1()


        def _fetch_instances(self):
            pass
            self.background_visible_sig._fetch_instances()
            self.timestamp_sig._fetch_instances()
            self.timestamp._fetch_instances()
            self.value_sig._fetch_instances()


        def _write__seq(self, io=None):
            super(RmV6.SceneInfoBackgroundVisible, self)._write__seq(io)
            self.background_visible_sig._write__seq(self._io)
            self._io.write_u4le(self.background_visible_length)
            self.timestamp_sig._write__seq(self._io)
            self.timestamp._write__seq(self._io)
            self.value_sig._write__seq(self._io)
            self._io.write_u1(self.value)


        def _check(self):
            pass
            if self.background_visible_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"background_visible_sig", self.background_visible_sig._root, self._root)
            if self.background_visible_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"background_visible_sig", self.background_visible_sig._parent, self)
            if self.timestamp_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._root, self._root)
            if self.timestamp_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp_sig", self.timestamp_sig._parent, self)
            if self.timestamp._root != self._root:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._root, self._root)
            if self.timestamp._parent != self:
                raise kaitaistruct.ConsistencyError(u"timestamp", self.timestamp._parent, self)
            if self.value_sig._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._root, self._root)
            if self.value_sig._parent != self:
                raise kaitaistruct.ConsistencyError(u"value_sig", self.value_sig._parent, self)

        @property
        def len(self):
            if hasattr(self, '_m_len'):
                return self._m_len

            self._m_len = (8 + self.timestamp.len)
            return getattr(self, '_m_len', None)

        def _invalidate_len(self):
            del self._m_len


