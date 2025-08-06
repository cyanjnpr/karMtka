from kaitai import rm_v6, kaitai_leb128
from .signature import *
import leb128
from typing import List

def create_packet_backbone(parent: rm_v6.ReadWriteKaitaiStruct):
    p = rm_v6.RmV6.Packet(None, parent, parent._root)
    return p

def create_header(parent: rm_v6.ReadWriteKaitaiStruct, 
        length: int, min_ver: int, ver: int, type: rm_v6.RmV6.PacketType):
    header = rm_v6.RmV6.PacketHeader(None, parent, parent._root)
    header.length = length
    header.first_version = 0
    header.minimal_version = min_ver
    header.version = ver
    header.header_type = type.value
    return header

def create_kaitai_leb(value: int) -> kaitai_leb128.Leb128:
    l = kaitai_leb128.Leb128.from_bytes(leb128.u.encode(value))
    # compiled with --no-auto-read
    l._read()
    return l

def chop_line(line: str, limit: int = 128):
    return chop_lines([line], limit)

def chop_lines(lines: List[str], limit: int = 128):
    result = []
    for line in lines:
        for i in range(0, len(line), 128):
            result.append(line[i:min(len(line), i+128)])
    return result

