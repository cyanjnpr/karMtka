from kaitai import rm_v6
from .packet import create_kaitai_leb

class RemarkableId():
    internal_counter: int = 1

    def __init__(self, major: int, minor: int = None):
        self.major = major
        if (minor != None):
            self.minor = minor
        else:
            self.minor = RemarkableId.internal_counter
            RemarkableId.internal_counter += 1

    def to_kaitai(self, parent: rm_v6.ReadWriteKaitaiStruct) -> rm_v6.RmV6.IdField:
        id = rm_v6.RmV6.IdField(None, parent, parent._root)
        id.major = create_kaitai_leb(self.major)
        id.minor = create_kaitai_leb(self.minor)
        return id
    
    def __sub__(self, other: int):
        return RemarkableId(self.major, max(0, self.minor - other))

    def __add__(self, other: int):
        return RemarkableId(self.major, self.minor + other)
    
    @staticmethod
    def position() -> int:
        return RemarkableId.internal_counter

    # text items move id by the amount of characters contained in them
    # equivalent of cursor in their case
    @staticmethod
    def move_counter(amount: int):
        if amount < 0:
            return
        RemarkableId.internal_counter += amount

    @staticmethod
    def zero():
        return RemarkableId(0, 0)
    
    @staticmethod
    def one():
        return RemarkableId(1, 1)


def create_id(parent: rm_v6.ReadWriteKaitaiStruct, 
        major: int, minor: int) -> rm_v6.RmV6.IdField:
    id = rm_v6.RmV6.IdField(None, parent, parent._root)
    id.major = create_kaitai_leb(major)
    id.minor = create_kaitai_leb(minor)
    return id

def id_from_str(parent: rm_v6.ReadWriteKaitaiStruct, raw: str) -> rm_v6.RmV6.IdField:
    parts = raw.split(":")
    if (len(parts) != 2):
        raise Exception("cannot construct valid id from given string value")
    return create_id(parent, int(parts[0]), int(parts[1]))